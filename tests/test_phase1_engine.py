"""Resampling, parsers, the ported detector, the hash chain, and paper math."""

from datetime import UTC, datetime, timedelta

import httpx
import numpy as np

from Core import http_client
from Repositories.MarketData.modules.binance import parse_klines as parse_binance
from Repositories.MarketData.modules.candles import CandleBar
from Repositories.MarketData.modules.kucoin import parse_klines as parse_kucoin
from Repositories.MarketData.modules.resample_module import resample
from Repositories.PaperTrading.modules.simulator import (
    EntrySignal,
    PaperTrade,
    TrailLevel,
    protective_stop,
    simulate,
)
from Repositories.Performance.modules.hashchain import GENESIS, chain_hash
from Repositories.Strategies.TimeMode.helpers import timemode as ported


def _bar(exchange: str, tf: str, open_time: datetime, price: float) -> CandleBar:
    return CandleBar(
        exchange=exchange,
        symbol="BTCUSDT",
        timeframe=tf,
        open_time=open_time,
        open=price,
        high=price + 2,
        low=price - 2,
        close=price + 1,
        volume=10,
    )


def test_binance_parser_drops_the_forming_bar() -> None:
    future = int((datetime.now(UTC) + timedelta(days=2)).timestamp() * 1000)
    past = future - 86_400_000 * 3
    rows = [
        [past, "1", "3", "0.5", "2", "9"],
        [future, "2", "4", "1", "3", "8"],
    ]
    bars = parse_binance("BTCUSDT", "1d", rows)
    assert len(bars) == 1
    assert bars[0].close == 2
    assert bars[0].open_time.tzinfo is UTC


def test_kucoin_parser_uses_open_close_high_low_order() -> None:
    start = int(datetime(2024, 1, 1, tzinfo=UTC).timestamp())
    rows = [[str(start), "10", "12", "13", "9", "4", "40"]]
    bars = parse_kucoin("BTCUSDT", "1d", rows)
    assert bars[0].open == 10
    assert bars[0].close == 12
    assert bars[0].high == 13
    assert bars[0].low == 9
    assert bars[0].volume == 4


def test_resample_8h_from_4h_and_3d_from_1d() -> None:
    start = datetime(2024, 1, 1, tzinfo=UTC)
    four = []
    for step in range(6):
        four.append(_bar("kucoin", "4h", start + timedelta(hours=4 * step), 100 + step))
    eight = resample(four, "4h", "8h", now=start + timedelta(days=3))
    assert [bar.open_time.hour for bar in eight] == [0, 8, 16]
    assert eight[0].open == four[0].open
    assert eight[0].close == four[1].close
    assert eight[0].origin == "resampled"
    daily = [
        _bar("kucoin", "1d", start + timedelta(days=offset), 50 + offset) for offset in range(6)
    ]
    three = resample(daily, "1d", "3d", now=start + timedelta(days=20))
    assert three
    assert all(bar.timeframe == "3d" for bar in three)


def test_hash_chain_changes_when_payload_changes() -> None:
    first = chain_hash(GENESIS, {"price": 1})
    second = chain_hash(first, {"price": 2})
    tampered = chain_hash(first, {"price": 3})
    assert first != GENESIS
    assert second != tampered
    assert chain_hash(GENESIS, {"b": 1, "a": 2}) == chain_hash(GENESIS, {"a": 2, "b": 1})


def test_ported_detector_matches_prototype_on_synthetic_bars() -> None:
    import sys

    sys.path.insert(0, "prototype")
    import timemode as prototype  # noqa: WPS433

    rng = np.random.default_rng(7)
    price = 100 + np.cumsum(rng.normal(0, 1, 400))
    candles = []
    for index, close in enumerate(price):
        candles.append(
            {
                "t": index * 86_400_000,
                "ct": (index + 1) * 86_400_000,
                "o": float(close - 0.4),
                "h": float(close + 1.2),
                "l": float(close - 1.3),
                "c": float(close),
            }
        )
    params = {
        "atr_length": 14,
        "confirm_atr_mult": 0.7,
        "sma_length": 70,
        "mode_min_bars": 5,
        "mode_max_bars": 20,
        "swing_lookback": 5,
        "consolidation_limit": 20,
        "body_range_ratio": 0.6,
        "mode_touch_density": 0.75,
        "mode_touch_tol_atr": 0.02,
        "expansion_rule": "either",
        "confirm_types": ["atr_expansion", "close_outside_range", "clear_gap"],
        "body_cross_count_rule": {"default": "confirm_bar", "1w": "part_of_mode_next_bar"},
        "flip_window_bars": 3,
        "flip_requires_engulfing": True,
        "flip_requires_expansion": True,
        "expiry_after_flip": False,
        "block_min_bars_after": 2,
        "sma_filter_timeframe": "entry",
        "exit_rule": "two_lower_closes",
        "enable_shorts": True,
        "block_ttl_bars": 30,
        "block_merge_atr": 0.25,
    }
    resolved = prototype.params_for(params, "1d")
    data = prototype.arrays(candles)
    assert ported.detect_modes(data, resolved) == prototype.detect_modes(data, resolved)


def test_paper_stop_and_fee_math() -> None:
    stop = protective_stop("long", 100, 100, 95, 4)
    assert stop < 100
    start = datetime(2024, 1, 1, tzinfo=UTC)
    bars = []
    for offset, close in enumerate([101, 102, 103, 90, 89]):
        bars.append(
            CandleBar(
                exchange="binance",
                symbol="BTCUSDT",
                timeframe="4h",
                open_time=start + timedelta(hours=4 * offset),
                open=close,
                high=close + 1,
                low=close - 1 if offset < 3 else 80,
                close=close,
                volume=1,
            )
        )
    entry = EntrySignal(
        exchange="binance",
        symbol="BTCUSDT",
        timeframe="4h",
        direction="long",
        close_time=bars[0].close_time,
        price=101,
        level=100,
        atr=4,
        stop=90,
        score=9,
        signal_id="abc",
        candle_low=99,
        candle_high=103,
        strategy_version="test",
        inputs={},
    )
    result = simulate([entry], {"4h": bars}, equity=10_000, slippage_bps=0)
    assert len(result.trades) == 1
    assert result.trades[0].exit_reason == "stop"
    assert result.trades[0].fee > 0
    assert result.equity < 10_000


def test_same_direction_signal_is_blocked_and_counted() -> None:
    start = datetime(2024, 1, 1, tzinfo=UTC)
    bars = [
        CandleBar(
            exchange="binance", symbol="BTCUSDT", timeframe="4h",
            open_time=start + timedelta(hours=4 * i),
            open=100, high=101, low=99, close=100, volume=1,
        )
        for i in range(6)
    ]

    def _entry(index: int) -> EntrySignal:
        return EntrySignal(
            "binance", "BTCUSDT", "4h", "long", bars[index].close_time, 100, 90, 4, 80,
            9, f"id{index}", 99, 101, "test", {},
        )

    result = simulate([_entry(0), _entry(2)], {"4h": bars}, slippage_bps=0, exit_mode="two_close")
    assert result.blocked == 1
    assert len(result.trades) == 1
    assert result.trades[0].realized is False


def test_opposite_signal_closes_and_reverses() -> None:
    start = datetime(2024, 1, 1, tzinfo=UTC)
    bars = [
        CandleBar(
            exchange="binance", symbol="BTCUSDT", timeframe="4h",
            open_time=start + timedelta(hours=4 * i),
            open=100, high=110, low=90, close=100, volume=1,
        )
        for i in range(4)
    ]
    long = EntrySignal(
        "binance", "BTCUSDT", "4h", "long", bars[0].close_time, 100, 90, 4, 80,
        9, "long", 99, 101, "test", {},
    )
    short = EntrySignal(
        "binance", "BTCUSDT", "4h", "short", bars[2].close_time, 100, 110, 4, 120,
        9, "short", 99, 101, "test", {},
    )
    result = simulate([long, short], {"4h": bars}, slippage_bps=0, exit_mode="opposite")
    closed = [trade for trade in result.trades if trade.realized]
    assert closed[0].exit_reason == "opposite_signal"
    assert any(trade.direction == "short" for trade in result.trades)


def test_trail_can_lock_a_profit() -> None:
    start = datetime(2024, 1, 1, tzinfo=UTC)
    bars = []
    for offset, close, low in ((0, 100, 99), (1, 120, 112), (2, 111, 108)):
        bars.append(
            CandleBar(
                exchange="binance",
                symbol="BTCUSDT",
                timeframe="4h",
                open_time=start + timedelta(hours=4 * offset),
                open=close,
                high=close + 1,
                low=low,
                close=close,
                volume=1,
            )
        )
    entry = EntrySignal(
        "binance", "BTCUSDT", "4h", "long", bars[0].close_time, 100, 90, 4, 90,
        9, "trail", 99, 101, "test", {},
    )
    trail = TrailLevel(bars[1].close_time, 110, "long", "swing")
    result = simulate(
        [entry], {"4h": bars}, slippage_bps=0, exit_mode="trail", trails=[trail]
    )
    assert result.trades[0].exit_reason == "trail"
    assert result.trades[0].r_multiple > 0


def test_win_rate_ignores_open_trades() -> None:
    from scripts.stats import window_metrics

    start = datetime(2024, 1, 1, tzinfo=UTC)
    daily = [
        CandleBar(
            exchange="binance", symbol="BTCUSDT", timeframe="1d",
            open_time=start + timedelta(days=i),
            open=100, high=101, low=99, close=100, volume=1,
        )
        for i in range(5)
    ]
    closed = PaperTrade(
        "a", "binance", "BTCUSDT", "4h", "long", daily[0].close_time, daily[1].close_time,
        100, 90, 110, "stop", 1, 10, 1.0, 0.2, True,
    )
    still = PaperTrade(
        "b", "binance", "BTCUSDT", "4h", "long", daily[2].close_time, None,
        100, 90, 100, "open", 1, -5, -0.5, 0.1, False, entry_fee=0.1,
    )
    stats = window_metrics([closed, still], daily, "2024-01-01", "2024-01-10")
    assert stats["closed"] == 1
    assert stats["win_rate"] == 1
    assert stats["avg_r"] == 1
    assert stats["realized"] == 10
    assert stats["unrealized"] != 0


def test_binance_fallback_uses_vision_after_primary_failure(monkeypatch) -> None:
    async def _no_sleep(_delay: float) -> None:
        return None

    monkeypatch.setattr(http_client.asyncio, "sleep", _no_sleep)
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        if "api.binance.com" in str(request.url):
            return httpx.Response(500, json={"code": -1})
        open_ms = 1_577_836_800_000
        return httpx.Response(
            200,
            json=[[open_ms, "1", "2", "0.5", "1.5", "3", open_ms + 86_400_000]],
        )

    http_client.set_client(httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    try:
        import asyncio

        from Repositories.MarketData.modules.binance import fetch_klines

        bars = asyncio.run(
            fetch_klines(
                "BTCUSDT",
                "1d",
                datetime(2020, 1, 1, tzinfo=UTC),
                datetime(2020, 1, 3, tzinfo=UTC),
            )
        )
    finally:
        http_client.set_client(None)
    assert any("data-api.binance.vision" in url for url in calls)
    assert bars and bars[0].exchange == "binance"

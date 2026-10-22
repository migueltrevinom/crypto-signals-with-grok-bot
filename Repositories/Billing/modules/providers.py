"""Payment providers. Stripe bills cards. BTCPay and NOWPayments are the crypto options.

Crypto subscriptions use renewal_mode manual. Coinbase Commerce is not an adapter.
"""

from typing import Any, Protocol


class PaymentProvider(Protocol):
    name: str

    async def create_checkout(self, user_id: str, plan_code: str) -> dict[str, Any]:
        """Return a URL the client redirects to. No card data comes back."""

    async def parse_webhook(self, body: bytes, signature: str) -> dict[str, Any]:
        """Verify the signature and return the event. Reject on a bad signature."""


class StripeProvider:
    name = "stripe"

    async def create_checkout(self, user_id: str, plan_code: str) -> dict[str, Any]:
        del user_id, plan_code
        raise NotImplementedError("Stripe checkout is not implemented in the planning skeleton.")

    async def parse_webhook(self, body: bytes, signature: str) -> dict[str, Any]:
        del body, signature
        raise NotImplementedError("Stripe webhooks are not implemented in the planning skeleton.")


class BtcPayProvider:
    name = "btcpay"

    async def create_checkout(self, user_id: str, plan_code: str) -> dict[str, Any]:
        del user_id, plan_code
        raise NotImplementedError("BTCPay subscriptions are specified and not implemented.")

    async def parse_webhook(self, body: bytes, signature: str) -> dict[str, Any]:
        del body, signature
        raise NotImplementedError("BTCPay webhooks are specified and not implemented.")


class NowPaymentsProvider:
    name = "nowpayments"

    async def create_checkout(self, user_id: str, plan_code: str) -> dict[str, Any]:
        del user_id, plan_code
        raise NotImplementedError("NOWPayments checkout is specified and not implemented.")

    async def parse_webhook(self, body: bytes, signature: str) -> dict[str, Any]:
        del body, signature
        raise NotImplementedError("NOWPayments webhooks are specified and not implemented.")

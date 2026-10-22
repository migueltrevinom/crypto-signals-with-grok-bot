"""Payment providers. Stripe first. Crypto uses the same subscription rows."""

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


class CryptoProvider:
    name = "crypto"

    async def create_checkout(self, user_id: str, plan_code: str) -> dict[str, Any]:
        del user_id, plan_code
        raise NotImplementedError("Crypto checkout is a later provider, not this pass.")

    async def parse_webhook(self, body: bytes, signature: str) -> dict[str, Any]:
        del body, signature
        raise NotImplementedError("Crypto payment events are a later provider, not this pass.")

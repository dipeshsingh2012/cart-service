import uuid
from typing import Optional
import httpx

from src.config import settings
from src.schemas.cart import AddItemRequest, CartResponse, LineItem


class CommercetoolsClient:
    def __init__(self):
        self.project_key = settings.CTP_PROJECT_KEY
        self.client_id = settings.CTP_CLIENT_ID
        self.client_secret = settings.CTP_CLIENT_SECRET
        self.api_url = settings.CTP_API_URL
        self.auth_url = settings.CTP_AUTH_URL

        # In-memory mock storage for offline / sandbox development
        self._mock_carts: dict[str, CartResponse] = {}

    def is_configured(self) -> bool:
        return bool(self.project_key and self.client_id and self.client_secret)

    async def get_or_create_cart(self, cart_id: Optional[str] = None) -> CartResponse:
        if cart_id and cart_id in self._mock_carts:
            return self._mock_carts[cart_id]

        new_id = cart_id or f"cart_{uuid.uuid4().hex[:12]}"
        cart = CartResponse(
            id=new_id,
            version=1,
            line_items=[],
            total_price_cents=0,
            currency_code="USD",
            total_items_count=0,
        )
        self._mock_carts[new_id] = cart
        return cart

    async def add_item(self, cart_id: str, item_req: AddItemRequest) -> CartResponse:
        cart = await self.get_or_create_cart(cart_id)
        price_cents = int(round(item_req.price * 100))

        # Check if already in cart
        existing = next((li for li in cart.line_items if li.product_id == item_req.product_id), None)
        if existing:
            existing.quantity += item_req.quantity
            existing.total_price_cents = existing.quantity * existing.price_cents
            if item_req.fitment_verified:
                existing.fitment_verified = True
        else:
            line_item = LineItem(
                id=f"li_{uuid.uuid4().hex[:8]}",
                product_id=item_req.product_id,
                name=item_req.name,
                quantity=item_req.quantity,
                price_cents=price_cents,
                total_price_cents=price_cents * item_req.quantity,
                currency_code="USD",
                image_url=item_req.image_url,
                brand=item_req.brand,
                dimensions_summary=item_req.dimensions_summary,
                fitment_verified=item_req.fitment_verified,
            )
            cart.line_items.append(line_item)

        self._recalculate(cart)
        return cart

    async def update_item_quantity(
        self, cart_id: str, line_item_id: str, quantity: int
    ) -> Optional[CartResponse]:
        if cart_id not in self._mock_carts:
            return None
        cart = self._mock_carts[cart_id]

        if quantity <= 0:
            cart.line_items = [li for li in cart.line_items if li.id != line_item_id]
        else:
            for li in cart.line_items:
                if li.id == line_item_id:
                    li.quantity = quantity
                    li.total_price_cents = li.quantity * li.price_cents
                    break

        self._recalculate(cart)
        return cart

    async def remove_item(self, cart_id: str, line_item_id: str) -> Optional[CartResponse]:
        return await self.update_item_quantity(cart_id, line_item_id, quantity=0)

    def _recalculate(self, cart: CartResponse):
        cart.version += 1
        cart.total_price_cents = sum(li.total_price_cents for li in cart.line_items)
        cart.total_items_count = sum(li.quantity for li in cart.line_items)

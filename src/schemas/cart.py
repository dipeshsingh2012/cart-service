from typing import Optional
from pydantic import BaseModel, Field


class CentPrecisionMoney(BaseModel):
    cent_amount: int
    currency_code: str = "USD"
    fraction_digits: int = 2

    @property
    def formatted_amount(self) -> float:
        return self.cent_amount / (10 ** self.fraction_digits)


class LineItem(BaseModel):
    id: str
    product_id: str
    name: str
    quantity: int
    price_cents: int
    total_price_cents: int
    currency_code: str = "USD"
    image_url: Optional[str] = None
    brand: Optional[str] = None
    dimensions_summary: Optional[str] = None  # e.g. "32.2 × 40.7 × 32.2 cm"
    fitment_verified: bool = False  # True if CounterCheck AI confirmed countertop fit


class CartResponse(BaseModel):
    id: str
    version: int = 1
    line_items: list[LineItem] = Field(default_factory=list)
    total_price_cents: int = 0
    currency_code: str = "USD"
    total_items_count: int = 0

    @property
    def formatted_total(self) -> float:
        return self.total_price_cents / 100.0


class AddItemRequest(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int = 1
    brand: Optional[str] = None
    image_url: Optional[str] = None
    dimensions_summary: Optional[str] = None
    fitment_verified: bool = False


class UpdateQuantityRequest(BaseModel):
    quantity: int = Field(..., ge=0, description="New line item quantity (0 removes item)")

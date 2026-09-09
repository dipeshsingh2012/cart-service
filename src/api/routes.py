from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status
from src.schemas.cart import AddItemRequest, CartResponse, UpdateQuantityRequest
from src.services.commercetools_client import CommercetoolsClient

router = APIRouter(prefix="/api/v1/cart", tags=["Cart"])
ct_client = CommercetoolsClient()


@router.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok",
        "service": "cart-service",
        "version": "0.1.0",
        "commercetools_configured": ct_client.is_configured(),
    }


@router.post("", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def create_cart(cart_id: Optional[str] = Query(None)):
    """Creates a new anonymous or user cart session."""
    return await ct_client.get_or_create_cart(cart_id)


@router.get("/{cart_id}", response_model=CartResponse)
async def get_cart(cart_id: str):
    """Retrieves an existing cart by ID."""
    cart = await ct_client.get_or_create_cart(cart_id)
    return cart


@router.post("/{cart_id}/items", response_model=CartResponse)
async def add_item_to_cart(cart_id: str, item: AddItemRequest):
    """Adds a product to the cart with fitment verification status."""
    return await ct_client.add_item(cart_id, item)


@router.patch("/{cart_id}/items/{line_item_id}", response_model=CartResponse)
async def update_line_item(
    cart_id: str, line_item_id: str, update_req: UpdateQuantityRequest
):
    """Updates line item quantity (or removes if quantity is 0)."""
    cart = await ct_client.update_item_quantity(
        cart_id, line_item_id, update_req.quantity
    )
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.delete("/{cart_id}/items/{line_item_id}", response_model=CartResponse)
async def remove_line_item(cart_id: str, line_item_id: str):
    """Removes a line item from the cart."""
    cart = await ct_client.remove_item(cart_id, line_item_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

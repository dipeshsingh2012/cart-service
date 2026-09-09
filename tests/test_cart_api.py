import pytest
from httpx import ASGITransport, AsyncClient
from src.main import app


@pytest.fixture
async def test_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_cart_lifecycle(test_client: AsyncClient):
    # 1. Create cart
    res = await test_client.post("/api/v1/cart")
    assert res.status_code == 201
    cart = res.json()
    cart_id = cart["id"]
    assert cart["total_items_count"] == 0

    # 2. Add line item with fitment verification
    add_payload = {
        "product_id": "prod_delonghi_dedica",
        "name": "Dedica Deluxe Slim Espresso",
        "price": 299.95,
        "quantity": 1,
        "brand": "De'Longhi",
        "dimensions_summary": "14.9 × 30.5 × 33.0 cm",
        "fitment_verified": True,
    }
    add_res = await test_client.post(f"/api/v1/cart/{cart_id}/items", json=add_payload)
    assert add_res.status_code == 200
    updated_cart = add_res.json()
    assert updated_cart["total_items_count"] == 1
    assert len(updated_cart["line_items"]) == 1
    assert updated_cart["line_items"][0]["fitment_verified"] is True
    line_item_id = updated_cart["line_items"][0]["id"]

    # 3. Update quantity
    update_res = await test_client.patch(
        f"/api/v1/cart/{cart_id}/items/{line_item_id}", json={"quantity": 2}
    )
    assert update_res.status_code == 200
    assert update_res.json()["total_items_count"] == 2

    # 4. Remove line item
    del_res = await test_client.delete(f"/api/v1/cart/{cart_id}/items/{line_item_id}")
    assert del_res.status_code == 200
    assert del_res.json()["total_items_count"] == 0

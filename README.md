# Cart Service (`cart-service`)

> **commercetools Cart Microservice with Kitchen Fitment Verification Metadata**

`cart-service` manages shopping carts, line items, price calculations, and kitchen fitment readiness flags. It connects to commercetools' MACH-certified commerce platform while providing an in-memory fallback engine for offline local development.

---

## 🎯 Features

1. **commercetools Client:** Authenticates via OAuth2 client credentials and executes Cart API actions (`create`, `addLineItem`, `changeLineItemQuantity`, `removeLineItem`).
2. **Fitment Verification Custom Fields:** Stores whether each appliance in the cart has had its kitchen counter clearance verified, preventing post-delivery dimensional returns.
3. **In-Memory Mock Fallback:** Full commercetools-compliant cart simulation when credentials are unset.

---

## 🚀 API Endpoints

- `POST /api/v1/cart` — Create new anonymous or customer cart.
- `GET /api/v1/cart/{cart_id}` — Retrieve cart by ID.
- `POST /api/v1/cart/{cart_id}/items` — Add product line item with fitment status.
- `PATCH /api/v1/cart/{cart_id}/items/{line_item_id}` — Update quantity.
- `DELETE /api/v1/cart/{cart_id}/items/{line_item_id}` — Remove line item.
- `GET /api/v1/health` — Health check endpoint.

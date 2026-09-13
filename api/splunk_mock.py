import json
import random
from datetime import datetime, timezone

from fastapi import FastAPI, Path

app = FastAPI()

MOCK_LOGS = {
    "auth": [
        {"level": "ERROR", "service": "auth-service", "message": "ERROR [AuthController] - Authentication failed for user user-123. Invalid credentials supplied. Trace: org.springframework.security.authentication.BadCredentialsException: Invalid username or password at AuthProvider.authenticate(AuthProvider.java:87)", "status_code": 401},
    ],
    "catalog": [
        {"level": "ERROR", "service": "catalog-service", "message": "FATAL [CatalogDAO] - Product catalog database unavailable. SQLException: Connection refused (DB_HOST:5432). Caused by: java.net.ConnectException: Connection timed out", "status_code": 503},
    ],
    "cart": [
        {"level": "ERROR", "service": "cart-service", "message": "ERROR [CartController] - Cart could not be loaded for cart cart-991. java.lang.NullPointerException: Cannot invoke getItems() on null object at CartService.loadCart(CartService.java:142)", "status_code": 500},
    ],
    "order": [
        {"level": "ERROR", "service": "order-service", "message": "ERROR [OrderValidator] - Order creation failed validation for order order-882. Field 'shipping_address' missing. javax.validation.ValidationException: Required field not present", "status_code": 422},
    ],
    "payment": [
        {"level": "ERROR", "service": "payment-service", "message": "ERROR [PaymentGatewayClient] - Connection timeout to payment gateway Stripe. java.net.SocketTimeoutException: Read timed out after 30000ms while calling https://api.stripe.com/v1/charges", "status_code": 504},
    ],
    "inventory": [
        {"level": "ERROR", "service": "inventory-service", "message": "ERROR [InventorySyncJob] - Inventory synchronization failed for SKU sku-441. OptimisticLockException: Row version mismatch. Caused by concurrent update at InventoryLedger.updateStock(InventoryLedger.java:211)", "status_code": 503},
    ],
    "shipping": [
        {"level": "ERROR", "service": "shipping-service", "message": "ERROR [ShippoClient] - Carrier API returned error for shipment ship-882. HTTP 502 Bad Gateway. Response body: {\"error\":\"Rate limit exceeded\"}", "status_code": 502},
    ],
    "notification": [
        {"level": "ERROR", "service": "notification-service", "message": "ERROR [EmailDispatcher] - Notification delivery failed for order order-771. javax.mail.MessagingException: 550 Requested action not taken: mailbox unavailable", "status_code": 502},
    ],
    "generic": [
        {"level": "ERROR", "service": "generic-ecommerce-service", "message": "ERROR [GatewayHandler] - Downstream dependency returned unexpected response. HTTP 502 Bad Gateway from recommendation-service. Caused by: com.fasterxml.jackson.databind.JsonMappingException: Cannot deserialize value of type 'Product' from String 'null'", "status_code": 502},
    ],
}

CATEGORY_ALIASES = {
    "products": "catalog",
    "product": "catalog",
    "orders": "order",
    "payments": "payment",
    "stock": "inventory",
    "delivery": "shipping",
    "notifications": "notification",
}


def _normalise_category(category: str) -> str:
    category = category.strip().lower().replace(" ", "-")
    return CATEGORY_ALIASES.get(category, category)


def _build_response(category: str):
    requested_category = category or "generic"
    normalised_category = _normalise_category(requested_category)
    selected_category = normalised_category if normalised_category in MOCK_LOGS else "generic"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    selected_logs = []

    available_logs = MOCK_LOGS[selected_category]
    for template in random.sample(available_logs, k=min(3, len(available_logs))):
        payload = {
            key: str(value)
            .replace("{uid}", str(random.randint(1000, 9999)))
            .replace("{category}", requested_category)
            if isinstance(value, str)
            else value
            for key, value in template.items()
        }
        payload["timestamp"] = now
        selected_logs.append(json.dumps(payload))

    return {
        "status": "Success",
        "originator": "mock-splunk-server",
        "requested_category": requested_category,
        "service_category": selected_category,
        "logs": selected_logs,
    }

@app.get("/api/splunk_mock")
def get_splunk_logs(category: str = "generic"):
    """Return logs for a category, or generic logs when it is unknown."""
    return _build_response(category)


@app.get("/api/splunk_mock/{category}")
def get_category_logs(
    category: str = Path(description="Ecommerce service category")
):
    """Path-based form of the category-specific mock endpoint."""
    return _build_response(category)

"""
CHA YUAN API - Django Ninja

Main API initialization with router aggregation.
"""

from ninja import NinjaAPI
from ninja.errors import HttpError

from apps.api.v1.products import router as products_router
from apps.api.v1.cart import router as cart_router
from apps.api.v1.checkout import router as checkout_router
from apps.api.v1.content import router as content_router


# Create main API instance
api = NinjaAPI(
    title="CHA YUAN API",
    version="1.0.0",
    description="Premium Tea E-Commerce API for Singapore",
    docs_url="/api/docs/",
    openapi_url="/api/openapi.json",
)

# Register routers
api.add_router("/products/", products_router, tags=["products"])
api.add_router("/cart/", cart_router, tags=["cart"])
api.add_router("/checkout/", checkout_router, tags=["checkout"])
api.add_router("/content/", content_router, tags=["content"])

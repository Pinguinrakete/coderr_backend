from django.urls import path
from .views import OrdersView, OrderSingleView, OrderCountView, CompletedOrderCountView

"""
URL patterns for order management.

Endpoints:

- GET /orders/
  Retrieves a list of all orders.
  Returns: list of orders.

- GET /orders/<int:id>/
  Retrieves details of a specific order identified by its ID.
  Returns: order data or 404 if not found.

- GET /order-count/<int:business_user_id>/
  Retrieves the total count of orders for a specific business user.
  Returns: integer count of orders.

- GET /completed-order-count/<int:business_user_id>/
  Retrieves the count of completed orders for a specific business user.
  Returns: integer count of completed orders.
"""
urlpatterns = [
    path('orders/', OrdersView.as_view()),
    path('orders/<int:id>/', OrderSingleView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-oder-count')
]
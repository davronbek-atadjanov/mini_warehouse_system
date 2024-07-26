from django.urls import path
from .views import WarehouseAPIView

urlpatterns = [
    path('product/', WarehouseAPIView.as_view(), name='product_get'),
]

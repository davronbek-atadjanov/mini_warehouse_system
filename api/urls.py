from django.urls import path
from .views import WarehouseListAPIView

urlpatterns = [
    path('product/list/', WarehouseListAPIView.as_view(), name='product_list'),
]

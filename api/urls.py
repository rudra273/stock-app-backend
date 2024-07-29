# api/urls.py

from django.urls import path
from .views import StockDataAPIView

urlpatterns = [
    path('stock-data/', StockDataAPIView.as_view(), name='stock-data'),
]

# api/urls.py

from django.urls import path
from .views import StockDataAPIView, HistoricalStockDataAPIView

urlpatterns = [
    path('stock-data/', StockDataAPIView.as_view(), name='stock-data'),
    path('historical-stock-data/', HistoricalStockDataAPIView.as_view(), name='historical-stock-data'),

]

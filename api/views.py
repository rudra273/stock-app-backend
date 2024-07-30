from django.shortcuts import render

# Create your views here.
# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.stock_services import get_stock_data
from api.serializers import StockDataSerializer, HistoricalStockDataSerializer
from services.postgres import fetch_data_from_pg, fetch_data_from_pg2
from datetime import datetime, timedelta

class StockDataAPIView(APIView):
    def get(self, request, *args, **kwargs):
        symbols = [
            "MSFT", "AAPL", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "ADBE", "INTC", "NFLX",
            "CSCO", "AMD", "BA", "IBM", "DIS", "PYPL", "MA", "V", "WMT", "KO"
        ]
        country = request.query_params.get('country', 'USA')
        data = get_stock_data(symbols, country)
        serializer = StockDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class HistoricalStockDataAPIView(APIView):
    def get(self, request, *args, **kwargs):
        symbol = request.query_params.get('symbol')
        period = request.query_params.get('period', '1y')

        if not symbol:
            return Response({"error": "Symbol parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        if period not in ['1d', '1w', '1mo', '3mo', '6mo', '1y']:
            return Response({"error": "Invalid period parameter."}, status=status.HTTP_400_BAD_REQUEST)
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days={
            '1d': 1,
            '1w': 7,
            '1mo': 30,
            '3mo': 90,
            '6mo': 180,
            '1y': 365
        }[period])

        query = f"""
        SELECT "Date", "Close"
        FROM public.historical_data
        WHERE symbol = %s AND "Date" BETWEEN %s AND %s
        ORDER BY "Date";
        """
        
        df = fetch_data_from_pg(schema_name='public', table_or_view_name='historical_data', query=query, params=(symbol, start_date, end_date))
        print(df)
        if df is not None:
            serializer = HistoricalStockDataSerializer(df.to_dict(orient='records'), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No data found."}, status=status.HTTP_404_NOT_FOUND)



class StockDataDBAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Define the query to fetch stock data from PostgreSQL
        query = """
        SELECT *
        FROM public.stock_data;
        """
        
        # Fetch data from PostgreSQL
        df = fetch_data_from_pg2(schema_name='public', table_or_view_name='stock_data', query=query)
        print(df)
        
        if df is not None:
            # Serialize the DataFrame
            serializer = StockDataSerializer(df.to_dict(orient='records'), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No data found."}, status=status.HTTP_404_NOT_FOUND) 
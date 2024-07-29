from rest_framework import serializers

class StockDataSerializer(serializers.Serializer):
    Symbol = serializers.CharField()
    Open = serializers.FloatField()
    High = serializers.FloatField()
    Low = serializers.FloatField()
    Close = serializers.FloatField()
    CurrentPrice = serializers.FloatField()
    PreviousClose = serializers.FloatField()
    FiftyTwoWeekRange = serializers.CharField()
    MarketCap = serializers.IntegerField(allow_null=True)
    CompanyName = serializers.CharField()
    Currency = serializers.CharField()
    PercentageChange = serializers.CharField()
    PriceChange = serializers.CharField() 



class HistoricalStockDataSerializer(serializers.Serializer):
    date = serializers.DateField()
    close = serializers.FloatField()

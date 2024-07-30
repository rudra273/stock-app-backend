import pandas as pd
from stock_services import get_stock_data
from datetime import datetime
from postgres import dump_to_postgresql


def ingest_stock_data(symbols, country):
    
    # Fetch stock data
    stock_data = get_stock_data(symbols, country)
    
    # Create DataFrame
    df = pd.DataFrame(stock_data)
    print(df)
    
    
    dump_to_postgresql(df, schema_name='public', table_name='stock_data')


def in_main():
    symbols = [
        "MSFT", "AAPL", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "ADBE", "INTC", "NFLX",
        "CSCO", "AMD", "BA", "IBM", "DIS", "PYPL", "MA", "V", "WMT", "KO"
    ]    
    country = "USA"
    ingest_stock_data(symbols, country) 

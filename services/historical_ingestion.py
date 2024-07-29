# data_ingestion/services/ingestion_services.py
import yfinance as yf
import pandas as pd
from postgres import dump_to_postgresql

def fetch_historical_data(symbols, period="1y"):
    historical_data = {}
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)
            hist['symbol'] = symbol
            hist['company_name'] = stock.info.get('shortName', 'N/A')
            hist['marketCap'] = stock.info.get('marketCap', 'N/A')
            hist['sector'] = stock.info.get('sector', 'N/A')
            hist['industry'] = stock.info.get('industry', 'N/A')
            historical_data[symbol] = hist
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {str(e)}")
    return historical_data

def process_historical_data(historical_data):
    historical_df_list = []
    for symbol, hist in historical_data.items():
        hist.reset_index(inplace=True)
        hist = hist[['Date', 'symbol', 'company_name', 'Volume', 'marketCap', 'sector', 'industry', 'Open', 'Close', 'High', 'Low']]
        historical_df_list.append(hist)
    
    if historical_df_list:
        combined_historical_df = pd.concat(historical_df_list, ignore_index=True)
        return combined_historical_df
    return None

def fetch_and_store_historical_data():
    symbols = [
        "MSFT", "AAPL", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "ADBE", "INTC", "NFLX",
        "CSCO", "AMD", "BA", "IBM", "DIS", "PYPL", "MA", "V", "WMT", "KO"
    ]
    
    historical_data = fetch_historical_data(symbols)
    historical_df = process_historical_data(historical_data)
    
    if historical_df is not None:
        dump_to_postgresql(historical_df, schema_name='public', table_name='historical_data')


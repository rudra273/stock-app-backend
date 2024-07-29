# import yfinance as yf
# import pytz
# from datetime import datetime

# COUNTRY_MARKET_HOURS = {
#     'USA': {
#         'timezone': 'US/Eastern',
#         'market_open': '09:30:00',
#         'market_close': '16:00:00'
#     },
#     'India': {
#         'timezone': 'Asia/Kolkata',
#         'market_open': '09:15:00',
#         'market_close': '15:30:00'
#     }
# }

# def get_stock_data(symbols, country):
#     data = []
#     market_hours = COUNTRY_MARKET_HOURS.get(country)
#     if not market_hours:
#         raise ValueError(f"Market hours for country '{country}' not found")

#     tz = pytz.timezone(market_hours['timezone'])
#     now = datetime.now(tz)
#     today = now.date()
#     current_time = now.time()
    
#     market_open = datetime.strptime(market_hours['market_open'], '%H:%M:%S').time()
#     market_close = datetime.strptime(market_hours['market_close'], '%H:%M:%S').time()

#     market_state = 'closed'
#     if today.weekday() < 5:  # Weekdays only
#         if market_open <= current_time <= market_close:
#             market_state = 'open'

#     for symbol in symbols:
#         stock = yf.Ticker(symbol)
#         hist = stock.history(period='1d')

#         if hist.empty:
#             continue
        
#         open_price = hist['Open'].iloc[0]
#         close_price = hist['Close'].iloc[0]
#         high_price = hist['High'].iloc[0]
#         low_price = hist['Low'].iloc[0]
#         previous_close = hist['Close'].iloc[0]  # No previous close for a single day; use current close
#         fifty_two_week_range = f"{stock.info.get('fiftyTwoWeekLow', 'N/A')} - {stock.info.get('fiftyTwoWeekHigh', 'N/A')}"
#         market_cap = stock.info.get('marketCap', 'N/A')
#         company_name = stock.info.get('shortName', 'N/A')
#         currency = stock.info.get('currency', 'N/A')

#         percentage_change = ((close_price - open_price) / open_price) * 100 if open_price else 'N/A'
#         price_change = 'up' if close_price > open_price else 'down'

#         data.append({
#             'Symbol': symbol,
#             'Open': open_price,
#             'High': high_price,
#             'Low': low_price,
#             'Close': close_price,
#             'CurrentPrice': close_price,
#             'PreviousClose': previous_close,
#             'FiftyTwoWeekRange': fifty_two_week_range,
#             'MarketCap': market_cap,
#             'CompanyName': company_name,
#             'Currency': currency,
#             'PercentageChange': f"{percentage_change:.2f}%" if percentage_change != 'N/A' else 'N/A',
#             'PriceChange': price_change
#         })

#     return data


# # Example usage with selected 15 companies
# # symbols = [
# #     "MSFT", "AAPL", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "ADBE", "INTC", "NFLX",
# #     "CSCO", "AMD", "BA", "IBM", "DIS"
# # ]

# # stock_data = get_stock_data(symbols, "USA")
# # for data in stock_data:
# #     print(data)

import yfinance as yf
import pytz
from datetime import datetime

COUNTRY_MARKET_HOURS = {
    'USA': {
        'timezone': 'US/Eastern',
        'market_open': '09:30:00',
        'market_close': '16:00:00'
    },
    'India': {
        'timezone': 'Asia/Kolkata',
        'market_open': '09:15:00',
        'market_close': '15:30:00'
    }
}

def get_stock_data(symbols, country):
    data = []
    market_hours = COUNTRY_MARKET_HOURS.get(country)
    if not market_hours:
        raise ValueError(f"Market hours for country '{country}' not found")

    tz = pytz.timezone(market_hours['timezone'])
    now = datetime.now(tz)
    today = now.date()
    current_time = now.time()
    
    market_open = datetime.strptime(market_hours['market_open'], '%H:%M:%S').time()
    market_close = datetime.strptime(market_hours['market_close'], '%H:%M:%S').time()

    market_state = 'closed'
    if today.weekday() < 5:  # Weekdays only
        if market_open <= current_time <= market_close:
            market_state = 'open'

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        hist = stock.history(period='1d')

        if hist.empty:
            continue
        
        open_price = hist['Open'].iloc[0]
        close_price = hist['Close'].iloc[0]
        high_price = hist['High'].iloc[0]
        low_price = hist['Low'].iloc[0]
        previous_close = hist['Close'].iloc[0]  # No previous close for a single day; use current close
        fifty_two_week_range = f"{stock.info.get('fiftyTwoWeekLow', 'N/A')} - {stock.info.get('fiftyTwoWeekHigh', 'N/A')}"
        market_cap = stock.info.get('marketCap', 'N/A')
        company_name = stock.info.get('shortName', 'N/A')
        currency = stock.info.get('currency', 'N/A')

        percentage_change = ((close_price - open_price) / open_price) * 100 if open_price else 'N/A'
        price_change = 'up' if close_price > open_price else 'down'

        data.append({
            'Symbol': symbol,
            'Open': open_price,
            'High': high_price,
            'Low': low_price,
            'Close': close_price,
            'CurrentPrice': close_price,
            'PreviousClose': previous_close,
            'FiftyTwoWeekRange': fifty_two_week_range,
            'MarketCap': market_cap,
            'CompanyName': company_name,
            'Currency': currency,
            'PercentageChange': f"{percentage_change:.2f}%" if percentage_change != 'N/A' else 'N/A',
            'PriceChange': price_change,
            'MarketState': market_state
        })

    return data

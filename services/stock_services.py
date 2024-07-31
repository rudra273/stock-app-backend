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
        
        open_price = round(float(hist['Open'].iloc[0]), 4)
        close_price = round(float(hist['Close'].iloc[0]), 4)
        high_price = round(float(hist['High'].iloc[0]), 4)
        low_price = round(float(hist['Low'].iloc[0]), 4)
        previous_close = round(float(hist['Close'].iloc[0]), 4)  # No previous close for a single day; use current close

        fifty_two_week_low = round(float(stock.info.get('fiftyTwoWeekLow', 0)), 4)
        fifty_two_week_high = round(float(stock.info.get('fiftyTwoWeekHigh', 0)), 4)

        weekly_hist = stock.history(period='5d')
        weekly_low = round(float(weekly_hist['Low'].min()), 4) if not weekly_hist.empty else float('nan')
        weekly_high = round(float(weekly_hist['High'].max()), 4) if not weekly_hist.empty else float('nan')

        monthly_hist = stock.history(period='1mo')
        monthly_low = round(float(monthly_hist['Low'].min()), 4) if not monthly_hist.empty else float('nan')
        monthly_high = round(float(monthly_hist['High'].max()), 4) if not monthly_hist.empty else float('nan')

        market_cap = int(stock.info.get('marketCap', 0)) if stock.info.get('marketCap') else None
        company_name = stock.info.get('shortName', 'N/A')
        currency = stock.info.get('currency', 'N/A')

        percentage_change = round(float(((close_price - open_price) / open_price) * 100), 4) if open_price else float('nan')
        price_change = 'up' if close_price > open_price else 'down'

        data.append({
            'Symbol': symbol,
            'Open': open_price,
            'High': high_price,
            'Low': low_price,
            'Close': close_price,
            'CurrentPrice': close_price,
            'PreviousClose': previous_close,
            'FiftyTwoWeekLow': fifty_two_week_low,
            'FiftyTwoWeekHigh': fifty_two_week_high,
            'WeeklyLow': weekly_low,
            'WeeklyHigh': weekly_high,
            'MonthlyLow': monthly_low,
            'MonthlyHigh': monthly_high,
            'MarketCap': market_cap,
            'CompanyName': company_name,
            'Currency': currency,
            'PercentageChange': percentage_change,
            'PriceChange': price_change,
            'MarketState': market_state
        })

    return data



# symbols = ["MSFT", "AAPL", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "ADBE", "INTC", "NFLX"]
# country = "USA"

# # Call the function
# data = get_stock_data(symbols, country)

# # Print the results
# for stock in data:
#     print(stock)


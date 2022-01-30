import requests
from datetime import datetime, timedelta


def get_price(ticker):
    token = 'TNZ8TGYUHJN5O1VW'
    ticker += '.SA'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={token}'
    r = requests.get(url)
    data = r.json()
    today = datetime.now().strftime("%Y-%m-%d")
    for i in range(10):
        if today in data["Time Series (Daily)"]:
            return {
                'day': today,
                'price': data["Time Series (Daily)"][today]['4. close']
            }
        today = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    return None

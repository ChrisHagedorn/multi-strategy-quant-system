import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup

def get_sp500_instruments():
    res = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))
    print(df[0])
    return list(df["Symbol"])

tickers = get_sp500_instruments()
print(tickers)
get_sp500_instruments()
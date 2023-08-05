import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup
import xlsxwriter

def get_sp500_instruments():
    res = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))
    return list(df[0]["Symbol"])


def get_sp500_df():
    symbols = get_sp500_instruments()
    symbols = symbols[:30] 
    ohlcvs = {}
    for symbol in symbols:
        symbol_df = yf.Ticker(symbol).history(period="10y")
        ohlcvs[symbol] = symbol_df[["Open", "High", "Low", "Close", "Volume"]].rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            }
        )
        print(symbol)
        print(ohlcvs[symbol])
    
    df = pd.DataFrame(index=ohlcvs["GOOGL"].index)
    df.index = df.index.tz_localize(None)
    df.index.name = "date"
    instruments = list(ohlcvs.keys())
    print(instruments)
    for inst in instruments:
        inst_df = ohlcvs[inst]
        columns = list(map(lambda x: "{} {}".format(inst, x), inst_df.columns))
        df[columns] = inst_df

    return df, instruments

df, instruments = get_sp500_df()

df.to_excel("./data/sp500_data.xlsx", engine='xlsxwriter')  
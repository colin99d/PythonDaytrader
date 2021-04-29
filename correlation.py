from numpy.random import default_rng
from scipy.stats import pearsonr
import yfinance as yf
import csv

def checkCorrelation(array1, array2):
    return pearsonr(array1, array2)

tickers = []
with open('convertcsv.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tickers.append(row['Option Symbol'])


numbers = default_rng().choice(len(tickers), size=20, replace=False)
symbols = [tickers[x] for x in numbers]



data = yf.download(symbols,period = "1y",interval = '1d')
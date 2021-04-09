import matplotlib.pyplot as plt
import yfinance as yf

stock = yf.Ticker("MSFT")
allOptions = stock.option_chain()
calls = allOptions.calls
puts = allOptions.puts
callsFilter = calls[calls['percentChange'] != 0]
putsFilter = puts[puts['percentChange'] != 0]
try:
    callsFilter.to_csv('options-data.csv')
except PermissionError:
    print("Data not saved, close CSV before running")

ax = plt.gca()
callsFilter.plot(kind='scatter',x='strike',y='percentChange',color='red',ax=ax)
#callsFilter.plot(kind='scatter',x='strike',y='impliedVolatility',color='blue',ax=ax)
#callsFilter.plot(kind='scatter',x='strike',y='ask',color='blue',ax=ax)
putsFilter.plot(kind='scatter',x='strike',y='percentChange',color='green',ax=ax)
#putsFilter.plot(kind='scatter',x='strike',y='impliedVolatility',color='purple',ax=ax)
#putsFilter.plot(kind='scatter',x='strike',y='ask',color='purple',ax=ax)
plt.show()

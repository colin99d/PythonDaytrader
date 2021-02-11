from logicHolder import get_pick
import scipy.stats as scpy
import yfinance as yf
import pandas as pd
import numpy as np

#Finding error GALT is good
symbols = ['GSUM','MDGS','FLDM','AMTX','SPI','MIST','MVIS','BHAT','SLCA','NHLD','LIVX','TKAT','NRT','OGEN','INSE','WHLM','MTP','AGRX','YTRA','MYO','BIMI','OPTT','SGBX','SNDL','HSDT','GMBL','CWBR','FNGD','MLND','CJJD','OCGN','GENE','SIEN','ACHV','FRAN','PME','AQMS','GALT']#,'FAT','GTEC','RIBT','OFS','NURO','DWSN','XELB','GVP','WKHS','WKHS','WKHS','PRCP','JBR','EVOL','PEI','AMPY','KMPH','GROW','TRIL','ATHX',]
data = yf.download(symbols, period = "1y",interval = '1d' )
for symbol in symbols:
    data['pHigh',symbol] = data['High',symbol].shift(1)
    data['pLow',symbol] = data['Low',symbol].shift(1)
    data['pClose',symbol] = data['Close',symbol].shift(1)
    data['pVolume',symbol] = data['Volume',symbol].shift(1)
data = data.iloc[1:]
data = data.fillna(0)
longs = []
shorts = []

for i in range(len(data)-66):
    print(str(100*i/(len(data)-66))+'% complete')
    l, s, ls, ss = get_pick(data, symbols, i)
    longs.append(ls)
    shorts.append(ss)
        

#Makes dataframes for performance over 9 months 
longperformance = pd.DataFrame(longs, columns=['date','ticker','open','decision','close'])
shortperformance = pd.DataFrame(shorts, columns=['date','ticker','open','decision','close'])
longprofit = lambda row: row['close'] - row['open']
shortprofit = lambda row: row['open'] - row['close'] 
longperformance['profit'] = longperformance.apply(longprofit, axis = 1)
shortperformance['profit'] = shortperformance.apply(shortprofit, axis = 1)
print(longperformance['profit'].sum())
print(shortperformance['profit'].sum())
longperformance.to_csv('longperformance.csv')
shortperformance.to_csv('shortperformance.csv')

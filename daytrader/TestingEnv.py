from logicHolder import get_pick, get_data
import scipy.stats as scpy
import pandas as pd
import numpy as np

symbols = ['GSUM','MDGS','FLDM','AMTX','SPI','MIST','MVIS','BHAT','SLCA','NHLD','LIVX','TKAT','NRT','OGEN','INSE','WHLM','MTP','AGRX','YTRA','MYO','BIMI','OPTT','SGBX','SNDL','HSDT','GMBL','CWBR','FNGD','MLND','CJJD','OCGN','GENE','SIEN','ACHV','FRAN','PME','AQMS','GALT']
data = get_data(symbols)

longs = []
shorts = []

for i in range(len(data)-66):
    print(str(100*i/(len(data)-66))+'% complete')
    l, s, ls, ss, pl, ps = get_pick(data, symbols, i)
    longs.append(ls)
    shorts.append(ss)
        

#Makes dataframes for performance over 9 months 
longperformance = pd.DataFrame(longs, columns=['date','ticker','open','decision','close'])
shortperformance = pd.DataFrame(shorts, columns=['date','ticker','open','decision','close'])
longprofit = lambda row: row['close'] - row['open']
shortprofit = lambda row: row['open'] - row['close'] 
longperformance['profit'] = longperformance.apply(longprofit, axis = 1)
shortperformance['profit'] = shortperformance.apply(shortprofit, axis = 1)
longperformance.to_csv('../longperformance.csv')
shortperformance.to_csv('../shortperformance.csv')

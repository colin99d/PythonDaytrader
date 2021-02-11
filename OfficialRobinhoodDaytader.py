import robin_stocks as r 
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import scipy.stats as scpy
import yfinance as yf
import pandas as pd
import numpy as np

r.authentication.login(username=, password=, expiresIn=86400, scope='internal', by_sms=True, store_session=True)
symbols = ['GSUM','MDGS','FLDM','AMTX','SPI','MIST','MVIS','BHAT','SLCA','AKRX','NHLD','LIVX','RTTR','TKAT','NRT','OGEN','INSE','WHLM','MTP','AGRX','YTRA','MYO','BIMI','OPTT','SGBX','SNDL','HSDT','GMBL','CWBR','FNGD','MLND','CJJD','OCGN','GENE','SIEN','ACHV','FRAN','PME','AQMS','GALT','FAT','GTEC','RIBT','OFS','NURO','DWSN','XELB','GVP','WKHS','WKHS','WKHS','PRCP','ECT','JBR','EVOL','PEI','KTP','AMPY','KMPH','GROW','TRIL','ATHX',]
data = yf.download(symbols, period = "1y",interval = '1d' )
data = data.fillna(0)



from sklearn.model_selection import train_test_split
from sklearn import linear_model
import scipy.stats as scpy
import yfinance as yf
import numpy as np
import pandas as pd
import datetime

def get_data(symbols):
    data = yf.download(symbols, period = "1y",interval = '1d' )
    for symbol in symbols:
        data['pHigh',symbol] = data['High',symbol].shift(1)
        data['pLow',symbol] = data['Low',symbol].shift(1)
        data['pClose',symbol] = data['Close',symbol].shift(1)
        data['pVolume',symbol] = data['Volume',symbol].shift(1)
        data = data.iloc[1:]
        data = data.fillna(0)
    return data

def get_pick(data, symbols, i='default'):
    opens = []
    closes = []
    decisions = []
    
    for symbol in symbols:
        
        if i != 'default':
            x=i+1
            y=i+64
            z=i+65
        else:
            x=0
            y=-2
            z=-1
        #features = ['Open','pHigh','pLow','pClose','pVolume']
        #symbolz = [x for symbol in features]
        #X = data[features, symbolz][i+1:i+64]
        X = data['Open', symbol][x:y].to_numpy().reshape(-1,1)
        y = data['Close',symbol][x:y]
            
        #Split data into train and test
        train_X, val_X, train_y, val_y = train_test_split(X, y)
        
        #Create model and predictions
        model = linear_model.LinearRegression()
        model.fit(train_X, train_y)
        preds_val = model.predict(val_X)
            
        #Compute stock 95% confidence interval
        l1 = preds_val - val_y
        mean = np.average(l1)
        stdev = np.std(l1)
        predict = data['Open',symbol][z].reshape(1,-1)
        pred_increase = model.predict(predict)- data['Open',symbol][z]

        #Compute long/short with confidence 
        zscore = 3
        while True:
            lowf = mean - zscore*stdev + pred_increase
            highf = mean + zscore*stdev + pred_increase
                
            if lowf > 0 and highf > 0:
                prob = scpy.norm.sf(abs(zscore))*2
                prob = 1 - prob
                decision = round(prob*100,2)
                break
                
            elif lowf < 0 and highf < 0:
                prob = scpy.norm.sf(abs(zscore))*2
                prob = 1 - prob
                decision = round(prob*100,2) *-1
                break 
                
            else:
                zscore -= .001

        #Add data to lists
        opens.append(data['Open',symbol][z])
        closes.append(data['Close',symbol][z])
        decisions.append(decision)
        
    #Turn lists into a Dataframe 
    df = pd.DataFrame({'ticker': symbols,'date': data.index[z],'open': opens,'decision': decisions,'close':closes})
    df_sorted = df.sort_values(by=['decision']).reset_index()
    long = df_sorted['ticker'][len(df_sorted)-1]
    short = df_sorted['ticker'][0]
    longs = [df_sorted['date'][len(df_sorted)-1],df_sorted['ticker'][len(df_sorted)-1],df_sorted['open'][len(df_sorted)-1],df_sorted['decision'][len(df_sorted)-1],df_sorted['close'][len(df_sorted)-1]]
    shorts = [df_sorted['date'][0],df_sorted['ticker'][0],df_sorted['open'][0],df_sorted['decision'][0],df_sorted['close'][0]]
    pricel = df_sorted['open'][len(df_sorted)-1]
    prices = short = df_sorted['open'][0]
    return long, short, longs, shorts, pricel, prices


class EST5EDT(datetime.tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5) + self.dst(dt)

    def dst(self, dt):
        d = datetime.datetime(dt.year, 3, 8)        #2nd Sunday in March
        self.dston = d + datetime.timedelta(days=6-d.weekday())
        d = datetime.datetime(dt.year, 11, 1)       #1st Sunday in Nov
        self.dstoff = d + datetime.timedelta(days=6-d.weekday())
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

    def tzname(self, dt):
        return 'EST5EDT'

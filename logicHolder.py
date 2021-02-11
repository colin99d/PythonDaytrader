from sklearn.model_selection import train_test_split
from sklearn import linear_model
import scipy.stats as scpy
import numpy as np
import pandas as pd


def get_pick(data, symbols, i):
    opens = []
    closes = []
    decisions = []
    
    for symbol in symbols:
        
        features = ['Open','pHigh','pLow','pClose','pVolume']
        symbolz = [symbol for x in features]
        #X = data[features, symbolz][i+1:i+64]
        X = data['Open', symbol][i+1:i+64].to_numpy().reshape(-1,1)
        y = data['Close',symbol][i+1:i+64]
        
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
        predict = data['Open',symbol][i+65].reshape(1,-1)
        pred_increase = model.predict(predict)- data['Open',symbol][i+65]
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
        opens.append(data['Open',symbol][i+65])
        closes.append(data['Close',symbol][i+65])
        decisions.append(decision)
        
    #Turn lists into a Dataframe 
    df = pd.DataFrame({'ticker': symbols,'date': data.index[i+65],'open': opens,'decision': decisions,'close':closes})
    df_sorted = df.sort_values(by=['decision']).reset_index()
    long = df_sorted['ticker'][len(df_sorted)-1]
    short = df_sorted['ticker'][0]
    longs = [df_sorted['date'][len(df_sorted)-1],df_sorted['ticker'][len(df_sorted)-1],df_sorted['open'][len(df_sorted)-1],df_sorted['decision'][len(df_sorted)-1],df_sorted['close'][len(df_sorted)-1]]
    shorts = [df_sorted['date'][0],df_sorted['ticker'][0],df_sorted['open'][0],df_sorted['decision'][0],df_sorted['close'][0]]

    return long, short, longs, shorts

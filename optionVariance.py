from datetime import date, timedelta
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
import csv

class OptionManager():
    def __init__(self, ticker, contract, show=True, graphAll=False):
        self.show = show
        self.long = None
        self.short = None
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.contract = contract
        self.graphAll = graphAll
        self.optionsChains = {}
        self.callChains = {}
        self.putChains = {}
        self.callChainsF = {}
        self.putChainsF = {}
        self.variances = {}

    def addExpirations(self):
        self.expirations = self.stock.options
        
    def addOptionsChain(self,expiration):
        chains = self.stock.option_chain(expiration)
        self.optionsChains[expiration] = chains
        self.callChains[expiration] = chains.calls
        self.putChains[expiration] = chains.puts
        self.cleanData(expiration)

    def cleanData(self, expiration):
        #Remove $0 Ask price
        self.callChainsF[expiration] = self.callChains[expiration][self.callChains[expiration]['ask'] != 0]
        self.putChainsF[expiration] =  self.putChains[expiration][ self.putChains[expiration]['ask'] != 0]
        #Only show in the money
        self.callChainsF[expiration] = self.callChainsF[expiration][self.callChainsF[expiration]['inTheMoney'] == True]
        self.putChainsF[expiration] =  self.putChainsF[expiration][ self.putChainsF[expiration]['inTheMoney'] == True]
        #Open interest greater than 0
        self.callChainsF[expiration] = self.callChainsF[expiration][self.callChainsF[expiration]['openInterest'] > 1]
        self.putChainsF[expiration] =  self.putChainsF[expiration][self.putChainsF[expiration]['openInterest'] > 1]
        #Regular contract size
        self.callChainsF[expiration] = self.callChainsF[expiration][self.callChainsF[expiration]['contractSize'] == "REGULAR"]
        self.putChainsF[expiration] =  self.putChainsF[expiration][ self.putChainsF[expiration]['contractSize'] == "REGULAR"]
        #Last trade date is equal to today

        if date.today().weekday() < 5:
            dateStr = date.today().isoformat()
        else:
            dateStr = date.today() + timedelta(days=4 - date.today().weekday())

        self.callChainsF[expiration] = self.callChainsF[expiration][self.callChainsF[expiration]['lastTradeDate'] >= pd.Timestamp(dateStr).floor('D')]
        self.putChainsF[expiration] =  self.putChainsF[expiration][ self.putChainsF[expiration]['lastTradeDate'] >= pd.Timestamp(dateStr).floor('D')]

    def saveCSV(self,expiration):
        try:
            self.putChainsF[expiration].to_csv(expiration+'-options-data.csv')
        except PermissionError:
            print("Data not saved, close CSV before running")

    def findObscure(self,expiration, ax):
        x = np.array(self.callChainsF[expiration].strike if self.contract == "call" else self.putChainsF[expiration].strike)
        y = np.array(self.callChainsF[expiration].ask if self.contract == "call" else self.putChainsF[expiration].ask)
        for i in range(len(y)-1):
            diff = (y[i+1]-y[i])/y[i] if self.contract == "call" else (y[i]-y[i+1])/y[i]
            if diff > 0.01:
                if self.graphAll:
                    self.graphLine("circle", x[i], y[i], ax)
                if expiration not in self.variances:
                    self.variances[expiration] = [{"ask":y[i], "strike":x[i], "dif": diff, "index": i}]
                else:
                    self.variances[expiration].append({"ask":y[i], "strike":x[i], "dif": diff, "index": i})

        if expiration in self.variances and self.graphAll:
            self.graphLine("line",x,y,label=expiration)

    def graphLine(self, shape, x, y, ax=None, label=None, color="r"):
        if shape == "circle":
            circle1 = plt.Circle((x, y), 5, color=color, fill=False, label=label)
            ax.add_patch(circle1)
        elif shape == "line":
            plt.plot(x, y, marker='o',label=str(label))

    #Only works for call right now
    def analyzeMax(self, ax):
        maxVar = 0
        expiration = ""
        for variance in self.variances:
            maxDif = max([x['dif'] for x in self.variances[variance]])
            if maxDif > maxVar:
                maxVar = maxDif
                expiration = variance
        if expiration != "":
            for item in self.variances[expiration]:
                if item['dif'] == maxVar:
                    #self.graphLine("circle", item['strike'], item['ask'], ax, label="Long")
                    index = item['index']
                    self.long=[item['strike'],item['ask']]

        if expiration != "":  
            x = np.array(self.callChainsF[expiration].strike if self.contract == "call" else self.putChainsF[expiration].strike)
            y = np.array(self.callChainsF[expiration].ask if self.contract == "call" else self.putChainsF[expiration].ask)
            z = np.array(self.callChainsF[expiration].bid if self.contract == "call" else self.putChainsF[expiration].bid)
            self.graphLine("line",x,y,label="Ask-"+str(expiration))
            self.graphLine("line",x,z,label="Bid-"+str(expiration))
            #self.graphLine("circle", x[index+1], z[index+1], ax, label="Short", color="g")
            self.short = [x[index+1],z[index+1]]
            ax.annotate('xyz',xy=(1.1,-3.8),xytext=(1.3,-3.8), annotation_clip=False)
            x_coord = (self.long[0] + self.short[0]) / 2
            plt.plot([x_coord,x_coord],[self.long[1],self.short[1]], color="g")
            plt.plot([x_coord,self.long[0]],[self.long[1],self.long[1]], color="g")
            plt.plot([x_coord,self.short[0]],[self.short[1],self.short[1]], color="g")

    def returnAnswer(self):
        if self.long and self.short:
            return self.short[1]-self.long[1]

    def createData(self):
        self.addExpirations()
        fig, ax = plt.subplots()
        for expiration in self.expirations:
            self.addOptionsChain(expiration)
            self.findObscure(expiration, ax)
        self.analyzeMax(ax)
        if self.show:
            plt.xlabel("Option Strike Price ($)")
            plt.ylabel("Option Market Price ($)")
            plt.suptitle(self.ticker + " " + self.contract.capitalize() + "s")
            if self.long and self.short:
                plt.title("Long at "+str(self.long[0]) + " and short at " + str(self.short[0]) +" for a profit between " +
                str(round(self.short[1]-self.long[1],2)) +" and " + str(round(self.short[1]-self.long[1] + self.short[0] - self.long[0],2)))
            plt.legend()
            plt.show()
        return self.returnAnswer()

tickers = []
with open('convertcsv.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tickers.append(row['Option Symbol'])

for ticker in tickers:
    value = OptionManager(ticker,"call",False, False).createData()
    print(str(tickers.index(ticker))+"/"+str(len(tickers)))
    if value is not None and value > 0:
        print(ticker+" "+str(value))
        break
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

class OptionManager():
    def __init__(self, ticker, contract):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.contract = contract
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
        self.callChainsF[expiration] = self.callChainsF[expiration][self.callChainsF[expiration]['openInterest'] > 0]
        self.putChainsF[expiration] =  self.putChainsF[expiration][self.putChainsF[expiration]['openInterest'] > 0]
        #Regular contract size
        self.callChainsF[expiration] = self.callChainsF[expiration][self.callChainsF[expiration]['contractSize'] == "REGULAR"]
        self.putChainsF[expiration] =  self.putChainsF[expiration][ self.putChainsF[expiration]['contractSize'] == "REGULAR"]


    def saveCSV(self,expiration):
        try:
            callsFilter.to_csv('options-data.csv')
        except PermissionError:
            print("Data not saved, close CSV before running")

    def graphLines(self,expiration):
        if self.contract == "call":
            x = np.array(self.callChainsF[expiration].strike)
            y = np.array(self.callChainsF[expiration].ask)
            for i in range(len(y)-1):
                if y[i] > y[i+1]:
                    if self.variances[expiration]:
                        self.variances[expiration] =[{"ask":y[i], "strike":x[i], "dif":(y[i+1]-y[i])/y[i]}]
                    else:
                        self.variances[expiration].append({"ask":y[i], "strike":x[i], "dif":(y[i+1]-y[i])/y[i]})
                    
        elif self.contract == "put":
            x = np.array(self.putChainsF[expiration].strike)
            y = np.array(self.putChainsF[expiration].ask)
            for i in range(len(y)-1):
                if y[i] < y[i+1]:
                    if self.variances[expiration]:
                        self.variances[expiration] =[{"ask":y[i], "strike":x[i], "dif":(y[i+1]-y[i])/y[i]}]
                    else:
                        self.variances[expiration].append({"ask":y[i], "strike":x[i], "dif":(y[i+1]-y[i])/y[i]})

        plt.plot(x, y, marker='o',label=str(expiration))

    def createData(self):
        self.addExpirations()
        for expiration in self.expirations[6:]:
            self.addOptionsChain(expiration)
            self.graphLines(expiration)
        plt.xlabel("Option Strike Price ($)")
        plt.ylabel("Option Ask Price ($)")
        plt.title(self.ticker + " " + self.contract.capitalize() + "s")
        plt.legend()
        plt.show()

    
msft = OptionManager("MSFT","call")
msft.createData()


#callsFilter.plot(kind='scatter',x='strike',y='ask',color='blue',ax=ax)


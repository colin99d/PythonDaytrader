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
        self.callChainsFiltered = {}
        self.putChainsFiltered = {}
        self.bestFitLines = {}

    def addExpirations(self):
        self.expirations = self.stock.options
        
    def addOptionsChain(self,expiration):
        chains = self.stock.option_chain(expiration)
        self.optionsChains[expiration] = chains
        self.callChains[expiration] = chains.calls
        self.callChainsFiltered[expiration] = chains.calls[chains.calls['percentChange'] != 0]
        self.putChains[expiration] = chains.puts
        self.putChainsFiltered[expiration] = chains.puts[chains.puts['percentChange'] != 0]

    def saveCSV(self,expiration):
        try:
            callsFilter.to_csv('options-data.csv')
        except PermissionError:
            print("Data not saved, close CSV before running")

    def bestFitLine(self,expiration):
        if self.contract == "call":
            x = np.array(self.callChains[expiration].strike)
            y = np.array(self.callChains[expiration].ask)
        elif self.contract == "put":
            x = np.array(self.putChains[expiration].strike)
            y = np.array(self.putChains[expiration].ask)

        plt.plot(x, y, marker='o',label="Act-"+str(expiration))
        """
        fit = np.polyfit(x, y, 2)
        print(fit)
        plt.plot(x, fit[0]*(x**2) + fit[1]*x + fit[2])
        """
        fit = np.polyfit(np.log(x), y, 1)
        print(fit)
        #plt.plot(x, fit[0]*np.log(x) + fit[1])
        
        self.bestFitLines[expiration] = fit

    def createData(self):
        self.addExpirations()
        for expiration in self.expirations:
            self.addOptionsChain(expiration)
            self.bestFitLine(expiration)
        plt.title(self.ticker + " " + self.contract.capitalize() + "s")
        plt.legend()
        plt.show()

    
msft = OptionManager("MSFT","call")
msft.createData()


#callsFilter.plot(kind='scatter',x='strike',y='ask',color='blue',ax=ax)


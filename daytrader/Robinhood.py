from logicHolder import get_pick, get_data, EST5EDT
from sensitive import LoginInfo
import robin_stocks as r
import datetime
import math
import json


symbols = ['GSUM','MDGS','FLDM','AMTX','SPI','MIST','MVIS','BHAT','SLCA','NHLD','LIVX','TKAT','NRT','OGEN','INSE','WHLM','MTP','AGRX','YTRA',
           'MYO','BIMI','OPTT','SGBX','SNDL','HSDT','GMBL','CWBR','FNGD','MLND','CJJD','OCGN','GENE','SIEN','ACHV','FRAN','PME','AQMS','GALT']

info = LoginInfo()
r.authentication.login(info.get_username(), info.get_password())

dt = datetime.datetime.now(tz=EST5EDT())

if dt.hour > 12:
    portfolio = r.account.build_holdings()
    for key in portfolio:
        if key in symbols:
            print(portfolio[key])
            quantity = portfolio[key]['value']
            response = r.orders.order_sell_market(key, quantity, timeInForce='gtc', extendedHours=False)
            trans = "sell"
        else:
            print(key+' is not in the managed portfolio')

else:
    acctInfo = r.profiles.load_account_profile()
    buyPow = 20
    #buyPow = acctInfo['buying_power']
    data = get_data(symbols)
    target, untarget, longs, shorts, pricel, prices = get_pick(data, symbols)
    quantity = math.floor(buyPow/pricel)
    response = r.orders.order_buy_market(target, quantity, timeInForce='gtc', extendedHours=False)
    trans = "buy"


trans = "buy"
final = dt.strftime("%m-%d-%Y")

with open('../'+trans+final+'.txt', 'w') as file:
     file.write(json.dumps(response))


import backtrader as bt
import datetime
import pandas as pd

#0.1 add indicator

#0.2 add strategy
class SMA(bt.Strategy):
    def __init__(self):
        self.bt_sma20 = bt.indicators.MovingAverageSimple(self.data,period=20)
        self.buy_sell_signal=bt.indicators.CrossOver(self.data.close,self.bt_sma20)

    def start(self):
        print("start")
    #def prenext(self):
    #    print("prenext")
    #def nextstart(self):
    #    print("nextstart")

    def next(self):
        if not self.position and self.buy_sell_signal == 1:
            self.order=self.buy(size=10)
        elif not self.position and self.buy_sell_signal == -1:
            self.order=self.sell(size=10)
        elif self.getposition().size<0 and self.buy_sell_signal == 1:
            self.order=self.close
            self.order=self.buy(size=10)
        elif self.getposition().size>0 and self.buy_sell_signal == -1:
            self.order=self.close
            self.order=self.sell(size=10)

def main():
    #1.Create a cerebro
    cerebro = bt.Cerebro()

    #2.Add data feed
    #2.1 Creat a data feed
    dataframe = pd.read_csv('C:\\FXDATA\\data\\USDJPY_es.csv',names=['datetime','open','high','low','close','Aopen','Ahigh','Alow','Aclose'])
    dataframe=dataframe.drop(['Aopen','Ahigh','Alow','Aclose'],axis=1)
    dataframe['datetime']=pd.to_datetime(dataframe['datetime'])
    dataframe.set_index('datetime',inplace=True)
    dataframe['openinterest']=0
    dataframe['volume']=1000
    brf_min=bt.feeds.PandasData(dataname=dataframe,
                                fromdate=datetime.datetime(2016,2,1),
                                todate=datetime.datetime(2018,6,30),
                                timeframe=bt.TimeFrame.Minutes
                                )

    #2.2 Add to Cerobro
    cerebro.adddata(brf_min)

    #3. Add strategy
    cerebro.addstrategy(SMA)

    #4. Run
    cerebro.run()

    #5. Plot
    cerebro.plot(style='candle')

if __name__ == '__main__':
    main()




import backtrader as bt
import datetime
import pandas as pd

#0.1 add indicator
class Joyo_ind(bt.Indicator):
    lines=('up','down')

#0.2 add strategy
class Joyo_str(bt.Strategy):
    def __init__(self):
        self.data1.plotinfo.plot=False

    def start(self):
        print("start")

    def prenext(self):
        print("prenext")

    def nextstart(self):
        print("nextstart")

    def next(self):
        print("next")

def main():
    #1.Create a cerebro
    cerebro = bt.Cerebro()

    #2.Add data feed
    #2.1 Load data
    dataframe = pd.read_csv('C:\\FXDATA\\data\\USDJPY_EX_20180601.csv')
    dataframe['datetime']=pd.to_datetime(dataframe['datetime'])
    dataframe.set_index('datetime',inplace=True)
    dataframe['openinterest']=0
    brf_min=bt.feeds.PandasData(dataname=dataframe,
                                timeframe=bt.TimeFrame.Minutes
                                )

    #2.2 Add to Cerobro
    cerebro.adddata(brf_min)
    cerebro.resampledata(brf_min,timeframe=bt.TimeFrame.Days)

    #3. Add strategy
    cerebro.addstrategy(Joyo_str)

    #4. Run
    cerebro.run()

    #5. Plot
    cerebro.plot(style='candle')

if __name__ == '__main__':
    main()



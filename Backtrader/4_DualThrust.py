
import backtrader as bt
import datetime
import pandas as pd

#0.1 add indicator
class DT_Line(bt.Indicator):
    lines=('U','D')
    params=(('period',2),('k_u',0.7),('k_d',0.7))

    def __init__(self):
        #Starting period
        self.addminperiod(self.params.period+1)

    def next(self):
        HH=max(self.data.high.get(-1,size=self.params.period))
        LC=min(self.data.close.get(-1,size=self.params.period))
        HC=max(self.data.close.get(-1,size=self.params.period))
        LL=min(self.data.low.get(-1,size=self.params.period))
        R=max(HH-LC,HC-LL)
        self.lines.U[0]=self.data.open[0]+self.params.k_u*R
        self.lines.D[0]=self.data.open[0]-self.params.k_d*R

class DualThrust(bt.Strategy):
    params=(('period',2),('k_u',0.7),('k_d',0.7))
    def __init__(self):
        self.dataclose=self.data0.close
        self.D_Line=DT_Line(self.data1,period=self.params.period, k_u=self.params.k_u, k_d=self.params.k_d)
        self.D_Line=self.D_Line()
        #self.D_Line.plotinfo.plot=False
        self.D_Line.plotinfo.plotmaster=self.data0

        self.buy_signal=bt.indicators.CrossOver(self.dataclose,self.D_Line.U)
        self.sell_signal=bt.indicators.CrossDown(self.dataclose,self.D_Line.D)

    def next(self):
        #if self.data.datetime.time() > datetime.time(9,3) and self.data.datetime() < datetime.time(22,55):
        if not self.position and self.buy_signal == 1:
            self.order=self.buy(size=10)
        elif not self.position and self.sell_signal == 1:
            self.order=self.sell(size=10)
        elif self.getposition().size<0 and self.buy_signal == 1:
            self.order=self.close()
            self.order=self.buy(size=10)
        elif self.getposition().size>0 and self.buy_signal == 1:
            self.order=self.buy(size=10)
        elif self.getposition().size>0 and self.sell_signal == 1:
            self.order=self.close()
            self.order=self.sell(size=10)
        elif self.getposition().size<0 and self.sell_signal == 1:
            self.order=self.sell(size=10)
        if self.data.datetime.time() >= datetime.time(22,55):
            self.order = self.close()


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
    cerebro.resampledata(brf_min,timeframe=bt.TimeFrame.Days)

    #3. Add strategy
    cerebro.addstrategy(DualThrust)

    #4. Run
    cerebro.run()

    #5. Plot
    cerebro.plot(style='candle')

if __name__ == '__main__':
    main()



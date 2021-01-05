
import backtrader as bt
import datetime
import pandas as pd

#0.1 add indicator
class three_bars(bt.Indicator):
    lines=('up','down')
    def __init__(self):
        #Starting period
        self.addminperiod(4)
        #plot setting
        self.plotinfo.plotmaster=self.data

    def next(self):
        self.up[0]=max(max(self.data.close.get(ago=-1,size=3)), max(self.data.open.get(ago=-1,size=3)))
        self.down[0]=min(min(self.data.close.get(ago=-1,size=3)), min(self.data.open.get(ago=-1,size=3)))

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

class t_s(bt.Strategy):
    def __init__(self):
        self.data1.plotinfo.plot=False
        #self.data1.close[0]

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.up_down=three_bars(self.data)
        self.buy_signal=bt.indicators.CrossOver(self.data.close,self.up_down.up)
        self.sell_signal=bt.indicators.CrossDown(self.data.close,self.up_down.down)
        self.buy_signal.plotinfo.plot=False
        self.sell_signal.plotinfo.plot=False
        #self.up_down.plotinfo.plot=False

    def next(self):
        if not self.position and self.buy_signal == 1:
            self.order=self.buy(size=10)
        elif not self.position and self.buy_signal == -1:
            self.order=self.sell(size=10)
        elif self.getposition().size<0 and self.buy_signal == 1:
            self.order=self.close
            self.order=self.buy(size=10)
        elif self.getposition().size>0 and self.buy_signal == -1:
            self.order=self.close
            self.order=self.sell(size=10)

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
    def stop(self):
        print('period: %s, k_u: %s, k_d: %s, final_value: %.2f' %
              (self.params.period, self,p.k_u, self.params.k_d, self.broker.getvalue()))
#        print('period: %s, k_u: k_d:, final_value: %.2f' %
#              (self.params.period, self.broker.getvalue()))

class SMA(bt.Strategy):
    def __init__(self):
        self.bt_sma144 = bt.indicators.MovingAverageSimple(self.data,period=144*60)
        self.bt_sma169 = bt.indicators.MovingAverageSimple(self.data,period=169*60)
        self.bt_sma288 = bt.indicators.MovingAverageSimple(self.data,period=288*60)
        self.bt_sma338 = bt.indicators.MovingAverageSimple(self.data,period=338*60)
        self.buy_sell_signal=bt.indicators.CrossOver(self.data.close,self.bt_sma144)

        self.buy_signal=0
        self.sell_signal=0
        #if self.data.high() > self.bt_sma144 and self.bt_sma144 > self.data.low() and self.data.low() > self.bt_sma169 and self.bt_sma169 > self.bt_sma288 and self.bt_sma288 > self.bt_sma338:
        #if self.data.close[-1] > self.bt_sma338[-1]:
        #self.buy_signal=bt.indicators.CrossOver(self.data.high,self.bt_sma144)
        #    self.buy_signal = 1
        #if self.data.low() < self.bt_sma144 and self.bt_sma144 < self.data.high() and self.data.high() < self.bt_sma169 and self.bt_sma169 < self.bt_sma288 and self.bt_sma288 < self.bt_sma338:
        #if self.data.low() < self.bt_sma144 and self.bt_sma144 < self.data.high() and self.data.high() < self.bt_sma169 and self.bt_sma169 < self.bt_sma288 and self.bt_sma288 < self.bt_sma338:
        #    self.sell_signal = 1

    def start(self):
        print("start")
    #def prenext(self):
    #    print("prenext")
    #def nextstart(self):
    #    print("nextstart")
    def next(self):
        if self.bt_sma144[-1] > self.bt_sma169[-1] and self.bt_sma169[-1] > self.bt_sma288[-1] and self.bt_sma288[-1] > self.bt_sma338[-1]:
            if not self.position and self.buy_sell_signal[0] == -1:
                self.order=self.buy(size=10)
        if self.bt_sma144[-1] < self.bt_sma169[-1] and self.bt_sma169[-1] < self.bt_sma288[-1] and self.bt_sma288[-1] < self.bt_sma338[-1]:
            if not self.position and self.buy_sell_signal[0] == 1:
                self.order=self.sell(size=10)
        if self.getposition().size<0 and self.buy_sell_signal[0] == -1:
                self.order=self.close()
                self.order=self.buy(size=10)

def main():
    #1.Create a cerebro
    cerebro = bt.Cerebro()

    #2.Add data feed
    #2.1 Creat a data feed
    dataframe = pd.read_csv('C:\\FXDATA\\data\\USDJPY_es.csv',names=['datetime','open','high','low','close','Aopen','Ahigh','Alow','Aclose'])
    dataframe=dataframe.drop(['Aopen','Ahigh','Alow','Aclose'],axis=1)
    #dataframe = pd.read_csv('C:\\FXDATA\\data\\USDJPY_EX_20180601.csv')
    dataframe['datetime']=pd.to_datetime(dataframe['datetime'])
    dataframe.set_index('datetime',inplace=True)
    dataframe['openinterest']=0
    dataframe['volume']=1000
    brf_min=bt.feeds.PandasData(dataname=dataframe,
                                fromdate=datetime.datetime(2016,2,1),
                                todate=datetime.datetime(2018,6,30),
                                timeframe=bt.TimeFrame.Minutes
                                )
    #brf_daily=bt.feeds.PandasData(dataname=dataframe)

    #cerebro.broker.setcommison(commission=2.0
    #2.2 Add to Cerobro
    cerebro.adddata(brf_min)
    cerebro.resampledata(brf_min,timeframe=bt.TimeFrame.Days)

    #3. Add strategy
    #cerebro.addstrategy(DualThrust)
    #cerebro.addstrategy(MyStrategy)
    #cerebro.addstrategy(SMA)
    #cerebro.addstrategy(t_s)

    cerebro.optstrategy(
        DualThrust,
        period=range(1,3),
        k_u=[n/10.0 for n in range(2,4)],
        k_d=[n/10.0 for n in range(2,4)])

    #4. Run
    #cerebro.run(maxcpus=4)
    cerebro.run()

    #5. Plot
    #cerebro.plot(style='candle')

if __name__ == '__main__':
    main()



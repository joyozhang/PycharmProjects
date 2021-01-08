import pandas as pd
# Merge old format
#All_pair=["AUDJPY","AUDUSD","CADJPY","CHFJPY","EURCHF","EURJPY","EURUSD","GBPCHF","GBPJPY","GBPUSD","NZDJPY","USDCHF","USDJPY"]
#for pair in All_pair:
#    dataframe = pd.read_csv('C:\\FXDATA\\ALL\\{}_new.csv'.format(pair),names=['datetime','open','high','low','close','Aopen','Ahigh','Alow','Aclose'])
#    dataframe=dataframe.drop(['Aopen','Ahigh','Alow','Aclose'],axis=1)
#    dataframe['datetime']=pd.to_datetime(dataframe['datetime'])
#    dataframe1 = pd.read_csv('C:\\FXDATA\\ALL\\{}_old.csv'.format(pair),names=['datetime','open','high','low','close','Aopen','Ahigh','Alow','Aclose'])
#    dataframe1=dataframe1.drop(['Aopen','Ahigh','Alow','Aclose'],axis=1)
#    dataframe1['datetime']=pd.to_datetime(dataframe1['datetime'], format='%Y%m%d%H%M%S')
#    dataframe.set_index('datetime',inplace=True)
#    dataframe1.set_index('datetime',inplace=True)
#    df = pd.concat([dataframe1,dataframe, dataframe],axis=0)
#    df.to_csv('C:\\FXDATA\\ALL\\{}_anew.csv'.format(pair))

import os
All_pair=["AUDJPY","AUDUSD","CADJPY","CHFJPY","EURCHF","EURJPY","EURUSD","GBPCHF","GBPJPY","GBPUSD","NZDJPY","USDCHF","USDJPY"]
for pair in All_pair:
    df = pd.read_csv('C:\\FXDATA\\ALL\\{}_anew.csv'.format(pair))
    df.set_index('datetime',inplace=True)
    g = os.walk("c:\\FXDATA\\new\\{}".format(pair))
    for path,dir_list,file_list in g:
        for dir_name in dir_list:
            g2 = os.walk(os.path.join(path, dir_name))
            for path2,dir_list2,file_list2 in g2:
                for file_name2 in file_list2:
                    dataframe1 = pd.read_csv(os.path.join(path2, file_name2),encoding="cp932")
                    dataframe1.rename(columns={'日時':'datetime' ,'始値(BID)':'open' ,'高値(BID)':'high' ,'安値(BID)':'low' ,'終値(BID)':'close' ,'始値(ASK)':'Aopen' ,'高値(ASK)':'Ahigh' ,'安値(ASK)':'Alow' ,'終値(ASK)':'Aclose'},inplace=True)
                    dataframe1=dataframe1.drop(['Aopen','Ahigh','Alow','Aclose'],axis=1)
                    dataframe1.set_index('datetime',inplace=True)
                    df = pd.concat([df,dataframe1],axis=0)
                    print(os.path.join(path2, file_name2))
    df.to_csv('C:\\FXDATA\\ALL\\{}_test.csv'.format(pair))

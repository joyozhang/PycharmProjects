import pandas as pd
dataframe = pd.read_csv('C:\\FXDATA\\data\\USDJPY_EX.csv',names=['datetime','open','high','low','close','Aopen','Ahigh','Alow','Aclose'])
dataframe=dataframe.drop(['Aopen','Ahigh','Alow','Aclose'],axis=1)
dataframe['datetime']=pd.to_datetime(dataframe['datetime'])
dataframe1 = pd.read_csv('C:\\FXDATA\\data\\USDJPY_o500.csv',names=['datetime','open','high','low','close','Aopen','Ahigh','Alow','Aclose'])
dataframe1=dataframe1.drop(['Aopen','Ahigh','Alow','Aclose'],axis=1)
dataframe1['datetime']=pd.to_datetime(dataframe1['datetime'], format='%Y%m%d%H%M%S')
dataframe.set_index('datetime',inplace=True)
dataframe1.set_index('datetime',inplace=True)

#dataframe['datetime']=pd.to_datetime(dataframe['datetime'], format='%Y%m%d%H%M%S')
#df['DateTime'] = dataframe['datetime'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
#dataframe['datetime']=dataframe['date'].apply(lambda x: pd.to_datetime(x, format='%Y%m%d%H%M%S'))
df = pd.concat([dataframe,dataframe1, dataframe],axis=0)
df.to_csv('C:\\FXDATA\\data\\USDJPY_NEW.csv')
#conding=utf8
import os
g = os.walk("c://")
for path,dir_list,file_list in g:
    for dir_name in dir_list:
        print(os.path.join(path, dir_name) )

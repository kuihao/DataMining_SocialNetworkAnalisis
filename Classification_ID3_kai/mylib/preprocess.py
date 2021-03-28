'''
Learning from https://aifreeblog.herokuapp.com/posts/64/Data_Analytics_in_Practice_Titanic/
(該網址是教學如何進行機器學習預處理，跟決策樹的程式碼無關，決策樹程式碼皆為本人手刻)
'''
import pandas as pd
import math
#import random
'''
[Column Types (欄位型態)]
    觀察訓練集與測試集共同的特徵欄位型態
'''
# 定義判別欄位型態的函數
def col_types(df_data):
    # [DataFrame.dtypes] 會返回欄位名稱及欄位資料型別
    # 判別每個欄位的型態 
    Column_Types = df_data.dtypes.to_frame().reset_index()
    Column_Types.columns = ['ColumnName','Type']
    Column_Types.sort_values(by='Type', inplace=True) 
    return Column_Types

'''
[Missing Rate (缺漏率)]
    計算缺漏值數量並換算為缺漏比率
    回傳:各欄位缺漏狀況表
'''
# 定義用來統計欄位缺漏值總數的函數
def missing_rate(df_data) : 
    # [DataFrame.isnull()] 回傳對整張 DataFrame 進行 isnull 邏輯比對結果
    # [DataFrame.isnull().sum()] 加總 True (=1) 並回傳各欄位及其 null 數量
    # 計算欄位中缺漏值的數量 
    missing_count = df_data.isnull().sum()
    missing_count = missing_count[missing_count>0]
    missing_count.sort_values(inplace=True) 
    
    # Convert Series to DataFrame
    Missing_Table = pd.DataFrame({'ColumnName':missing_count.index, 'MissingCount':missing_count.values})
    # [DataFrame.apply()] 對 DataFrame 所有資料套用相同函數
    # [lambda] 外號無名函數，就是簡化版的函數，不需要給予函式名稱
    #          lambda 後面空一格，接上需要使用的 private 變數 (variable) 名稱，在賦予運算式 (expression)
    #          常用於 filter()、map()，亦可作為 return 值
    Missing_Table[ 'Percentage(%)' ] = Missing_Table['MissingCount'].apply( lambda x:round(x/df_data.shape[0]*100,2) )
    return  Missing_Table

'''
[Z-score Function] 
標準化: 標準分數法
'''
def z_score(pd_data):
    mu = pd_data.mean()
    std = pd_data.std()
    standard_score = round((pd_data - mu) / std, 2)
    return standard_score

'''
[Sigmoid Function] 
    The sigmoid function is commonly used for predicting probabilities 
    since the probability is always between 0 and 1.
'''
def sigmoid(x):
  return round(1 / (1 + math.exp(-x)), 2)

def shuffle_dataset(data_pd, bool_shuffle):
    if bool_shuffle:
        #random.shuffle(data_pd)
        # frac=1 means return all rows (in random order)
        return data_pd.sample(frac=1)
    else:
        return data_pd
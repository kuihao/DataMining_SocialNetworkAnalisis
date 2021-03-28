"""
[Model Training/Testing] 本程式仿效真實套件，具有完善的模型訓練、驗證、測試功能
---
Problem: Classification (Homework 3)
Algorithm: ID3-kai (ID3搭配2個補強演算法：(a)可自動處理連續資料(b)缺失值仍可預測)
---
<Dataset 說明> 
    Attribute: 
    0: 婚姻狀態 marital_status (S: single單身, M: maried已婚)(type: string)(類別/離散資料), 
    1: 家中孩子數量 num_children_at_home (type: Integer)(連續資料), 
    2: 會員卡等級 member_card (Basic, Normal, Silver, Gold)(type: string)(類別/離散資料),
    3: 年齡 age (type: Integer)(連續資料), 
    4: 年收入 year_income (type: Integer)(連續資料)
Labels(classes): 依 Attribute 為會員進行分類，Classes 共有四種會員卡等級
訓練集資料量: 491
驗證集資料量: 98 (20% of training set)
測試集資料量: 211
---
<訓練結果>
2021/03/22: 不理會部分 bug ...... Testing 不錯
訓練集正確率: 0.58
測試集正確率: 0.63

2021/03/23: 修正 bug 之後 ...... 正確建置 ID3 卻 Overfitting
Training accuracy: 0.8961
Testing accuracy: 0.1422

2021/03/24: 加入連續型資料自動切割演算法 ...... Testing 有上升，但 Training 下降頗多
Training accuracy: 0.5743
Testing accuracy: 0.5924
---
<Weka 測試極限: J48>
訓練集正確率: 0.71
測試集正確率: 0.68
"""
# --- 匯入模組 --- #
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
import mylib.myio as io
import mylib.myfun as myfun
import mylib.preprocess as prep 
from mylib import myID3 

# --- Hyperparameter --- #
CLOSEWARNING = True # 關閉 panda 警告
OUTPUT_RESULT_MSG = True # 螢幕顯示
OUTPUT_RESULT_FILE = True # 輸出檔案

# 關閉 pandas 警告
myfun.close_pandas_warning(CLOSEWARNING)
'''
[Load Dataset]
'''
# 第一次訓練時要匯入原始資料，並進行格式調整，之後的訓練都直接使用 CSV 檔案減少運算時間
#df_train = io.load_data(file_path='train_set/training.txt', istest=False)
#df_test = io.load_data(file_path='test_set/test.txt', istest=True)
#io.save_df_to_csv("train_set/train_df", df_train, True)
#io.save_df_to_csv("test_set/test_df", df_test, True)

# 資料集內容跟作業原始檔案是相同的，只是換成 DataFrame 可直接讀取的形式
df_train = io.load_csv_to_df("train_set/train_df_20210322_012249.csv")
df_test = io.load_csv_to_df("test_set/test_df_20210322_012249.csv")
'''
[檢視資料型態]
    若存有缺失值 (匯入時訂為None) 則該欄會顯示 object 型態
'''
#print('[Training set]\nAttributes\' types:\n', prep.col_types(df_train))
#print('[Testing set]\nAttributes\' types:\n', prep.col_types(df_test))

'''
[檢視 Missing Rate]
分析小結:
    Training set
        Num_ChildrenAtHome 30.55%
        MaritalStatus 50.10%
    Testing set
        Num_ChildrenAtHome 34.60%
        MaritalStatus 51.18%
    訓練及測試資料相似，
        MaritalStatus 超過五成的缺失資料，相當嚴重
        Num_ChildrenAtHome 約三成也不低
        皆須考慮與其他 Attributes 的關聯性，若僅約 1% 倒是可考慮用眾數或中位數填補
'''
#print('[Training set-Missing rating]\n', prep.missing_rate(df_train), '\n')
#print('[Testing set-Missing rating]\n', prep.missing_rate(df_test))

'''
[資料分析(Data Analysis)&預處理(preprocessing)]
    (1) 將訓練資料及測試資料合併做預處理
        內部測試時可將兩資料集合併做預處理，
        外部測試時，除了要匯入 Model，
        Private Testset 也需進行相同的預處理才能真正發揮 Model 的能力 
    (2) 分析資料樣態 (敘述性統計、關聯性分析...etc)
    (3) 預處理 (正規化、標準化、特徵合併、特徵重要度篩選、連續轉離散...etc)
'''
# --- (1)合併 training data 及 testing data --- #
df_data = df_train.append(df_test, ignore_index=True)
#print( 'df_data\n', df_data)

# --- (2)資料樣態分析 --- #
# 由於 ID3-kai 或 C4.5 可以「免預處理『連續資料轉換』及『缺失值填補』」
# 因此其實可跳過樣態分析
'''
[缺失值分析: 大膽假設]
    經過交叉比對發現每一筆客戶資料中，
    Marital_Status 完全沒有 Single 'S' 的紀錄 
    Num_Children_At_Home 完全沒有 0位孩子 的紀錄
    因此大膽猜測缺失值並非銀行人員的疏失，而是純粹不會記錄 Single 及 0 位孩子
    故預處理可直接將空值分別取代為 S (Marital_Status) 與 0 (Num_Children_At_Home)
[可視化分析: 大膽假設]
    將資料繪製成分布圖發現 YearIncome 其實是離散資料，
    估計銀行員紀錄客戶資料時就是登記為類別型態，每 20,000 元一個區間
'''
## --- 缺失值分析 --- ##
filter1 = (df_data.MaritalStatus == 'S')
filter2 = (df_data.Num_ChildrenAtHome == 0) 
#print(df_data.MaritalStatus[filter1].count())
#print(df_data.Num_ChildrenAtHome[filter2].count())

## --- Data Visualization --- ##
#plt.hist(df_data['YearIncome'], 100, label="YearIncome")
#plt.show()

# --- (3)預處理 (文字型態儲存值數值化編碼、資料標準化) --- #
# ID3-kai 或 C4.5 可以「免預處理『連續資料轉換』及『缺失值填補』」
## --- 數值化編碼 --- ##
# Missing Value Exchange
df_data['MaritalStatus'] = df_data.MaritalStatus.fillna('S')
df_data['Num_ChildrenAtHome'] = df_data.Num_ChildrenAtHome.fillna(0)

# Label Encoding
MaritalStatus_mapping = {'S':0, 'M':1}
df_data['MaritalStatus'] = df_data.MaritalStatus.map(MaritalStatus_mapping)

MemberCard_mapping = {'Basic':0, 'Normal':1, 'Silver':2, 'Gold':3}
df_data['MemberCard'] = df_data.MemberCard.map(MemberCard_mapping)

df_data['YearIncome'] = df_data.YearIncome.astype('category').cat.codes

# Type Exchange (float -> int)
df_data['Num_ChildrenAtHome'] = df_data.Num_ChildrenAtHome.astype('int')

## --- 資料標準化、特徵縮放 --- ##
# 將年齡資料標準化後，利用四捨五入取至小數第二位，將資料稍微分群
# 再透過 sigmoid 函數加強資料的落差，並四捨五入取至小數第二位
# 將資料量從 71 種下降至 65 種 (壓縮 92%) # 先測試降至 19 種
# ***小結：這樣的方式反而使訓練準確率下降***
#df_data['Age'] = prep.z_score(df_data.Age)
#sigmoidal = df_data['Age'].apply(prep.sigmoid, 0)
#plt.hist(df_data['Age'], 100, label="Age")
#plt.hist(sigmoidal, 100, label="new")
#print(sigmoidal.value_counts().count()) 
#plt.show()
#df_data['Age'] = df_data.Age.apply(prep.sigmoid, 0)
#print('Heterogeneous valus\'s count:\n', df_data.Age.value_counts().count()) 

'''
Descriptive Static (敘述統計) (參考用)
'''
#print("[Training set]\n", df_train.describe())
#print("[Testing set]\n", df_test.describe())

'''
[儲存預處理/切割資料集]
    分成 train set, partial train set, validation set, test set
'''
## --- Train set --- ##
df_train = df_data[:491]

## --- Test set --- ##
# inplace=True 會在原 DataFrame 本身進行更改；drop=True: 不加入原始索引的欄位
df_test = df_data[491:].reset_index(inplace=False, drop=True)
# [儲存] 預處理後的測試資料集
#io.save_df_to_csv("test_set/test_df_preprocessed", df_test, True)

## --- Shuffle Dataset --- ##
#df_train =  prep.shuffle_dataset(df_train, True)
# [儲存] 預處理、亂序排序後的訓練資料集
#io.save_df_to_csv("train_set/train_df_preprocessed_Shuffle", df_train, True)
# [匯入] 預處理、亂序排序後的訓練資料集
#df_train = io.load_csv_to_df('train_set/train_df_preprocessed_shuffle_20210322_012609.csv')

## --- Validation set --- ##
df_validation = df_train.iloc[:98]

## --- Partial Train set --- ##
# inplace=True 會在原 DataFrame 本身進行更改；drop=True: 不加入原始索引的欄位
df_partial_train = df_train.iloc[98:].reset_index(inplace=False, drop=True)


'''
[模型訓練、模型測試]
'''
## --- 特徵標籤分離  --- ##
train_x, train_y = myfun.split_dataset_to_xy(df_train)
partial_train_x, partial_train_y = myfun.split_dataset_to_xy(df_partial_train)
validation_x, validation_y = myfun.split_dataset_to_xy(df_validation)
test_x, test_y = myfun.split_dataset_to_xy(df_test)

## --- 特徵型態 (離散或連續) --- ##
# 離散 = 0, 連續 = 1
LabelProperties = { 'MaritalStatus':0, 'Num_ChildrenAtHome':1,
                    'MemberCard':0, 'Age':1, 'YearIncome':1}

## --- 建立模型 --- ##
DCT = myID3.ID3_kai(LabelProperties, 0)

## --- 訓練模型 --- ##
DCT.fit(train_x, train_y)
print('Training accuracy:', DCT.accuracy()) # 訓練準確率
#Result = DCT.predict() # 輸出結果
#if OUTPUT_RESULT_MSG: output_msg = io.output_result('train_set/training.txt', Result, 5) # 螢幕顯示

## --- 模型測試 --- ##
print('Testing accuracy:', DCT.accuracy(test_x, test_y)) # 測試準確率
Result = DCT.predict(test_x) # 輸出結果
if OUTPUT_RESULT_MSG: output_msg = io.output_result('test_set/test.txt', Result) # 螢幕顯示
if OUTPUT_RESULT_FILE: io.save_string_to_txt('', output_msg) # 輸出成檔案
#io.save_dict_to_json('add_conti_split' ,DCT.DecisionTree)
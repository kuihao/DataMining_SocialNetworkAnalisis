import pandas as pd
import numpy as np
import json
from datetime import datetime
"""
匯入原始資料集
---
參數: 檔案路徑 (string)
---
回傳: 
"""
def load_data(file_path=''):
    # [open...]: r 表示唯讀模式
    with open(file_path, 'r') as file_datas: # file_datas 是 python 儲存讀入檔案的 buffer 
        # 先讀一行知道有個幾維度並設為 dataframe 的 columns 
        onerow = file_datas.readline().strip('\n') # [strip('\n')] 去除換行符號
        list_data = onerow.split(' ') # [split(' ')]: 依照 Space (空格) 分切，資料結構為 list
        list_data =  list(map(float, list_data)) # 轉型 str -> float
        number_dimension = len(list_data)
        indexs_dimension = list(range(number_dimension))
        dataset = pd.DataFrame( data = [list_data], columns = indexs_dimension ) # 初始化 DataFrame

        # 讀取檔案中剩餘的資料，每次讀一列
        for row in file_datas:
            row = row.strip('\n') # [strip('\n')] 去除換行符號
            list_data = row.split(' ') # [split(' ')]: 依照 Space (空格) 分切，資料結構為 list
            list_data =  list(map(float, list_data)) # 轉型 str -> float
            dataset = dataset.append([list_data], ignore_index = True)

    return dataset.to_numpy() # 暫時回傳 numpy 陣列

'''
[顯示結果]
輸出範例：X Y ClusterID 
---
回傳: 字串形式的結果
'''
def user_output(database:'numpy', cluster_label:list, init_msg:str) -> ('text_result:str'): 
    print(init_msg+"\n")
    text_result = init_msg+'\n\n'
    for xy, label in zip(database, cluster_label):
        print(xy, "ClusterID = ", label)
        text_result += f"{xy[0]} {xy[1]} ClusterID = {label}\n"
    return text_result

'''
將 DataFrame 存成 CSV 檔案
def save_df_to_csv(file_path='', df_data=None, bool_save=True):
    if bool_save:
        time_now = datetime.now()
        time_str =  time_now.strftime("_%Y%m%d_%H%M%S")
        file_path += time_str+".csv"
        
        df_data.to_csv(file_path , index=False)
        print(file_path, 'has been saved.')
'''

'''
將 CSV 匯入 DataFrame
def load_csv_to_df(file_path=''):
    return pd.read_csv(file_path) 
'''

'''
將 dict 存成 json 檔案
def save_dict_to_json(file_path='', dict_data=None, bool_save=True):
    if bool_save:
        time_now = datetime.now()
        time_str =  time_now.strftime("_%Y%m%d_%H%M%S")
        file_path += time_str+".json"
        with open(file_path, 'w') as jsonfile:
            json.dump(dict_data, jsonfile)
            print(file_path, 'has been saved.')
'''

'''
將 json 匯入 dict
def load_json_to_dict(file_path=''):
    with open(file_path, 'r') as jsonfile:
        return json.load(jsonfile)
'''

'''
將 string 存成 txt 檔案
'''
def save_string_to_txt(file_path='', string_data=None):
    time_now = datetime.now()
    time_str = time_now.strftime("_%Y%m%d_%H%M%S")
    
    file_path += "OutputResult"+time_str+".txt"
    result_file = open(file_path, 'w')
    result_file.writelines(string_data)

    print("*** Saving result in folder complete~ ***")
    result_file.close()
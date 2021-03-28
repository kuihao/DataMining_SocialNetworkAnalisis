import pandas as pd
import json
from datetime import datetime
"""
匯入資料集
---
參數: 檔案路徑 (string)
---
回傳: 會員資料表 (pd.DataFrame)，Row: Member ID, Column: Attributes
"""
def load_data(file_path='', istest=False):
    # initialize member_table
    member_table = pd.DataFrame(columns = ['0', '1', '2', '3', '4'])
    # [open...]: r 表示唯讀模式
    with open(file_path, 'r') as file_datas: 
        # 每次從檔案資料中取一列
        # [!!!] 若檔案過大，請於此監視 row 的狀態
        for row in file_datas:
            # [member_list] 初始化暫時存放單筆資料的 dict
            if not(istest):
                member_list = {'0': None, '1': None, '2':'Basic', '3': None, '4': None}
            else:
                # 此作業兩者沒有差異，但基本上測試資料不應該給 Ground Truth
                member_list = {'0': None, '1': None, '2': 'Basic', '3': None, '4': None}
            # [strip()]: 去除 {、} 符號
            row = row.strip("{}\n")
            # [split(',')]: 依照逗號分切每個 Attribute info.，資料結構為 list
            temp_list1 = row.split(',')
            for col in temp_list1:
                # [strip()]: 以字串切割 Attribute No. 與 value
                temp_list2 = col.split(' ')
                attrbute_number = temp_list2[0]
                attrbute_value = temp_list2[1]
                member_list[attrbute_number] = attrbute_value
            member_table = member_table.append(member_list, ignore_index=True)  
    # 變更欄位名稱以增加分析可讀性
    member_table.columns = ['MaritalStatus', 'Num_ChildrenAtHome', 'MemberCard', 'Age', 'YearIncome']
    #print(member_table)
    return member_table

'''
[顯示結果]
輸出範例：{0 M,1 1,3 59,4 60000} member_card = basic
---
回傳: 字串形式的結果
'''
def output_result(file_path, predict_class:list, number_print = None): 
    MemberCard_mapping = {0:'Basic', 1:'Normal', 2:'Silver', 3:'Gold', -1:'Fail'}
    predict_class = list(map(MemberCard_mapping.get, predict_class))

    with open(file_path, 'r') as file_datas: 
        result_msg = ''
        i = 0
        for row in file_datas:
            row = row.strip("\n")
            tmp_str = row + ' member_card = ' + predict_class[i]
            print(tmp_str)
            result_msg += tmp_str + '\n'
            i += 1
            if number_print and number_print == i: break
    return result_msg

'''
將 DataFrame 存成 CSV 檔案
'''
def save_df_to_csv(file_path='', df_data=None, bool_save=True):
    if bool_save:
        time_now = datetime.now()
        time_str =  time_now.strftime("_%Y%m%d_%H%M%S")
        file_path += time_str+".csv"
        
        df_data.to_csv(file_path , index=False)
        print(file_path, 'has been saved.')

'''
將 CSV 匯入 DataFrame
'''
def load_csv_to_df(file_path=''):
    return pd.read_csv(file_path) 

'''
將 dict 存成 json 檔案
'''
def save_dict_to_json(file_path='', dict_data=None, bool_save=True):
    if bool_save:
        time_now = datetime.now()
        time_str =  time_now.strftime("_%Y%m%d_%H%M%S")
        file_path += time_str+".json"
        with open(file_path, 'w') as jsonfile:
            json.dump(dict_data, jsonfile)
            print(file_path, 'has been saved.')
'''
將 json 匯入 dict
'''
def load_json_to_dict(file_path=''):
    with open(file_path, 'r') as jsonfile:
        return json.load(jsonfile)
    
'''
將 string 存成 txt 檔案
'''
def save_string_to_txt(file_path='', string_data=None):
    time_now = datetime.now()
    time_str = time_now.strftime("_%Y%m%d_%H%M%S")
    
    file_path += "OutputResult"+time_str+".txt"
    result_file = open(file_path, 'w')
    result_file.writelines(string_data)
    result_file.close()
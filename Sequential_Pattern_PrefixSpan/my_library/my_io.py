# 導入 pandas: 可進行大數據檢視、切割或快速排序，內含資料框架結構
import pandas as pd
import csv

# Load InputData File
def load_data(file_path):
    '''
        # [database_table]: type = dict
        #                   struct: {cid: {timecode: [item] 
        #                   'cid' = integer of "Customer ID"
        #                   'timecode' = different time point means different itemset
        #                   '[item]' = list of "Item Set", 為了實作方便
        #                              將 set 以字典序儲存，因此以 list 結構儲存
        #                   'item' = element in Item Set
    '''
    # Initicialize database_talbe
    database_table = {}
    # [open...]: r 表示唯讀模式
    with open(file_path, 'r') as file_datas: 
        # 每次從檔案資料中取一列
        # [!!!] 若檔案過大，請於此監視 row 的狀態
        for row in file_datas:            
            # [row.split()]: 依照空格分切元素，資料結構為 list
            temp_list = row.split()
            temp_list = list(map(int, temp_list))
            # temp_list 第一個 node 是 CID
            cid = temp_list[0]
            # 第一層 dict 的 key = cid
            # [.get()]: 如果查不到東西 .get() 會回傳 None
            if database_table.get(cid) == None:
                database_table[cid] = {}
                temp_list.pop(0)
            
            # 開始處理 Transaction Time Senquence 與 Items
            # 利用 dict 將特定時間購買的 item 映射至該時間的 itemset
            for i in range(0, len(temp_list), 2):
                timecode = temp_list[i]
                item = temp_list[i+1]
                # 第二層 dict 的 key = timecode, value = [item]
                if database_table[cid].get(timecode) == None:
                    database_table[cid][timecode] = [item]
                # 若 timecode 已存在，直接於現有 list 尾巴新增 item
                else:
                    database_table[cid][timecode].append(item)
        # 將 itemset (struct: list) 以字典序升冪排序
        for key_timecode in database_table[cid]:
            database_table[cid][key_timecode].sort()
    # print(database_table)
    return database_table

# 使用者輸入：輸入 min_sup 並轉成整數
def user_unput(open, min_sup, database_length):
    if open:
        percentage = input("Please enter the \"decimal number\" (percentage) of minimum support\n(Ex. 0.001 means minimum support = 0.1%)\n:")
        return round(database_length*float(percentage), 2)
    else:
        return min_sup

# 自動控制輸出訊息
def showing_info(flag, msg):
    if flag:
        print('*Debug info: ', msg)

# 顯示結果: 調整格式 9126 || 7088 9126 || SUP: 187
def output_sequencial_pattern(final_sequencial_patterns, min_sup, database_length):
    prompt1 = "PrefixSpan Algorithm: Find Sequential Patterns\n"
    prompt2 = prompt1 + 'Minimum support percentage: '+str(round(float(min_sup)/database_length, 3))+'\n'
    print(prompt2)
    ResultInOneLine = prompt2
    if final_sequencial_patterns == 0:
        print('No Sequential Patterns')
        ResultInOneLine += 'No Sequential Patterns'
        return ResultInOneLine
    else:
        for list_ans in final_sequencial_patterns: 
            rule = list_ans[0]
            sup = list_ans[1]
            temp_str = ''
            if len(rule) > 1: 
                for i in range(len(rule)):
                    for item in rule[i]:
                        temp_str += str(int(item)) + ' '
                    temp_str += '|| '
                temp_str += 'SUP: ' + str(sup) + "\n"
                print(temp_str)
                ResultInOneLine += temp_str
        return ResultInOneLine

# Output Result File
# 時間戳記 (方便檢閱輸出檔案)
# 此時 frequent_rule_list 每條 rule 要加上 \n 或改成 for 讀取之類
from datetime import datetime
def output_result_file_txt(final_sequencial_pattern_txt, changename, name):
    time_now = datetime.now()
    time_str =  time_now.strftime("_%Y%m%d_%H%M%S")
    if changename:
        output_path = str(name)+time_str+".txt"
    else:
        output_path = "OutputResult"+time_str+".txt"
    result_file = open(output_path, 'w')
    result_file.writelines(final_sequencial_pattern_txt)
    result_file.close()

def output_result_file_csv(final_sequencial_pattern_csv):
    time_now = datetime.now()
    time_str =  time_now.strftime("_%Y%m%d_%H%M%S")
    output_path = "OutputResult"+time_str+".csv"
    result_file = open(output_path, 'w', newline='')
    result_file.writelines(final_sequencial_pattern_csv)
    result_file.close()

def save_database_cav(save, transformed_database):
    if save:
        time_now = datetime.now()
        time_str =  time_now.strftime("_%Y%m%d_%H%M%S")
        output_path = "Database"+time_str+".csv"
        # with open: 結束時會自動呼叫 .close()
        with open(output_path, 'w', newline='') as csvfile:
            # 建立 csv 檔寫入器
            writer = csv.writer(csvfile)
            # 寫入一列資料
            writer.writerow(['CID'])
            writer.writerow(['Timecode_length'])
            writer.writerow(['Sequence'])
            for key_cid in transformed_database:
                writer.writerow([key_cid])
                writer.writerow(str(len(transformed_database[key_cid])))
                for key_timecode in transformed_database[key_cid]:
                    writer.writerow(transformed_database[key_cid][key_timecode])

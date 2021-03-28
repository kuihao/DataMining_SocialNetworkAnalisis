import pandas as pd
# 說明
'''
    #[實作演算法]: PrefixSpan (上課簡報為 Partition-Based)
    #[參考論文]: J. Pei, J. Han, H. Pinto, Q. Chen, U. Dayal, and M.-C. Hsu.
    #            PrefixSpan: Mining Sequential Patterns Efficiently by 
    #            PrefixProjected Pattern Growth. ICDE'01 (TKDE’04).
    #[定義問題]: 
    #    (1) 長度為 1 的 item 出現次數大於或等於 Minimum Support 即為 Pattern
    #    (2) 仿效 Prifix 論文的定義：同一條 CID 內，同樣的 Sequencial Pattern 只會統計一次
    #        Ex. CID 001 有 [1 -> 2 -> 3 -> 1 -> 2 -> 3] 則 1 -> 2 -> 3 的 support = 1
    #    (3) 仿效 Prifix 論文的定義：同一個 set 中的 elements 也可算為 Sequence 
    #        Ex. 
    #        CID 001, [1 -> (2, 3) -> 3]
    #        CID 002, [4 -> (3, 2) -> 6]
    #        則 (2, 3) 的 support = 2
    #---
'''

# --- Hyperparameter --- #
# 是否開啟使用者輸入模式
OPEN_USER_INPUT = True
# 是否印出 Debug 訊息
OPEN_DEBUG_INFO = False
# 是否儲存整理好的 Database
SAVE_TRANSFORM_DATABASE = False
# 是否開啟整理好的 Database
# LOAD_TRANSFORM_DATABASE = False
# 作業規定輸入檔案
FILE_PATH = 'seqdata_dat.txt'
# 迷你測試檔案 (10%)
FILE_PATH2 = 'testdata_10_persentage.txt'
# Minimum Support 初始值 (個數表示法)
MIN_SUP = 10 #150  #F2 31 #F1 310

# --- Import Function --- #
import my_library.my_io as myio

### ------ Main Code ------ ###
print("Start! Good Luck~")
# --- Load data & Make table --- #
Database = myio.load_data(FILE_PATH)
print('Load database fiinished.\n')
# Save preprocessed database
myio.save_database_cav(SAVE_TRANSFORM_DATABASE, Database)

# --- User input minimum support --- #
database_length = len(Database)
print('Okay, please wait for few "seconds"~\n----------')
MIN_SUP = myio.user_unput(OPEN_USER_INPUT, MIN_SUP, database_length)

# --- PrefixSpan Algorithm --- #
import my_library.PrefixSpan as ps
# Use PrefixSpan Algorithm
Final_Result = ps.PrefixSpan([], 0, Database, {}, MIN_SUP)
# --- Output and Save Result --- #
tidy_datas = myio.output_sequencial_pattern(Final_Result, MIN_SUP, database_length)
print('Ready write in file...')
myio.output_result_file_txt(tidy_datas, False, None)
print('Result file finish. :)')
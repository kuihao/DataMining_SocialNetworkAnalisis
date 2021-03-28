# ==={ The Apriori Algorithm (微改) }=== #

# --- 導入 numpy 模組 --- #
# Numpy 是 N 維度的陣列模組 (N-dimensional array)
# 宣告 npobj 為 np.array 的實體，則具有以下 Method：
# ndim (返回維度), shape (返回元素個數), dtype (返回資料型別) 
# 若想對 list 結構進行矩陣數學運算，則轉成 Numpy 會更有效率、簡單
import numpy as np
# --- 導入 pandas 大數據處理模組，進行資料檢視、切割處理或快速排序 --- #
import pandas as pd
# 引入深度複製模組
from copy import deepcopy
# 時間戳記 (方便檢閱輸出檔案)
from datetime import datetime
import time

# --- Function ---#

# Debug: 顯示運作資訊
ShowingInfo = False

# Load InputData File
def Load_Data(File_Path, DB_table):
    with open(File_Path, 'r') as file:
        for row in file:
            temp_arr = row.split() # 依照空格分切元素，資料結構為 list
            temp_set = set(map(int, temp_arr)) # 將元素由 str 轉型為 int，並轉成 Set 結構
            DB_table.append(temp_set) # 動態新增一條交易紀錄至資料表
    return DB_table

# Candidate Itemset 產生聯集關聯表 (因為技術上 set 結構無法當作主鍵，只好改成關聯表)
def Candidate_Itemset_Generator(Frequent_Table=None, k=None, Pruning=True):
    ItemsetColumn = []
    # Self-Joining 產生聯集
    for i in range(0, len(Frequent_Table[k])):
        for j in range(i+1, len(Frequent_Table[k])):
            if k < 1:
                temp_setA = set()
                temp_setA.add(deepcopy(Frequent_Table[k]['itemset'][i]))
                temp_setB = set()
                temp_setB.add(deepcopy(Frequent_Table[k]['itemset'][j]))
                ItemsetColumn.append(temp_setA | temp_setB)
            else:
                temp_setA = set()
                temp_setA = deepcopy(Frequent_Table[k]['itemset'][i])
                temp_setB = set()
                temp_setB = deepcopy(Frequent_Table[k]['itemset'][j])
                union_set = temp_setA | temp_setB
                IsReapet = False
                for m in range(len(ItemsetColumn)):
                    if ItemsetColumn[m] == union_set:
                        IsReapet = True
                        break
                if not(IsReapet):
                    ItemsetColumn.append(union_set)
    #print("The ItemsetColumn is:", ItemsetColumn)
    # Pruning 刪去子集不足，實際上無法構成的聯集
    # 然而 C3 之後才需要使用，C2 是兩元素聯集，必定由 L1 產生，因此無須檢測 C2
    if ShowingInfo: print("Start pruning in candidate.")
    if Pruning == True:
        i = 0
        while(i < len(ItemsetColumn)):
            subset_count = 0
            downward_limit = len(ItemsetColumn[i]) # Downward Closure Property
            for subset_L_lastk in Frequent_Table[k]['itemset']:
                if subset_count >= downward_limit:
                    break
                elif ItemsetColumn[i].issuperset(subset_L_lastk):
                    subset_count += 1
            if subset_count < downward_limit:
                #print("Prun:", ItemsetColumn[i], 'i=', i)
                ItemsetColumn.pop(i)
                i -= 1
                if i < 0: i=0
            else:
                i += 1
    return ItemsetColumn

# Candidate_Table C2 以後的產生器 (C1初始化另外處理)
# 根據所產生的 Candidate Itemset (聯集) 去遍歷計算 Support Counts
def Candidate_Support_Generator(DB_table, ItemSet):
    Candidate_Supports_Table = {}
    # DB_Table Traverse
    if ShowingInfo: print("Caulating the candidate support in Trans-Table.")
    for Transaction_Set in DB_table:
        for i in range(len(ItemSet)):
            if ItemSet[i].issubset(Transaction_Set):
                if Candidate_Supports_Table.get(i) !=None:
                    Candidate_Supports_Table[i] += 1
                else:
                    Candidate_Supports_Table.setdefault(i, 1)
    return Candidate_Supports_Table

# 產生 Frequent Table
def Frequent_Table_Generator(Candidate_Table=None, ItemSet=None, Candidate_Supports_Table=None, min_support=0):
    if (ItemSet==None) and (Candidate_Supports_Table==None):
        # 用 Pandas DataFrame 盛裝 Candidate_Table (原結構為 dict)
        temp_df = pd.DataFrame(Candidate_Table, index=[0])
        # 行列互換 (純粹方便閱讀)
        trans_df = temp_df.transpose()
        # 排序 (此非原演算法的步驟，但這能增進程式效能)
        sorted_df = trans_df.sort_values(axis=0, by=0, ascending=False)
        # 依照 Minima Support 去除不合規則的 Candidate Items
        # 得到 Frequent Table
        mask = sorted_df[0]>=min_support
        Frequent_Table = sorted_df[mask]
        
        list_supps = Frequent_Table.iloc[:, 0].to_list()
        list_itset = Frequent_Table.index.to_list()
        Frequent_Table = pd.DataFrame({'itemset':list_itset, 'sup':list_supps})
        return Frequent_Table
#       #   print(df.sort_values(axis=1, by=0, ascending=False)) 數量由大至小排序
#       #   print(rev_df.sort_values(axis=0, by=0, ascending=False)) 數量由大至小排序
#       #   L1.rename(columns={0:'value'})
    else:
        # 用 Pandas DataFrame 盛裝 Candidate_Table (原結構為 dict)
        temp_df = pd.DataFrame(Candidate_Supports_Table, index=[0])
        # 行列互換 (純粹方便閱讀)
        trans_df = temp_df.transpose()
        # 排序 (此非原演算法的步驟，但這能增進程式效能)
        sorted_df = trans_df.sort_values(axis=0, by=0, ascending=False)
        # 依照 Minima Support 去除不合規則的 Candidate Items
        # 得到 Frequent Table
        mask = sorted_df[0]>=min_support
        Frequent_Table = sorted_df[mask]

        Candidate_Itemsets_Table = pd.DataFrame({'itemset':ItemSet}).to_dict()

        list_itset = []
        for i in range(len(Frequent_Table)):
            list_itset.append( Candidate_Itemsets_Table['itemset'][Frequent_Table.index[i]] )
        list_supps = Frequent_Table.iloc[:,0].to_list()
        Frequent_Table = pd.DataFrame({'itemset':list_itset, 'sup':list_supps})
        #print(L2)

        return Frequent_Table

# --- Code Start --- #

# --- 使用者自定義輸入 --- #
min_supp = int(input("HI! Please enter the \"Integer\" number of \"Minima Support\".\n:"))
min_conf = float(input("HI! Please enter the \"Folat\" number of \"Minima Confidence\"."
                    + "(Ex. 0.66)\n:"))
#min_supp = 2
#min_conf = 0.666

# --- 使用 Pyton 鏈串結構建立 DataBase 的資料表 --- #
TransactionTable = []

# --- 載入 InputData 檔案 --- #
File1 = 'testdata.txt'
File2 = 'InputData.txt'
TransactionTable = Load_Data(File2, TransactionTable)

# --- Candidate Table: 使用字典結構建立 C1 --- #
C1 = {} # {} 相當於 dict()；建立字典 (即 C++ 的 map 映射結構)。C1[key] 回傳 value
for i in range(0, len(TransactionTable)):
    for item in TransactionTable[i]:
        if C1.get(item)!=None: # C1.__contains__(str(item)):
            C1[item] += 1 # 或是製作 dict2 = {item, 1}; C1.update(dict2)
        else:
            C1.setdefault(item, 1)
if ShowingInfo: print('C1 finish.')

# --- 建立 Frequent Table: L1 --- #
L1  = Frequent_Table_Generator(Candidate_Table = C1, min_support = min_supp)
if ShowingInfo: print('L1 finish.')

# 刪除已無用的 C1 表格節省資源
del C1

# --- 依演算法找出所有 Association Frequent Tables Lk --- #
# L 為 k 張 Frequent Tables 組成的大陣列 (動態二維 List，每一張 Lk 又是二維 DataFrame) 
L = []
# 塞入 L1
if not(L1.empty):
    L.append(L1)
    if ShowingInfo: print(L1)

# 迴圈開始!!
# 依照演算法，產生 L1 後進入迴圈，k 從第一張的序數開始，
# 本 Code 從 0 開始計數，因此 k = 0 (和簡報上 k = 1 相同意義)
k = 0
while(True):
    # 若 Lk 不存在則結束迴圈
    try:
        L[k]
    except IndexError:
        #print('Ready to stop!!')
        break
    except:
        print('Something else wrong! Please debug.')
    # 製作候選表 Ck 的 Itemset 欄位 (由集合聯集組成的關聯表，以 index 為主鍵)
    # Candidate_Itemset_Generator 內部實作「Self-joining」跟「Pruning」演算法
    if k == 0:
        # C2 的 ItemSet 為組合運算 Combinatorics (n取2)，無須 Pruning
        C_next_k_itemset = Candidate_Itemset_Generator(Frequent_Table=L, k=k, Pruning=False)
    else:
        C_next_k_itemset = Candidate_Itemset_Generator(Frequent_Table=L, k=k, Pruning=True)
    # 遍歷計算 Supps
    C_next_k_Supps = Candidate_Support_Generator(TransactionTable, C_next_k_itemset)
    if ShowingInfo: print('C'+str(k+2)+' finish.')
    # 產生 Frequent Table: L2 
    L_next_k = Frequent_Table_Generator(ItemSet=C_next_k_itemset, Candidate_Supports_Table=C_next_k_Supps, min_support=min_supp)

    # 刪除無用表格節省空間
    del C_next_k_itemset
    del C_next_k_Supps

    # L2 加入 L 總表
    if not(L_next_k.empty):
        temp_L = deepcopy(L_next_k)
        L.append(temp_L)
        if ShowingInfo: print('L'+str(k+2)+' finish.')

    # 下一圈投入此次生產的表
    k += 1
#print(L)

# 得出所有 L 表之後速算答案
print("------ Report ------")
rep1 = str("1. The minima support is "+str(min_supp)+"\n")
rep2 = str("2. The minima confidence is "+str(min_conf)+"\n")
rep3 = str("3. The strong association rules:\n")
rep = rep1+rep2+rep3
print(rep)
AssociationRules = []
AssociationRules.append(rep)

for k in reversed(range(len(L))):
    if k != 0:
        for m in range(len(L[k].index)):
          for p in range(len(L[k-1].index)):
                M_sup = L[k]['sup'][m]
                P_sup = L[k-1]['sup'][p]
                # 這裡不夠嚴謹，confidence 應考慮分母不同的組合，
                # 並非只看單一前一張 Large Table 的 support，這樣會少算關聯規則
                if (M_sup/P_sup) >= min_conf:
                    if k == 1:
                        Rule = str('{'+str(L[k-1]['itemset'][p])+'}'+' -> '+str(L[k]['itemset'][m])+
                        ' ('+str(M_sup)+'/'+str(P_sup)+')'+'\n')
                        print(Rule)
                    else:
                        Rule = str(str(L[k-1]['itemset'][p])+' -> '+str(L[k]['itemset'][m])+
                        ' ('+str(M_sup)+'/'+str(P_sup)+')'+'\n')
                        print(Rule)
                    AssociationRules.append(Rule)

time_now = datetime.now()
time_str =  time_now.strftime("_%Y%m%d_%H%M%S")
OutputPath = "OutputResult"+time_str+".txt"
ResultFile = open(OutputPath, 'w')
ResultFile.writelines(AssociationRules)
ResultFile.close()
if ShowingInfo: print("Result File Generated Successfully.")

print("*** Process will end in 5 seconds...... ***")
time.sleep(5)
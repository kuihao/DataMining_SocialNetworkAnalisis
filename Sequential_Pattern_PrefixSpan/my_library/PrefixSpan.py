'''
    # [最至要關鍵的演算法核心]：用 Prefix 產生 Sequential Patterns
    # 參數 1: sequential pattern --> prefix sequence of last level
    #        type: list, seq.: [item], [item], [item]], timecode: last itemset's timecode
    #        prefix sequence: [seq, timecode]        
    # 參數 2: prefix sequence length
    # 參數 3: original sequence database
    # 參數 4: the N-projection database 
    # 參數 5: minimum support threshold
'''
# 導入 pandas: 可進行大數據檢視、切割或快速排序，內含資料框架結構，合併 df 是新的記憶體位置
import pandas as pd
# 導入 deepcopy 用於更改記憶體位置獨立儲存
from copy import deepcopy
# 導入偵錯函式

if __name__ == '__main__': 
    from my_io import showing_info
    from my_io import output_sequencial_pattern
    from my_io import output_result_file_txt
    from step1 import find_length1_sequential_patterns
    from step2 import divide_search_space
    from step3 import find_subsets_of_sequential_patterns
    #from bi_level_projection import bi_level_projection
else: 
    try: 
        from my_library.my_io import showing_info
        from my_library.my_io import output_sequencial_pattern
        from my_library.my_io import output_result_file_txt 
        from my_library.step1 import find_length1_sequential_patterns
        from my_library.step2 import divide_search_space
        from my_library.step3 import find_subsets_of_sequential_patterns
        #from my_library.bi_level_projection import bi_level_projection
    except: print('Import Error in PrefixSpan.py')


# --- Hyperparameter --- #
OPEN_DEBUG_INFO = False

# --- [Algorithm] PrefixSpan (Prefixprojected Pattern Growth) --- #
def PrefixSpan( prefix_sequence = None, length_prefix_seq = 0,
                database = {}, pseudo_database = {},
                min_sup = 999): 
    # [sequential_pattern] prifix seq. of last level
    # [Final_Sequential_Patterns_Table] 用來回傳當前找到的 Sequential Patterns
    Final_Sequential_Patterns_Table = [] # [!!!] 考慮無用
    
    # --- {Step 1} Find length-1 sequential patterns --- #
    # [length1_patterns] = the prefix of this level 
    payload1 = find_length1_sequential_patterns(database, pseudo_database,
                                                min_sup, length_prefix_seq)
    length1_patterns = payload1[0]
    new_pseudo_database = payload1[1] # [!!!] 可考慮不在此步驟產生 new_pseudo_database 用 bi 替換
    
    # 原應檢查 length-1 pattern a 是否能和原本輸入的 Sequential patterns s 形成 New Sequential patterns s'
    # 因為使用 Bi-level projection 作最佳化，因此必然能形成 Sequential patterns，應毋須再檢查
    if not(length1_patterns):
        return 0
    
    # --- {Step 2}: Divide search space (因使用 Pseudo projection 此步驟僅需合成 seq.) --- #
    # new_sequence_pattern_table: [[Seq.Pat., sup]]
    new_sequence_pattern_table = divide_search_space(prefix_sequence, length1_patterns)
    Final_Sequential_Patterns_Table += new_sequence_pattern_table
    
    # ---{Step 3}: Find subsets of sequential patterns --- #
    # 最佳化: bi-level projection 運算 (利用 Length-1 Pattern)，找出下一層能形成 Seq. Pat. 的 Rule
    # [!!!] bi-level projection 因論文無詳述如何實作，自行實作後效能反而變差而棄之，
    # L2_Sequence_Pattern_Table = bi_level_projection(database, pseudo_database, length1_patterns, min_sup)
    '''
    # [!!!] 演算法最關鍵的地方： 於第三步驟，此層新找到的 Sequencial Pattern 要視為「Prefix」
        #       意思是相對於下一層所使用的 Sub-database 中的那些 (Sub-)Sequence 而言是  Pre-sequence
        #       事實上，Prefix 的最後一個 element 就是 Length-1 Pattern，但要傳入遞迴的是 Prefix
        #       論文中似乎把 Pre-sequence 和 bi-level sequence 的第一個字都稱為 Prefix，使人有些混淆
        #       因此，此處定義 Pre-sequence 為 Prefix，
        #       並定義 bi-level sequence 是由 bi-prefix 和 bi-postfix 組成 Length-2 sequence
    '''
    for this_prefix_seq in new_sequence_pattern_table:
        postfix = this_prefix_seq[0][-1][-1]
        if new_pseudo_database.get(postfix) != None:
            recursive_back = PrefixSpan(this_prefix_seq,
                                            length_prefix_seq+1,
                                            database,
                                            new_pseudo_database[postfix],
                                            min_sup)
            if recursive_back != 0:
                Final_Sequential_Patterns_Table += recursive_back
    return Final_Sequential_Patterns_Table


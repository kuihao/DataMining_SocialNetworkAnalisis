'''
Step 2: Divide search space
    (1) 產生 new sequential patterns:
        For each length1 pattern e, append it to prefix s to form a sequential pattern s'
    (2) 輸出 new sequential patterns
        將 length1_pattern 的 sup 作為 new sequential patterns 的 sup 次數
        因為原本演算法是專門從 projected database 挑出 patterns e
        如果 s' = s + e 成立，則 sup(s) <= sup(e) = sup(s') 
'''
from copy import deepcopy
# [prefix_sequence] list[Seq.Pat.(prefix), last timecode of prefix]
# [length1_patterns] dict{key = this level prefix, value = sup}
def divide_search_space(prefix_sequence, length1_patterns):
    # [new_sequence_pattern_table] [Seq.Pat., sup] 
    new_sequence_pattern_table = []
    
    # 第一次 PrifixSpan 因 prefix_sequence 尚未存在
    # 則 length1_patterns 就是此層的 Seq.Pat. 直接輸出即可 
    if not(prefix_sequence):
        for key_pattern in length1_patterns:
            new_sequence_pattern_table.append([[[key_pattern]], length1_patterns[key_pattern]])
        return new_sequence_pattern_table
    # 若 prefix_sequence 存在則黏合 length1_patterns 並輸出
    # 注意需判斷是否在同一個集合
    else:
        for key_pattern in length1_patterns:
            # 組合 seq.
            #   prefix_sequence[0]: list of prefix_sequence
            #   prefix_sequence[1]: lset prefix_sequence's timecode
            new_sequence = deepcopy(prefix_sequence[0])
            # 若 type(key_pattern) 是 str，表示這個 pattern 要放入 prefix_sequence 的最後一個 set
            if type(key_pattern) == type('String'):
                inset = False
                for element in new_sequence[-1]:
                    if int(element) == int(key_pattern):
                        inset = True
                        break
                if not(inset):
                    new_sequence[-1].append(key_pattern)
            else:
                new_sequence.append([key_pattern])
            # 取出 sup
            sup = length1_patterns[key_pattern]
            # 放進輸出表
            new_sequence_pattern_table.append([new_sequence, sup])
        return new_sequence_pattern_table
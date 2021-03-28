'''
Step 3: Find subsets of sequential patterns
    (1) For each α’, construct α’-projected database S|α’
        [翻譯]: 將目前組成的 sequential patterns 視為 prefix，依序產生子資料庫 [可怕]
        [可怕之處]: 論文沒提到如何有效率地產生 Projected Database，莫非是線性建立 
        [不用怕]: 改成先用 Bi-level projection 算出 Freq. 再切出 Projected Database
        [變勇敢]: 搭配 pseudo_projection 用指標假裝建立子資料庫
        [Projected Database 要點]: 若 prefix 最後一的 element 與 Projected sequence 
                                       重疊於同一個 itemset，須將 Postfix 改成底線替換元素
    (2) [Recursive] call PrefixSpan(α’, l+1, S|α’).
    (3) 最後應可刪除原資料庫
    !!! 切子資料庫時要替換出底線元素
'''
def find_subsets_of_sequential_patterns(l2_prefix, l2_postfix, database, sameset):
    psrudo_sub_database = pseudo_projection()
    list_pointer = []
    list_offset_itemset = []
    list_offset_element = []
    if sameset:
        tmp_union = {str(l2_prefix), str(l2_postfix)}
        record = False
        for rowindex in range(len(database['Seq_ItemSet'])): 
            idx = 0
            for itemset in database['Seq_ItemSet'][rowindex]:
                # if record == True
                if record:
                    list_pointer.append(database.index[rowindex])
                    list_offset_itemset.append(idx)
                    list_offset_element.append(0)
                    record = False
                    # 既然這條 CID 已經在最一開始登記完，則不必再重複查看這條 Seq.
                    break
                if itemset.issuperset(tmp_union):
                    record = True
                idx += 1
    else:
        ready_record = False
        jump_next_seq = False
        for rowindex in range(len(database['Seq_ItemSet'])): 
            if jump_next_seq: jump_next_seq = False
            for itemset in range(len(database['Seq_ItemSet'][rowindex])):
                if jump_next_seq:
                    jump_next_seq = False 
                    break
                tmp_list = sorted(list(database['Seq_ItemSet'][rowindex][itemset]))
                list_itemset = tmp_list
                #list_itemset =  list(map(int, tmp_list))
                for element in range(len(list_itemset)):
                    if ready_record:
                        if list_itemset[element] == l2_postfix:
                            list_pointer.append(database.index[rowindex])
                            list_offset_itemset.append(itemset)
                            list_offset_element.append(element) 
                            ready_record = False
                            # 這條 CID 已登記，直接看下一條
                            jump_next_seq = True
                            break
                    if ready_record == False and list_itemset[element] == l2_prefix:
                        ready_record = True
                        # 兩項物品在不同集合，因此不必再檢查 prefix 所在的集合
                        break
    psrudo_sub_database['Pointer'] = list_pointer
    psrudo_sub_database['Offset_Itemset'] = list_offset_itemset
    psrudo_sub_database['Offset_Element'] = list_offset_element
    return psrudo_sub_database
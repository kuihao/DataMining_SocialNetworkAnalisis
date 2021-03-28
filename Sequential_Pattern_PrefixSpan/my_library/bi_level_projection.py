'''
# Optimization 1: Bi-level projection
功能：計算次層 Frequent Pattern
---
Prefix 原始概念是先用 Length-k (level k) 的 Prefix 對 Database 產生所有 Sub Database (Projected Database) 之後遞迴，
進入次層遞迴才算出 Length-k+1 (level k+1) Prefix，並再度分切出 Sub Sub Database，切完才檢查是否有 Frequent Pattern 
但隨著遞迴層數增加，許多 Sub Database 根本不會再有 Frequent Pattern，等同於許多分切 Sub Database 其實是在做白工
---
因此 Bi-level projection 是在 level k 時就預先算出 level k+1 的所有 Frequent Pattern，
只針對存在 Frequent Pattern 進行 Sub Database 的分切工作
實作方式是建一個動態三角形陣列統計 sup，設定兩個指針 (此為 front & rear)，
對資料庫掃描兩次 (兩層迴圈) 即可將表填完
---
效果：(論文說:也許能) 降低 Projected Database 的數量 (Number)、大小 (Size)
---
* 此方法於第二次修正時棄絕，因為論文本身無詳細描述此最佳化的使用時機及實作方法
  僅敘述使用三角陣列儲存及掃瞄 Database 2 次可完成所有統計，經嘗試仍難以理解其實作方式
'''
# [database] dict{ cid:dict{ timecode:list[item] }}
# [prefix_sequence] list[Seq.Pat.(prefix), last timecode of prefix]
# [length1_patterns] dict{ this level prefix: sup}
# [pseudo_database] dict{ this level prefix: dict{'cid': , 'offset_timecode': ,'offset_item': } }
def bi_level_projection(database, pseudo_database, length1_pattern, min_sup): 
    # 同樣方法走訪原 database，但走訪表改成 prefix 字 構成
    # 統計 postfix support 數，同時能知道是否在同個 set 並直接 "得出新 seq." 
    # (不使用第二步黏出而是走訪第二次來確認新的 seq)
    #  if 不同 timecode then (1)切子表 (2) 不同 set 之 postfix table
    #  if 同 timecode then  (1)切子表 (2) 同 set 之 postfix table
    #      if postfix table 未達 support 就砍掉它
    # 把 prefix 與 postfix 黏合放進 seq table
    # 最後生出 (1) prefix的子表 及 (2) seq table
    return 
    '''
    # (1) Make Triangular Matrix
    Length2_SeqPat_Triangle = {}
    Length2_SeqPat_Triangle['U'] = {}
    prefix_list = list(map(toInt ,length1_pattern['length-1 pattern']))
    prefix_list = list(map(str, prefix_list))
    prefix_dict = toDict(prefix_list)
    del prefix_list
    
    # (2) Scan Database and fill the Triangular Matrix
    for rowindex_f in range(len(database['Seq_ItemSet'])): 
        for itemset_f in range(len(database['Seq_ItemSet'][rowindex_f])):
            tmp_list1 = sorted(list(database['Seq_ItemSet'][rowindex_f][itemset_f]))
            list_itemset_f =  tmp_list1
            #list_itemset_f =  list(map(int, tmp_list1))
            for element_f in range(len(list_itemset_f)):
                fornt_ptr = list_itemset_f[element_f]
                for rowindex_r in range(rowindex_f, len(database['Seq_ItemSet'])): 
                    for itemset_r in range(itemset_f, len(database['Seq_ItemSet'][rowindex_r])):
                        tmp_list2 = sorted(list(database['Seq_ItemSet'][rowindex_r][itemset_r]))
                        list_itemset_r =  tmp_list2
                        #list_itemset_r =  list(map(int, tmp_list2))
                        for element_r in range(element_f+1, len(list_itemset_r)):
                            rear_ptr = list_itemset_r[element_r]                                                       
                            # 存在於 Prefix 字典
                            if prefix_dict.get(fornt_ptr)!=None and prefix_dict.get(rear_ptr)!=None:
                                # 兩個 items 位於相同 CID 之集合之中
                                if rowindex_f == rowindex_r and itemset_f == itemset_r:
                                    temp_union = {fornt_ptr}.union({rear_ptr})
                                    temp_key = tuple(temp_union)   
                                    if Length2_SeqPat_Triangle['U'].get(temp_key) != None:
                                        Length2_SeqPat_Triangle['U'][temp_key] += 1
                                    else: Length2_SeqPat_Triangle['U'][temp_key] = 1 
                                # 兩個 items 位於不同集合之中              
                                else:    
                                    # 若 fornt_ptr 存在於三角字典
                                    if Length2_SeqPat_Triangle.get(fornt_ptr) != None:
                                        # 若 rear_ptr 存在於三角字典
                                        if Length2_SeqPat_Triangle[fornt_ptr].get(rear_ptr) != None:
                                            # 位於不同集合卻是同一個商品
                                            if fornt_ptr == rear_ptr:
                                                if Length2_SeqPat_Triangle[fornt_ptr].get(fornt_ptr) != None:
                                                    Length2_SeqPat_Triangle[fornt_ptr][fornt_ptr] += 1
                                                else: Length2_SeqPat_Triangle[fornt_ptr][fornt_ptr] = 1
                                            # 位於不同集合且是不同商品
                                            else: Length2_SeqPat_Triangle[fornt_ptr][rear_ptr] += 1
                                        else:
                                            Length2_SeqPat_Triangle[fornt_ptr][rear_ptr] = 1
                                    else: 
                                        Length2_SeqPat_Triangle[fornt_ptr] = {}
                                        Length2_SeqPat_Triangle[fornt_ptr][rear_ptr] = 1
    '''
    # (3) Find Length-2 Sequence Pattern
    '''
    # 此方法是產生 DataFrame，但後來發現產生映射表會更有用
    L2_Sequence_Pattern_Table = pd.DataFrame(columns=['L2-SeqPat', 'sup'])
    tmp_list_SeqPat = []
    tmp_list_sup = []
    for key1 in Length2_SeqPat_Triangle:
        for key2 in Length2_SeqPat_Triangle[key1]:
            L2seq_sup = Length2_SeqPat_Triangle[key1][key2]
            if L2seq_sup >= min_sup:
                temp_list = []
                temp_list.append(key1)
                temp_list.append(key2)
                tmp_list_SeqPat.append(temp_list)
                tmp_list_sup.append(L2seq_sup)
                del temp_list
    L2_Sequence_Pattern_Table['L2-SeqPat'] = tmp_list_SeqPat
    L2_Sequence_Pattern_Table['sup'] = tmp_list_sup
    del tmp_list_SeqPat
    del tmp_list_sup

    return L2_Sequence_Pattern_Table
    '''
    '''
    L2_Sequence_Pattern_Table = {}
    tmp_list_union = []
    for key1 in Length2_SeqPat_Triangle:
        for key2 in Length2_SeqPat_Triangle[key1]:
            L2seq_sup = Length2_SeqPat_Triangle[key1][key2]
            if L2seq_sup >= min_sup:
                if key1 == 'U':
                    tmp_list_union.append(key2)
                else:
                    L2_Sequence_Pattern_Table[key1] = key2
    L2_Sequence_Pattern_Table['U'] = tmp_list_union
    
    return L2_Sequence_Pattern_Table
    '''
# --- little function --- #
def toSet(obj): return set({obj})
def toInt(obj): return list(obj)[0]
def toDict(obj):
    mydict = {}
    for i in obj:
        mydict[i] = 1
    return mydict


'''
    Step 1: Find length-1 sequential patterns
        (1) Scan database, count support, generate projection
        (2) generate frequential prefix pattern (length-1 pattern)
'''
if __name__ == '__main__': 
    import pseudo_projection as pp
else:
    try:
        import my_library.pseudo_projection as pp
    except: print('Import Error in Step1.py')
def find_length1_sequential_patterns(database, pseudo_database, min_sup, level):
    # Debug: 紀錄 Prefix 最大 support
    debug_max_support = 0

    # (1) Scan database, count support, generate projection
    # [Traversal]: 用來記錄該 CID 序列之 Prefix 是否已計數 
    Traversal = {}
    # [prefix_table]: record number of prefix, dtype: dict
    #                 [key]: prefix, [value]: support (prefix's count)
    prefix_table = {}
    # [new_pseudo_sub_database]: record projected database (sub database)
    #                            [key]: prefix, [value]: list of pseudo_sub_database 
    new_pseudo_sub_database = {}
    prefix = None
    # level = 0 表示遞迴在第一圈
    if not(level):
        for key_cid in database:
            # [ready_record] 表示是否要產生 last_prefix 的 pseudo_sub_database
            ready_record = False
            length_timecode = 0
            for key_timecode in database[key_cid]:
                length_timecode += 1
                # 若尚未走訪過此 item 其就是 prefix
                for item_i_idx in range(len(database[key_cid][key_timecode])):
                    item_i = database[key_cid][key_timecode][item_i_idx]
                    
                    # 若 ready_record 仍為 True，表示 Postfix 出現於後一個 timecode (itemset)
                    if ready_record:   
                        timecode_idx = list(database[key_cid].keys()).index(key_timecode)                 
                        new_pseudo_sub_database[prefix].append(pp.generate(key_cid, timecode_idx, item_i_idx, False))
                        ready_record = False
                    
                    # 若 Traversal 尚未紀錄此 item 為 prefix
                    if Traversal.get(item_i) == None:
                        prefix = item_i
                        Traversal[prefix] = 1
                        prefix_table[prefix] = 1
                        new_pseudo_sub_database[prefix] = []
                        ready_record = True
                    # 若 Traversal[prefix] == 0
                    elif not(Traversal[item_i]):
                        prefix = item_i
                        Traversal[prefix] = 1
                        prefix_table[prefix] += 1
                        ready_record = True
                    # else: 若 Traversal[prefix] == 1 表示此 CID 已有紀錄，故不作任何計數

                    # 若有紀錄 prefix，則接續紀錄 prefix 的 Projected Database
                    if ready_record and (item_i_idx+1) < len(database[key_cid][key_timecode]):
                        # 依序查看每個 element，因為是同個 set 因此不能跟自己重複
                        for item_j_idx in range(item_i_idx+1, len(database[key_cid][key_timecode])):                     
                            item_j = database[key_cid][key_timecode][item_j_idx]
                            if prefix != item_j:
                                timecode_idx = list(database[key_cid].keys()).index(key_timecode)
                                new_pseudo_sub_database[prefix].append(pp.generate(key_cid, timecode_idx, item_j_idx, True))
                                ready_record = False
                                break 
                    
                # 若 prefix 位在 CID 的最後一個 itemset 且 set 中只有 prefix 自己，
                # 表示 projected database 是空
                if ready_record and length_timecode == len(database[key_cid]):
                    new_pseudo_sub_database[prefix].append([])
                    ready_record = False
                #elif ready_record:
                #    print("*Debug: sth error happen! prefix table problem!")
            # 此 CID 序列已走訪結束，將 prefix traversal table 歸零，換下一筆 CID    
            Traversal = reset_traversal(Traversal)
        # print(new_pseudo_sub_database[2]) => [{'cid': 1976, 'offset_item': 1, 'offset_timecode': 88201}]
    else:
        # pseudo_database is a list
        for pseudo_sequence in pseudo_database:
            if type(pseudo_sequence) == type([]):continue

            # [ready_record] 表示是否要產生 last_prefix 的 pseudo_sub_database
            ready_record = False
            length_timecode = 0
            # 從 pseudo_database ptr 找出 cid
            key_cid = pseudo_sequence['cid']
            # 取得 database[key_cid].key() 之 list
            list_timecode = list(database[key_cid].keys())
            length_list_timecode = len(list_timecode)
            # 用來判定是否同 set 的變數之一
            first_loop = True
            # [timecode]: index
            for timecode in range(pseudo_sequence['offset_timecode'], length_list_timecode):
                key_timecode = list_timecode[timecode]
                # 若尚未走訪過此 item 其就是 prefix
                for item_i_idx in range(pseudo_sequence['offset_item'] ,len(database[key_cid][key_timecode])):
                    item_i = database[key_cid][key_timecode][item_i_idx]
                    # 若 item_i 是在第一個字就將它變成字串型別
                    if first_loop: item_i = str(item_i)

                    # 若 ready_record 仍為 True，表示 Postfix 出現於後一個 timecode (itemset)
                    if ready_record:   
                        timecode_idx = list(database[key_cid].keys()).index(key_timecode)                 
                        new_pseudo_sub_database[prefix].append(pp.generate(key_cid, timecode_idx, item_i_idx, False))
                        ready_record = False
                    
                    # 若 Traversal 尚未紀錄此 item 為 prefix
                    if Traversal.get(item_i) == None: 
                        prefix = item_i
                        Traversal[prefix] = 1
                        prefix_table[prefix] = 1
                        new_pseudo_sub_database[prefix] = []
                        ready_record = True
                    # 若 Traversal[prefix] == 0
                    elif not(Traversal[item_i]):     
                        prefix = item_i
                        Traversal[prefix] = 1
                        prefix_table[prefix] += 1
                        ready_record = True
                    # else: 若 Traversal[prefix] == 1 表示此 CID 已有紀錄，故不作任何計數

                    # 若有紀錄 prefix，則接續紀錄 prefix 的 Projected Database
                    if ready_record:
                        # 依序查看每個 element，因為是同個 set 因此不能跟自己重複
                        for item_j_idx in range(item_i_idx+1, len(database[key_cid][key_timecode])):                     
                            item_j = database[key_cid][key_timecode][item_j_idx]
                            if int(prefix) != item_j:
                                timecode_idx = list(database[key_cid].keys()).index(key_timecode)
                                new_pseudo_sub_database[prefix].append(pp.generate(key_cid, timecode_idx, item_j_idx, True))
                                ready_record = False
                                break 
                    
                    
                # 若 prefix 位在 CID 的最後一個 itemset 且 set 中只有 prefix 自己，
                # 表示 projected database 是空
                if ready_record and (timecode+1) == length_list_timecode:
                    new_pseudo_sub_database[prefix].append([]) #[!!!]
                    ready_record = False
                #elif ready_record:
                #    print("*Debug: sth error happen! prefix table problem!")
                first_loop = False
            # 此 CID 序列已走訪結束，將 prefix traversal table 歸零，換下一筆 CID    
            Traversal = reset_traversal(Traversal)

    # (2) generate frequential prefix pattern (length-1 pattern)
    # 依照 Minimum Support 去除不合 pattern 規則的 Items
    not_frequent = []
    for prefix in prefix_table:
        support = prefix_table[prefix]
        if support < min_sup:
            not_frequent.append(prefix)
        if debug_max_support < support: debug_max_support = support
    # 將未達 min_sup 的 prefix 刪除
    for item in not_frequent:
        del prefix_table[item]
        del new_pseudo_sub_database[item]
    

    #print(debug_max_support)
    payload = [prefix_table, new_pseudo_sub_database]
    return payload

def reset_traversal(traversal):
    for key in traversal:
        traversal[key] = 0
    return traversal

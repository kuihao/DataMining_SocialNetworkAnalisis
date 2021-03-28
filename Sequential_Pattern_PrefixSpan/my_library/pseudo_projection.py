'''
# Optimization 2: Pseudo-Projection
    功能：產生指標結構
    ---
    Prefix 原始方法是為每個 Sub Projected Database 產生新的表 (儲存空間)，
    但使用遞迴產生表格對記憶體有不小的負擔
    ---
    每張 Sub Projected Database 只記錄 Pointer (指向原本 Database 的 Sequence) 跟 Offset (Postfix 的位置)
    效果：節省主記憶體空間
'''
def generate(cid, offset_timecode, offset_item, sameset):
    pseudo_sub_database = {}
    pseudo_sub_database['cid'] = cid
    # [dict.keys()].index()
    pseudo_sub_database['offset_timecode'] = offset_timecode
    # index
    pseudo_sub_database['offset_item'] = offset_item
    # if first timecode's element in same set: bool
    pseudo_sub_database['sameset'] = sameset
    return pseudo_sub_database

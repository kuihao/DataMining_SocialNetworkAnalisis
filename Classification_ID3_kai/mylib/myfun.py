'''
'''
import pandas as pd

'''
關閉 Pandas 存取警告
"A value is trying to be set on a copy of a slice from a DataFrame"
'''
def close_pandas_warning(bool_close=False):
    if bool_close:
        pd.set_option('mode.chained_assignment', None)

'''
將 dataset 的 Ground Truth 部分切離
'''
def split_dataset_to_xy(dataset:'DataFrame') -> ('dataset_x', 'dataset_y'):
    dataset_y = pd.DataFrame(dataset.MemberCard)
    dataset.drop( 'MemberCard', axis=1, inplace=True )
    dataset_x = dataset
    return dataset_x, dataset_y
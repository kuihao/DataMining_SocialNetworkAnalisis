'''
ID3: Iterative Dichotomiser 3 (迭代二元樹第3代)
    Algorithm:  1. Selects the attribute which has the smallest entropy 
                   (or largest information gain) value
                2. Decision Tree 就是依大數法則分類到最後給一個唯一確定的答案
                   似乎沒有機率分布的可能性，無法動態調整結構
    Keyword 1: Dichotomiser (二分法)
    Keyword 2: DCT (Decision Tree Classifier)
    Keyword 3: Majority voting (多數決)
'''
import math
from random import shuffle
import pandas as pd
from copy import deepcopy
class Node():
    def __init__(self):
        return


'''
Construct ID3 DCT
    # DCT: Decision Tree Classifier
    # Let original set S as the root node
    # 判斷型別，if type == 'float' 就呼叫切割連續
'''
class ID3_kai():
    #====== Initialization ======#
    def __init__(self, LabelProperties:dict, Limit_NodeClass:int):
        self.LabelProperties = LabelProperties # 離散 = 0, 連續 = 1
        self.Limit_NodeClass = Limit_NodeClass
        self.DecisionTree = {} # dict 作為樹的結構，這是樹根 Tree Root
        self.TrainingSet_x = None
        self.TrainingSet_y = None
        self.ValidationSet_x = None
        self.ValidationSet_y = None

    #====== Public Method ======#
    '''
    [fit] 訓練 Model 輸入訓練資料: x 特徵, y 標籤
    '''
    def fit(self, train_x:'DataFrame', train_y:'DataFrame') -> ('TreeAsDict'):
        self.TrainingSet_x = train_x
        self.TrainingSet_y = train_y
        # [Temp_DecisionTree] 這是 Tree Node
        Temp_DecisionTree = {}
        # 紀錄 Attribute 是否已做為類別
        Attributes = deepcopy(self.__init_attributes_record(train_x))
        # 建立決策樹
        self.DecisionTree = self.__construct_DT(train_x, train_y, Attributes, Temp_DecisionTree)
        return
    
    # [accuracy] 分類正確 / 總樣本數
    def accuracy(self, validation_set_x = None, validation_set_y = None):
        # 若不預設 validation_set_xy 則改計算「訓練資料」的正確率 
        if type(validation_set_x) == type(None) and type(validation_set_y) == type(None):
            validation_set_x = self.TrainingSet_x
            validation_set_y = self.TrainingSet_y
        # 若「只有給特徵資料」、無標籤資料，表示這是實務盲測，無法計算正確率
        elif type(validation_set_y) == type(None):
            print("No ground truths (labels) can't calculate accuracy!")
            return
        # 只給 validation_set_y 的值，表示輸入錯誤
        elif type(validation_set_x) == type(None) and type(validation_set_y) != type(None):
            print("Lack of arguments.")
            return
        # 若 validation_set_xy 都有值表示計算「驗證資料」的正確率 
        else:
            self.ValidationSet_x = validation_set_x
            self.ValidationSet_y = validation_set_y
        result = self.predict(validation_set_x, validation_set_y)
        number_samples = len(result)
        correct = 0
        for idx in range(number_samples):
            if result[idx] == validation_set_y.MemberCard[idx]:
                correct +=1 
        return round( float(correct)/float(number_samples), 4)
    
    # [predict] 預測分類結果，其實就是走訪決策樹
    def predict(self, validation_set_x = None, validation_set_y = None):
        # 若不預設 validation_set_xy 則改預測「訓練資料」 
        if type(validation_set_x) == type(None) and type(validation_set_y) == type(None):
            validation_set_x = self.TrainingSet_x
            validation_set_y = self.TrainingSet_y
        # 若「只有給特徵資料」、無標籤資料，表示這是實務盲測，依舊給予預測，但不存為 Validation set
        elif type(validation_set_y) == type(None): validation_set_x = validation_set_x
        # 只給 validation_set_y 的值，表示輸入錯誤
        elif type(validation_set_x) == type(None) and type(validation_set_y) != type(None):
            print("Missing some arguments!")
            return
        # 若 validation_set_xy 都有值表示計算「驗證資料」的正確率
        else:
            self.ValidationSet_x = validation_set_x
            self.ValidationSet_y = validation_set_y
        
        Result_Table = []
        for idx in range(len(validation_set_x)):
            attributes = {  'MaritalStatus':validation_set_x.loc[idx, 'MaritalStatus'],
                            'Num_ChildrenAtHome':validation_set_x.loc[idx, 'Num_ChildrenAtHome'],
                            'Age':validation_set_x.loc[idx, 'Age'],
                            'YearIncome':validation_set_x.loc[idx, 'YearIncome']}
            DCTree = self.DecisionTree
            # [__traverse_DT] 決策樹走訪
            result = self.__traverse_DT(DCTree, attributes, self.TrainingSet_x, self.TrainingSet_y)
            Result_Table.append(result)
        return Result_Table

    # (給出各列別的機率) ID3 和 C4.5 似乎沒有此功能
    #def predict_proba(self): return
    
    #====== Private Method ======#
    '''
    [__construct_DT()] 遞迴建樹 
    '''
    def __construct_DT(self, train_x, train_y, AttributesRecord, DecisionTree:'dict') -> ('TreeAsDict'):
        # --- 遞迴終止條件 Stop Partitioning --- #
        '''
        [Stop-event 1] 如果 Samples 沒了，表示這是 Null Leaf
                       依訓練資料無法直接判定這種類別的結果，
                       可以選擇返回後剪枝，或是返回後依多數決賦值
        '''
        if train_y.empty: 
            return None
        '''
        [Stop-event 2] 當所有 class 都相同，表示已經 (提早) 分完了，值接回傳 class
        '''
        # [classes_unique_statics] 紀錄目前有幾種 class 及 其數量，pd.Series, 自動降冪排序, index:分群項目 values:數量                         
        classes_unique_statics = train_y.value_counts()
        # [list_classes_unique_name] 相異 classes 的名稱
        # [classes_unique_statics.index] Int64Index([3], dtype='int64') 需要轉型成 list
        # 不知為何有可能變成 <class 'pandas.core.indexes.multi.MultiIndex'>
        list_classes_unique_name = list(set(classes_unique_statics.index))
        if len(list_classes_unique_name) == 1: 
            leaf = list_classes_unique_name[0]
            if type(leaf) == type( (2021,) ):
                leaf = list(list_classes_unique_name[0])[0]
                return leaf
            else:
                return leaf
        '''
        [Stop event 3] 若 Attribute 都分完了，則依剩餘 class 依「多數決」決定結果 
                       (也許能改成以機率判定？)
                       # [not(AttributesRecord)] 表示 list 為空
        '''
        if not(AttributesRecord): 
            return self.__majority_voting(classes_unique_statics)
        
        '''
        [__find_best_classifier] 找出最佳分類屬性
            回傳 payload = [best_classifier:str, splitvalue:int, remove_this_attribute:bool]
        '''
        payload_best_classifier = self.__find_best_classifier(train_x, train_y, AttributesRecord)
        # 拆封包
        best_classifier = payload_best_classifier[0]
        splitvalue = payload_best_classifier[1]
        remove_this_attribute = payload_best_classifier[2]
        # AttributesRecord 刪去此 best_classifier
        if remove_this_attribute:
            AttributesRecord.remove(best_classifier)

        '''
        [建立新節點] 將 best_classifier 放入 DecisionTree
        '''
        # [If 離散資料] 用這些方法
        if not(self.LabelProperties[best_classifier]):
            # [best_classifier_unique_statics] 紀錄目前 best_classifier 有幾種 partition 及其數量，pd.Series, 自動降冪排序, index:分群項目 values:數量 
            best_classifier_unique_statics = train_x[best_classifier].value_counts()
            # [list_partition_unique_name] best_classifier 內部分群 (partition) 的名稱
            list_partition_unique_name = list(best_classifier_unique_statics.index)
            # 初始化新的子節點
            DecisionTree[best_classifier] = {}
            for partition in list_partition_unique_name:
                ## 初始化形成子樹的所需參數
                DecisionTree[best_classifier][partition] = {}
                ## 依據現在的分類法選出子節點的 dataset x y 
                classifier_filter = (train_x[best_classifier] == partition)
                ## AttributesRecord 需要 copy，每層遞迴要用獨立的 AttributesRecord
                AttributesRecord_for_ChildNode = deepcopy(AttributesRecord)
                ## 需要一個 Temp tree node 放進去
                Temp_DecisionTree = {}
                
                # [if-esle] 此處是限制樹高，若子樹的 dataset samples 數量少於 Limit_NodeClass (限制數量)，則停止生長
                # 然而，這個方法似乎沒有用
                if len(train_y[classifier_filter].MemberCard) < self.Limit_NodeClass:
                    DecisionTree[best_classifier][partition] = self.__majority_voting(classes_unique_statics)
                    continue
                else:
                    DecisionTree[best_classifier][partition] = self.__construct_DT( train_x[classifier_filter],
                                                                                    train_y[classifier_filter], 
                                                                                    AttributesRecord_for_ChildNode, 
                                                                                    Temp_DecisionTree)
                # [!!! debug: 若回傳葉子型態是 tuple 表示葉子生成發生問題]
                if type(DecisionTree[best_classifier][partition]) == type( (1,) ):print("Tuple show up!")
                # [] 若葉子已分完，則依當前分類方式中最多數的 Class 作為該節點的結果
                if DecisionTree[best_classifier][partition] == None:
                    DecisionTree[best_classifier][partition] = self.__majority_voting(classes_unique_statics)      
        # [else if 連續資料] 用以下演算法:
        else:
            '''
            [連續資料二分樹--演算法思考]
                # partition 只分為二，變成左右子樹
                # DecisionTree[best_classifier][splitvalue]['Bigger&Equal'] = self.__construct_DT(...)
                # DecisionTree[best_classifier][splitvalue]['Smaller'] = self.__construct_DT(...)
                # |->  self.__construct_DT( train_x[splitvalue_?_filter], train_y[splitvalue_?_filter],
                #                        AttributesRecord_for_ChildNode, Temp_DecisionTree)
                #       |-> splitvalue_BET_filter = (train_x[best_classifier] >= splitvalue)
                #       |-> splitvalue_ST_filter = (train_x[best_classifier] < splitvalue)
                # Return 是葉子會發生什麼事情?
            '''
            ## 初始化形成子樹的所需參數 ##
            DecisionTree[best_classifier] = {}
            DecisionTree[best_classifier][splitvalue] = {'Bigger&Equal':{}, 'Smaller':{}}
            # BET: Bigger and Equal than, ST: Smaller than
            # 每層遞迴要用獨立的 AttributesRecord
            AttributesRecord_for_ChildNode_BET = deepcopy(AttributesRecord)
            AttributesRecord_for_ChildNode_ST = deepcopy(AttributesRecord)
            # 子樹是新生的節點 Temp tree node
            Temp_DecisionTree_BET = {}
            Temp_DecisionTree_ST = {}
            # 切割資料子集需要用到
            splitvalue_BET_filter = (train_x[best_classifier] >= splitvalue)
            splitvalue_ST_filter = (train_x[best_classifier] < splitvalue)
            
            ## 生出左右子樹 ##
            # [if-esle] 此處是限制樹高，若子樹的 dataset samples 數量少於 Limit_NodeClass (限制數量)，則停止生長
            # 然而，這個方法似乎沒有用
            if len(train_y[splitvalue_BET_filter].MemberCard) < self.Limit_NodeClass:
                DecisionTree[best_classifier][splitvalue]['Bigger&Equal'] = self.__majority_voting(classes_unique_statics)
            else:
                DecisionTree[best_classifier][splitvalue]['Bigger&Equal'] = self.__construct_DT( train_x[splitvalue_BET_filter], train_y[splitvalue_BET_filter],
                                                                                                AttributesRecord_for_ChildNode_BET, Temp_DecisionTree_BET)
            if len(train_y[splitvalue_ST_filter].MemberCard) < self.Limit_NodeClass:
                DecisionTree[best_classifier][splitvalue]['Smaller'] = self.__majority_voting(classes_unique_statics)
            else:    
                DecisionTree[best_classifier][splitvalue]['Smaller'] = self.__construct_DT( train_x[splitvalue_ST_filter], train_y[splitvalue_ST_filter],
                                                                                            AttributesRecord_for_ChildNode_ST, Temp_DecisionTree_ST)
            
            # 若該樹的葉子已分完 (沒有 class)，則依當前分類方式中最多數的 Class 作為該節點的結果
            if DecisionTree[best_classifier][splitvalue]['Bigger&Equal'] == None:
                DecisionTree[best_classifier][splitvalue]['Bigger&Equal'] = self.__majority_voting(classes_unique_statics)
            if DecisionTree[best_classifier][splitvalue]['Smaller'] == None:
                DecisionTree[best_classifier][splitvalue]['Smaller'] = self.__majority_voting(classes_unique_statics)
        return DecisionTree

    
    # 初始化分類紀錄表: 所有 Attributes 皆尚未用來分類
    def __init_attributes_record(self, train_x:'DataFrame') -> ('list'):
        tmp_list = []
        for col in list(train_x.columns):
            tmp_list.append(col)
        return tmp_list
    
    # Find the best classifier 找出最佳分類屬性 (利用最小 Entropy 或 最大 Information Gain)
    def __find_best_classifier(self, train_x, train_y, AttributesRecord:list) -> ('payload_best_classifier:list'):
        # [dict_conditonal_entropys] = {attribute: weight_entropy} 
        #   紀錄所有 Attribute 算出的 entropy
        dict_conditonal_entropys = {}
        # [best_classifier] 最佳的分類屬性 (特徵)
        best_classifier = None
        # [連續資料專用] 表示連續資料的切割點
        splitvalue = None
        dict_splitvalues = {}
        # [連續資料專用] False 表示不從 AttributeRecord 刪除此 attribute
        #               因為連續型資料每一輪只會切成左右子樹，可能還有非常多輪要切割
        remove_this_attribute = False

        # 分別對每個 attrubute 計算 weight_entropy
        for attrubute in AttributesRecord:
            # self.LabelProperties[attrubute] = 0 為「離散資料」
            if not(self.LabelProperties[attrubute]):    
                # [__conditional_entropy] 計算 weight_entropy, Entropy(S|A) = H(S|A)
                weight_entropy = self.__conditional_entropy(train_x[attrubute], train_y)
                dict_conditonal_entropys[attrubute] = weight_entropy
            # self.LabelProperties[attrubute] = 1 為「連續資料」
            else:
                '''
                [演算法思考] 如何切分連續資料、其Entropy算法 
                    # 0. 目標結構：dict{ 'Age':{ 'splitvalue':{ 'Bigger&Equal':{}, 'Smaller':{} } } }
                    # 1. 取得 train['Age']
                    # 2. 取 set 再取 list 達成排序目的
                    # 3-1. list 取前 n-1 筆，每筆與下一個 idx 算 mean 作為切割點 
                    # 3-2. 條件商 = Sum( 被切割佔比 * Entropy( 四種 class in 被切割 ) )
                    #            = number(Bigger&Equal) / number(train['Age']) * Entropy(切割後的train_y)
                    #            + number(Smaller) / number(train['Age']) * Entropy(切割後的train_y)
                    # 3-3. 比較 n-1 筆條件商，找到連續資料中的最小條件商
                    # *3-4 若 list 只剩兩筆，則須回傳 stop_watch_this_class_next_time
                    # *3-5 若 length(list) == 1，表示無須切割，但仍將其視為分切值後續再處理，此也要回傳 stop_watch_this_class_next_time
                    # (可以寫函式直接給出連續資料的「最小條件商」「最佳切割點」)
                    # 4. 比較所有 attrubute 誰的條件商最小，若是連續資料為最佳分類器，則也需要回傳「連續的切分值」
                    # 5. 回傳: best_classifier 可改成 payload_best_classifier[best_classifier, splitvalue, stop_watch_this_class_next_time]
                '''
                # {1, 2} 對連續 Attribute 中不同種類的 partitions 作排序
                sorted_unique_partitions =  list(set(train_x[attrubute]))
                # {3-4, 3-5}
                if len(sorted_unique_partitions) <= 2:
                    remove_this_attribute = True
                # {3-4}
                if len(sorted_unique_partitions) == 1:
                    splitvalue = sorted_unique_partitions[0]
                    weight_entropy = self.__conditional_entropy(train_x[attrubute], train_y)
                    dict_conditonal_entropys[attrubute] = weight_entropy
                # {3-1~3-3}
                else:
                    splitvalue, weight_entropy = self.__get_best_splitvalue_entropy(train_x, train_y, attrubute, sorted_unique_partitions)
                    dict_conditonal_entropys[attrubute] = weight_entropy
                    dict_splitvalues[attrubute] = splitvalue
        # {4}
        best_classifier = self.__get_minimum_entropy_classifier(dict_conditonal_entropys)
        # 若最後決定的 best_classifier 是離散資料，則出去後仍要把 Attribute 從走訪記錄中移除
        if not(self.LabelProperties[best_classifier]):
            remove_this_attribute = True
            splitvalue = None
        else:
            splitvalue = dict_splitvalues[best_classifier]
        
        # {5} 回傳值需要打包，因為離散屬性和連續屬性的回傳個數不同
        payload_best_classifier = [best_classifier, splitvalue, remove_this_attribute]
        return payload_best_classifier
    
    # 決策樹走訪 #key = list(DCT.keys())[0]
    def __traverse_DT(self, DecisionTree, attributes, train_x, train_y):
        # 若 "DecisionTree" 不是整數型態，表示仍是 Tree 而不是葉子
        if type(DecisionTree)!=type(123):
            # 字典 key 解碼: 
            # list(DecisionTree.keys())[0]: 逆向直接取得字典的 key 也就是 Attribute
            key = list(DecisionTree.keys())[0]
            # attributes[key]: 用 key (dataset 的 Attribute) 從 attributes (
            # sample 的 attributes 字典，取得 sample 對應 attribute 的答案做為第二把鑰匙)
            next_key = attributes[key]

            # 試著往下走訪
            try:
                # 若 key 所象徵的 Attribute 是離散資料，用鑰匙連開兩層就往下走
                if not(self.LabelProperties[key]):
                    # 分切子資料集
                    classifier_filter = (train_x[key] == next_key)
                    leaf = self.__traverse_DT(  DecisionTree[key][next_key], 
                                                attributes, 
                                                train_x[classifier_filter], train_y[classifier_filter])
                # 若 key 所象徵的 Attribute 是連續資料，兩把鑰匙還不夠，還要回答比大小謎語! (開玩笑的)
                else:
                    # DecisionTree[key] => splitvalue
                    #   DecisionTree[key][splitvalue] = { 'Bigger&Equal':{}, 'Smaller':{}  }
                    key_splitvalue = list(DecisionTree[key].keys())[0]
                    # next_key 就是 sample 的 value，若 value 大於等於 key_splitvalue，往 Bigger&Equal
                    if next_key >= key_splitvalue:
                        # 分切子資料集
                        classifier_filter = (train_x[key] >= next_key)
                        leaf = self.__traverse_DT(  DecisionTree[key][key_splitvalue]['Bigger&Equal'], 
                                                    attributes, 
                                                    train_x[classifier_filter], train_y[classifier_filter])
                    # 若 value 小於 key_splitvalue 則往 Smaller
                    else:
                        # 分切子資料集
                        classifier_filter = (train_x[key] < next_key)
                        leaf = self.__traverse_DT(  DecisionTree[key][key_splitvalue]['Smaller'], 
                                                    attributes, 
                                                    train_x[classifier_filter], train_y[classifier_filter])

            ## 若測試時 Sample 於 Model 無路可走會出現 KeyError
            except KeyError:
                # 則此處是用簡單方式處理: 直接看上一層分類情況下，最多的 class 當作答案
                # 可優化之更嚴謹的方法: 將此分類下的其他子樹都走訪一次，統計回傳的 class 結果，選出現最大者
                classes_unique_statics = train_y.value_counts()
                return self.__majority_voting(classes_unique_statics)
            # 若發生意想不到的意外錯誤就判定為「無法預測」
            except:
                print("Traverse error!!")
                return -1
        # [Basic condition] 若 DecisionTree 是整數型態，表示其實是葉子
        else:
            leaf = DecisionTree
            return leaf
        return leaf

    '''
    # entropy = H(S) = info.(S)
    # p(Class C): Proportion of |C| to |S|
    # Where H(S) = 0 means perfectly classified 
    #              (i.e. all elements in S are of the same class)
    '''
    def __entropy(self, train_y):
        Entropy_dataset = 0
        number_dataset = len(train_y.index)
        for number_class in list(train_y.MemberCard.value_counts()):
            proportion = number_class/number_dataset
            partial_entropy = (-1)*proportion*(math.log(proportion))
            Entropy_dataset += partial_entropy
        return Entropy_dataset
    
    '''
    # condition_entropy = H(S|A) = info._A(S)
    '''
    def __conditional_entropy(self, train_x_attribute:'DataFrane', train_y:'DataFrane'):
        Weighted_Entropy = 0
        # [attribute_unique_statics] 紀錄目前 best_classifier 有幾種 partition 及其數量，pd.Series, 自動降冪排序, index:分群項目 values:數量 
        attribute_unique_statics = train_x_attribute.value_counts()
        # [number_partitions] attribute 內部分群的數量 
        number_partitions = len(attribute_unique_statics)
        # [list_partitions_unique_name] attribute 內部分群的名稱
        list_partitions_unique_name = list(attribute_unique_statics.index)
        # [list_partitions_unique_count] attribute 內部分群的數量
        list_partitions_unique_count = list(attribute_unique_statics.index)
        for idx in range(number_partitions):
            number_single_partition = list_partitions_unique_count[idx]
            proportion_single_partition = number_single_partition/number_partitions
            filter_partition = train_x_attribute.isin([list_partitions_unique_name[idx]])
            Weighted_Entropy += proportion_single_partition*self.__entropy( pd.DataFrame(train_y[filter_partition]) )
        return Weighted_Entropy

    '''
    [Information Gain] 其實 C4.5 才需要用到，若不計算 Gain Ratio 則派不上用場；算法：IG(A) = H(S) - H(S|A)
    '''
    # def __information_gain(self, entropy_dataset, conditional_entropy): return entropy_dataset-conditional_entropy

    '''
    [__minimum_entropy()] 找出最小 conditonal entropy，並回傳 KEY
    '''
    def __get_minimum_entropy_classifier(self, conditonal_entropys:dict) -> ('Minimum Entropy\'s Key'):
        mini_entropy = float('inf')
        best_classifier = None
        for key in conditonal_entropys:
            current_entropy = conditonal_entropys[key]
            if current_entropy < mini_entropy:
                mini_entropy = current_entropy
                best_classifier = key
        return best_classifier # 無須回傳 mini_entropy，用不到
    
    '''
    補強演算法1：計算連續資料的 Conditional Entropy
        # Automatically find the best split point (連續資料最佳切割點作為分群點)
        # Algorithm: Find the minimum conditional_entropy (information)
        # Keyword: Siblings (意旨同層的左或右節點)
            # {3-2.} 條件火商 = Sum( 被切割佔比 * Entropy( 四種 class in 被切割 ) )
            #               = number(Bigger&Equal) / number(train['Age']) * Entropy(切割後的train_y)
            #               + number(Smaller) / number(train['Age']) * Entropy(切割後的train_y)
            # conditional_entropy: 
            #           Sum( proportion * Entropy(train_y[partition_filter]) ), 
            #           number(Bigger&Equal), number(Smaller), number(train_x['Attribute'])
            #           partition_filter    
        # 回傳: weighted_entropy, list of partitions
    '''
    def __get_best_splitvalue_entropy(self, train_x, train_y, attribute:str, sorted_unique_partitions:list) -> ('Splitvalue', 'WeightedEntropy'):
        all_splitvalue_weighted_entropy = {}
        for idx in range(0, len(sorted_unique_partitions)-1):
            # splitvalue 是連續兩個值之間的平均值，並取整數
            splitvalue = int(round((sorted_unique_partitions[idx] + sorted_unique_partitions[idx+1])/2, 0))
            # 計算 Proportion 所需
            number_attribute = len(train_x[attribute])
            number_BET = len( train_x[attribute][lambda x: x >= splitvalue] ) # BET: Bigger & Equal than splitvalue
            number_ST = len( train_x[attribute][lambda x: x < splitvalue] ) # ST: Smaller than splitvalue
            # 計算 Conditional entropy 所需
            proportion_BET = number_BET/number_attribute
            proportion_ST = number_ST/number_attribute
            # 計算 Conditional entropy 所需
            partition_filter_BET = (train_x[attribute] >= splitvalue)
            partition_filter_ST = (train_x[attribute] < splitvalue)
            # 計算 Conditional entropy 所需
            entropy_BET = self.__entropy( pd.DataFrame( train_y[partition_filter_BET] ) )
            entropy_ST = self.__entropy( pd.DataFrame( train_y[partition_filter_ST] ) )
            # 此 splitvalue 的 conditional_entropy
            Weighted_Entropy = proportion_BET * entropy_BET + proportion_ST * entropy_ST
            all_splitvalue_weighted_entropy[splitvalue] = Weighted_Entropy
        BestSplitvalue = self.__get_minimum_entropy_classifier(all_splitvalue_weighted_entropy)
        return BestSplitvalue, all_splitvalue_weighted_entropy[BestSplitvalue]
    
    def __continuous_split_2(self, dataset, axis:'依第幾個attri切割', value:'劃分特徵的值', LorR = 'L'):
        returnDataset = []
        feature_vecture = []
        if LorR == 'L':
            for feature_vecture in dataset:
                if float(feature_vecture[axis]) < value:
                    returnDataset.append(feature_vecture)
        else:
            for feature_vecture in dataset:
                if float(feature_vecture[axis]) > value:
                    returnDataset.append(feature_vecture)
        return returnDataset

    '''
    補強演算法2-1：缺漏值分類預測、葉子存在多種class時的分類結果判定 
    [__majority_voting] 當出現 Null Leaf 時，以多數決方式決定 
    '''
    def __majority_voting(self, classes_unique_statics):
        # 過濾出最多的 Classes (可能有相同數量的 Class)
        majority_Series = classes_unique_statics[lambda x: x == max(classes_unique_statics)] # <class 'pandas.core.series.Series'>
        majority_list = list(majority_Series.index)
        # 因為都數量都相同只好隨機抽一個，用 shuffle() 會將 list 內部亂序編排
        shuffle(majority_list)
        leaf = majority_list[0]
        # Series.index 有可能試圖回傳 tuple
        if type(leaf) == type( (2021,) ):
            leaf = list(leaf)[0]
            return leaf
        else:
            return leaf
    '''
    補強演算法2-2 (未實作)：缺漏值分類判別，用深度走訪為每一層加上 Null Node
    思考：此狀況可以於測試模型時當作例外狀況解決
    '''
    def __add_MissingNode(self):
        # 設法 Bottom-up 加 node
        # 不論如何都要加上缺漏值項目
        # Top-down 想法是該層的 Missing-node 從 sibling nodes 往下走訪，走到 left 就回傳統計到的結果
        #                      最後一多數決決定此 Missing-node 應給予的分類結果
        #                      若為 50% 50% 則 Random 給一個答案
        # Bottom-up: 用深度優先，走到葉子 return 結果並"要乘上該 partion 的 Proportion"，至父節點統計結果；若子節點都走訪完，
        #            依統計結果生出一個 Missing-node附加統計結果，然後回傳目前蒐集的結果 (不會重複計算 missing node 的結果，
        #            因為這裡就是用大數分布來猜，不能重複計數這個猜的結果)
        # 回到 root 就 return 這棵樹 ID3-kai
        # 子節點 return [tree dict] 及  統計結果
        # 判斷是 root 只回傳 [tree dict]
        return
    

    







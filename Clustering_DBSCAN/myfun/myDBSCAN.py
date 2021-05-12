"""
DBSCAN: Density-Based Clustring
    * Ref: Ester, et al. “A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise” (KDD, 1996)
    * 本程式碼的變數命名有參考 Scikit-learn 及 wikipedia，但絕對沒有抄襲，全手刻！
        * 變數命名參考自 Scikit-learn: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html
"""
import numpy as np
"""[演算法定義與說明]：
    * Eps-neighbourhood: A range of points 某點的勢力範圍 (半徑需為 Eps)
        * 顯然論文將 Range 稱為 Neighbourhood (鄰居)
    * Eps: 代號為 Epsilon，意指 Neighbourhood 的最大半徑 (即 Range 的最大半徑限制) 
    * MinPts: Minimum number of points in Eps-neighbourhood (滿足 Eps 的 Neighbourhood)，
              (即 range 中 points 的最低數量限制)
              (或說: 形成高密度區域所需要的最少點數)
    * Density: 距離 Eps 中，滿足 MinPts 的範圍，稱為 Density (neighbourhood) (高密度區域)
    * NEps(p): 即 Neighbourhood-(with Eps)-Points，對 p 而言，Eps-neighbourhood 中所有點 (樣本) 所構成的集合 (包含 p)
        * For any point q，滿足 dist(p, q) <= Eps
        * Core point (核心點): 若 |NEps(p)| >= MinPts，則 p 為 Core point，意即 p 為中心的範圍內的近鄰居密度很高，p 住在小鎮中心
        * Border point (邊緣點, 又有論文稱為 Expend_point): 若 |NEps(p')| < MinPts，則 p' is Border point，意即 p' 住在小鎮邊緣，他的近鄰居密度不高
    * Directly density-reachable: (1 跨度)
                                1. 若 point q 屬於 NEps(p)
                                2. p 是 Core point ( |NEps(p)| >= MinPts )
                                則稱 q 是 p 的 directly density-reachable，意即 q 是 p 的近鄰居
                                * 示意：p -> q
    * Density-reachable: (至少2跨度) if q is density-reachable to p, 則存在一個 point m 屬於 Density-NEps(p) ∩ Density-NEps(q)
                                或說 m is p's directly density-reachable, 且 m is also q's directly density-reachable.
                                * "至少"：所有核心樣本相連稱為存在一條 Path，則 p -> m 之間的 Path 可以存在 1 個以上的跨度
                                * 示意：p -> m -> q
    * Density-connected: (至少4跨度) if p is density-connected to q, 
                                且 n = p's density-reachable (2跨度),
                                   n = q's density-reachable (2跨度),
                                即存在 point n 同時屬於 p 與 q 的 density-reachable
                                使得 p 可以間接認識 n 再間接認識 q
                                * Connection: 連結性，定義連結性是為了使兩樣本之間存在對稱性
                                * "至少"：p -> m1 與 m2 -> q 之間可存在多跨度的 Path
                                * 示意：p -> m1 -> n -> m2 -> q
    * Cluster (群): 由 Density-connected points 所構成的最大範圍
                    (Cluster is defined as a maximal set of density-connected points)
                    * Facebook 說六跨度能認識任何人，意指 6 跨度則大家都在同一個群？
    * 性質:
        1. 一個群 (聚類) 裡的任意兩個樣本 (點) 都是互相連結的 (has a connection, not mean Density-connected)
        2. 如果一個樣本 (點) p 是由一個在群 (聚類) 裡的點 q 可達的，那麼 p 也在 q 所屬的群 (聚類) 裡
    ------
    * Algorithm:
        * Arbitrary select a point p
        * Retrieve all points density-reachable from p w.r.t. Eps and MinPts .
        * If p is a core point, a cluster is formed.
        * If p is a border point, no points are densityreachable from p and DBSCAN visits the next point of the database.
        * Continue the process until all of the points have been processed.
        ** Key: 只有 Core-point 有能力把別人的群改成自己的群"""
"""[My DBSCAN 變數、方法說明]:
    * self.eps: 論文中的 Eps
    * self.min_samples: 論文中的 MinPts
    * self.core_sample_indices_: list 結構，存放所有 Core point 於 database 的 index
    * self.labels_: list 結構，存放所有 samples (points) 對應被分類到的群 (聚類)，
                    以 int 型態表示，-1 為雜訊、0 為尚未分群、other positive integer 為分群
    * [method] regionQuery(P, eps): 回傳論文中的 NEps(p)，rtype: list
                                    為了讓程式碼易讀，定義 NEps(p) 不包含 P，
                                    僅需使判斷時的 MinPts -1 即可，不影響演算法正確性
    * NeighborEpsPts: 論文中的 NEps(p)
    * 兩點距離以「歐基里德距離」進行計算
    """

class DBSCAN:
    '''# ====== Initialization ====== #'''
    def __init__(self, eps = 0.5, min_samples = 5):
        self.eps = eps
        self.min_samples = min_samples
        self.database = None
        self.core_sample_indices_ = None
        '''# <class 'numpy.ndarray'>
            # ndarray of shape (n_core_samples,)
            # Indices of core samples.'''
        self.labels_ = None
        '''# <class 'numpy.ndarray'>
            # ndarray of shape (n_samples)
            # Cluster labels for each point in the dataset given to fit(). Noisy samples are given the label -1.'''
    #def __repr__(self):return 
    
    '''# ====== Public Method ====== #'''
    def fit(self, database:'numpy'):
        self.database = database
        self.labels_ = np.zeros(len(database), dtype=int) # 初始化 labels 並同時用來記錄走訪
        self.core_sample_indices_ = np.array([], int)
        MinPts = self.min_samples - 1 # 定義新的 MinPts 使程式碼簡化，不影響結果
        Now_ClusterID = 0
        # 開始依序計算距離、比較 eps min_pts 給予分群
        for sample_idx in range(len(database)):
            if self.labels_[sample_idx] != 0: continue # 若此點已走訪過、擁有自己的群，不需要重複計算
            
            NeighborEpsPts = self.__regionQuery(sample_idx) # [NeighborEpsPts] 即 NEsp(P) where P is "sample_idx"
            # 區分 Core-point 與 Noise，如果是 bolder-point 其實等效於 Noise，等其他 Core-points 來認養自己即可
            if len(NeighborEpsPts) >= MinPts:
                # database[sample_idx] is Core-point
                self.core_sample_indices_ = np.append(self.core_sample_indices_, sample_idx) # 紀錄為 Core-point 
                Now_ClusterID += 1
                self.labels_[sample_idx] = Now_ClusterID
                # 從 Neighbourhood (Directly density-reachable points) 進一步計算 Neighbour 是否也是 Core-point
                self.__expandCluster(sample_idx, NeighborEpsPts, Now_ClusterID, MinPts)
            else:
                # database[sample_idx] is Noise (in this moment), Noise，ClusterID = -1
                self.labels_[sample_idx] = -1
        self.core_sample_indices_ = np.sort(self.core_sample_indices_)
    
    '''# ====== Private Method ====== #'''
    # [Parameter] point P (index in db), eps, database db,  
    def __regionQuery(self, P:int) -> (list):
        NeighborEpsPts = list() # 初始化 NEps(P)
        for sample_idx in range(len(self.database)):
            if sample_idx == P: continue # 簡化程式碼，不必加入自己，最終效果相同
            Q = sample_idx
            # [!!!] 歐基里德距離，此處把維度寫死，需用到多維度時，記得更改此處
            destination = (((self.database[P][0] - self.database[Q][0]) ** 2) + ((self.database[P][1] - self.database[Q][1]) ** 2)) ** 0.5
            if self.eps >= destination: NeighborEpsPts.append(Q)
        return NeighborEpsPts
    
    def __expandCluster(self, P:int, NEpsPts:list, Now_ClusterID:int, MinPts:int):
        for neighbour_idx in NEpsPts:
            # 因為是 Core-point P 的鄰居，所屬相同群
            self.labels_[neighbour_idx] = Now_ClusterID # 此步驟同時能將別的群同化成自己的群 (處在邊界上的點可能會被後生成的群搶走)
            # 檢查 neighbour 自己是不是 Core-point，令 NeighborEpsPts_neighbour 是 neighbour 的 neighbour (NEpsPts') (笑)
            NeighborEpsPts_neighbour = self.__regionQuery(neighbour_idx) # 紀錄為 Core-point
            if len(NeighborEpsPts_neighbour) >= MinPts:
                self.core_sample_indices_ = np.append(self.core_sample_indices_, neighbour_idx) 
                # 表示還要把 neighbour 的 NEpsPts' 加進 P 的 NEpsPts，使迴圈延展
                for idx in NeighborEpsPts_neighbour:
                    if idx not in NEpsPts: NEpsPts.append(idx) # 只需加入新鄰居

'''
[Pseudocode] 參考自 https://zh.wikipedia.org/wiki/DBSCAN
    DBSCAN(D, eps, MinPts) {
        C = 0
        for each point P in dataset D {
            if P is visited
                continue next point
            mark P as visited
            NeighborPts = regionQuery(P, eps)
            if sizeof(NeighborPts) < MinPts
                mark P as NOISE
            else {
                C = next cluster
                expandCluster(P, NeighborPts, C, eps, MinPts)
            }
        }
    }

    expandCluster(P, NeighborPts, C, eps, MinPts) {
        add P to cluster C
        for each point P' in NeighborPts { 
            if P' is not visited {
                mark P' as visited
                NeighborPts' = regionQuery(P', eps)
                if sizeof(NeighborPts') >= MinPts
                    NeighborPts = NeighborPts joined with NeighborPts'
            }
            if P' is not yet member of any cluster
                add P' to cluster C
        }
    }

    regionQuery(P, eps)
        return all points within P's eps-neighborhood (including P)

    注意這個算法可以以下方式簡化：
        其一，"has been visited" 和 "belongs to cluster C" 可被結合起來，
        另外 "expandCluster" 副程式不必被抽出來，因為它只在一個位置被調用。
        以上算法沒有以簡化方式呈現，以反映原本出版的版本。
        另外，regionQuery 是否包含 P 並不重要，它等價於改變 MinPts 的值。
'''
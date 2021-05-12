#from sklearn.cluster import DBSCAN # 純粹測試用，比較我的演算法結果和 sklearn 的結果是否相似
import numpy as np
from myfun import io as myio
from myfun.myDBSCAN import DBSCAN as myDBSCAN

# ====== Hyperparameter ====== #
EPS = 0.257 # DBSCAN: Epsilon，意指 Neighbourhood 的最大半徑
MIN_SAMPLE = 21 # DBSCAN: 構成 Core Sample 的必要條件，ESP 範圍內的最低樣本數量限制 
STANDARDIZING = True # 是否啟用資料正規化
OUTPUT_MSG = True # 是否顯示結果
OUTPUT_FILE = True # 是否輸出結果檔案

# 防呆
if not(OUTPUT_MSG): OUTPUT_FILE = False

# 測試檔案
#TestingFile1 = 'Clustering_test1'
#TestingFile2 = 'mytest'

# ====== 導入原始資料集 ====== #
X = myio.load_data(f'TestingSet/Clustering_test5')

# ====== 資料正規化 ====== #
from sklearn.preprocessing import StandardScaler
if STANDARDIZING: X = StandardScaler().fit_transform(X)

# ====== 進行資料分群 ====== #
# 使用 DBSCAN 分群 
#db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLE) # 純粹測試用，比較我的演算法結果和 sklearn 的結果是否相似
db = myDBSCAN(eps=EPS, min_samples=MIN_SAMPLE)
db.fit(X)

# 製作群中「核心樣本」的遮罩，與 Database & operating 能得到所有核心樣本
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
# list of label 每個樣本所屬的分群
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

# ====== 輸出 ====== #
init_msg = f"Standarizing = {STANDARDIZING}, EPS = {EPS}, Min_sample = {MIN_SAMPLE}"
if OUTPUT_MSG: str_result = myio.user_output(X, labels, init_msg)
if OUTPUT_FILE: myio.save_string_to_txt('Result/', str_result)

# --- Debug --- #
#print(set(db.labels_))
#print(db.core_sample_indices_)

# --------------------------------------- #
'''
## ============  資料視覺化  ============ ##
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels) # set of 最後切出的群的種類
colors = [  plt.cm.Spectral(each)
            for each in np.linspace(0, 1, len(unique_labels))]
            # list of color，為所有樣本依所屬群上色
# 每次將一筆樣本畫進畫布，[zip(list1, list2)] 將 list1, list2 依 index 打包成 tuple
for k, col in zip(unique_labels, colors):
    # 若樣本 == -1 表示為 outlier (noise) 一律改塗成黑色 (剛剛是給予彩色)
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k) # 於 Database 遮罩出現在這筆樣本

    # 若樣本是核心點就畫成 size=14 的點
    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    # 若樣本不是就畫成 size=6 的點 (包含邊緣點及雜訊點)
    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

# 設定畫布標題
text1 = "Estimated number of clusters: "+str(n_clusters_)+"\n"
plt.title( text1+init_msg )

# 將軸的刻度文字隱藏
ax = plt.gca()
ax.axes.xaxis.set_ticklabels([])
ax.axes.yaxis.set_ticklabels([])

plt.show()
'''

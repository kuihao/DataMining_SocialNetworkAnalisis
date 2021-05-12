# [資料探勘問題]: Clustring
## [實作演算法]: DBSCAN 
* [輸入檔案規格]:
    * 每列有兩個 float type 變數，代表二維空間的 x 與 y 坐標
    * 輸入資料檔案位置: /TestingSet/Clustering_testX (X=1~5)
* [主程式檔案]:
    1. code: Clustering.py
    2. output result: 
        * Result 資料夾
            * 內含 5 個測試資料的文字輸出結果 及 資料視覺化圖片 
* [環境]: 
    * 作業系統: windows 10、python 3.8.1
    * 以 command line 啟動 MemberCard_Classification.py
* [分群結果]: 
    * Test1: EPS = 0.2, Min_sample = 10, 分成 4 群
    * Test2: EPS = 6, Min_sample = 17, 分成 4 群
    * Test3: EPS = 5, Min_sample = 20, 分成 4 群
    * Test4: EPS = 4, Min_sample = 6, 分成 3 群
    * Test5: EPS = 0.257, Min_sample = 21, 分成 5 群
* [參考來源]: 
    * sklearn.cluster 的 DBSCAN 文件 (純粹參考 class 的架構及 function 命名，演算法實作完全由本人實刻)
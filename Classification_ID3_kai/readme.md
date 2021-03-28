# [資料探勘問題]: Classification
## [實作演算法]: ID3-改 (新增：可自動處理連續型資料問題、可處理缺失值問題)

* [輸入說明]
    * Dataset File: 
        * Training dataset: training.txt
        * Testing dataset: testing.txt
    * Attributes (Features):
        * 共有五種 Attribute
            * @attribute marital_status {S,M} (婚姻狀態，類別型態：S (單身)、M (已婚))
            * @attribute num_children_at_home numeric (家中孩子數量，連續數值型態：整數)
            * @attribute member_card {Basic,Normal,Silver,Gold} (會員卡級別，類別型態：共有四種等級)
            * @attribute age numeric (年齡，連續數值型態：整數)
            * @attribute year_income numeric (年收入，連續數值型態：整數)
        * 欲分類的目標 Attribute 為 **member_card**
    * 每一列為一筆資料，用 {} 符號框住，連續兩個數字為一組，第一個數字表示 attribute 的序號 (0~4 對應 marital_status~year_income)，第二個數字表示 attribute 的 Value (會員實際資料) 
    * dataset 有缺失值，其中 member_card 的缺失值皆視為 Basic 級別
    * 此處 Testing dataset 也有標記 member_card 的答案
* [輸出說明]
    * 輸出格式為：原本單筆資料 {...} 加上 member_card = "分類結果"
* [主程式檔案]:
    1. code: MemberCard_Classification.py (此為第三版 Model)
    2. output result: 
        * 第一版 Model: OutputResult_20210322_233249.txt
        * 第三版 Model: OutputResult_20210324_220614.txt
* [環境]: 
    * 作業系統: windows 10、python 3.8.1
    * 以 command line 啟動 MemberCard_Classification.py
* [訓練結果]: 
    * 第一版 Model (有缺陷的 ID3)：
        訓練集正確率: 0.58、測試集正確率: 0.63
    * 第二版 Model (完整的 ID3)：
        訓練集正確率: 0.90、測試集正確率: 0.14 (Overfitting)
    * 第三版 Model (ID3 加入連續資料型態分切處理)：
        訓練集正確率: 0.57、測試集正確率: 0.59
# Sequential Pattern Mining
## [實作演算法]: PrefixSpan (上課簡報標題為 Partition-Based)

* [輸入資料說明]:
    * File Name: seqdata_dat.txt
        * Each sequence is a customer transaction record (每一列是一位客人長期的交易紀錄)
        * The first number of each sequence is the sequence ID (每一列的第一個數字是 Sequence ID (SID)，即不同顧客的ID，於某些論文會取名為 CID 或 TID，皆指同一個東西 )
        * The pair of number such as "11 166" is the "transaction time" and the "item ID". (SID 之後的數字是兩個數字為一組，第一個數字表示交易時間 (象徵購買的次序，可能有多組資料皆為同個時間點購買，例如：若時間次序以日期為單位，表示同一天購買了多樣商品)，第二個數字表示商品的編號
        * 同一個顧客的同一個時間點購買的商品應視為同個集合 (Set)，集合中沒有順序之分
* [主程式檔案說明]:
    1. code: Sequential_Pattern.py
    2. output result: OutputResult_20210317_210019.txt
* [資料夾說明]:
    * my_library: IO模組(my_io.py)、演算法主體為 PrefixSpan.py
    * test_record: 存放輸出的結果檔案、匯出的資料庫
* [實驗結果]: Mimimum support 設為 「0.001 (0.1%)」 於可接受時間內 (約 6.3 秒) 可以順利跑完結果

* [參考論文]: J. Pei, J. Han, H. Pinto, Q. Chen, U. Dayal, and M.-C. Hsu.
            PrefixSpan: Mining Sequential Patterns Efficiently by 
            PrefixProjected Pattern Growth. ICDE'01 (TKDE’04).
* [定義問題]: 
    (1) 長度為 1 的 item 出現次數大於或等於 Minimum Support 即為 Pattern
    (2) 仿效 Prifix 論文的定義：同一條 CID 內，同樣的 Sequencial Pattern 只會統計一次
        Ex. CID 001 有 [1 -> 2 -> 3 -> 1 -> 2 -> 3] 則 1 -> 2 -> 3 的 support = 1
    (3) 仿效 Prifix 論文的定義：同一個 set 中的 elements 也可算為 Sequence 
        Ex. 
        CID 001, [1 -> (2, 3) -> 3]
        CID 002, [4 -> (3, 2) -> 6]
        則 (2, 3) 的 support = 2
* [環境]: 作業系統: windows 10、python 3.8.1、以 command line 啟動 Sequential_Pattern.py
* [附註]: 
    1. 因為 Prifix 論文本身對於 Sequencial Pattern 的定義可能和其他演算法有些不同，因此結果會有些差異
    2. 輸出每條 Sequencial Pattern 的 SUP 表示 support，由於其算法是每次遞迴時若前綴 element 有達 Mimimum support 才會計入，因此 Sequencial Pattern 的 SUP 看似不多
    3. 重複修改程式碼總計逾 5 天
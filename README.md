# Catering-Marginal-Profit-Simulation-Engine
微型餐飲邊際營運決策引擎：階梯式人事成本與 SPLH 人效驗證模擬工具
# 獨立餐飲門市邊際利潤與勞動產能推演系統 (Catering Marginal Profit Simulation Engine)

## 專案定位 (Project Vision)
本系統專為微型與獨立餐飲門市設計，旨在解決傳統損益表 (P&L) 缺乏動態決策預測能力的痛點。透過導入**管理會計**與**個體經濟學**框架，將抽象的門市排班決策與財務結構，轉化為具備高度視覺化與可操作性的 SaaS 級決策儀表板。

## 核心學理框架 (Theoretical Framework)

### 1. 階梯式固定成本吸收模型 (Step-Fixed Cost Absorption)
傳統視角常將人事成本視為單純的變動或固定成本。本模型引入「階梯式固定成本」概念：當門市增聘全職人員時，勞動成本並非平滑上升，而是呈現剛性的階梯跳增。系統可動態推演增量營收是否足以跨越「固定成本吸收不良區間 (Under-absorption Interval)」，避免企業陷入「營收創新高、淨利反倒縮」的盲目擴張陷阱。

### 2. 勞動產能利用率與 SPLH (Sales Per Labor Hour)
摒棄單純的「人事成本率 (%)」財務迷思，本模型採用國際連鎖餐飲通用的 **SPLH (人時銷售額)** 作為產能物理指標。透過精算現有工時與新增工時的 SPLH 變化，界定產能的「緊繃飽和點」與「實質閒置率」，為全職與兼職的排班資源配置提供嚴謹的量化基準。

### 3. 法定附加成本內化 (Legal & Compliance Costing)
為消除業主心算誤差與認知盲區，底層演算法自動將台灣勞動法規之雇主隱含負擔（勞保、健保、6% 勞退提繳、職災及就業保險）參數化。全職員工薪資自動加權約 20%，兼職人員時薪加權約 11%，確保邊際利潤推演具備絕對的財務精確性與法規合規性。

## 技術架構 (Tech Stack)
* **前端視覺與動態互動 (UI/UX)**: Streamlit (Python)
* **資料運算與模型推演**: Pandas, NumPy
* **互動式圖表渲染**: Plotly (動態折線圖、區間遮罩、精確座標標籤定位)
* **版本控制與持續整合部署**: Git, GitHub, Streamlit Community Cloud

## 系統展示 (Demo)
🔗 **線上互動儀表板**: *(待雲端部署後補上專屬網址)*

## 系統演算邏輯架構 (System Architecture)

本決策引擎底層依循以下邏輯流進行動態推演，確保從財務參數到排班策略的數據一致性：

```mermaid
graph LR
    subgraph Input["1. 門市營運參數與決策輸入 (User Inputs)"]
        direction TB
        A1[現況月營業額]
        A2[變動成本率: 食材]
        A3[固定成本率: 租金/管銷雜支]
        A4[現有產能配置: 全職/兼職編制]
        A5[擴張決策: 新增全職 vs 調增兼職]
    end

    subgraph Engine["2. 邊際利潤演算引擎 (Core Simulation Engine)"]
        direction TB
        B1[法定人事附加成本自動加權<br>全職+20%, 兼職+11%]
        B2[階梯式固定成本池聚總<br>Step-Fixed Cost Pool]
        B3[邊際貢獻率計算<br>Contribution Margin]
        B4[SPLH 產能物理量換算<br>Total Labor Hours]

        B1 --> B2
        B2 & B3 --> C1[吸收門檻推導 R1 Threshold]
        B4 --> C2[產能利用率診斷 SPLH]
    end

    subgraph Output["3. 決策輸出與視覺化 (Executive Dashboard)"]
        direction TB
        D1[四柱指標看板<br>基準 vs 擴張門檻]
        D2[損益結構路徑圖<br>成本吸收不良區間遮罩]
        D3[營收階梯敏感度矩陣<br>利潤倒縮預警]
        D4[系統推演摘要<br>最適排班策略]
    end

    %% 連接 Input 到 Engine
    A1 & A2 & A3 & A4 & A5 --> B1
    A4 & A5 --> B4
    A2 --> B3

    %% 連接 Engine 到 Output
    C1 --> D1 & D2 & D3 & D4
    C2 --> D4
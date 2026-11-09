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
    %% 全域樣式設定
    classDef inputNode fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#334155;
    classDef engineNode fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a,font-weight:bold;
    classDef outputNode fill:#f0fdf4,stroke:#22c55e,stroke-width:1px,color:#166534;
    
    subgraph S1["1. 營運與決策參數輸入 (User Inputs)"]
        direction TB
        I_Rev["現況月營業額"]:::inputNode
        I_Cost["變動與固定成本率設定"]:::inputNode
        I_Labor["現有產能配置與擴張決策"]:::inputNode
    end

    subgraph S2["2. 邊際利潤核心引擎 (Simulation Engine)"]
        direction TB
        E_Cost["階梯固定成本與附加費用聚總"]:::engineNode
        E_Margin["邊際貢獻率計算"]:::engineNode
        E_SPLH["SPLH 產能利用率診斷"]:::engineNode
        
        E_Cost & E_Margin --> E_Threshold["擴張吸收門檻推導 (R1)"]:::engineNode
        E_SPLH -.-> E_Threshold
    end

    subgraph S3["3. 決策輸出看板 (Dashboard)"]
        direction TB
        O_Metrics["四柱指標: 基準 vs 門檻"]:::outputNode
        O_Chart["損益路徑與吸收不良區間圖"]:::outputNode
        O_Matrix["營收階梯敏感度矩陣表"]:::outputNode
        O_Summary["產能配置與排班策略摘要"]:::outputNode
    end

    %% 主線資料流連接
    I_Rev & I_Cost --> E_Cost
    I_Rev & I_Cost --> E_Margin
    I_Rev & I_Labor --> E_SPLH
    I_Labor --> E_Cost
    
    E_Threshold --> O_Metrics & O_Chart & O_Matrix
    E_Threshold & E_SPLH --> O_Summary
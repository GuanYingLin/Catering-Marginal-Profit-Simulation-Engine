"""
餐飲門市邊際利潤與勞動產能推演系統
Core Model: Step-Fixed Cost Absorption & SPLH Capacity Evaluation
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="餐飲門市邊際利潤與勞動產能推演系統",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    div[data-testid="stSliderTickBar"] { display: none !important; }
    div[data-testid="stSlider"] > div:nth-child(2) { margin-bottom: 0px !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 48px; font-weight: 600; font-size: 1.0rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("餐飲門市邊際利潤與勞動產能推演系統")
st.caption("基於階梯式固定成本 (Step-Fixed Costs) 吸收模型與人時銷售額 (SPLH) 產能邊界之量化分析")
st.markdown("---")

# ==================== 側邊欄：參數輸入區 ====================
with st.sidebar:
    st.subheader("一、基準營運財務結構")
    
    rev_0 = st.number_input(
        "基準月營業額 (含稅實收, 元)",
        min_value=0,
        value=440000,
        step=10000,
        help="扣除通路平台抽成與金流手續費後之實際銷貨淨額"
    )

    # 1. 食材成本
    st.markdown("<span style='font-size:0.9rem; font-weight:600;'>食材成本佔比 (變動成本)</span>", unsafe_allow_html=True)
    cogs_pct = st.slider("食材成本佔比", min_value=10.0, max_value=60.0, value=36.0, step=0.5, format="%.1f%%", label_visibility="collapsed")
    cogs_amt = rev_0 * (cogs_pct / 100.0)
    st.markdown(f"<div style='text-align: right; color: #475569; font-size: 0.85rem; margin-top: -10px; margin-bottom: 10px;'>折合金額：<b>${cogs_amt:,.0f} 元</b></div>", unsafe_allow_html=True)

    # 2. 租金成本
    st.markdown("<span style='font-size:0.9rem; font-weight:600;'>店面租金佔比 (固定成本)</span>", unsafe_allow_html=True)
    rent_pct = st.slider("店面租金佔比", min_value=1.0, max_value=20.0, value=6.5, step=0.1, format="%.1f%%", label_visibility="collapsed")
    rent_amt = rev_0 * (rent_pct / 100.0)
    st.markdown(f"<div style='text-align: right; color: #475569; font-size: 0.85rem; margin-top: -10px; margin-bottom: 10px;'>折合金額：<b>${rent_amt:,.0f} 元</b></div>", unsafe_allow_html=True)

    # 3. 營業費用 (OpEx)
    st.markdown("<span style='font-size:0.9rem; font-weight:600;'>其他營業費用佔比 (OpEx)</span>", unsafe_allow_html=True)
    overhead_pct = st.slider(
        "其他營業費用佔比",
        min_value=1.0,
        max_value=25.0,
        value=10.0,
        step=0.5,
        format="%.1f%%",
        label_visibility="collapsed",
        help="排除食材、租金、人事後之營業費用總額：水電瓦斯、稅捐、系統維持費、設備折舊攤提、維護耗材"
    )
    overhead_amt = rev_0 * (overhead_pct / 100.0)
    st.markdown(f"<div style='text-align: right; color: #475569; font-size: 0.85rem; margin-top: -10px; margin-bottom: 12px;'>折合金額：<b>${overhead_amt:,.0f} 元</b></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("二、勞動編制與法定成本")
    st.caption("模型自動外加雇主法定負擔：全職 +20% (勞健保與6%勞退)；兼職 +11% (法定保險與勞退)。排除延長工時加給。")

    num_ft = st.number_input("全職人員編制 (180 工時/月/人)", min_value=0, max_value=8, value=3, step=1)
    
    ft_salaries = []
    if num_ft > 0:
        for i in range(int(num_ft)):
            defaults = [44000, 38000, 36000, 32000]
            def_v = defaults[i] if i < len(defaults) else 32000
            salary_input = st.number_input(
                f"全職員工 {chr(65+i)} 約定全薪 (元)",
                min_value=0,
                value=def_v,
                step=1000,
                key=f"ft_{i}"
            )
            ft_salaries.append(salary_input * 1.20)

    col_pt1, col_pt2 = st.columns(2)
    with col_pt1:
        cur_pt_hours = st.number_input("兼職月總工時", min_value=0, max_value=600, value=80, step=10)
    with col_pt2:
        cur_pt_rate = st.number_input("兼職約定時薪", min_value=0, max_value=500, value=195, step=5)

    cur_pt_cost = cur_pt_hours * (cur_pt_rate * 1.11)
    cur_labor_total = sum(ft_salaries) + cur_pt_cost
    labor_pct = (cur_labor_total / rev_0) * 100.0 if rev_0 > 0 else 0.0
    st.markdown(f"<div style='color: #1e293b; font-size: 0.88rem; margin-top: 4px;'>人事總成本：<b>${cur_labor_total:,.0f} 元</b> ({labor_pct:.1f}%)</div>", unsafe_allow_html=True)
    
    cur_profit = rev_0 - (cogs_amt + rent_amt + overhead_amt + cur_labor_total)
    cur_margin = (cur_profit / rev_0) * 100.0 if rev_0 > 0 else 0.0

    st.markdown("---")

    st.subheader("三、產能擴張方案設定")
    hire_type = st.radio(
        "評估擴張方案：",
        ("方案 A：增聘全職 (階梯成本)", "方案 B：調增兼職 (邊際成本)")
    )

    if "全職" in hire_type:
        new_hire_base = st.number_input("增聘全職約定全薪 (元)", min_value=0, value=32000, step=1000)
        new_hire_cost = new_hire_base * 1.20
        new_hire_hours = 180.0
    else:
        add_pt_h = st.number_input("預計每月新增工時 (hr)", min_value=0, value=80, step=10)
        add_pt_r = st.number_input("兼職約定時薪 (元/hr)", min_value=0, value=195, step=5)
        new_hire_cost = add_pt_h * (add_pt_r * 1.11)
        new_hire_hours = float(add_pt_h)

    st.markdown(f"<div style='color: #475569; font-size: 0.85rem; margin-top: -6px; margin-bottom: 10px;'>每月增量人事成本：<b>${new_hire_cost:,.0f} 元</b></div>", unsafe_allow_html=True)

    lock_profit = st.checkbox(f"鎖定基準淨利 (${cur_profit:,.0f}) 為底線", value=True)
    new_fixed_pool = rent_amt + overhead_amt + cur_labor_total + new_hire_cost

    if lock_profit:
        denom = 1.0 - (cogs_pct / 100.0)
        r1_threshold = (new_fixed_pool + cur_profit) / denom if denom > 0 else rev_0 * 1.5
        target_margin = (cur_profit / r1_threshold) * 100.0 if r1_threshold > 0 else 0.0
    else:
        target_margin = st.slider("設定擴張後目標淨利率 (%)", min_value=5.0, max_value=25.0, value=float(round(max(5.0, cur_margin), 1)), step=0.5)
        contribution_ratio = 1.0 - (cogs_pct / 100.0) - (target_margin / 100.0)
        r1_threshold = new_fixed_pool / contribution_ratio if contribution_ratio > 0 else rev_0 * 1.5

    growth_needed_pct = ((r1_threshold - rev_0) / rev_0) * 100.0 if rev_0 > 0 else 0.0

# ==================== 核心指標推導 ====================
cur_total_hours = (num_ft * 180.0) + cur_pt_hours
cur_splh = rev_0 / cur_total_hours if cur_total_hours > 0 else 0.0
expanded_total_hours = cur_total_hours + new_hire_hours

healthy_splh_min, healthy_splh_max = 650.0, 800.0
rev_range_cur_max = cur_total_hours * healthy_splh_max
rev_range_exp_min = expanded_total_hours * healthy_splh_min

# ==================== 區塊 1：頂層指標看板 (四柱結構) ====================
m1, m2, m3, m4 = st.columns(4)
m1.metric("基準月營業額", f"${rev_0:,.0f} 元", f"基準總工時 {cur_total_hours:.0f} hr", delta_color="off")
m2.metric("基準實質月淨利", f"${cur_profit:,.0f} 元", f"基準淨利率 {cur_margin:.2f}%", delta_color="off")
m3.metric("基準人時銷售額 (SPLH)", f"{cur_splh:.0f} 元/hr", f"擴張後總工時 {expanded_total_hours:.0f} hr", delta_color="off")
m4.metric("成本吸收營收門檻", f"${r1_threshold:,.0f} 元", f"需增長 +{growth_needed_pct:.1f}%", delta_color="inverse")

st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

# ==================== 區塊 2：損益結構路徑分析圖 ====================
sim_ratios = sorted(list(set([0.85, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, (r1_threshold / rev_0) if rev_0 > 0 else 1.0, 1.3])))
df_sim = pd.DataFrame([{
    "營收": rev_0 * r,
    "淨利": (rev_0 * r) - (rev_0 * r * (cogs_pct / 100.0)) - new_fixed_pool,
} for r in sim_ratios])

fig = go.Figure()

fig.add_trace(go.Scatter(x=[df_sim["營收"].min(), df_sim["營收"].max()], y=[cur_profit, cur_profit], mode="lines", name="基準淨利水準", line=dict(color="#0f172a", width=1.5, dash="dash")))
fig.add_trace(go.Scatter(x=df_sim["營收"], y=df_sim["淨利"], mode="lines+markers", name="擴張配置淨利路徑", line=dict(color="#2563eb", width=2.5)))
fig.add_trace(go.Scatter(x=[rev_0], y=[cur_profit], mode="markers+text", name="基準營運點", text=[f" 基準點: ${cur_profit:,.0f}"], textposition="top left", marker=dict(color="#0f172a", size=9)))
fig.add_trace(go.Scatter(x=[r1_threshold], y=[cur_profit], mode="markers+text", name="成本吸收平衡點", text=[f" 吸收門檻: ${r1_threshold:,.0f}"], textposition="bottom right", marker=dict(color="#dc2626", size=11)))

fig.add_vrect(x0=rev_0, x1=r1_threshold, fillcolor="#fee2e2", opacity=0.4, layer="below", line_width=0, annotation_text=" 固定成本吸收不良區間 (Under-absorption)", annotation_position="top left", annotation_font_size=12, annotation_font_color="#991b1b")

fig.update_layout(
    xaxis_title="月度營業額 (元)",
    yaxis_title="月淨利 (元)",
    xaxis_tickformat="$,.0f",
    yaxis_tickformat="$,.0f",
    hovermode="x unified",
    margin=dict(l=10, r=10, t=20, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor="rgba(248, 250, 252, 0.5)",
)
st.plotly_chart(fig, width="stretch")

# ==================== 區塊 3：分析與數據報表 ====================
tab1, tab2 = st.tabs(["系統推演摘要 (Analytical Findings)", "情境敏感度矩陣 (Sensitivity Matrix)"])

with tab1:
    splh_at_zero = rev_0 / expanded_total_hours if expanded_total_hours > 0 else 0.0
    idle_hours_pct = ((cur_splh - splh_at_zero) / cur_splh) * 100.0 if cur_splh > 0 else 0.0
    plan_clean_name = hire_type.split(" (")[0]
    
    st.markdown(
        f"""
        <div style="padding: 10px 16px; line-height: 1.8; color: #334155; font-size: 1.0rem;">
            <ul style="margin-bottom: 0;">
                <li style="margin-bottom: 10px;"><b>基準配置產能評估：</b> 現有編制（{cur_total_hours:.0f} 工時）之 SPLH 產能健康上限為 <b>${rev_range_cur_max:,.0f} 元</b>。目前基準營收落於產能飽和邊界（{cur_splh:.0f} 元/hr），具備評估產能擴張之客觀條件。</li>
                <li style="margin-bottom: 10px;"><b>固定成本吸收要求：</b> 執行<b>【{plan_clean_name}】</b>後，月營業額須達 <b>${r1_threshold:,.0f} 元（較基準增長 +{growth_needed_pct:.1f}%）</b>，方能完全吸收新增人事支出（${new_hire_cost:,.0f} 元/月）並維持既有淨利水準。未達此門檻前將產生利潤倒縮。</li>
                <li style="margin-bottom: 10px;"><b>未達規模之產能沉沒：</b> 若增聘後營收未能同步增長，人時銷售額將由 {cur_splh:.0f} 元/hr 降至 <b>{splh_at_zero:.0f} 元/hr</b>，實質產生 <b>{idle_hours_pct:.1f}%</b> 之工時閒置率。</li>
                <li style="margin-bottom: 0px;"><b>最適產能配置策略：</b> 若預期月營業額尚無法常態性突破全職擴張所需之規模門檻（<b>${rev_range_exp_min:,.0f} 元</b>），基於邊際利潤最大化原則，應優先採取彈性工時配置（方案 B）以規避階梯式固定成本風險。</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with tab2:
    sample_table = []
    for r in sim_ratios:
        sim_rev = rev_0 * r
        sim_profit = sim_rev - (sim_rev * (cogs_pct / 100.0)) - new_fixed_pool
        sim_margin = (sim_profit / sim_rev) * 100.0 if sim_rev > 0 else 0.0
        sim_splh = sim_rev / expanded_total_hours if expanded_total_hours > 0 else 0.0
        
        diff = sim_profit - cur_profit
        if abs(diff) < 1.0:
            status = "損益平衡 ($0)"
        elif diff < 0:
            status = f"利潤倒縮 (-${abs(diff):,.0f})"
        else:
            status = f"利潤增長 (+${diff:,.0f})"
            
        profit_str = f"-${abs(sim_profit):,.0f}" if sim_profit < 0 else f"${sim_profit:,.0f}"
        
        sample_table.append({
            "推演營業額": f"${sim_rev:,.0f}",
            "營收增幅": f"{((sim_rev - rev_0) / rev_0) * 100.0:+.1f}%",
            "推演月淨利": profit_str,
            "推演淨利率": f"{sim_margin:.2f}%",
            "推演 SPLH": f"{sim_splh:.0f} 元/hr",
            "損益吸收定性": status,
        })
    st.dataframe(pd.DataFrame(sample_table), width="stretch", hide_index=True)
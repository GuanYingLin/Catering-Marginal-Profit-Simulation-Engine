"""
微型餐飲階梯式人事成本與邊際淨利計算引擎
Core Engine: Step-Fixed Cost & Sales Per Labor Hour (SPLH)
"""
from typing import Dict, List, Tuple
import pandas as pd


def calc_baseline_kpis(
    revenue: float,
    cogs_ratio: float,
    labor_cost: float,
    rent_cost: float,
    overhead_cost: float,
    labor_hourly_rate: float = 200.0,
) -> Dict[str, float]:
    """計算基準期（現況）之財務與人效指標"""
    cogs_amount = revenue * (cogs_ratio / 100.0)
    total_cost = cogs_amount + labor_cost + rent_cost + overhead_cost
    net_profit = revenue - total_cost
    net_margin = (net_profit / revenue) * 100.0 if revenue > 0 else 0.0

    total_hours = labor_cost / labor_hourly_rate if labor_hourly_rate > 0 else 0.0
    splh = revenue / total_hours if total_hours > 0 else 0.0

    return {
        "revenue": revenue,
        "net_profit": net_profit,
        "net_margin": net_margin,
        "total_hours": total_hours,
        "splh": splh,
        "cogs_amount": cogs_amount,
        "fixed_overhead": rent_cost + overhead_cost,
    }


def calc_expansion_threshold(
    baseline_kpis: Dict[str, float],
    cogs_ratio: float,
    new_hire_cost: float,
    target_margin: float,
) -> float:
    """計算增聘人力後，維持目標淨利率所需之新營收門檻 (R1)"""
    total_fixed_cost = (
        (baseline_kpis["revenue"] - baseline_kpis["cogs_amount"] - baseline_kpis["net_profit"])
        + new_hire_cost
    )
    contribution_rate = 1.0 - (cogs_ratio / 100.0) - (target_margin / 100.0)
    if contribution_rate <= 0:
        return 0.0

    return total_fixed_cost / contribution_rate


def generate_simulation_curve(
    baseline_kpis: Dict[str, float],
    cogs_ratio: float,
    new_hire_cost: float,
    new_hire_hours: float,
    target_margin: float,
    steps: int = 50,
) -> Tuple[pd.DataFrame, float]:
    """生成營業額擴張時的邊際淨利與人效變化曲線"""
    r0 = baseline_kpis["revenue"]
    new_fixed_cost = (
        (baseline_kpis["revenue"] - baseline_kpis["cogs_amount"] - baseline_kpis["net_profit"])
        + new_hire_cost
    )
    contribution_rate = 1.0 - (cogs_ratio / 100.0) - (target_margin / 100.0)
    r1 = new_fixed_cost / contribution_rate if contribution_rate > 0 else r0 * 1.5

    min_rev = max(50000.0, r0 * 0.8)
    max_rev = r1 * 1.25
    step_size = (max_rev - min_rev) / steps

    records: List[Dict[str, float]] = []
    total_hours_expanded = baseline_kpis["total_hours"] + new_hire_hours

    for i in range(steps + 1):
        sim_rev = min_rev + i * step_size
        sim_cogs = sim_rev * (cogs_ratio / 100.0)
        sim_profit = sim_rev - sim_cogs - new_fixed_cost
        sim_margin = (sim_profit / sim_rev) * 100.0 if sim_rev > 0 else 0.0
        sim_splh = sim_rev / total_hours_expanded if total_hours_expanded > 0 else 0.0

        records.append({
            "營收 (元)": sim_rev,
            "實質淨利 (元)": sim_profit,
            "淨利率 (%)": sim_margin,
            "SPLH 人時產值 (元/小時)": sim_splh,
            "落點狀態": "達標區" if sim_rev >= r1 else "階梯陷阱區",
        })

    return pd.DataFrame(records), r1

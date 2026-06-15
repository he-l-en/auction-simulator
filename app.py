import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="拍卖实验模拟器", layout="wide")

# ========== AI辅助标识 ==========
st.markdown("""
<div style='background-color:#e8f5e9; padding:15px; border-radius:8px; border-left:6px solid #4CAF50; margin-bottom:20px;'>
<b>🤖 AI辅助说明</b><br>
本模拟器由AI辅助设计开发，包含：AI策略生成（0-1背包优化）、数据可视化优化、行为偏差识别、理论辅助理解等环节。<br>
<small>中南财经政法大学 | 经济管理前沿方法 | 实验2</small>
</div>
""", unsafe_allow_html=True)

st.title("🎯 一级密封价格拍卖实验模拟器")

# ========== 完整实验数据 ==========
VALUES_FULL = [200, 200, 200, 250, 250, 250, 300, 300, 300, 400, 400, 500]

ROUND1_FULL = {
    "小组1": [198, 198, 198, 248, 248, 248, 298, 298, 298, 398, 398, 498],
    "小组2": [20, 150, 20, 20, 20, 20, 20, 20, 20, 20, 350, 450],
    "小组3": [199, 199, 199, 249, 249, 249, 249, 0, 0, 0, 0, 0],
    "小组4": [199, 199, 180, 245, 249, 249, 299, 280, 299, 399, 398, 499],
    "小组5": [150, 175, 199, 248, 248, 248, 297, 297, 297, 397, 397, 495],
    "小组6": [196, 196, 196, 246, 246, 246, 296, 296, 296, 396, 400, 500],
}

ROUND2_FULL = {
    "小组1": [190, 180, 0, 0, 210, 240, 290, 0, 0, 390, 0, 0],
    "小组2": [20, 20, 20, 10, 240, 10, 245, 245, 245, 30, 380, 30],
    "小组3": [100, 100, 100, 220, 230, 240, 210, 100, 100, 100, 0, 0],
    "小组4": [101, 101, 101, 151, 200, 151, 101, 101, 101, 101, 290, 0],
    "小组5": [190, 190, 112, 0, 226, 230, 0, 276, 276, 0, 0, 0],
    "小组6": [0, 30, 0, 0, 0, 0, 299, 299, 0, 392, 0, 480],
}

ROUND3_FULL = {
    "小组1": [160, 180, 0, 0, 240, 240, 0, 290, 0, 390, 0, 0],
    "小组2": [10, 180, 20, 0, 200, 235, 0, 260, 280, 0, 380, 0],
    "小组3": [1, 1, 1, 20, 241, 1, 40, 0, 1, 361, 361, 471],
    "小组4": [191, 191, 191, 236, 250, 0, 0, 0, 292, 0, 368, 0],
    "小组5": [0, 191, 191, 231, 0, 201, 278, 0, 0, 0, 386, 22],
    "小组6": [0, 0, 0, 0, 0, 0, 281, 0, 0, 361, 0, 421],
}

VALUES_PARTIAL_R1 = [500, 200, 200, 200, 250, 250, 300, 300, 300, 250, 400, 400]
VALUES_PARTIAL_R2 = [200, 200, 200, 500, 250, 250, 250, 300, 300, 300, 400, 400]

ROUND1_PARTIAL = {
    "小组1": [201, 0, 191, 0, 0, 0, 108, 298, 292, 9, 392, 9],
    "小组2": [203, 188, 188, 20, 20, 20, 20, 10, 20, 213, 380, 223],
    "小组3": [200, 196, 197, 200, 20, 20, 200, 20, 20, 200, 28, 200],
    "小组4": [201, 0, 193, 201, 0, 236, 201, 271, 0, 201, 0, 0],
    "小组5": [202, 0, 0, 202, 236, 236, 202, 0, 18, 202, 0, 202],
    "小组6": [203, 0, 192, 202, 0, 0, 202, 293, 0, 201, 0, 200],
}

ROUND2_PARTIAL = {
    "小组1": [250, 0, 0, 250, 246, 0, 254, 0, 0, 250, 0, 250],
    "小组2": [0, 196, 185, 211, 0, 0, 230, 292, 0, 0, 386, 0],
    "小组3": [288, 0, 0, 288, 0, 0, 288, 0, 0, 288, 0, 288],
    "小组4": [0, 196, 196, 253, 209, 238, 0, 0, 0, 0, 0, 253],
    "小组5": [301, 0, 0, 301, 0, 0, 299, 0, 0, 300, 0, 299],
    "小组6": [254, 0, 193, 254, 0, 0, 254, 0, 0, 254, 0, 254],
}

TOTAL_PROFITS = {
    "小组1": {"完全信息-R1": 0.4, "完全信息-R2": 2, "完全信息-R3": 6, "不完全信息-R1": 3.6, "不完全信息-R2": 0.8, "总计": 8.8},
    "小组2": {"完全信息-R1": 0, "完全信息-R2": 6, "完全信息-R3": 0, "不完全信息-R1": 101.2, "不完全信息-R2": 5.2, "总计": 112.4},
    "小组3": {"完全信息-R1": 1, "完全信息-R2": 6, "完全信息-R3": 5.8, "不完全信息-R1": 1.4, "不完全信息-R2": 0, "总计": 14.2},
    "小组4": {"完全信息-R1": 0.8, "完全信息-R2": 0, "完全信息-R3": 5.2, "不完全信息-R1": 2.8, "不完全信息-R2": 3.2, "总计": 12},
    "小组5": {"完全信息-R1": 0, "完全信息-R2": 26.4, "完全信息-R3": 4.6, "不完全信息-R1": 22, "不完全信息-R2": 29, "总计": 82},
    "小组6": {"完全信息-R1": 0, "完全信息-R2": 7.5, "完全信息-R3": 4.75, "不完全信息-R1": 0, "不完全信息-R2": -1, "总计": 11.25},
}

# ========== 核心拍卖引擎 ==========
def run_auction(bids_dict, values, budget=None, seed=42):
    np.random.seed(seed)
    groups = list(bids_dict.keys())
    n_items = len(values)
    matrix = np.array([bids_dict[g] for g in groups])

    winners = []
    winning_bids = []

    for item_idx in range(n_items):
        item_bids = matrix[:, item_idx]
        valid_mask = item_bids > 0

        if not np.any(valid_mask):
            winners.append(-1)
            winning_bids.append(0)
        else:
            valid_bids = item_bids[valid_mask]
            valid_indices = np.where(valid_mask)[0]
            max_bid = np.max(valid_bids)
            max_indices = valid_indices[valid_bids == max_bid]
            winner_idx = np.random.choice(max_indices)
            winners.append(int(winner_idx))
            winning_bids.append(float(max_bid))

    winners = np.array(winners)
    winning_bids = np.array(winning_bids)

    results = {}
    for i, g in enumerate(groups):
        won_items = np.where(winners == i)[0]
        num_won = len(won_items)
        spent = sum(winning_bids[j] for j in won_items)
        total_value = sum(values[j] for j in won_items)
        profit = total_value - spent
        over_budget = False

        if budget is not None and spent > budget:
            over_budget = True

        results[g] = {
            'items': [int(j) + 1 for j in won_items],
            'num': int(num_won),
            'spent': spent,
            'value': total_value,
            'profit': profit,
            'over_budget': over_budget,
            'budget': budget,
        }

    return results, winners, winning_bids, groups

# ========== AI策略模块（0-1背包算法） ==========
def ai_knapsack_strategy(values, history_dict, budget=1500, risk_aversion=1.0):
    hist_matrix = np.array([history_dict[g] for g in history_dict.keys()])
    hist_max = np.max(hist_matrix, axis=0)
    estimated_win = hist_max * risk_aversion + 1
    estimated_win = np.minimum(estimated_win, values)
    expected_profits = values - estimated_win

    n = len(values)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    keep = [[False] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(budget + 1):
            if estimated_win[i-1] <= w and expected_profits[i-1] > 0:
                if dp[i-1][w - int(estimated_win[i-1])] + expected_profits[i-1] > dp[i-1][w]:
                    dp[i][w] = dp[i-1][w - int(estimated_win[i-1])] + expected_profits[i-1]
                    keep[i][w] = True
                else:
                    dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = dp[i-1][w]

    selected = []
    ai_bids = [0] * n
    w = budget
    for i in range(n, 0, -1):
        if keep[i][w]:
            selected.append(i)
            ai_bids[i-1] = int(estimated_win[i-1])
            w -= int(estimated_win[i-1])

    selected.reverse()
    total_spent = sum(ai_bids)
    total_profit = sum(values[i-1] - ai_bids[i-1] for i in selected)

    return ai_bids, selected, total_spent, total_profit, hist_max, estimated_win

# ========== AI策略模式识别 ==========
def ai_strategy_classifier(bids_dict, values):
    strategies = {}
    for g, bids in bids_dict.items():
        valid_ratios = [b/v for b, v in zip(bids, values) if b > 0]
        if not valid_ratios:
            strategies[g] = {'type': '完全放弃', 'avg_ratio': 0, 'variance': 0, 'zero_count': 12}
            continue

        avg_ratio = np.mean(valid_ratios)
        variance = np.var(valid_ratios) if len(valid_ratios) > 1 else 0
        zero_count = sum(1 for b in bids if b == 0)

        if avg_ratio > 0.95:
            type_name = "激进型（接近估值出价）"
        elif avg_ratio < 0.5:
            type_name = "保守型（大幅低于估值）"
        elif zero_count > 6:
            type_name = "选择性竞拍（聚焦高价值物品）"
        elif variance > 0.3:
            type_name = "混合型（策略不稳定）"
        else:
            type_name = "均衡型（接近理论最优）"

        strategies[g] = {
            'type': type_name,
            'avg_ratio': avg_ratio,
            'variance': variance,
            'zero_count': zero_count
        }

    return strategies

# ========== 侧边栏导航 ==========
st.sidebar.header("📋 实验条件")

experiment_type = st.sidebar.radio(
    "选择实验条件",
    ["完全信息（估值公开）", "不完全信息（估值私有）"]
)

round_num = st.sidebar.radio(
    "选择轮次",
    ["第一轮", "第二轮", "第三轮（仅完全信息）"]
)

if experiment_type == "完全信息（估值公开）":
    if round_num == "第一轮":
        current_data = ROUND1_FULL
        current_values = VALUES_FULL
        budget = None
        info_text = "完全信息 | 第一轮 | 无预算约束"
    elif round_num == "第二轮":
        current_data = ROUND2_FULL
        current_values = VALUES_FULL
        budget = 1500
        info_text = "完全信息 | 第二轮 | 预算1500"
    else:
        current_data = ROUND3_FULL
        current_values = VALUES_FULL
        budget = 1500
        info_text = "完全信息 | 第三轮 | 预算1500 | 可交流"
else:
    if round_num == "第一轮":
        current_data = ROUND1_PARTIAL
        current_values = VALUES_PARTIAL_R1
        budget = None
        info_text = "不完全信息 | 第一轮 | 无预算约束"
    elif round_num == "第二轮":
        current_data = ROUND2_PARTIAL
        current_values = VALUES_PARTIAL_R2
        budget = 1500
        info_text = "不完全信息 | 第二轮 | 预算1500 | 可交流"
    else:
        st.sidebar.error("不完全信息没有第三轮数据")
        st.stop()

st.sidebar.info(info_text)

# ========== 主界面 ==========
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 实验结果", 
    "🏆 模拟竞拍", 
    "🤖 AI策略", 
    "📈 理论分析",
    "👥 我们小组"
])

# ========== Tab 1: 实验结果 ==========
with tab1:
    st.header(f"实验结果：{info_text}")
    st.caption("🤖 AI辅助：数据整理与可视化")

    results, winners, wb, groups = run_auction(current_data, current_values, budget)

    df_results = []
    for g in groups:
        r = results[g]
        df_results.append({
            "小组": g,
            "赢得物品": f"{r['num']}件",
            "物品编号": str(r['items']),
            "总支出": r['spent'],
            "总价值": r['value'],
            "净利润": r['profit'],
            "预算状态": "✅" if not r['over_budget'] else "❌超支",
        })

    df = pd.DataFrame(df_results)
    st.dataframe(df, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("净利润对比")
        chart_df = df.set_index('小组')[['净利润']]
        st.bar_chart(chart_df)

    with col2:
        st.subheader("赢得物品数")
        chart_df2 = df.copy()
        chart_df2['数量'] = chart_df2['赢得物品'].str.extract(r'(\d+)').astype(int)
        st.bar_chart(chart_df2.set_index('小组')[['数量']])

    # 逐物品明细
    st.subheader("逐物品拍卖明细")
    df_items = []
    for i in range(12):
        if winners[i] >= 0:
            winner = groups[winners[i]]
            win_bid = wb[i]
        else:
            winner = "流拍"
            win_bid = 0

        df_items.append({
            "物品": i + 1,
            "估值": current_values[i],
            "成交价": win_bid,
            "获胜者": winner,
            "利润": current_values[i] - win_bid if winners[i] >= 0 else 0,
        })

    st.dataframe(pd.DataFrame(df_items), hide_index=True, use_container_width=True)

    # AI策略模式识别
    st.subheader("🤖 AI策略模式识别")
    strategies = ai_strategy_classifier(current_data, current_values)
    df_strat = pd.DataFrame([
        {"小组": g, "策略类型": s['type'], "平均出价/估值": f"{s['avg_ratio']:.1%}", 
         "零出价数": s['zero_count'], "策略稳定性": "高" if s['variance'] < 0.2 else "低"}
        for g, s in strategies.items()
    ])
    st.dataframe(df_strat, hide_index=True, use_container_width=True)

# ========== Tab 2: 模拟竞拍 ==========
with tab2:
    st.header("🏆 模拟竞拍体验")
    st.caption("🤖 AI辅助：交互式模拟引擎")
    st.info("输入你的出价，与历史数据中的小组竞争")

    user_budget = st.slider("你的预算", 500, 3000, 1500, key="sim_budget")
    opponent_options = list(current_data.keys())
    selected_opponents = st.multiselect(
        "选择对手（至少选1个）",
        opponent_options,
        default=opponent_options[:3],
    )

    if len(selected_opponents) == 0:
        st.warning("请至少选择一个对手")
        st.stop()

    st.subheader("你的出价")
    user_bids = []
    cols = st.columns(4)
    for i in range(12):
        with cols[i % 4]:
            bid = st.number_input(
                f"物品{i+1}(估值{current_values[i]})",
                0, 1000, 0,
                key=f"user_bid_{i}"
            )
            user_bids.append(bid)

    total_bid = sum(user_bids)
    st.write(f"**你的总出价: {total_bid}** {'✅' if total_bid <= user_budget else '❌超支'}")

    if st.button("🚀 开始拍卖", key="sim_button"):
        sim_bids = {"你": user_bids}
        for opp in selected_opponents:
            sim_bids[opp] = current_data[opp]

        sim_results, sim_winners, sim_wb, sim_groups = run_auction(
            sim_bids, current_values, user_budget
        )

        you = sim_results["你"]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("赢得物品", f"{you['num']}件")
        with col2:
            st.metric("总支出", f"{you['spent']}")
        with col3:
            st.metric("总价值", f"{you['value']}")
        with col4:
            st.metric("净利润", f"{you['profit']}",
                     delta="盈利" if you['profit'] > 0 else "亏损")

        df_sim = []
        for i in range(12):
            winner = sim_groups[sim_winners[i]] if sim_winners[i] >= 0 else "流拍"
            df_sim.append({
                "物品": i + 1,
                "估值": current_values[i],
                "你的出价": user_bids[i],
                "成交价": sim_wb[i],
                "获胜者": winner,
                "你赢了": "✅" if winner == "你" else "❌",
            })

        st.dataframe(pd.DataFrame(df_sim), hide_index=True, use_container_width=True)

        # AI对比
        st.subheader("🤖 AI策略对比")
        ai_bids, ai_selected, ai_spent, ai_profit, hist_max, est_win = ai_knapsack_strategy(
            current_values, current_data, user_budget
        )

        ai_sim_bids = {"AI": ai_bids}
        for opp in selected_opponents:
            ai_sim_bids[opp] = current_data[opp]
        ai_sim_results, _, _, _ = run_auction(ai_sim_bids, current_values, user_budget)
        ai_actual = ai_sim_results["AI"]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("AI利润（估计）", f"{ai_profit:.0f}")
        with col2:
            st.metric("AI利润（实际）", f"{ai_actual['profit']}")
        with col3:
            st.metric("你的利润", f"{you['profit']}")

# ========== Tab 3: AI策略 ==========
with tab3:
    st.header("🤖 AI策略分析")
    st.caption("🤖 AI辅助：0-1背包优化算法")

    ai_budget = st.slider("AI预算", 500, 3000, 1500, key="ai_budget")
    risk_level = st.slider("风险厌恶系数", 0.5, 2.0, 1.0, 0.1,
                          help=">1更保守（出价更高确保获胜），<1更激进")

    ai_bids, ai_selected, ai_spent, ai_profit, hist_max, est_win = ai_knapsack_strategy(
        current_values, current_data, ai_budget, risk_level
    )

    st.subheader("AI出价策略")
    df_ai = []
    for i in range(12):
        df_ai.append({
            "物品": i + 1,
            "估值": current_values[i],
            "历史最高": hist_max[i],
            "估计获胜价": est_win[i],
            "AI出价": ai_bids[i] if ai_bids[i] > 0 else "放弃",
            "估计利润": current_values[i] - ai_bids[i] if ai_bids[i] > 0 else 0,
        })

    st.dataframe(pd.DataFrame(df_ai), hide_index=True, use_container_width=True)

    st.subheader("AI选择结果")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("选中物品", f"{len(ai_selected)}件")
    with col2:
        st.metric("预计支出", f"{ai_spent}")
    with col3:
        st.metric("预计利润", f"{ai_profit:.0f}")

    st.write(f"**选中物品编号**: {ai_selected}")

    # AI在真实竞争中的表现
    st.subheader("AI在真实竞争中的模拟")
    ai_test = {"AI": ai_bids}
    for g in current_data.keys():
        ai_test[g] = current_data[g]

    ai_test_results, _, _, _ = run_auction(ai_test, current_values, ai_budget)
    ai_actual = ai_test_results["AI"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("实际赢得", f"{ai_actual['num']}件")
    with col2:
        st.metric("实际支出", f"{ai_actual['spent']}")
    with col3:
        st.metric("实际利润", f"{ai_actual['profit']}")

    st.info("""
    **AI策略说明**：
    - 基于历史数据估计每个物品的获胜价格
    - 使用0-1背包算法在预算约束下最大化利润
    - 风险厌恶系数调整估计的保守程度
    - 实际利润取决于对手本轮的真实出价（AI无法预知）
    """)

# ========== Tab 4: 理论分析（去掉83.3修正） ==========
with tab4:
    st.header("📈 理论分析")
    st.caption("🤖 AI辅助：理论理解与行为偏差识别")

    st.subheader("拍卖理论基础")
    st.markdown("""
    **第一价格密封拍卖理论要点**：
    - 竞拍者同时独立出价，最高出价者获胜并支付自己的出价
    - 在完全信息条件下，竞争会推高价格接近真实价值
    - 在不完全信息条件下，竞拍者需基于贝叶斯推断估计他人出价
    - 赢者诅咒：获胜者往往是对物品估值过高的人，可能反而亏损
    - 学习效应：多轮竞拍中，参与者通过经验调整策略
    """)

    # 实际出价分析
    st.subheader("实际出价分析")

    df_compare = []
    for g in current_data.keys():
        bids = current_data[g]
        for i in range(12):
            if bids[i] > 0:
                ratio = bids[i] / current_values[i]
                df_compare.append({
                    "小组": g,
                    "物品": i + 1,
                    "估值": current_values[i],
                    "出价": bids[i],
                    "出价/估值": ratio,
                })

    df_comp = pd.DataFrame(df_compare)
    avg_ratio = df_comp['出价/估值'].mean()
    std_ratio = df_comp['出价/估值'].std()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("平均出价/估值", f"{avg_ratio:.1%}")
    with col2:
        st.metric("出价离散度", f"{std_ratio:.2f}")

    st.dataframe(df_comp, hide_index=True, use_container_width=True)

    # 可视化
    st.subheader("出价分布可视化")
    fig, ax = plt.subplots(figsize=(10, 6))

    for g in current_data.keys():
        group_data = df_comp[df_comp['小组'] == g]
        if not group_data.empty:
            ax.scatter(group_data['物品'], group_data['出价/估值'],
                      label=g, alpha=0.7, s=60)

    ax.axhline(y=1.0, color='red', linestyle='--',
              linewidth=2, label='真实估值 (100%)')
    ax.axhline(y=avg_ratio, color='green', linestyle=':',
              linewidth=2, label=f'平均出价 ({avg_ratio:.1%})')

    ax.set_xlabel('物品编号')
    ax.set_ylabel('出价 / 估值')
    ax.set_title('各组出价分布与理论参照对比')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.2)

    st.pyplot(fig)

    # 行为经济学解释
    st.subheader("🧠 AI辅助的行为经济学解释")

    all_ratios = df_comp['出价/估值'].values
    overconfident = np.mean(all_ratios > 0.95)

    st.markdown(f"""
    **AI识别的行为偏差**：

    | 偏差类型 | 证据 | 程度 |
    |---------|------|------|
    | **过度自信** | {overconfident:.1%}的出价接近/超过估值 | {'高' if overconfident > 0.3 else '中' if overconfident > 0.1 else '低'} |
    | **赢者诅咒** | 高估值物品竞争激烈，利润趋近于0 | 显著 |
    | **预算效应** | {'有预算时出价显著降低' if budget else '本轮无预算约束'} | {'显著' if budget else '无'} |
    | **信息效应** | {'不完全信息下出价更分散' if '不完全' in info_text else '完全信息下出价集中'} | 显著 |

    **AI辅助结论**：人类行为系统性地偏离理性假设，但AI可以量化这些偏差并辅助理解理论。
    """)

# ========== Tab 5: 我们小组 ==========
with tab5:
    st.header("👥 我们小组的实验表现与AI辅助分析")
    st.caption("🤖 AI辅助：策略评估与改进建议")

    our_group = st.selectbox("选择你们的小组", list(current_data.keys()))

    our_bids = current_data[our_group]
    our_results = results[our_group]

    st.subheader(f"{our_group}的出价策略")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("净利润", f"{our_results['profit']}")
    with col2:
        st.metric("赢得物品", f"{our_results['num']}件")
    with col3:
        st.metric("总支出", f"{our_results['spent']}")
    with col4:
        st.metric("预算状态", "✅正常" if not our_results['over_budget'] else "❌超支")

    df_our = []
    for i in range(12):
        ratio = our_bids[i] / current_values[i] if our_bids[i] > 0 else 0
        df_our.append({
            "物品": i + 1,
            "估值": current_values[i],
            "我们出价": our_bids[i] if our_bids[i] > 0 else "放弃",
            "出价/估值": f"{ratio:.1%}" if our_bids[i] > 0 else "-",
            "成交": "✅" if (i+1) in our_results['items'] else "❌",
        })
    st.dataframe(pd.DataFrame(df_our), hide_index=True, use_container_width=True)

    # AI策略对比
    st.subheader("🤖 AI策略对比与建议")

    ai_bids, ai_selected, ai_spent, ai_profit, hist_max, est_win = ai_knapsack_strategy(
        current_values, current_data, budget or 1500
    )

    our_valid_ratios = [b/v for b, v in zip(our_bids, current_values) if b > 0]
    our_avg_ratio = np.mean(our_valid_ratios) if our_valid_ratios else 0
    our_zero_count = sum(1 for b in our_bids if b == 0)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **我们小组的策略特征**：
        - 平均出价/估值：**{our_avg_ratio:.1%}**
        - 放弃物品数：**{our_zero_count}件**
        - 策略类型：**{ai_strategy_classifier({our_group: our_bids}, current_values)[our_group]['type']}**
        """)

    with col2:
        st.markdown(f"""
        **AI建议策略**：
        - AI平均出价/估值：**{np.mean([b/v for b, v in zip(ai_bids, current_values) if b > 0]):.1%}**
        - AI放弃物品数：**{sum(1 for b in ai_bids if b == 0)}件**
        - AI预计利润：**{ai_profit:.0f}**
        """)

    # 逐物品对比
    st.subheader("逐物品：我们 vs AI")
    df_compare_our = []
    for i in range(12):
        our_bid = our_bids[i]
        ai_bid = ai_bids[i]
        df_compare_our.append({
            "物品": i + 1,
            "估值": current_values[i],
            "我们出价": our_bid if our_bid > 0 else "放弃",
            "AI出价": ai_bid if ai_bid > 0 else "放弃",
            "差异": (our_bid - ai_bid) if our_bid > 0 and ai_bid > 0 else "-",
            "AI建议": "出价过高" if our_bid > ai_bid > 0 else "出价过低" if 0 < our_bid < ai_bid else "一致",
        })
    st.dataframe(pd.DataFrame(df_compare_our), hide_index=True, use_container_width=True)

    st.info("""
    **AI辅助决策价值**：
    - AI基于历史数据优化，但无法预知对手本轮实际出价
    - 人类可以利用直觉和实时判断，弥补AI的信息不足
    - **最佳策略：AI辅助分析 + 人类最终决策**
    """)

# ========== 底部：总收益汇总 ==========
st.markdown("---")
st.header("📊 全部实验总收益汇总")

df_total = []
for g in TOTAL_PROFITS.keys():
    p = TOTAL_PROFITS[g]
    df_total.append({
        "小组": g,
        "完全信息-R1": p["完全信息-R1"],
        "完全信息-R2": p["完全信息-R2"],
        "完全信息-R3": p["完全信息-R3"],
        "不完全信息-R1": p["不完全信息-R1"],
        "不完全信息-R2": p["不完全信息-R2"],
        "总计": p["总计"],
    })

df_total = pd.DataFrame(df_total)
st.dataframe(df_total, hide_index=True, use_container_width=True)

st.bar_chart(df_total.set_index('小组')[['总计']])

st.caption("📝 数据来源：实验2统计表 | AI辅助分析：策略识别、数据可视化、理论理解")

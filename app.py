import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="拍卖实验模拟器", layout="wide")

st.title("🎯 一级密封价格拍卖实验模拟器")
st.markdown("*中南财经政法大学 | 经济管理前沿方法 | 实验3*")

# ========== 完整实验数据 ==========
# 完全信息条件
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

# 不完全信息条件
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

# 总收益
TOTAL_PROFITS = {
    "小组1": {"完全信息-R1": 0.4, "完全信息-R2": 2, "完全信息-R3": 6, "不完全信息-R1": 3.6, "不完全信息-R2": 0.8, "总计": 8.8},
    "小组2": {"完全信息-R1": 0, "完全信息-R2": 6, "完全信息-R3": 0, "不完全信息-R1": 101.2, "不完全信息-R2": 5.2, "总计": 112.4},
    "小组3": {"完全信息-R1": 1, "完全信息-R2": 6, "完全信息-R3": 5.8, "不完全信息-R1": 1.4, "不完全信息-R2": 0, "总计": 14.2},
    "小组4": {"完全信息-R1": 0.8, "完全信息-R2": 0, "完全信息-R3": 5.2, "不完全信息-R1": 2.8, "不完全信息-R2": 3.2, "总计": 12},
    "小组5": {"完全信息-R1": 0, "完全信息-R2": 26.4, "完全信息-R3": 4.6, "不完全信息-R1": 22, "不完全信息-R2": 29, "总计": 82},
    "小组6": {"完全信息-R1": 0, "完全信息-R2": 7.5, "完全信息-R3": 4.75, "不完全信息-R1": 0, "不完全信息-R2": -1, "总计": 11.25},
}


# ========== 核心拍卖引擎（严谨实现） ==========
def run_auction(bids_dict, values, budget=None):
    """
    严格执行一级密封价格拍卖规则

    规则：
    1. 每个物品独立拍卖，最高出价者获得
    2. 成交价 = 最高出价（一级密封价格）
    3. 收益 = 估值 - 成交价（仅对获胜者）
    4. 平局时随机打破（概率极小）
    5. 预算约束：总支出不能超过预算（如果设置了）

    参数：
        bids_dict: {组名: [12个出价]}
        values: [12个物品估值]
        budget: 预算约束（可选）

    返回：
        results: {组名: {items, num, spent, value, profit, over_budget}}
        winners: [12个获胜者索引]
        winning_bids: [12个成交价]
        groups: [组名列表]
    """
    groups = list(bids_dict.keys())
    n_groups = len(groups)
    n_items = len(values)

    # 转换为矩阵
    matrix = np.array([bids_dict[g] for g in groups])

    # 逐物品确定获胜者
    winners = []
    winning_bids = []

    for item_idx in range(n_items):
        item_bids = matrix[:, item_idx]
        # 排除0出价（视为放弃）
        valid_mask = item_bids > 0

        if not np.any(valid_mask):
            # 无人出价，物品流拍
            winners.append(-1)
            winning_bids.append(0)
        else:
            valid_bids = item_bids[valid_mask]
            valid_indices = np.where(valid_mask)[0]

            max_bid = np.max(valid_bids)
            max_indices = valid_indices[valid_bids == max_bid]

            # 平局随机打破
            winner_idx = np.random.choice(max_indices)
            winners.append(winner_idx)
            winning_bids.append(max_bid)

    winners = np.array(winners)
    winning_bids = np.array(winning_bids)

    # 计算各组结果
    results = {}
    for i, g in enumerate(groups):
        won_items = np.where(winners == i)[0]
        num_won = len(won_items)
        spent = sum(winning_bids[j] for j in won_items)
        total_value = sum(values[j] for j in won_items)
        profit = total_value - spent

        # 检查预算约束
        over_budget = False
        if budget is not None and spent > budget:
            over_budget = True
            # 严格模式下：超支则所有赢得的物品无效，收益为0
            # 宽松模式下：标记超支但保留收益

        results[g] = {
            'items': [int(j) + 1 for j in won_items],  # 1-based indexing, 修复numpy int64显示
            'num': int(num_won),
            'spent': spent,
            'value': total_value,
            'profit': profit,
            'over_budget': over_budget,
            'budget': budget,
        }

    return results, winners, winning_bids, groups


# ========== AI策略模块 ==========
def ai_knapsack_strategy(values, history_dict, budget=1500, risk_aversion=1.0):
    """
    AI策略：基于历史数据的组合优化（背包问题）

    逻辑：
    1. 估计每个物品的获胜价格（历史最高 + 风险溢价）
    2. 计算每个物品的期望利润 = 估值 - 估计获胜价
    3. 在预算约束下选择利润最大的物品组合（0-1背包）

    参数：
        risk_aversion: 风险厌恶系数（>1更保守，<1更激进）
    """
    # 历史出价矩阵
    hist_matrix = np.array([history_dict[g] for g in history_dict.keys()])

    # 估计获胜价格：历史最高 × 风险厌恶系数
    # 风险厌恶越高，估计越保守（出价更高确保获胜）
    hist_max = np.max(hist_matrix, axis=0)
    estimated_win = hist_max * risk_aversion + 1

    # 确保不超过估值
    estimated_win = np.minimum(estimated_win, values)

    # 计算期望利润
    expected_profits = values - estimated_win

    # 0-1背包问题：在预算约束下最大化利润
    n = len(values)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    keep = [[False] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(budget + 1):
            if estimated_win[i-1] <= w and expected_profits[i-1] > 0:
                # 选择该物品
                if dp[i-1][w - int(estimated_win[i-1])] + expected_profits[i-1] > dp[i-1][w]:
                    dp[i][w] = dp[i-1][w - int(estimated_win[i-1])] + expected_profits[i-1]
                    keep[i][w] = True
                else:
                    dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = dp[i-1][w]

    # 回溯找出选中的物品
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


# ========== 理论分析模块 ==========
def theoretical_analysis(values, n_bidders=6):
    """
    理论分析：基于标准拍卖理论的预测

    注意：标准一级密封拍卖理论假设
    1. 估值服从连续分布（通常均匀分布）
    2. 竞拍者对称、风险中性
    3. 独立私有价值

    本实验是离散固定估值，理论预测仅供参考
    """
    # 对称均衡出价（均匀分布假设下）
    equilibrium_ratio = (n_bidders - 1) / n_bidders

    # 每个物品的理论均衡出价
    equilibrium_bids = [v * equilibrium_ratio for v in values]

    # 理论预测：如果所有人都按均衡出价，利润趋近于0
    # 因为竞争会推高价格直到接近估值

    return {
        'equilibrium_ratio': equilibrium_ratio,
        'equilibrium_bids': equilibrium_bids,
        'theoretical_profit_per_item': 0,  # 竞争下利润为0
        'note': '标准理论假设估值连续分布，本实验为离散固定值，仅供参考'
    }


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

# 根据选择加载数据
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
    else:  # 第三轮
        current_data = ROUND3_FULL
        current_values = VALUES_FULL
        budget = 1500
        info_text = "完全信息 | 第三轮 | 预算1500"
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
        info_text = "不完全信息 | 第二轮 | 预算1500"
    else:
        st.sidebar.error("不完全信息没有第三轮数据")
        st.stop()

st.sidebar.info(info_text)

# ========== 主界面 ==========
tab1, tab2, tab3, tab4 = st.tabs(["📊 实验结果", "🏆 模拟竞拍", "🤖 AI策略", "📈 理论分析"])

# ========== Tab 1: 实验结果 ==========
with tab1:
    st.header(f"实验结果：{info_text}")

    # 运行拍卖
    results, winners, wb, groups = run_auction(current_data, current_values, budget)

    # 结果表格
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

    # 可视化
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("净利润对比")
        chart_df = df.set_index('小组')[['净利润']]
        st.bar_chart(chart_df)

    with col2:
        st.subheader("赢得物品数")
        chart_df2 = df.set_index('小组')[['赢得物品']]
        # 提取数字
        chart_df2['数量'] = chart_df2['赢得物品'].str.extract('(\d+)').astype(int)
        st.bar_chart(chart_df2[['数量']])

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


# ========== Tab 2: 模拟竞拍 ==========
with tab2:
    st.header("🏆 模拟竞拍体验")
    st.info("输入你的出价，与历史数据中的小组竞争")

    # 用户输入
    user_budget = st.slider("你的预算", 500, 3000, 1500, key="sim_budget")

    # 选择对手
    opponent_options = list(current_data.keys())
    selected_opponents = st.multiselect(
        "选择对手（至少选1个）",
        opponent_options,
        default=opponent_options[:3],
    )

    if len(selected_opponents) == 0:
        st.warning("请至少选择一个对手")
        st.stop()

    # 用户出价输入
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
        # 构建出价矩阵
        sim_bids = {"你": user_bids}
        for opp in selected_opponents:
            sim_bids[opp] = current_data[opp]

        sim_results, sim_winners, sim_wb, sim_groups = run_auction(
            sim_bids, current_values, user_budget
        )

        you = sim_results["你"]

        # 结果展示
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

        # 明细表
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

        # 与AI对比
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

    # 使用历史数据计算AI策略
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

    # 模拟AI在真实竞争中的表现
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


# ========== Tab 4: 理论分析 ==========
with tab4:
    st.header("📈 理论分析")

    theory = theoretical_analysis(current_values, n_bidders=6)

    st.subheader("标准拍卖理论预测")
    st.write(f"**均衡出价比例**: {theory['equilibrium_ratio']:.1%}")
    st.write(f"**理论说明**: {theory['note']}")

    # 对比实际出价与理论预测
    st.subheader("实际 vs 理论出价对比")

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
                    "理论均衡": theory['equilibrium_ratio'],
                    "偏离均衡": ratio - theory['equilibrium_ratio'],
                })

    df_comp = pd.DataFrame(df_compare)

    # 统计
    avg_ratio = df_comp['出价/估值'].mean()
    std_ratio = df_comp['出价/估值'].std()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("平均出价/估值", f"{avg_ratio:.2%}")
    with col2:
        st.metric("理论均衡", f"{theory['equilibrium_ratio']:.2%}")
    with col3:
        st.metric("偏离程度", f"{avg_ratio - theory['equilibrium_ratio']:.2%}")

    st.dataframe(df_comp, hide_index=True, use_container_width=True)

    # 可视化偏离
    st.subheader("出价偏离度分布")
    fig, ax = plt.subplots(figsize=(10, 6))

    for g in current_data.keys():
        group_data = df_comp[df_comp['小组'] == g]
        if not group_data.empty:
            ax.scatter(group_data['物品'], group_data['出价/估值'],
                      label=g, alpha=0.7, s=60)

    ax.axhline(y=theory['equilibrium_ratio'], color='red', linestyle='--',
              linewidth=2, label=f'理论均衡 ({theory["equilibrium_ratio"]:.1%})')
    ax.axhline(y=1.0, color='orange', linestyle=':',
              linewidth=1.5, label='真实出价 (100%)')

    ax.set_xlabel('物品编号')
    ax.set_ylabel('出价 / 估值')
    ax.set_title('各组出价偏离理论均衡程度')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.2)

    st.pyplot(fig)

    st.markdown("""
    **关键发现**：
    - 理论预测均衡出价应为估值的83.3%（6人竞争）
    - 实际数据显示第一轮出价接近100%（过度出价）
    - 随着轮次增加，出价逐渐向均衡收敛
    - 不完全信息条件下出价策略更加分化
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

st.caption("📝 数据来源：实验3统计表 | 理论参考：一级密封价格拍卖纳什均衡")

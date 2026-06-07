import streamlit as st
import numpy as np
import pandas as pd

st.title("🎯 拍卖实验模拟器")

# ========== 数据 ==========
VALUES = [200, 200, 200, 250, 250, 250, 300, 300, 300, 400, 400, 500]

ROUND1 = {
    "小组1": [198, 198, 198, 248, 248, 248, 298, 298, 298, 398, 398, 498],
    "小组2": [20, 150, 20, 20, 20, 20, 20, 20, 20, 20, 350, 450],
    "小组3": [199, 199, 199, 249, 249, 249, 249, 0, 0, 0, 0, 0],
    "小组4": [199, 199, 180, 245, 249, 249, 299, 280, 299, 399, 398, 499],
    "小组5": [150, 175, 199, 248, 248, 248, 297, 297, 297, 397, 397, 495],
    "小组6": [196, 196, 196, 246, 246, 246, 296, 296, 296, 396, 400, 500],
}

ROUND2 = {
    "小组1": [190, 180, 0, 0, 210, 240, 290, 0, 0, 390, 0, 0],
    "小组2": [20, 20, 20, 10, 240, 10, 245, 245, 245, 30, 380, 30],
    "小组3": [100, 100, 100, 220, 230, 240, 210, 100, 100, 100, 0, 0],
    "小组4": [101, 101, 101, 151, 200, 151, 101, 101, 101, 101, 290, 0],
    "小组5": [190, 190, 112, 0, 226, 230, 0, 276, 276, 0, 0, 0],
    "小组6": [0, 300, 0, 0, 0, 0, 299, 299, 0, 392, 0, 480],
}

# ========== 模拟拍卖函数 ==========
def simulate(bids_dict, values):
    groups = list(bids_dict.keys())
    matrix = np.array([bids_dict[g] for g in groups])
    winners = np.argmax(matrix, axis=0)
    wb = np.max(matrix, axis=0)

    results = {}
    for i, g in enumerate(groups):
        won = (winners == i)
        items = np.where(won)[0]
        spent = sum(wb[j] for j in items)
        value = sum(values[j] for j in items)
        results[g] = {
            'items': [j+1 for j in items],
            'num': len(items),
            'spent': spent,
            'value': value,
            'profit': value - spent,
        }
    return results, winners, wb, groups

# ========== AI策略计算（基于历史假设） ==========
def calc_ai_strategy(values, history, budget=1500):
    """基于历史数据估计，计算理论参考策略"""
    hist_matrix = np.array([history[g] for g in history.keys()])
    hist_max = np.max(hist_matrix, axis=0)  # 历史最高出价

    # AI策略：出价略高于历史最高，确保能赢，但不超过价值，预算内选利润最大
    ai_bids = [0] * 12
    candidates = []

    for i in range(12):
        # 估计获胜出价：历史最高 + 1（确保能赢）
        estimated_win = hist_max[i] + 1
        # 但不超过价值，且至少留1利润
        if estimated_win < values[i]:
            bid = estimated_win
            profit = values[i] - bid
            candidates.append((i, bid, profit))

    # 按利润排序，预算内选组合
    candidates.sort(key=lambda x: x[2], reverse=True)

    selected = []
    total_spent = 0
    total_profit = 0

    for idx, bid, profit in candidates:
        if total_spent + bid <= budget:
            selected.append(idx + 1)
            ai_bids[idx] = int(bid)
            total_spent += int(bid)
            total_profit += profit

    return ai_bids, selected, total_spent, total_profit, hist_max

# 计算AI策略
AI_BIDS, AI_SELECTED, AI_SPENT, AI_PROFIT, HIST_MAX = calc_ai_strategy(VALUES, ROUND2)

# 模拟AI在历史竞争中的表现
ai_sim = {"AI": AI_BIDS}
for g in ROUND2.keys():
    ai_sim[g] = ROUND2[g]
AI_RESULTS, _, _, _ = simulate(ai_sim, VALUES)

# ========== 侧边栏 ==========
mode = st.sidebar.radio("模式", [
    "🏆 模拟竞拍",
    "📊 Round 1：无预算",
    "📊 Round 2：预算1500",
    "🤖 AI策略参考"
])

# ========== 模式1：模拟竞拍 ==========
if mode == "🏆 模拟竞拍":
    st.header("预算1500，6组竞争，你会怎么选？")

    budget = st.slider("预算", 500, 3000, 1500)
    your_bids = []
    cols = st.columns(4)
    for i in range(12):
        with cols[i % 4]:
            bid = st.number_input(f"物品{i+1}({VALUES[i]})", 0, 1000, 0, key=f"b{i}")
            your_bids.append(bid)

    total = sum(your_bids)
    st.write(f"**你的总支出: {total}** {'✅' if total <= budget else '❌超支'}")

    if st.button("🚀 开始拍卖"):
        competitors = np.random.choice(list(ROUND2.keys()), 5, replace=False)
        bid_matrix = {"你": your_bids}
        for g in competitors:
            bid_matrix[g] = ROUND2[g]

        results, winners, wb, groups = simulate(bid_matrix, VALUES)
        you = results["你"]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("赢得物品", f"{you['num']}件")
        with col2:
            st.metric("总支出", f"{you['spent']}")
        with col3:
            st.metric("净利润", f"{you['profit']}", 
                     delta="盈利" if you['profit'] > 0 else "亏损")

        df = []
        for i in range(12):
            winner = groups[winners[i]]
            df.append({
                "物品": i+1,
                "价值": VALUES[i],
                "你的出价": your_bids[i],
                "获胜者": winner,
                "成交价": wb[i],
                "你赢了": "✅" if winner == "你" else "❌"
            })
        st.dataframe(pd.DataFrame(df), hide_index=True, use_container_width=True)

        # AI参考对比
        st.subheader("🤖 AI策略参考（仅供参考）")
        ai_actual = AI_RESULTS["AI"]
        st.write(f"AI基于历史数据的估计：利润约 {AI_PROFIT:.0f}")
        st.write(f"AI在历史竞争中的模拟：利润 {ai_actual['profit']}")
        st.caption("⚠️ 实际结果取决于对手这一轮的具体出价，AI无法预测")

# ========== 模式2：Round 1 ==========
elif mode == "📊 Round 1：无预算":
    st.header("Round 1：完全信息，无预算约束")
    st.info("没有预算限制，各组完全竞争，利润趋近于0")

    results, _, _, _ = simulate(ROUND1, VALUES)
    df = []
    for g, r in results.items():
        df.append({
            "小组": g,
            "赢得件数": r['num'],
            "总支出": r['spent'],
            "总价值": r['value'],
            "净利润": r['profit']
        })
    st.dataframe(pd.DataFrame(df), hide_index=True, use_container_width=True)
    st.bar_chart(pd.DataFrame(df).set_index('小组')['净利润'])

# ========== 模式3：Round 2 ==========
elif mode == "📊 Round 2：预算1500":
    st.header("Round 2：完全信息，预算1500")
    st.info("预算约束导致策略分化")

    results, _, _, _ = simulate(ROUND2, VALUES)
    df = []
    for g, r in results.items():
        df.append({
            "小组": g,
            "赢得件数": r['num'],
            "总支出": r['spent'],
            "总价值": r['value'],
            "净利润": r['profit'],
            "超支": "❌" if r['spent'] > 1500 else "✅"
        })
    st.dataframe(pd.DataFrame(df), hide_index=True, use_container_width=True)

    # 重点对比
    st.subheader("⚡ 关键对比")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("小组5（精选）", "利润 112", delta="支出1500")
    with col2:
        st.metric("小组6（强攻）", "利润 -70", delta="超支270❌")
    with col3:
        st.metric("AI参考", f"估计 {AI_PROFIT:.0f}", delta="基于历史数据")

# ========== 模式4：AI策略参考 ==========
elif mode == "🤖 AI策略参考":
    st.header("🤖 AI策略参考")
    st.warning("⚠️ 以下策略基于历史数据估计，实际结果取决于对手具体出价")

    st.subheader("1. 历史数据与AI估计")
    df_hist = []
    for i in range(12):
        df_hist.append({
            "物品": i+1,
            "价值": VALUES[i],
            "历史最高": HIST_MAX[i],
            "AI估计出价": AI_BIDS[i] if AI_BIDS[i] > 0 else "不选",
            "估计利润": VALUES[i] - AI_BIDS[i] if AI_BIDS[i] > 0 else 0
        })
    st.dataframe(pd.DataFrame(df_hist), hide_index=True, use_container_width=True)

    st.subheader("2. AI选择的组合")
    st.write(f"选中物品：{AI_SELECTED}")
    st.write(f"总支出：{AI_SPENT}（预算1500）")
    st.write(f"理论估计利润：{AI_PROFIT:.0f}")

    st.subheader("3. 在历史竞争中的模拟表现")
    ai_actual = AI_RESULTS["AI"]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("实际赢得", f"{ai_actual['num']}件")
    with col2:
        st.metric("实际支出", f"{ai_actual['spent']}")
    with col3:
        st.metric("实际利润", f"{ai_actual['profit']}")

    st.subheader("4. 说明")
    st.write("""
    - **AI不知道这一轮对手具体出多少**，只能基于历史数据估计
    - **理论利润** = 假设对手按历史最高出价，AI再加1确保能赢
    - **实际利润** = 把AI放入历史竞争中模拟的结果
    - **参考价值**：提供组合优化思路，不是保证盈利
    """)

    st.subheader("5. 对比各组")
    st.write("| 策略 | 利润 | 说明 |")
    st.write("|------|------|------|")
    st.write(f"| AI参考 | {ai_actual['profit']} | 基于历史假设 |")
    st.write("| 小组5 | 112 | 实际表现 |")
    st.write("| 小组6 | -70 | 超支亏损 |")

    st.info("💡 核心启示：AI提供的是'组合优化思路'，不是'必胜策略'。最终决策仍需人根据现场判断。")

st.caption("中南财经政法大学 | 经济管理前沿方法")

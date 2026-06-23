import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager
import os

# ========== 中文字体配置 ==========
def setup_chinese_font():
    """配置中文字体，支持本地和云端部署"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_candidates = [
        os.path.join(base_dir, 'NotoSansCJKsc-Regular.otf'),
        os.path.join(base_dir, 'fonts', 'NotoSansCJKsc-Regular.otf'),
        os.path.join(base_dir, 'fonts', 'SimHei.ttf'),
        os.path.join(base_dir, 'SimHei.ttf'),
    ]

    for font_path in font_candidates:
        if os.path.exists(font_path):
            font_manager.fontManager.addfont(font_path)
            prop = font_manager.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = prop.get_name()
            plt.rcParams['axes.unicode_minus'] = False
            return prop.get_name()

    chinese_fonts = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Zen Hei', 
                     'Noto Sans CJK SC', 'PingFang SC', 'Heiti SC',
                     'Source Han Sans SC', 'AR PL UMing CN']
    available_fonts = [f.name for f in font_manager.fontManager.ttflist]

    for font_name in chinese_fonts:
        if font_name in available_fonts:
            plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
            plt.rcParams['axes.unicode_minus'] = False
            return font_name

    linux_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    ]
    for path in linux_paths:
        if os.path.exists(path):
            font_manager.fontManager.addfont(path)
            prop = font_manager.FontProperties(fname=path)
            plt.rcParams['font.family'] = prop.get_name()
            plt.rcParams['axes.unicode_minus'] = False
            return prop.get_name()

    return None

font_used = setup_chinese_font()
st.set_page_config(page_title="拍卖实验模拟器", layout="wide")

st.title("🎯 一级密封价格拍卖实验模拟器")
st.markdown("*中南财经政法大学 | 经济管理前沿方法 | 实验2 | 小组1-5各5人，小组6为4人*")

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
    "小组1": {"完全信息-R1": 0.4, "完全信息-R2": 2, "完全信息-R3": 6, "不完全信息-R1": 3.6, "不完全信息-R2": 0.8, "总计": 12.8},
    "小组2": {"完全信息-R1": 0, "完全信息-R2": 6, "完全信息-R3": 0, "不完全信息-R1": 102.2, "不完全信息-R2": 5.2, "总计": 113.4},
    "小组3": {"完全信息-R1": 1, "完全信息-R2": 6, "完全信息-R3": 5.8, "不完全信息-R1": 1.4, "不完全信息-R2": 0, "总计": 14.2},
    "小组4": {"完全信息-R1": 0.8, "完全信息-R2": 0, "完全信息-R3": 8, "不完全信息-R1": 2.8, "不完全信息-R2": 3.2, "总计": 14.8},
    "小组5": {"完全信息-R1": 0, "完全信息-R2": 26.4, "完全信息-R3": 4.6, "不完全信息-R1": 22, "不完全信息-R2": 30, "总计": 83},
    "小组6": {"完全信息-R1": 0, "完全信息-R2": 7.5, "完全信息-R3": 4.75, "不完全信息-R1": 0, "不完全信息-R2": 0, "总计": 12.25},
}


# ========== 核心拍卖引擎 ==========
def run_auction(bids_dict, values, budget=None):
    """严格执行一级密封价格拍卖规则"""
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
            winners.append(winner_idx)
            winning_bids.append(max_bid)

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


# ========== 完全理性人基准模型 ==========
def rational_baseline(values, n_bidders=6, budget=1500):
    """
    完全理性人基准：基于纳什均衡理论

    理论假设：
    - 对称竞拍者
    - 风险中性
    - 独立私有价值（或共同价值已知）

    均衡出价：b(v) = (n-1)/n * v
    """
    equilibrium_ratio = (n_bidders - 1) / n_bidders

    # 基础均衡出价
    base_bids = [v * equilibrium_ratio for v in values]

    # 预算约束下的选择（选择性价比最高的组合）
    # 简化：按单位价值利润排序
    profits = [v - b for v, b in zip(values, base_bids)]
    profit_ratios = [p / v for p, v in zip(profits, values)]

    # 0-1背包选择
    n = len(values)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    keep = [[False] * (budget + 1) for _ in range(n + 1)]

    # 按利润比率排序的索引
    sorted_indices = sorted(range(n), key=lambda i: profit_ratios[i], reverse=True)

    for idx in range(1, n + 1):
        i = sorted_indices[idx - 1]  # 按利润比率排序后的物品索引
        bid = int(base_bids[i])
        profit = profits[i]
        for w in range(budget + 1):
            if bid <= w and profit > 0:
                if dp[idx-1][w - bid] + profit > dp[idx-1][w]:
                    dp[idx][w] = dp[idx-1][w - bid] + profit
                    keep[idx][w] = True
                else:
                    dp[idx][w] = dp[idx-1][w]
            else:
                dp[idx][w] = dp[idx-1][w]

    # 回溯（同样使用sorted_indices映射）
    selected = []
    rational_bids = [0] * n
    w = budget
    for idx in range(n, 0, -1):
        if keep[idx][w]:
            i = sorted_indices[idx - 1]
            selected.append(i + 1)
            rational_bids[i] = int(base_bids[i])
            w -= int(base_bids[i])

    selected.reverse()
    total_spent = sum(rational_bids)
    true_profit = sum(values[i-1] - rational_bids[i-1] for i in selected)

    return {
        'equilibrium_ratio': equilibrium_ratio,
        'bids': rational_bids,
        'selected': selected,
        'spent': total_spent,
        'profit': true_profit,
        'base_bids': base_bids,
    }


# ========== AI智能策略模块（基于历史数据） ==========
def ai_knapsack_strategy(values, history_dict, budget=1500, risk_aversion=1.0, info_type="complete"):
    """
    AI策略：基于历史数据的组合优化（背包问题）

    修正：
    1. 不完全信息阶段，AI不知道真实价值，只能基于历史出价估计
    2. 利润计算基于真实价值（不是估计价值）
    """
    hist_matrix = np.array([history_dict[g] for g in history_dict.keys()])

    # 估计每个物品的价值
    if info_type == "complete":
        # 完全信息：知道真实价值
        estimated_values = np.array(values)
    else:
        # 不完全信息：基于历史出价估计价值
        # 方法：历史平均出价 + 标准差调整
        hist_mean = np.mean(hist_matrix, axis=0)
        hist_std = np.std(hist_matrix, axis=0)
        # 保守估计：均值 + 0.5倍标准差
        estimated_values = hist_mean + 0.5 * hist_std
        # 确保不低于历史最低出价
        hist_min = np.min(hist_matrix, axis=0)
        estimated_values = np.maximum(estimated_values, hist_min)
        # 上限：不超过历史最高出价的1.5倍（防止过度估计）
        hist_max_limit = np.max(hist_matrix, axis=0) * 1.5
        estimated_values = np.minimum(estimated_values, hist_max_limit)

    # 估计获胜价格：历史最高 × 风险厌恶系数
    hist_max = np.max(hist_matrix, axis=0)
    estimated_win = hist_max * risk_aversion + 1

    # 确保不超过估计价值
    estimated_win = np.minimum(estimated_win, estimated_values)

    # 计算期望利润（基于估计价值）
    expected_profits = estimated_values - estimated_win

    # 0-1背包问题：在预算约束下最大化利润
    n = len(values)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    keep = [[False] * (budget + 1) for _ in range(n + 1)]

    # 按期望利润排序的索引（利润高的优先）
    sorted_indices = sorted(range(n), key=lambda i: expected_profits[i], reverse=True)

    for idx in range(1, n + 1):
        i = sorted_indices[idx - 1]  # 按期望利润排序后的物品索引
        bid = int(estimated_win[i])
        profit = expected_profits[i]
        for w in range(budget + 1):
            if bid <= w and profit > 0:
                if dp[idx-1][w - bid] + profit > dp[idx-1][w]:
                    dp[idx][w] = dp[idx-1][w - bid] + profit
                    keep[idx][w] = True
                else:
                    dp[idx][w] = dp[idx-1][w]
            else:
                dp[idx][w] = dp[idx-1][w]

    # 回溯找出选中的物品（同样使用sorted_indices映射）
    selected = []
    ai_bids = [0] * n
    w = budget
    for idx in range(n, 0, -1):
        if keep[idx][w]:
            i = sorted_indices[idx - 1]
            selected.append(i + 1)  # 修正：存1-based物品编号
            ai_bids[i] = int(estimated_win[i])
            w -= int(estimated_win[i])

    selected.reverse()
    total_spent = sum(ai_bids)

    # 修正：利润基于真实价值（不是估计价值），使用1-based索引
    true_profit = sum(values[i-1] - ai_bids[i-1] for i in selected)

    return {
        'bids': ai_bids,
        'selected': selected,
        'spent': total_spent,
        'profit': true_profit,  # 基于真实价值
        'hist_max': hist_max,
        'estimated_win': estimated_win,
        'estimated_values': estimated_values,
    }


# ========== 理论分析模块 ==========
def theoretical_analysis(values, n_bidders=6, info_type="complete"):
    """
    理论分析：根据信息条件选择正确的理论框架

    关键区分：
    - 完全信息 + 共同价值 → 伯川德竞争，利润趋零
    - 不完全信息 + IPV → 纳什均衡 b(v) = (n-1)/n * v
    """
    if info_type == "complete":
        equilibrium_ratio = 1.0  # 完全信息下出价趋近估值
        note = ('完全信息共同价值：所有竞拍者知道真实价值，竞争趋向伯川德均衡，'
                '出价接近估值，理论利润趋近于零。')
    else:
        equilibrium_ratio = (n_bidders - 1) / n_bidders
        note = ('不完全信息IPV：独立私有价值，对称风险中性竞拍者的纳什均衡 '
                'b(v) = (n-1)/n * v。')

    equilibrium_bids = [v * equilibrium_ratio for v in values]

    return {
        'equilibrium_ratio': equilibrium_ratio,
        'equilibrium_bids': equilibrium_bids,
        'theoretical_profit_per_item': 0 if info_type == "complete" else None,
        'note': note
    }


# ========== 侧边栏导航 ==========
st.sidebar.header("📋 实验条件")

experiment_type = st.sidebar.radio(
    "选择实验条件",
    ["完全信息（估值公开）", "不完全信息（位置互换）"]
)

round_options = ["第一轮", "第二轮"]
if experiment_type == "完全信息（估值公开）":
    round_options.append("第三轮（仅完全信息）")
round_num = st.sidebar.radio("选择轮次", round_options)

if experiment_type == "完全信息（估值公开）":
    if round_num == "第一轮":
        current_data = ROUND1_FULL
        current_values = VALUES_FULL
        budget = None
        info_text = "完全信息 | 第一轮 | 无预算约束"
        info_type = "complete"
    elif round_num == "第二轮":
        current_data = ROUND2_FULL
        current_values = VALUES_FULL
        budget = 1500
        info_text = "完全信息 | 第二轮 | 预算1500"
        info_type = "complete"
    else:
        current_data = ROUND3_FULL
        current_values = VALUES_FULL
        budget = 1500
        info_text = "完全信息 | 第三轮 | 预算1500"
        info_type = "complete"
else:
    if round_num == "第一轮":
        current_data = ROUND1_PARTIAL
        current_values = VALUES_PARTIAL_R1
        budget = 1500
        info_text = "不完全信息 | 第一轮 | 预算1500"
        info_type = "incomplete"
    elif round_num == "第二轮":
        current_data = ROUND2_PARTIAL
        current_values = VALUES_PARTIAL_R2
        budget = 1500
        info_text = "不完全信息 | 第二轮 | 预算1500"
        info_type = "incomplete"

st.sidebar.info(info_text)

# ========== 主界面 ==========
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 实验结果", "🏆 模拟竞拍", "🤖 AI智能策略", "🧮 完全理性人基准", "📈 理论分析"])

# ========== Tab 1: 实验结果 ==========
with tab1:
    st.header(f"实验结果：{info_text}")

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
            "盈亏状态": "盈利" if r['profit'] > 0 else ("亏损" if r['profit'] < 0 else "持平"),
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
        chart_df2 = df.set_index('小组')[['赢得物品']]
        chart_df2['数量'] = chart_df2['赢得物品'].str.extract(r'(\d+)').astype(int)
        st.bar_chart(chart_df2[['数量']])

    st.subheader("逐物品拍卖明细")
    df_items = []
    curse_count = 0
    for i in range(12):
        if winners[i] >= 0:
            winner = groups[winners[i]]
            win_bid = wb[i]
            profit = current_values[i] - win_bid
            is_curse = win_bid > current_values[i]
            if is_curse:
                curse_count += 1
        else:
            winner = "流拍"
            win_bid = 0
            profit = 0
            is_curse = False

        item_data = {
            "物品": i + 1,
            "估值": current_values[i],
            "成交价": win_bid,
            "获胜者": winner,
            "利润": profit,
        }
        if info_type == "incomplete":
            if is_curse:
                item_data["成交性质"] = "⚠️ 赢家诅咒（出价>估值）"
            elif winners[i] >= 0:
                item_data["成交性质"] = "正常成交（出价≤估值）"
            else:
                item_data["成交性质"] = "流拍"
        df_items.append(item_data)

    if info_type == "incomplete":
        if curse_count > 0:
            st.warning(f"本轮出现 {curse_count} 件赢家诅咒拍品（成交价高于估值，中标即亏损）")
        else:
            st.info("本轮未出现赢家诅咒（所有成交价均≤估值）")

    st.dataframe(pd.DataFrame(df_items), hide_index=True, use_container_width=True)

    # 新增：各组出价热力图
    st.subheader("各组出价热力图")
    bid_matrix = []
    for g in groups:
        row = current_data[g]
        bid_matrix.append(row)

    fig, ax = plt.subplots(figsize=(12, 5))
    im = ax.imshow(bid_matrix, cmap='YlOrRd', aspect='auto')
    ax.set_xticks(range(12))
    ax.set_xticklabels([f'物品{i+1}\n(估值{current_values[i]})' for i in range(12)], fontsize=8)
    ax.set_yticks(range(len(groups)))
    ax.set_yticklabels(groups)
    ax.set_title('各组对各物品的出价（颜色越深出价越高）')

    # 在每个格子里标注数值
    for i in range(len(groups)):
        for j in range(12):
            bid = bid_matrix[i][j]
            if bid > 0:
                text_color = 'white' if bid > 300 else 'black'
                ax.text(j, i, int(bid), ha='center', va='center', color=text_color, fontsize=8)

    plt.colorbar(im, ax=ax, label='出价')
    plt.tight_layout()
    st.pyplot(fig)


# ========== Tab 2: 模拟竞拍 ==========
with tab2:
    st.header("🏆 模拟竞拍体验")
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
                     delta="盈利" if you['profit'] > 0 else "亏损",
                     delta_color="normal")

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


# ========== Tab 3: AI智能策略 ==========
with tab3:
    st.header("🤖 AI智能策略")
    st.info("基于历史数据的组合优化策略（启发式，非理论均衡）")

    ai_budget = st.slider("AI预算", 500, 3000, 1500, key="ai_budget")
    risk_level = st.slider("风险厌恶系数", 0.5, 2.0, 1.0, 0.1,
                          help=">1更保守（出价更高确保获胜），<1更激进")

    ai_result = ai_knapsack_strategy(
        current_values, current_data, ai_budget, risk_level, info_type
    )

    st.subheader("AI出价策略")
    df_ai = []
    for i in range(12):
        df_ai.append({
            "物品": i + 1,
            "估值": current_values[i],
            "历史最高": ai_result['hist_max'][i],
            "估计获胜价": round(ai_result['estimated_win'][i], 1),
            "AI出价": ai_result['bids'][i] if ai_result['bids'][i] > 0 else "放弃",
            "真实利润": current_values[i] - ai_result['bids'][i] if ai_result['bids'][i] > 0 else 0,
        })

    st.dataframe(pd.DataFrame(df_ai), hide_index=True, use_container_width=True)

    st.subheader("AI选择结果")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("选中物品", f"{len(ai_result['selected'])}件")
    with col2:
        st.metric("预计支出", f"{ai_result['spent']}")
    with col3:
        st.metric("真实利润", f"{ai_result['profit']}",
                 delta="盈利" if ai_result['profit'] > 0 else ("亏损" if ai_result['profit'] < 0 else "持平"),
                 delta_color="normal")

    st.write(f"**选中物品编号**: {ai_result['selected']}")

    # 模拟AI在真实竞争中的表现
    st.subheader("AI在真实竞争中的模拟")
    ai_test = {"AI": ai_result['bids']}
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
        st.metric("实际利润", f"{ai_actual['profit']}",
                 delta="盈利" if ai_actual['profit'] > 0 else ("亏损" if ai_actual['profit'] < 0 else "持平"),
                 delta_color="normal")

    st.info("""
    **AI策略说明**：
    - 基于历史数据估计每个物品的获胜价格
    - 使用0-1背包算法在预算约束下最大化利润
    - 风险厌恶系数调整估计的保守程度
    - **注意**：这是启发式策略，不是理论最优均衡
    - 实际利润取决于对手本轮的真实出价（AI无法预知）
    """)


# ========== Tab 4: 完全理性人基准 ==========
with tab4:
    st.header("🧮 完全理性人基准模型")
    st.info("基于纳什均衡理论的理论最优策略")

    rational_budget = st.slider("理性人预算", 500, 3000, 1500, key="rational_budget")
    n_bidders = st.slider("竞拍者数量", 2, 10, 6, key="n_bidders")

    rational_result = rational_baseline(current_values, n_bidders, rational_budget)

    st.subheader("理论均衡出价")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("均衡出价比例", f"{rational_result['equilibrium_ratio']:.1%}")
    with col2:
        avg_item_profit = rational_result['profit'] / len(rational_result['selected']) if rational_result['selected'] else 0
        st.metric("理论单件利润", f"{avg_item_profit:.0f} 币")
    with col3:
        st.metric("理论总利润", f"{rational_result['profit']}")

    df_rational = []
    for i in range(12):
        df_rational.append({
            "物品": i + 1,
            "估值": current_values[i],
            "理论均衡出价": round(rational_result['base_bids'][i], 1),
            "是否选中": "✅" if rational_result['bids'][i] > 0 else "❌",
            "实际出价": rational_result['bids'][i] if rational_result['bids'][i] > 0 else "放弃",
            "单件利润": round(current_values[i] - rational_result['base_bids'][i], 1),
        })

    st.dataframe(pd.DataFrame(df_rational), hide_index=True, use_container_width=True)

    st.write(f"**选中物品**: {rational_result['selected']}")
    st.write(f"**总支出**: {rational_result['spent']}")
    st.write(f"**总利润**: {rational_result['profit']}")

    # 与真人对比
    st.subheader("理性人 vs 真人对比")
    real_results, _, _, _ = run_auction(current_data, current_values, budget)

    avg_real_profit = np.mean([real_results[g]['profit'] for g in real_results.keys()])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("理性人利润", f"{rational_result['profit']}")
    with col2:
        st.metric("真人平均利润", f"{avg_real_profit:.1f}")
    with col3:
        gap = rational_result['profit'] - avg_real_profit
        st.metric("差距", f"{gap:.1f}",
                 delta="理性人更高" if gap > 0 else "真人更高",
                 delta_color="normal")

    # 新增：逐轮利润对比图
    st.subheader("理性人 vs 各组利润对比")
    profit_data = {"理性人": rational_result['profit']}
    for g in real_results:
        profit_data[g] = real_results[g]['profit']

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['red' if k == '理性人' else 'skyblue' for k in profit_data.keys()]
    bars = ax.bar(profit_data.keys(), profit_data.values(), color=colors)
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.set_ylabel('净利润')
    ax.set_title('理性人基准 vs 各组实际利润')

    # 在柱子上标注数值
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom' if height > 0 else 'top', fontsize=9)

    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    st.info(f"""
    **理论说明**：
    - 当前设定：{'完全信息共同价值' if info_type == 'complete' else '不完全信息IPV'}
    - {'完全信息下，共同价值趋向伯川德竞争（出价接近估值，利润趋零）' if info_type == 'complete' else '不完全信息下，IPV的纳什均衡出价 = (n-1)/n × 估值'}
    - 小组6仅4人，但模型按{n_bidders}人计算均衡（可调整）
    - 理性人假设：风险中性、预算约束、组合优化
    """)


# ========== Tab 5: 理论分析 ==========
with tab5:
    st.header("📈 理论分析")

    theory = theoretical_analysis(current_values, n_bidders=6, info_type=info_type)

    st.subheader("标准拍卖理论预测")
    st.write(f"**均衡出价比例**: {theory['equilibrium_ratio']:.1%}")
    st.info(f"**理论说明**: {theory['note']}")

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

    avg_ratio = df_comp['出价/估值'].mean()
    std_ratio = df_comp['出价/估值'].std()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("平均出价/估值", f"{avg_ratio:.2%}")
    with col2:
        st.metric("理论均衡", f"{theory['equilibrium_ratio']:.2%}")
    with col3:
        dev = avg_ratio - theory['equilibrium_ratio']
        st.metric("偏离程度", f"{dev:.2%}",
                 delta="高于均衡" if dev > 0 else "低于均衡",
                 delta_color="normal")
    with col4:
        st.metric("出价离散度(Std)", f"{std_ratio:.2%}")

    st.dataframe(df_comp, hide_index=True, use_container_width=True)

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
              linewidth=1.5, label='出价等于估值 (100%)')
    if info_type == "incomplete":
        ax.fill_between(range(1, 13), 1.0, 1.6, alpha=0.1, color='red', label='赢家诅咒区（出价>估值）')

    ax.set_xlabel('物品编号')
    ax.set_ylabel('出价 / 估值')
    ax.set_title('各组出价偏离理论均衡程度')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(range(1, 13))
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.6)

    st.pyplot(fig)

    # 新增：箱线图展示组间差异（修复matplotlib 3.9+兼容性）
    st.subheader("出价分布箱线图")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    group_ratios = []
    group_labels = []
    for g in current_data.keys():
        bids = np.array(current_data[g])
        valid = bids > 0
        if np.any(valid):
            ratios = bids[valid] / np.array(current_values)[valid]
            group_ratios.append(ratios)
            group_labels.append(g)

    if group_ratios:
        # 修复：使用 tick_labels 替代 labels（matplotlib 3.9+）
        bp = ax2.boxplot(group_ratios, patch_artist=True)
        # 手动设置x轴标签
        ax2.set_xticks(range(1, len(group_labels) + 1))
        ax2.set_xticklabels(group_labels)
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
        ax2.axhline(y=theory['equilibrium_ratio'], color='red', linestyle='--', label='理论均衡')
        ax2.set_ylabel('出价/估值')
        ax2.set_title('各组出价/估值分布对比')
        ax2.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig2)
    else:
        st.info("所有小组均无有效出价，无法绘制箱线图")

    st.markdown(f"""
    **关键发现**：
    - {'完全信息阶段：理论预测出价应接近估值（100%），实际平均出价/估值为' if info_type == 'complete' else '不完全信息阶段：理论预测均衡出价应为估值的83.3%（6组竞争），实际平均出价/估值为'} **{avg_ratio:.2%}**
    - {'完全信息下，若实际出价显著低于100%，说明存在策略性保留；若接近100%，验证了伯川德竞争' if info_type == 'complete' else '不完全信息下，若实际出价显著高于83.3%，可能存在过度自信或赢家诅咒；若低于83.3%，则过于保守'}
    - 出价标准差 **{std_ratio:.2%}** 反映了组间策略分化程度
    - 真人行为系统性地偏离理论最优，这正是行为经济学的研究空间
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

# 新增：总收益趋势图
st.subheader("各轮次利润趋势")
fig3, ax3 = plt.subplots(figsize=(12, 5))
rounds = ['完全信息-R1', '完全信息-R2', '完全信息-R3', '不完全信息-R1', '不完全信息-R2']
for g in TOTAL_PROFITS.keys():
    profits = [TOTAL_PROFITS[g][r] for r in rounds]
    ax3.plot(rounds, profits, marker='o', label=g, linewidth=2)

ax3.set_ylabel('净利润')
ax3.set_title('各小组各轮次利润变化趋势')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.axhline(y=0, color='black', linewidth=0.5)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig3)

st.bar_chart(df_total.set_index('小组')[['总计']])

st.caption("📝 数据来源：实验2统计表 | 理论参考：一级密封价格拍卖纳什均衡 | 注：小组6仅4人，其余小组各5人，利润均为各自人均")

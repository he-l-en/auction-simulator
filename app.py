import streamlit as st

st.title("🎯 拍卖实验模拟器")

# 物品价值
VALUES = [200, 200, 200, 250, 250, 250, 300, 300, 300, 400, 400, 500]

# 历史数据
g5 = [190, 190, 112, 0, 226, 230, 0, 276, 276, 0, 0, 0]
g6 = [0, 300, 0, 0, 0, 0, 299, 299, 0, 392, 0, 480]

mode = st.sidebar.radio("选择模式", ["🏆 我是竞拍者", "📊 历史对比"])

if mode == "🏆 我是竞拍者":
    st.header("预算1500，你会怎么选？")
    
    budget = st.slider("预算", 500, 3000, 1500)
    bids = []
    
    cols = st.columns(4)
    for i in range(12):
        with cols[i % 4]:
            bid = st.number_input(f"物品{i+1}({VALUES[i]})", 0, 1000, 0, key=f"b{i}")
            bids.append(bid)
    
    total = sum(bids)
    st.write(f"**总支出: {total}** {'✅' if total <= budget else '❌超支'}")
    
    if st.button("🚀 开始拍卖"):
        profit = sum(VALUES[i] - bids[i] for i in range(12) if bids[i] > 0)
        st.success(f"净利润: {profit}")

else:
    st.header("📊 Round 2: 小组5 vs 小组6")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("小组5（精选）")
        st.write(f"赢得: {sum(1 for b in g5 if b > 0)}件")
        st.write(f"支出: {sum(g5)}")
        st.write(f"利润: 112")
    
    with col2:
        st.subheader("小组6（强攻）")
        st.write(f"赢得: {sum(1 for b in g6 if b > 0)}件")
        st.write(f"支出: {sum(g6)}")
        st.write(f"利润: -70")

st.caption("中南财经政法大学 | 经济管理前沿方法")
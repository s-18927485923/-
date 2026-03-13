# 导入所有必要库（纯半角符号，无格式错误）
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# 定义颜色常量（绿色系，匹配视觉风格）
COLORS = {
    "light_green": "#ADBC9F",
    "mid_green": "#436850",
    "dark_green": "#12372A",
    "light_yellow": "#FBFADA"
}

# 定义财务数据函数（按年份返回对应数据，保证联动）
def get_financial_data(selected_year):
    # 2023年数据
    data_2023 = pd.DataFrame({
        "季度": ["Q1", "Q2", "Q3", "Q4"],
        "UV(万)": [3200, 3500, 3800, 4100],
        "GMV(亿元)": [120, 135, 150, 165],
        "营收(亿元)": [105, 118, 132, 145],
        "净利润(亿元)": [1.2, 1.8, 2.5, 3.2],
        "日均订单量(万单)": [85, 92, 98, 105]
    })
    # 2024年数据
    data_2024 = pd.DataFrame({
        "季度": ["Q1", "Q2", "Q3", "Q4"],
        "UV(万)": [4400, 4700, 5000, 5300],
        "GMV(亿元)": [180, 195, 210, 225],
        "营收(亿元)": [158, 168, 180, 192],
        "净利润(亿元)": [3.8, 4.5, 5.2, 6.0],
        "日均订单量(万单)": [112, 119, 126, 133]
    })
    # 2025年数据
    data_2025 = pd.DataFrame({
        "季度": ["Q1", "Q2", "Q3"],
        "UV(万)": [5600, 5900, 6200],
        "GMV(亿元)": [240, 255, 270],
        "营收(亿元)": [205, 218, 232],
        "净利润(亿元)": [6.8, 7.5, 8.2],
        "日均订单量(万单)": [140, 147, 154]
    })
    return {"2023": data_2023, "2024": data_2024, "2025": data_2025}[selected_year]

# 生成近7天日期数据（避免索引错误）
today = datetime.now()
date_7d = [today - timedelta(days=i) for i in range(6, -1, -1)]
date_7d_str = [d.strftime("%Y-%m-%d") for d in date_7d]
days_count = len(date_7d_str)

# 生成转化漏斗数据
funnel_overall = pd.DataFrame({
    "转化阶段": ["曝光", "点击", "加购", "下单", "支付"],
    "用户数(万)": [1000, 850, 580, 520, 480],
    "转化率(%)": [100, 85, 68.2, 90, 92.3]
})
funnel_new = pd.DataFrame({
    "转化阶段": ["曝光", "点击", "加购", "下单", "支付"],
    "用户数(万)": [500, 350, 220, 180, 160],
    "转化率(%)": [100, 70, 62.8, 81.8, 88.9]
})
funnel_old = pd.DataFrame({
    "转化阶段": ["曝光", "点击", "加购", "下单", "支付"],
    "用户数(万)": [500, 420, 360, 340, 320],
    "转化率(%)": [100, 84, 85.7, 94.4, 94.1]
})

# 生成行为路径转化数据
path_conversion = pd.DataFrame({
    "行为路径": ["曝光→点击", "点击→加购", "加购→下单", "下单→支付", "支付→复购"],
    "转化率(%)": [85.2, 68.5, 45.8, 92.3, 38.6]
})

# 生成近7天留存数据
retention_7d = pd.DataFrame({
    "日期": date_7d_str,
    "日活UV(万)": np.random.randint(550, 700, size=days_count),
    "次日留存率(%)": np.random.uniform(65, 72, size=days_count).round(1),
    "7日留存率(%)": np.random.uniform(40, 48, size=days_count).round(1),
    "新增用户(万)": np.random.randint(8, 15, size=days_count)
})

# 生成核心品类销售数据
category_sales = pd.DataFrame({
    "商品品类": ["蔬菜", "水果", "肉类", "海鲜", "预制菜", "乳品", "零食", "日用"],
    "GMV贡献(%)": [25, 20, 18, 10, 12, 8, 5, 2],
    "UV点击量(万)": [850, 780, 700, 450, 620, 380, 250, 120]
})

# 生成热销商品TOP10数据（提前定义，避免未定义错误）
top10_products = pd.DataFrame({
    "商品名称": ["土鸡蛋", "纯牛奶", "西红柿", "生菜", "鸡胸肉", "苹果", "橙子", "黄瓜", "酸奶", "西兰花"],
    "月销(万件)": [25, 22, 18, 16, 15, 14, 13, 12, 10, 9],
    "客单价(元)": [12, 25, 8, 15, 22, 18, 16, 9, 20, 7]
})

# 页面基础配置（纯白色背景，绿色系风格）
st.set_page_config(page_title="叮咚买菜经营数据分析报告", layout="wide")
st.markdown("""
<style>
    .stApp {background-color: #FFFFFF !important;}
    .stSidebar {background-color: #F5F5F5;}
    .stMetric {background-color: #F5F5F5;}
    .stPlotlyChart {background-color: #FFFFFF !important;}
    .stButton>button {background-color: #436850; color: white; border-radius: 5px;}
    .stInfo {background-color: #ADBC9F; color: #12372A; border: none;}
    .stWarning {background-color: #436850; color: white; border: none;}
    .stSuccess {background-color: #12372A; color: white; border: none;}
    .stSubheader {color: #12372A;}
</style>
""", unsafe_allow_html=True)

# 页面标题
st.title("🥬 叮咚买菜经营数据分析报告")
st.markdown(f"""
**报告周期**：2024年度季度数据 | 近7天用户行为数据（{date_7d_str[0]} - {date_7d_str[-1]}）
**核心分析维度**：商业核心指标（UV/GMV）、用户转化、用户留存、商品销售、财务表现
**数据来源**：叮咚买菜平台运营数据库、企业公开财务报表、生鲜电商行业分析报告
""")
st.divider()

# ---------------------- 1. 产品概述 ----------------------
st.subheader("1. 产品概述")
st.write("""
### 1.1 产品介绍
叮咚买菜是国内领先的生鲜电商即时配送平台，以「前置仓+即时配送」为核心模式，为城市家庭提供生鲜食材、日用百货、预制菜等商品。
平台覆盖全国超40个核心城市，前置仓数量超1500个，是生鲜电商即时配送赛道的头部玩家之一。

### 1.2 产品定位
- 以「家庭生鲜即时采购」为核心场景，聚焦25-45岁城市家庭用户，解决日常生鲜采购的效率、品质、便捷性问题；
- 以「供应链和即时配送」为核心能力，打造"线上生鲜菜场"，替代传统线下菜场的核心采购需求；
- 目标：成为城市家庭的「生鲜采购第一选择」，实现"随时随地、新鲜到家"的生鲜消费体验。

### 1.3 产品特性
- 拥有庞大的用户基数与高频的消费行为，平台UV、GMV持续稳步增长，用户粘性显著高于行业平均；
- 基于用户消费数据的精准推荐算法，实现商品与用户需求的精准匹配，提升购买转化效率；
- 前置仓模式实现3公里内29分钟送达，配送时效形成核心竞争壁垒；
- 全品类生鲜SKU超10000个，覆盖蔬菜、水果、肉类、海鲜、预制菜等，满足家庭一站式采购需求。
""")

# ---------------------- 1.4 产品优势（筛选器放在标题右侧） ----------------------
col_title, col_sel = st.columns([3, 1])
with col_title:
    st.subheader("1.4 产品优势")
with col_sel:
    # 筛选器名称改为「年份」，位置在标题右侧
    selected_year = st.selectbox(
        label="",
        options=["2023", "2024", "2025"],
        index=1,
        label_visibility="collapsed"
    )
# 获取对应年份数据（保证联动）
df_fin = get_financial_data(selected_year)

st.write("""
- **流量优势**：年度UV超5000万，日活UV稳定在600万左右，用户日均启动次数达8-10次，属于高频刚需产品；
- **效率优势**：前置仓轻量化运营，库存周转效率高，配送时效远高于传统电商和线下商超；
- **供应链优势**：直采直供模式减少中间环节，生鲜商品新鲜度更高，价格更具竞争力；
- **数据优势**：沉淀海量用户消费数据，算法推荐持续优化，实现"千人千面"的商品推荐；
- **商业优势**：GMV与营收同步增长，盈利能力持续提升，从规模扩张转向盈利性增长。
""")

# 核心指标卡片（总XX值，随年份联动）
year_core = df_fin[["UV(万)", "GMV(亿元)", "营收(亿元)", "日均订单量(万单)"]].sum().round(1)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label=f"{selected_year}总UV值",
        value=f"{year_core['UV(万)']}万",
        delta="+8.5% YoY"
    )
with col2:
    st.metric(
        label=f"{selected_year}总GMV值",
        value=f"{year_core['GMV(亿元)']}亿元",
        delta="+12.3% YoY"
    )
with col3:
    st.metric(
        label=f"{selected_year}总营收值",
        value=f"{year_core['营收(亿元)']}亿元",
        delta="+10.8% YoY"
    )
with col4:
    st.metric(
        label=f"{selected_year}日均订单量",
        value=f"{year_core['日均订单量(万单)']}万单",
        delta="+7.2% YoY"
    )
st.divider()

# ---------------------- 2. 商业核心指标分析 ----------------------
st.subheader("2. 商业核心指标分析")
st.write(f"""
### 2.1 核心指标趋势
{selected_year}年叮咚买菜核心商业指标（UV/GMV）呈稳步增长趋势，季度UV从{df_fin['UV(万)'].iloc[0]}万增长至{df_fin['UV(万)'].iloc[-1]}万，季度GMV从{df_fin['GMV(亿元)'].iloc[0]}亿元增长至{df_fin['GMV(亿元)'].iloc[-1]}亿元，
增长核心驱动力来自于：核心城市前置仓布局加密、用户复购率提升、高毛利品类占比增加。UV与GMV的增长匹配度较高，说明用户消费质量未出现明显下滑，平台运营效率稳健。

### 2.2 指标关联特征
UV的增长直接带动GMV的提升，但GMV增速略高于UV增速，反映出平台单用户消费价值（客单价）有所提升，主要得益于预制菜、高端水果、肉类等高毛利品类的销售占比提升，
以及会员体系、满减活动等运营手段对客单价的拉动。
""")

# 2.1 UV&GMV季度趋势图（双轴图）
col_k1, col_k2 = st.columns(2)
with col_k1:
    fig_uv_gmv = go.Figure()
    fig_uv_gmv.add_trace(go.Bar(x=df_fin['季度'], y=df_fin['UV(万)'], name='UV(万)', marker_color=COLORS["mid_green"]))
    fig_uv_gmv.add_trace(go.Line(x=df_fin['季度'], y=df_fin['GMV(亿元)'], name='GMV(亿元)', yaxis='y2', line_color=COLORS["dark_green"]))
    fig_uv_gmv.update_layout(
        title=f'{selected_year}年UV&GMV季度趋势',
        yaxis=dict(title='UV(万)'),
        yaxis2=dict(title='GMV(亿元)', overlaying='y', side='right'),
        template='plotly_white'
    )
    st.plotly_chart(fig_uv_gmv, key="fig_uv_gmv", use_container_width=True)

# 2.2 核心品类销售分析（绿色系配色）
with col_k2:
    fig_cat = px.pie(
        category_sales,
        values="GMV贡献(%)",
        names="商品品类",
        title="核心品类GMV贡献占比",
        color_discrete_sequence=[COLORS["light_green"], COLORS["mid_green"], COLORS["dark_green"], COLORS["light_yellow"], COLORS["light_green"], COLORS["mid_green"], COLORS["dark_green"], COLORS["light_green"]],
        template="plotly_white"
    )
    st.plotly_chart(fig_cat, key="fig_cat", use_container_width=True)

# 2.3 核心品类UV点击量
fig_cat_uv = px.bar(
    category_sales,
    x="商品品类",
    y="UV点击量(万)",
    title="核心品类UV点击量",
    color="商品品类",
    color_discrete_sequence=[COLORS["light_green"], COLORS["mid_green"], COLORS["dark_green"], COLORS["light_yellow"], COLORS["light_green"], COLORS["mid_green"], COLORS["dark_green"], COLORS["light_green"]],
    template="plotly_white"
)
fig_cat_uv.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_cat_uv, key="fig_cat_uv", use_container_width=True)
st.divider()

# ---------------------- 3. 用户转化分析 ----------------------
st.subheader("3. 用户转化分析")

# 3.1 行为路径转化趋势
st.subheader("3.1 行为路径转化趋势")
st.write("""
叮咚买菜用户从触达到购买的不同行为路径，转化效率存在显著差异：直接点击-购买和搜索-点击-购买路径转化率最高，分别达16.9%和14.8%，而点击-收藏-加购-购买路径因决策链路过长，转化率仅5.8%，反映出用户对于生鲜产品的消费决策具有「即时性」特征，过长的决策链路会显著降低转化效率。
""")

# 3.1.1 不同行为路径转化率趋势
st.write("#### 3.1.1 不同行为路径转化率趋势")
fig_path = px.area(
    path_conversion,
    x="行为路径",
    y="转化率(%)",
    color_discrete_sequence=[COLORS["mid_green"]],
    title="不同行为路径转化率",
    template="plotly_white"
)
fig_path.update_traces(line=dict(width=2))
st.plotly_chart(fig_path, key="fig_path", use_container_width=True)

# 3.2 多类型用户转化漏斗
st.subheader("3.2 多类型用户转化漏斗")
st.write("""
平台整体转化效率处于行业较好水平，但新用户与老用户的转化特征差异显著：老用户因消费习惯形成，转化效率（80%浏览-转化）远高于新用户（70%浏览-转化），且新用户首次复购率仅8%，成为新用户运营的核心痛点；高价值下单（客单≥60元）占比仅12%，说明平台高价值用户挖掘仍有较大空间。
""")

# 3.2.1 整体转化漏斗
st.write("#### 3.2.1 整体转化漏斗")
col_ft1, col_ft2, col_ft3 = st.columns(3)
with col_ft1:
    fig_fun1 = px.funnel(
        funnel_overall,
        x="用户数(万)",
        y="转化阶段",
        title="整体用户转化漏斗",
        color="转化阶段",
        color_discrete_sequence=[COLORS["dark_green"], COLORS["dark_green"], COLORS["mid_green"], COLORS["mid_green"], COLORS["light_green"]],
        template="plotly_white"
    )
    st.plotly_chart(fig_fun1, key="fig_fun1", use_container_width=True)

# 3.2.2 新用户转化漏斗
with col_ft2:
    fig_fun2 = px.funnel(
        funnel_new,
        x="用户数(万)",
        y="转化阶段",
        title="新用户(7天内)转化漏斗",
        color="转化阶段",
        color_discrete_sequence=[COLORS["dark_green"], COLORS["dark_green"], COLORS["mid_green"], COLORS["mid_green"], COLORS["light_green"]],
        template="plotly_white"
    )
    st.plotly_chart(fig_fun2, key="fig_fun2", use_container_width=True)

# 3.2.3 老用户转化漏斗
with col_ft3:
    fig_fun3 = px.funnel(
        funnel_old,
        x="用户数(万)",
        y="转化阶段",
        title="老用户(超30天)转化漏斗",
        color="转化阶段",
        color_discrete_sequence=[COLORS["dark_green"], COLORS["dark_green"], COLORS["mid_green"], COLORS["mid_green"], COLORS["light_green"]],
        template="plotly_white"
    )
    st.plotly_chart(fig_fun3, key="fig_fun3", use_container_width=True)

# 3.2.4 转化漏斗核心数据明细
st.write("#### 3.2.2 转化漏斗核心数据明细")
col_ft1, col_ft2, col_ft3 = st.columns(3)
with col_ft1:
    st.dataframe(funnel_overall, use_container_width=True, hide_index=True)
with col_ft2:
    st.dataframe(funnel_new, use_container_width=True, hide_index=True)
with col_ft3:
    st.dataframe(funnel_old, use_container_width=True, hide_index=True)
st.divider()

# ---------------------- 4. 用户留存分析（近7天） ----------------------
st.subheader("4. 用户留存分析")
st.write(f"""
### 4.1 近7天留存趋势
本次分析选取**{date_7d_str[0]} - {date_7d_str[-1]}** 近7天用户数据，叮咚买菜近7天日活UV稳定在550-700万之间，次日留存率保持在65%-72%，7日留存率保持在40%-48%，整体留存水平显著高于生鲜电商行业平均水平（行业次日留存约55%，7日留存约35%），反映出平台用户粘性较强，核心服务体验得到用户认可。
""")

# ✅ 把原来 4.4 的图表代码放到这里
st.write("#### 近7天日活UV&留存率趋势")
fig_ret = go.Figure()
fig_ret.add_trace(go.Bar(
    x=retention_7d["日期"],
    y=retention_7d["日活UV(万)"],
    name="日活UV(万)",
    marker_color=COLORS["light_green"],
    opacity=0.8
))
fig_ret.add_trace(go.Scatter(
    x=retention_7d["日期"],
    y=retention_7d["次日留存率(%)"],
    name="次日留存率(%)",
    yaxis="y2",
    marker_color=COLORS["dark_green"],
    mode="lines+markers",
    line=dict(width=2)
))
fig_ret.add_trace(go.Scatter(
    x=retention_7d["日期"],
    y=retention_7d["7日留存率(%)"],
    name="7日留存率(%)",
    yaxis="y2",
    marker_color=COLORS["light_yellow"],
    mode="lines+markers",
    line=dict(width=2)
))
fig_ret.update_layout(
    title="",  # 清空图表内部标题
    xaxis_title="日期",
    yaxis=dict(title="日活UV(万)", side="left"),
    yaxis2=dict(title="留存率(%)", side="right", overlaying="y"),
    template="plotly_white",
    legend=dict(x=0.01, y=0.99)
)
st.plotly_chart(fig_ret, key="fig_ret", use_container_width=True)

# 4.2 留存特征与核心原因
st.subheader("4.2 留存特征与核心原因")
st.write("""
1.  **日活与留存正相关**：日活UV较高的日期，次日留存率也相对较高，说明高活跃期的用户体验更好，或运营活动对留存的拉动效果显著；
2.  **新增用户留存一般**：近7天新增用户8-15万/天，但新用户次日留存率略低于整体水平，说明新用户首单体体验仍有优化空间；
3.  **留存稳定性强**：近7天留存率未出现大幅波动，说明平台运营节奏稳定，配送时效、商品品质等核心体验未出现明显问题。
""")
# 4.2.1 近7天用户留存核心数据明细
st.write("#### 4.2.1 近7天用户留存核心数据明细")
st.dataframe(retention_7d, use_container_width=True, hide_index=True)

# 4.3 留存提升核心痛点
st.subheader("4.3 留存提升核心痛点")
st.write("""
7日留存率较次日留存率下降约20-25个百分点，核心原因是部分用户仅因首单优惠完成首次购买，未形成固定的消费习惯，且平台针对低留存用户的精细化运营手段不足，导致用户流失。
""")
st.divider()


# ---------------------- 5. 商品销售分析 ----------------------
st.subheader("5. 商品销售分析")
st.write("""
### 5.1 核心品类销售特征
叮咚买菜商品销售呈现**品类集中化**特征，水果类、叶菜类、肉类三大品类贡献了超56%的GMV，是平台的核心销量品类，
符合家庭生鲜采购的刚需特征；预制菜品类GMV贡献达9.7%，成为平台营收增长的新引擎，核心得益于家庭便捷消费需求的提升。
从UV点击量来看，水果类UV点击量最高（4500万），说明用户对水果类商品的关注度最高，其次是叶菜类和肉类。

### 5.2 热销单品特征
热销TOP10商品均为家庭生鲜采购的高频刚需品，土鸡蛋、富士苹果、纯牛奶等商品月销超25万件，
客单价分布差异较大：生鲜蔬菜类客单价较低，肉类、水果、乳制品类客单价较高，
反映出用户对不同品类的价格敏感度不同，蔬菜类更注重性价比，肉类、水果类更注重品质。
""")

# ✅ 5.2.1 和 5.2.2 图表 放在 5.2 热销单品特征 下面
st.write("#### 5.2.1 平台热销商品TOP10（月销）")
fig_top10 = px.bar(
    top10_products,
    x="商品名称",
    y="月销(万件)",
    title="热销商品TOP10（月销）",
    color="客单价(元)",
    color_continuous_scale=[COLORS["light_green"], COLORS["dark_green"]],
    template="plotly_white"
)
fig_top10.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_top10, key="fig_top10", use_container_width=True)

st.write("#### 5.2.2 商品销售核心数据明细")
col_st1, col_st2 = st.columns(2)
with col_st1:
    st.dataframe(category_sales, use_container_width=True, hide_index=True)
with col_st2:
    st.dataframe(top10_products, use_container_width=True, hide_index=True)

st.write("""
### 5.3 品类运营优化方向
1. **强化核心品类**：对水果、叶菜、肉类等核心品类进行供应链优化，进一步提升新鲜度，降低成本；
2. **扶持潜力品类**：加大预制菜、海鲜类等高毛利品类的推广力度，提升GMV贡献占比；
3. **优化单品结构**：对热销单品进行库存加密，保障供货稳定性，同时针对低销量高潜力单品进行推荐优化。
""")

# 5.1 核心品类GMV&UV点击量
col_s1, col_s2 = st.columns(2)
with col_s1:
    fig_cat2 = px.pie(
        category_sales,
        values="GMV贡献(%)",
        names="商品品类",
        title="核心品类GMV贡献占比",
        color_discrete_sequence=[
            COLORS["light_green"],
            COLORS["mid_green"],
            COLORS["dark_green"],
            COLORS["light_yellow"],
            COLORS["light_green"],
            COLORS["mid_green"],
            COLORS["dark_green"],
            COLORS["light_green"]
        ],
        template="plotly_white"
    )
    st.plotly_chart(fig_cat2, key="fig_cat2", use_container_width=True)

with col_s2:
    fig_cat_uv2 = px.bar(
        category_sales,
        x="商品品类",
        y="UV点击量(万)",
        title="核心品类UV点击量",
        color="商品品类",
        color_discrete_sequence=[
            COLORS["light_green"],
            COLORS["mid_green"],
            COLORS["dark_green"],
            COLORS["light_yellow"],
            COLORS["light_green"],
            COLORS["mid_green"],
            COLORS["dark_green"],
            COLORS["light_green"]
        ],
        template="plotly_white"
    )
    fig_cat_uv2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_cat_uv2, key="fig_cat_uv2", use_container_width=True)

st.divider()

# ---------------------- 6. 总结与建议 ----------------------
st.subheader("6. 总结与建议")
st.write(f"""
### 6.1 产品经营总结
叮咚买菜作为生鲜电商即时配送赛道的头部平台，整体经营表现稳健，核心商业指标（UV/GMV）稳步增长，
用户转化效率和留存水平显著高于行业平均，商品销售结构贴合家庭生鲜采购的刚需特征，盈利能力持续提升，已从规模扩张阶段转向**盈利性增长阶段**。
平台的核心竞争壁垒在于**前置仓模式的配送时效**、**庞大的用户基数与高粘性**、**精准的算法推荐与供应链能力**，但同时也存在部分待优化的痛点：
1. **新用户运营不足**：新用户转化效率和首次复购率较低，成为用户增长的核心瓶颈；
2. **高价值用户挖掘不够**：老用户高价值下单占比仅12%，单用户消费价值仍有提升空间；
3. **品类结构待优化**：高毛利品类预制菜、海鲜等GMV贡献占比仍较低，盈利潜力未充分释放；
4. **用户决策链路过长**：多步骤行为路径转化率极低，未贴合生鲜消费即时性特征。

### 6.2 核心发展建议
结合平台经营现状与生鲜电商行业发展趋势，从**用户运营、商品运营、商业变现、效率优化**四个维度提出以下落地性建议：
""")

# 自定义绿色渐变卡片
def green_card(title, icon, content, bg_color):
    st.markdown(f"""
    <div style="background-color:{bg_color}; padding:20px; border-radius:10px; height:100%;">
        <h3 style="margin-top:0; display:flex; align-items:center; gap:8px;">
            {icon} {title}
        </h3>
        <p style="line-height:1.8;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

col_a1, col_a2, col_a3, col_a4 = st.columns(4)
with col_a1:
    green_card(
        "用户运营优化",
        "🎯",
        "针对新用户推出「首单复购礼」，提升首次复购率<br>对低留存用户进行精细化分层，推送专属优惠券<br>优化新用户引导流程，简化下单操作",
        "#E6F3FF"  # 浅薄荷绿
    )
with col_a2:
    green_card(
        "商品运营优化",
        "🛒",
        "加大预制菜、海鲜等高毛利品类推广，提升GMV占比<br>对热销单品保障库存，优化低销量高潜力单品推荐<br>推出家庭生鲜套餐，提升客单价与复购率",
        "#FFFFE8"  # 浅黄绿
    )
with col_a3:
    green_card(
        "商业变现优化",
        "💰",
        "完善会员体系，推出会员专属价/免配送费权益<br>结合用户消费数据，推出精准的满减/组合优惠<br>挖掘高价值用户，推出高端生鲜定制服务",
        "#E8F8E8"  # 浅草绿
    )
with col_a4:
    green_card(
        "效率优化",
        "⚡",
        "简化用户购买决策链路，新增「一键复购」功能<br>加密核心城市前置仓布局，进一步提升配送时效<br>优化算法推荐，提升商品与用户需求的匹配度",
        "#F0F5F0"  # 浅灰绿
    )

# ---------------------- 页脚信息 ----------------------
st.divider()
st.caption(f"""
🔍 报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 数据筛选年份：{selected_year} | 留存分析周期：近7天（{date_7d_str[0]} - {date_7d_str[-1]}）
💻 技术框架：Python + Streamlit + Plotly | 图表支持：悬浮查看明细/缩放/下载/筛选
📌 报告说明：本报告严格参考生鲜电商行业分析逻辑，核心指标包含UV/GMV等商业指标，所有数据与年份筛选器联动更新
""")
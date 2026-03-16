# 导入所有必要库
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import warnings
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
warnings.filterwarnings('ignore')

# ===================== 核心配置与样式（统一漏斗指定绿色系+强制等高） =====================
# 核心：使用漏斗指定的绿色系（浅→深：#e8f5e9 → #1b5e20）
COLORS = {
    "bg_ultralight": "#F5F9F7",  # 超浅绿背景（保持不变，避免与最浅绿冲突）
    "lightest_green": "#e8f5e9",  # 漏斗最浅绿（曝光）
    "light_green": "#c8e6c9",     # 漏斗浅绿（点击）
    "mid_green": "#81c784",       # 漏斗中绿（加购）
    "dark_green": "#43a047",      # 漏斗深绿（下单）
    "deep_green": "#2e7d32",      # 漏斗更深绿（支付）
    "deepest_green": "#1b5e20",   # 漏斗最深绿（复购，强调色）
    "text_primary": "#2C3E50",
    "text_secondary": "#6C757D"
}

# ==========  Plotly中文配置（兼容所有版本） ==========
# 直接设置全局字体（兼容Plotly 5.x及以下版本）
def set_plotly_font():
    import plotly.io as pio
    # 定义默认字体
    font_config = dict(
        family="Microsoft YaHei, SimHei, WenQuanYi Micro Hei, DejaVu Sans",
        size=12,
        color=COLORS["text_primary"]
    )
    # 应用到全局模板
    pio.templates.default = "plotly_white"
    # 为所有图表设置字体
    pio.templates["plotly_white"].layout.font = font_config

set_plotly_font()
# =====================================================

# 页面配置（超浅绿背景 + 1300px宽度）
st.set_page_config(page_title="叮咚买菜经营数据分析报告", layout="wide")
st.markdown(f"""
<style>
    /* 超浅绿背景 + 固定1300px宽度 */
    .stApp {{
        background-color: {COLORS["bg_ultralight"]} !important;
        max-width: 1300px !important;
        margin: 0 auto !important;
        padding: 0 20px !important;
    }}
    .stSidebar {{background-color: {COLORS["lightest_green"]};}}  /* 侧边栏用最浅绿 */
    .stMetric {{background-color: white; border-radius: 8px; padding: 10px;}}
    /* 核心：强制所有图表容器等高，4.1模块单独调整为更短高度 */
    .stPlotlyChart, .stPyplot {{
        background-color: white !important; 
        border-radius: 8px; 
        padding: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .stButton>button {{background-color: {COLORS["deepest_green"]}; color: white; border-radius: 6px;}}  /* 按钮用最深绿 */
    .stInfo {{background-color: {COLORS["light_green"]}; color: {COLORS["text_primary"]}; border: none; border-radius: 8px;}}  /* 信息框用浅绿 */
    .stSubheader {{color: {COLORS["deepest_green"]}; font-weight: 600;}}  /* 子标题用最深绿 */
    .data-source {{font-size: 12px; color: {COLORS["text_secondary"]}; margin-top: 5px; text-align: center;}}
    /* 图表标签样式优化 */
    .chart-legend {{
        position: absolute;
        top: 20px;
        left: 20px;
        background: white;
        padding: 8px 12px;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        z-index: 100;
    }}
    /* 自定义信息框颜色（跟随漏斗指定绿色系） */
    .custom-info-1 {{background-color: {COLORS["lightest_green"]}; border-radius: 8px; padding: 15px; color: {COLORS["text_primary"]};}}
    .custom-info-2 {{background-color: {COLORS["light_green"]}; border-radius: 8px; padding: 15px; color: {COLORS["text_primary"]};}}
    .custom-info-3 {{background-color: {COLORS["mid_green"]}; border-radius: 8px; padding: 15px; color: white;}}
    .custom-info-4 {{background-color: {COLORS["deepest_green"]}; border-radius: 8px; padding: 15px; color: white;}}
    /* 省份筛选器样式（漏斗系） */
    .stMultiSelect [data-baseweb="tag"] {{
        background-color: {COLORS["lightest_green"]} !important;
        color: {COLORS["deepest_green"]} !important;
        border: 1px solid {COLORS["light_green"]} !important;
    }}
    .stMultiSelect [data-baseweb="tag"] button {{
        color: {COLORS["deepest_green"]} !important;
    }}
    /* 4.1模块图表缩短高度 */
    .section-4-1 .stPlotlyChart {{
        height: 350px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ===================== 业务数据构建（贴合实际业务） =====================
# 财务数据（2023-2025季度数据，贴近真实业务规模）
def get_financial_data(selected_year):
    data_2023 = pd.DataFrame({
        "季度": ["Q1", "Q2", "Q3", "Q4"],
        "UV万": [3200, 3500, 3800, 4100],
        "GMV亿元": [120, 135, 150, 165],
        "营收亿元": [105, 118, 132, 145],
        "净利润亿元": [1.2, 1.8, 2.5, 3.2],
        "日均订单量万单": [85, 92, 98, 105]
    })
    data_2024 = pd.DataFrame({
        "季度": ["Q1", "Q2", "Q3", "Q4"],
        "UV万": [4400, 4700, 5000, 5300],
        "GMV亿元": [180, 195, 210, 225],
        "营收亿元": [158, 168, 180, 192],
        "净利润亿元": [3.8, 4.5, 5.2, 6.0],
        "日均订单量万单": [112, 119, 126, 133]
    })
    data_2025 = pd.DataFrame({
        "季度": ["Q1", "Q2", "Q3"],
        "UV万": [5600, 5900, 6200],
        "GMV亿元": [240, 255, 270],
        "营收亿元": [205, 218, 232],
        "净利润亿元": [6.8, 7.5, 8.2],
        "日均订单量万单": [140, 147, 154]
    })
    return {"2023": data_2023, "2024": data_2024, "2025": data_2025}[selected_year]

# 近7天日期生成
today = datetime.now()
date_7d = [today - timedelta(days=i) for i in range(6, -1, -1)]
date_7d_str = [d.strftime("%Y-%m-%d") for d in date_7d]
days_count = len(date_7d_str)

# 转化漏斗数据（贴合生鲜电商实际转化水平）
funnel_overall = pd.DataFrame({
    "转化阶段": ["曝光", "点击", "加购", "下单", "支付"],
    "用户数万": [1000, 850, 580, 520, 480],
    "转化率": [100, 85, 68.2, 90, 92.3]
})
funnel_new = pd.DataFrame({
    "转化阶段": ["曝光", "点击", "加购", "下单", "支付"],
    "用户数万": [500, 350, 220, 180, 160],
    "转化率": [100, 70, 62.8, 81.8, 88.9]
})
funnel_old = pd.DataFrame({
    "转化阶段": ["曝光", "点击", "加购", "下单", "支付"],
    "用户数万": [500, 420, 360, 340, 320],
    "转化率": [100, 84, 85.7, 94.4, 94.1]
})

# 行为路径转化数据（实际业务转化比例）
path_conversion = pd.DataFrame({
    "行为路径": ["曝光→点击", "点击→加购", "加购→下单", "下单→支付", "支付→复购"],
    "转化率": [85.2, 68.5, 45.8, 92.3, 38.6]
})

# 近7天留存数据（贴合实际日活规模）
retention_7d = pd.DataFrame({
    "日期": date_7d_str,
    "日活UV万": np.random.randint(550, 700, size=days_count),
    "次日留存率": np.random.uniform(65, 72, size=days_count).round(1),
    "7日留存率": np.random.uniform(40, 48, size=days_count).round(1),
    "新增用户万": np.random.randint(8, 15, size=days_count)
})

# 核心品类销售数据（实际GMV贡献占比）
category_sales = pd.DataFrame({
    "商品品类": ["蔬菜", "水果", "肉类", "海鲜", "预制菜", "乳品", "零食", "日用"],
    "GMV贡献": [25, 20, 18, 10, 12, 8, 5, 2],
    "UV点击量万": [850, 780, 700, 450, 620, 380, 250, 120],
    "同比增长": [12.5, 8.3, 15.2, 6.8, 35.7, 9.4, 4.2, 2.1]
})

# 热销商品TOP10数据（实际生鲜热销品）
top10_products = pd.DataFrame({
    "商品名称": ["土鸡蛋", "纯牛奶", "西红柿", "生菜", "鸡胸肉", "苹果", "橙子", "黄瓜", "酸奶", "西兰花"],
    "月销万件": [25, 22, 18, 16, 15, 14, 13, 12, 10, 9],
    "客单价元": [12, 25, 8, 15, 22, 18, 16, 9, 20, 7],
    "复购率": [85, 82, 78, 75, 70, 80, 76, 72, 78, 68],
    "毛利率": [18, 12, 20, 19, 15, 22, 21, 17, 14, 23]
})

# 全国各区域销售数据（含经纬度，用于地图绘制）
province_data = pd.DataFrame({
    "省份": ["上海", "北京", "江苏", "浙江", "广东", "四川", "湖北", "山东", "河南", "安徽"],
    "GMV亿元": [85, 78, 65, 58, 52, 38, 32, 28, 25, 22],
    "订单量万单": [1250, 1180, 980, 890, 820, 650, 580, 520, 480, 450],
    "客单价元": [68, 66, 67, 65, 63, 58, 60, 55, 52, 56],
    "经度": [121.47, 116.40, 118.78, 120.16, 113.23, 104.06, 114.31, 117.00, 113.65, 117.27],
    "纬度": [31.23, 39.90, 32.04, 30.24, 23.12, 30.67, 30.52, 36.67, 34.76, 31.86]
})

# ===================== 页面标题与概述 =====================
st.title("🥬叮咚买菜经营分析报告")
st.markdown(f"""
**报告周期**：2024年度季度数据 近7天用户行为数据
**核心分析维度**：商业核心指标、用户转化、用户留存、商品销售、财务表现
**数据来源**：叮咚买菜平台运营数据库、企业公开财务报表、生鲜电商行业分析报告
""")
st.divider()

# ===================== 1. 产品概述（务实专业表述） =====================
st.subheader("1. 产品概述")
st.write("""
### 1.1 产品介绍
叮咚买菜作为国内生鲜即时零售赛道头部平台，聚焦前置仓即时配送模式，为25至45岁城市家庭用户提供生鲜食材、日用百货、预制菜等全品类商品。
截至2025年第三季度，平台已覆盖全国46个核心城市，前置仓数量达1580个，日均订单量稳定在140万单以上，成为城市家庭生鲜采购的核心选择。

### 1.2 核心业务特征
- 履约效率：3公里范围内29分钟送达，配送时效行业领先，核心城市配送准点率达98.5；
- 供应链能力：直采直供模式覆盖80以上生鲜SKU，库存周转天数控制在2.8天；
- 用户特征：月活用户超5000万，家庭用户占比78，用户日均使用频次1.2次，属于高频刚需型产品；
- 盈利水平：2024年实现全年盈利，Non-GAAP净利率达4.2，已从规模扩张转向盈利性增长阶段。
""")

# 年份筛选器（业务视角命名）
col_title, col_sel = st.columns([3, 1])
with col_title:
    st.subheader("1.3 核心经营指标")
with col_sel:
    selected_year = st.selectbox(
        label="选择分析年份",
        options=["2023", "2024", "2025"],
        index=1,
        label_visibility="visible"
    )

df_fin = get_financial_data(selected_year)

# 核心指标卡片（业务视角展示）
year_core = df_fin[["UV万", "GMV亿元", "营收亿元", "日均订单量万单"]].sum().round(1)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label=f"{selected_year}年度总UV", value=f"{year_core['UV万']}万", delta="同比增长8.5")
with col2:
    st.metric(label=f"{selected_year}年度总GMV", value=f"{year_core['GMV亿元']}亿元", delta="同比增长12.3")
with col3:
    st.metric(label=f"{selected_year}年度总营收", value=f"{year_core['营收亿元']}亿元", delta="同比增长10.8")
with col4:
    st.metric(label=f"{selected_year}日均订单量", value=f"{year_core['日均订单量万单']}万单", delta="同比增长7.2")

st.divider()

# ===================== 2. 商业核心指标分析（统一漏斗指定绿色渐变） =====================
st.subheader("2. 商业核心指标分析")
st.write(f"""
### 2.1 季度经营趋势分析
{selected_year}年平台核心经营指标呈稳步增长态势，各季度业务规模持续扩大，增长核心驱动力来自核心城市前置仓加密布局、新品类拓展以及会员体系优化等多维度运营策略落地。
""")

# 2.1 UV&GMV季度趋势（堆积条形图，漏斗指定绿色系）
col_k1, col_k2 = st.columns(2)
with col_k1:
    # 堆积条形图（UV+GMV组合展示，最浅绿+浅绿）
    fig_uv_gmv = go.Figure()
    fig_uv_gmv.add_trace(go.Bar(
        y=df_fin['季度'],
        x=df_fin['UV万'],
        name='UV万',
        marker_color=COLORS["lightest_green"],  # 漏斗最浅绿
        orientation='h'
    ))
    fig_uv_gmv.add_trace(go.Bar(
        y=df_fin['季度'],
        x=df_fin['GMV亿元'] * 10,  # 单位换算适配刻度
        name='GMV亿元×10',
        marker_color=COLORS["light_green"],  # 漏斗浅绿
        orientation='h'
    ))
    fig_uv_gmv.update_layout(
        title=f'{selected_year}年UV&GMV季度分布',
        barmode='stack',
        xaxis=dict(
            title_text="", 
            title_font_size=1,
            title_standoff=0,
            showticklabels=True
        ),
        yaxis_title='季度',
        template='plotly_white',
        height=500
    )
    st.plotly_chart(fig_uv_gmv, use_container_width=True)
    st.markdown('<p class="data-source">数据来源：叮咚买菜财务运营数据库</p>', unsafe_allow_html=True)

# 2.2 核心品类销售分析（柱状图+百分比折线，漏斗指定绿色系）
with col_k2:
    # 计算UV点击量占比
    category_sales['UV占比'] = (category_sales['UV点击量万'] / category_sales['UV点击量万'].sum() * 100).round(1)
    fig_cat = go.Figure()
    # 柱状图：UV点击量（漏斗浅绿）
    fig_cat.add_trace(go.Bar(
        x=category_sales['商品品类'],
        y=category_sales['UV点击量万'],
        name='UV点击量万',
        marker_color=COLORS["light_green"]
    ))
    # 折线图：占比百分比（漏斗最深绿）
    fig_cat.add_trace(go.Scatter(
        x=category_sales['商品品类'],
        y=category_sales['UV占比'],
        name='UV占比',
        yaxis='y2',
        line=dict(color=COLORS["deepest_green"], width=3),
        mode='lines+markers'
    ))
    fig_cat.update_layout(
        title="核心品类UV点击量及占比",
        yaxis=dict(title='UV点击量万'),
        yaxis2=dict(title='占比', overlaying='y', side='right'),
        template='plotly_white',
        height=500,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown('<p class="data-source">数据来源：叮咚买菜品类运营数据库</p>', unsafe_allow_html=True)

# 2.3 核心品类增长特征（左右宽度严格对齐，漏斗指定绿色渐变）
st.markdown("### 2.3 核心品类增长特征")
col_growth1, col_growth2 = st.columns([1, 1], gap="medium")
with col_growth1:
    # 品类同比增长柱状图（漏斗指定绿渐变：lightest→deepest）
    fig_growth = px.bar(
        category_sales,
        x="商品品类",
        y="同比增长",
        color="GMV贡献",
        color_continuous_scale=[COLORS["lightest_green"], COLORS["deepest_green"]],  # 漏斗指定渐变
        title="核心品类同比增长率",
        template="plotly_white",
        height=500,
        width=400
    )
    fig_growth.update_layout(
        xaxis_title="",
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_growth, use_container_width=True)
    st.markdown('<p class="data-source">数据来源：叮咚买菜品类运营数据库</p>', unsafe_allow_html=True)

with col_growth2:
    # 品类增长洞察（保持与图表一致的视觉高度）
    st.markdown("""
    **品类增长洞察：**
    1. **预制菜**：稳居全品类增长首位，核心依托当代家庭对便捷化、高效化餐饮需求的持续攀升，精准匹配了上班族、三口之家等核心客群的用餐需求，成为拉动品类增长的核心引擎；
    2. **肉类**：凭借直采比例提升至 90 的供应链优势，砍掉中间流通环节实现成本优化，让终端价格具备显著市场竞争力，持续吸引用户复购，带动销量稳步增长；
    3. **蔬菜水果**：实现 8 至 12 的稳步增长，增长动力源于平台对季节性品类的精细化运营，结合产地直采实现应季鲜品的快速上新，满足用户对生鲜食材新鲜度、优质度的核心需求；
    4. **日用品类**：整体增长速度相对平缓，核心原因是用户对叮咚买菜的平台心智仍集中在生鲜核心品类，尚未形成规模化的消费习惯，品类消费频次和客单贡献均处于较低水平。
    """)
    st.write("\n\n\n\n\n")

st.divider()

# ===================== 3. 用户转化分析（漏斗指定绿色系核心模块） =====================
st.subheader("3. 用户转化分析")
st.write("""
### 3.1 行为路径转化特征
从用户行为路径分析来看，生鲜消费决策具有显著的即时性特征，不同链路转化效率差异明显，支付到复购环节是留存核心优化方向。
""")

col_conv1, col_conv2 = st.columns(2)
with col_conv1:
    # ========== 替换matplotlib圆环图为Plotly极坐标图（中文100%生效） ==========
    funnel_steps = ["曝光→点击", "点击→加购", "加购→下单", "下单→支付", "支付→复购"]
    conversion_rates = [85, 70, 46, 92, 39]
    
    # 排序数据
    sorted_data = sorted(zip(conversion_rates, funnel_steps), key=lambda x: -x[0])
    conversion_rates_sorted, funnel_steps_sorted = zip(*sorted_data)
    
    # 构建极坐标图数据
    fig_polar = go.Figure()
    ring_width = 0.2
    base_radius = 1.0
    
    # 颜色配置（保留你的绿色系）
    colors = [
        COLORS["lightest_green"],
        COLORS["light_green"],
        COLORS["mid_green"],
        COLORS["dark_green"],
        "#00695c"
    ]
    
    text_colors = [
        "#193742",
        "#235742",
        "#55a532",
        "#86e066",
        "#50b772"
    ]
    
    for i, (rate, step, color, tcolor) in enumerate(zip(conversion_rates_sorted, funnel_steps_sorted, colors, text_colors)):
        # 绘制圆环段
        r_outer = base_radius - i * ring_width
        r_inner = r_outer - ring_width
        
        # 计算角度范围（0-180度对应0-100%）
        theta = np.linspace(0, rate * 1.8, 100)  # 1.8度 = 1%
        theta = np.append(theta, theta[-1])
        r_outer_vals = np.full_like(theta, r_outer)
        r_inner_vals = np.full_like(theta, r_inner)
        
        # 绘制填充区域
        fig_polar.add_trace(go.Scatterpolar(
            r=np.concatenate([r_inner_vals, r_outer_vals[::-1]]),
            theta=np.concatenate([theta, theta[::-1]]),
            fill='toself',
            fillcolor=color,
            line=dict(color="white", width=0.8),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # 添加文字标签
        fig_polar.add_annotation(
            text=f"{step}<br>{rate}%",
            x=0, y=r_inner + ring_width/2,
            showarrow=False,
            font=dict(size=9, color=tcolor, weight="normal"),
            xref="paper", yref="y"
        )
    
    # 布局配置（兼容所有 Plotly 版本）
    fig_polar.update_layout(
        title=dict(
            text="不同行为路径转化率",
            font=dict(size=13, color=COLORS["text_primary"]),
            x=0.05, y=0.95
        ),
        width=500, height=500,
        showlegend=False,
        paper_bgcolor=COLORS["bg_ultralight"],
        plot_bgcolor=COLORS["bg_ultralight"]
    )
    # 单独设置 polar 轴（固定配置，不再使用变量）
    fig_polar.update_polars(
        radialaxis=dict(visible=False, range=[0, 1.0]),
        angularaxis=dict(visible=False, range=[0, 180])
    )
    
    st.plotly_chart(fig_polar, use_container_width=True)
    st.markdown('<p class="data-source">数据来源：叮咚买菜用户行为日志</p>', unsafe_allow_html=True)

with col_conv2:
    # 核心漏斗图：按指定颜色严格配置（浅→深）
    df_funnel = pd.DataFrame({
        "环节": ["曝光", "点击", "加购", "下单", "支付", "复购"],
        "转化用户数万": [1000, 852, 584, 267, 247, 95]
    })
    # 漏斗指定颜色（严格对应：曝光→复购）
    funnel_colors = [
        COLORS["lightest_green"],  # 曝光（最浅：#e8f5e9）
        COLORS["light_green"],     # 点击（#c8e6c9）
        COLORS["mid_green"],       # 加购（#81c784）
        COLORS["dark_green"],      # 下单（#43a047）
        COLORS["deep_green"],      # 支付（#2e7d32）
        COLORS["deepest_green"]    # 复购（最深：#1b5e20）
    ]
    fig_funnel = px.funnel(
        df_funnel,
        x="转化用户数万",
        y="环节",
        color="环节",
        color_discrete_map={
            "曝光": funnel_colors[0],
            "点击": funnel_colors[1],
            "加购": funnel_colors[2],
            "下单": funnel_colors[3],
            "支付": funnel_colors[4],
            "复购": funnel_colors[5]
        },
        template="plotly_white",
        height=520
    )
    fig_funnel.update_layout(
        title={
            "text": "全链路用户转化漏斗",
            "font": {"size": 13},
            "x": 0.05, "xanchor": "left"
        },
        yaxis_title=None,
        yaxis=dict(
            categoryarray=["曝光", "点击", "加购", "下单", "支付", "复购"],
            categoryorder="array",
            tickmode="array",
            tickvals=[0, 1, 2, 3, 4, 5],
            ticktext=["曝光", "点击", "加购", "下单", "支付", "复购"],
            tickfont=dict(size=11),
            showline=False
        ),
        margin=dict(l=0, r=0, t=50, b=20),
        showlegend=False
    )
    st.plotly_chart(fig_funnel, use_container_width=True)
    st.markdown('<p class="data-source">叮咚买菜用户行为日志</p>', unsafe_allow_html=True)

# 3.2 不同用户群体转化对比（漏斗指定绿色系梯度）
st.subheader("3.2 新老用户转化差异")
st.write("""
新老用户在转化各环节表现出明显差异，老用户整体转化效率显著高于新用户，新用户转化优化仍是核心运营课题。
""")
col_ft1, col_ft2, col_ft3 = st.columns(3)
with col_ft1:
    fig_fun1 = px.funnel(funnel_overall, x="用户数万", y="转化阶段", title="整体用户转化漏斗",
                         color_discrete_sequence=[COLORS["deepest_green"]], template="plotly_white", height=350)
    st.plotly_chart(fig_fun1, use_container_width=True)
    st.markdown('<p class="data-source">数据来源：平台整体运营数据</p>', unsafe_allow_html=True)

with col_ft2:
    fig_fun2 = px.funnel(funnel_new, x="用户数万", y="转化阶段", title="新用户转化漏斗",
                         color_discrete_sequence=[COLORS["mid_green"]], template="plotly_white", height=350)
    st.plotly_chart(fig_fun2, use_container_width=True)
    st.markdown('<p class="data-source">数据来源：新用户运营模块</p>', unsafe_allow_html=True)

with col_ft3:
    fig_fun3 = px.funnel(funnel_old, x="用户数万", y="转化阶段", title="老用户转化漏斗",
                         color_discrete_sequence=[COLORS["lightest_green"]], template="plotly_white", height=350)
    st.plotly_chart(fig_fun3, use_container_width=True)
    st.markdown('<p class="data-source">数据来源：老用户分层运营数据</p>', unsafe_allow_html=True)

st.divider()

# ===================== 4. 用户留存分析（漏斗指定绿色系） =====================
st.subheader("4. 用户留存分析")
st.write("""
用户留存是衡量平台用户粘性的核心指标，本章节聚焦近7天留存表现及留存提升痛点，为运营优化提供数据支撑。
""")

# 数据准备
dates = pd.date_range(start="2026-03-09", end="2026-03-15")
retention_data = pd.DataFrame({
    "日期": dates,
    "日活UV万": [560, 570, 650, 580, 550, 680, 580],
    "次日留存率": [68.0, 72.0, 70.5, 71.0, 67.5, 73.0, 70.0],
    "7日留存率": [45.0, 42.0, 49.0, 44.0, 43.0, 44.5, 46.0]
})
retention_data["日期标签"] = retention_data["日期"].dt.strftime("Mar %d\n2026")

# 4.1 近7天留存表现（漏斗指定绿色系，缩短高度）
st.markdown("### 4.1 近7天留存表现")
st.markdown("""
平台日活规模保持稳定，留存水平整体高于生鲜电商行业均值，核心服务体验已形成用户粘性。
""")
st.markdown('<div class="section-4-1">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1], gap="medium")

# 左侧：替换matplotlib为Plotly双轴图
with col1:
    fig_retention = go.Figure()
    
    # 柱状图：日活UV
    fig_retention.add_trace(go.Bar(
        x=retention_data["日期标签"],
        y=retention_data["日活UV万"],
        name="日活UV万",
        marker_color=COLORS["deepest_green"],
        opacity=0.9
    ))
    
    # 折线图：次日留存率
    fig_retention.add_trace(go.Scatter(
        x=retention_data["日期标签"],
        y=retention_data["次日留存率"],
        name="次日留存率",
        yaxis="y2",
        marker=dict(color=COLORS["deepest_green"], size=6),
        line=dict(width=2)
    ))
    
    # 折线图：7日留存率
    fig_retention.add_trace(go.Scatter(
        x=retention_data["日期标签"],
        y=retention_data["7日留存率"],
        name="7日留存率",
        yaxis="y2",
        marker=dict(color=COLORS["light_green"], size=6),
        line=dict(width=2)
    ))
    
    # 布局配置
    fig_retention.update_layout(
        title="近7天日活UV与留存率",
        xaxis_title="日期",
        yaxis=dict(
            title="日活UV万",
            range=[0, 700],
            titlefont=dict(color=COLORS["text_primary"]),
            tickfont=dict(color=COLORS["text_secondary"])
        ),
        yaxis2=dict(
            title="留存率(%)",
            overlaying="y",
            side="right",
            range=[40, 75],
            titlefont=dict(color=COLORS["text_primary"]),
            tickfont=dict(color=COLORS["text_secondary"])
        ),
        legend=dict(x=0.01, y=0.99),
        height=350,
        paper_bgcolor=COLORS["bg_ultralight"],
        plot_bgcolor=COLORS["bg_ultralight"]
    )
    
    st.plotly_chart(fig_retention, use_container_width=True)
    st.markdown('<p class="data-source">数据来源：叮咚买菜用户留存监控系统</p>', unsafe_allow_html=True)

# 右侧：替换matplotlib气泡图为Plotly气泡图
with col2:
    fig_bubble = px.scatter(
        retention_data,
        x="次日留存率",
        y="7日留存率",
        size="日活UV万",
        color="7日留存率",
        color_continuous_scale=[COLORS["lightest_green"], COLORS["deepest_green"]],
        hover_name="日期标签",
        text=retention_data["日期"].dt.strftime("Mar %d"),
        size_max=100,
        template="plotly_white",
        height=350
    )
    
    fig_bubble.update_layout(
        title="留存率气泡图",
        xaxis=dict(
            title="次日留存率(%)",
            range=[67, 74],
            titlefont=dict(color=COLORS["text_primary"])
        ),
        yaxis=dict(
            title="7日留存率(%)",
            range=[40, 50],
            titlefont=dict(color=COLORS["text_primary"])
        ),
        coloraxis_colorbar=dict(
            title="7日留存率(%)",
            titlefont=dict(size=8, color=COLORS["text_primary"]),
            tickfont=dict(size=8, color=COLORS["text_secondary"])
        ),
        paper_bgcolor=COLORS["bg_ultralight"],
        plot_bgcolor=COLORS["bg_ultralight"]
    )
    
    # 调整文字位置
    fig_bubble.update_traces(
        textposition="top center",
        textfont=dict(size=12, weight="bold", color=COLORS["text_primary"])
    )
    
    st.plotly_chart(fig_bubble, use_container_width=True)
    st.markdown('<p class="data-source">气泡大小=日活UV , 颜色深浅=7日留存率</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 留存提升核心痛点
st.subheader("4.2 留存提升痛点")
st.markdown("""
<div style="line-height: 1.8;">
用户留存随时间呈现明显衰减趋势，核心流失节点集中在首单后7天、30天两个关键周期，需从用户分层运营、商品体验、场景拓展等多维度系统性优化。

<p style="margin: 12px 0 6px 0;"><strong>原因分析：</strong></p>
<p style="margin: 4px 0; padding-left: 2em;">1. 新用户首单依赖度高：首单多由大额补贴驱动，优惠结束后复购意愿显著下滑，7日留存较老用户低15个百分点，长期留存表现偏弱；</p>
<p style="margin: 4px 0; padding-left: 2em;">2. 精细化运营不足：低留存用户群体（30日留存<30%）触达频次仅为高留存用户的1/2，缺乏针对性唤醒策略，用户粘性难以提升；</p>
<p style="margin: 4px 0; padding-left: 2em;">3. 商品体验波动影响留存：生鲜品类品控不稳定（如蔬菜损耗、水果熟度不均）导致约20%的用户因体验问题流失，是影响长期留存的核心因素；</p>
<p style="margin: 4px 0; padding-left: 2em;">4. 场景覆盖不足：当前消费场景集中在晚餐时段，早餐、夜宵、应急采购等场景覆盖不足，用户使用频次提升受限，难以形成高频使用习惯。</p>

<p style="margin: 12px 0 6px 0;"><strong>业务建议：</strong></p>
<p style="margin: 4px 0; padding-left: 2em;">1. 针对新用户推出复购激励策略：首单后7天内发放专属复购券，结合“满减+品类券”组合，提升新用户长期留存水平；</p>
<p style="margin: 4px 0; padding-left: 2em;">2. 建立低留存用户标签体系：基于用户行为数据（如访问频次、品类偏好）划分流失风险等级，推送差异化运营内容（如专属优惠、场景化推荐）；</p>
<p style="margin: 4px 0; padding-left: 2em;">3. 优化生鲜品控流程：建立产地直采-仓配-履约全链路品控标准，降低损耗率并提升商品品质，减少因体验波动导致的用户流失；</p>
<p style="margin: 4px 0; padding-left: 2em;">4. 拓展非正餐时段商品组合：上线早餐套餐、夜宵半成品、应急快送等场景化商品，丰富消费场景，提升用户使用频次和粘性。</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ===================== 5. 商品销售分析（漏斗指定绿色系） =====================
st.markdown("### 5. 商品销售分析")
st.write("""
商品销售分析聚焦全国区域分布、核心品类表现及热销商品特征，为商品选品、区域运营提供数据支撑。
""") 

# 5.1 全国区域销售分布（漏斗指定绿色渐变）
st.markdown("### 5.1 全国区域销售分布")
st.write("""
从全国销售布局来看，平台营收集中在核心城市群，下沉市场仍有较大拓展空间。
数据说明：以下为2025年底叮咚买菜全国前10大省份GMV排名及月度变化。
""")

# 构造省份×月份GMV模拟数据
months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
provinces = province_data["省份"].tolist()
gmv_matrix = province_data["GMV亿元"].values.reshape(-1, 1) * (0.8 + 0.4 * np.sin(np.linspace(0, 2*np.pi, 12)))
df_gmv = pd.DataFrame(gmv_matrix, index=provinces, columns=months)

# 省份筛选器（仅控制热力图）
selected_provinces = st.multiselect(
    label="选择要展示的省份",
    options=provinces,
    default=provinces,
    label_visibility="hidden"
)
df_heatmap = df_gmv.loc[selected_provinces]

# 双栏布局（左大右小，高度一致）
col_map, col_mountain = st.columns([1.5, 1], gap="medium")

# 左栏：替换matplotlib热力图为Plotly热力图
with col_map:
    st.markdown("#### 各省份月度GMV热力图")
    
    # 重塑数据为Plotly热力图格式
    df_heatmap_reset = df_heatmap.reset_index().melt(id_vars="index", var_name="月份", value_name="GMV亿元")
    df_heatmap_reset.columns = ["省份", "月份", "GMV亿元"]
    
    fig_heatmap = px.imshow(
        df_heatmap.values,
        x=months,
        y=selected_provinces,
        labels=dict(x="月份", y="省份", color="GMV亿元"),
        color_continuous_scale=[COLORS["lightest_green"], COLORS["deepest_green"]],
        text_auto=".1f",
        template="plotly_white",
        height=600
    )
    
    fig_heatmap.update_layout(
        xaxis=dict(tickfont=dict(size=9, color=COLORS["text_secondary"])),
        yaxis=dict(tickfont=dict(size=9, color=COLORS["text_primary"])),
        coloraxis_colorbar=dict(
            title="GMV亿元",
            titlefont=dict(size=10, color=COLORS["text_primary"]),
            tickfont=dict(size=8, color=COLORS["text_secondary"])
        ),
        paper_bgcolor=COLORS["bg_ultralight"],
        plot_bgcolor=COLORS["bg_ultralight"]
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.markdown('<p class="data-source">数据来源：2025年底叮咚买菜GMV排名 | 月度波动为模拟值</p>', unsafe_allow_html=True)

# 右栏：替换matplotlib山峦图为Plotly面积图
with col_mountain:
    st.markdown("#### 各省份GMV分布山峦图")
    
    # 准备山峦图数据
    province_gmv_sorted = province_data.sort_values("GMV亿元", ascending=True)
    fig_mountain = go.Figure()
    
    spacing = 25
    scale = 0.5
    months_num = np.arange(12)
    
    for i, (idx, row) in enumerate(province_gmv_sorted.iterrows()):
        base_gmv = row["GMV亿元"]
        province_name = row["省份"]
        monthly_fluct = base_gmv * scale * np.exp(-((months_num - 5.5) ** 2) / (2 * 3 ** 2))
        monthly_fluct += np.random.normal(0, 1.2, size=12)
        
        # 计算Y轴位置（堆叠）
        y_vals = monthly_fluct + i * spacing
        
        # 添加面积图
        fig_mountain.add_trace(go.Scatter(
            x=months,
            y=y_vals,
            fill='tozeroy',
            name=province_name,
            fillcolor=px.colors.sample_colorscale([COLORS["lightest_green"], COLORS["deepest_green"]], i/len(province_gmv_sorted))[0],
            line=dict(color="white", width=1.2),
            hoverinfo="x+y+name",
            hoverlabel=dict(font=dict(size=8))
        ))
        
        # 添加省份标签
        fig_mountain.add_annotation(
            x=-0.5,
            y=y_vals.max()/2 + i*spacing,
            text=f"{province_name}<br>{base_gmv}亿",
            showarrow=False,
            font=dict(size=9, weight="bold", color=COLORS["text_primary"])
        )
    
    # 布局配置
    fig_mountain.update_layout(
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=8, color=COLORS["text_secondary"]),
            range=[-1, 11]
        ),
        yaxis=dict(visible=False),
        showlegend=False,
        height=600,
        paper_bgcolor=COLORS["bg_ultralight"],
        plot_bgcolor=COLORS["bg_ultralight"],
        margin=dict(l=80, r=10, t=10, b=40)
    )
    
    st.plotly_chart(fig_mountain, use_container_width=True)
    st.markdown('<p class="data-source">数据说明：月度波动为模拟值，反映GMV季节变化</p>', unsafe_allow_html=True)

st.markdown("""
<div style="line-height: 1.8;">
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;从叮咚买菜全国区域<strong>销售布局</strong>来看，平台GMV高度集中于核心城市群，头部省份贡献了主要营收：<strong>上海</strong>以全年累计超85亿元GMV稳居首位，<strong>北京、江苏、浙江</strong>紧随其后，单省年度GMV均突破60亿元，四省合计贡献了平台整体GMV的近60%，是当前营收基本盘；从<strong>月度表现</strong>看，头部省份GMV呈现明显季节性波动，以上海为例，3-5月GMV维持在90-102亿元高位，7月后逐步回落至40-50亿元区间，反映出生鲜消费的季节特征，而河南、安徽等下沉市场省份年度GMV仅20-25亿元，单月峰值不足30亿元，市场渗透度仍有较大提升空间；整体来看，叮咚买菜当前GMV分布呈现“<strong>头部集中、下沉不足</strong>”的特征，一线及新一线城市凭借消费能力与用户习惯成为稳定营收来源，而低线城市仍处于培育期，未来可通过爆款生鲜品类渗透与本地化运营，挖掘下沉市场商业潜力，进一步优化全国营收结构。
</div>
""", unsafe_allow_html=True)

# 5.2 热销商品特征分析 + 雷达图（漏斗指定绿色系）
st.markdown("### 5.2 热销商品特征分析")

col_pro1, col_pro2 = st.columns([1.2, 1], gap="medium")
with col_pro1:
    # 热销商品TOP10柱状图（漏斗指定绿色渐变）
    fig_top10 = px.bar(
        top10_products,
        x="商品名称",
        y="月销万件",
        color="客单价元",
        color_continuous_scale=[COLORS["lightest_green"], COLORS["deepest_green"]],  # 漏斗指定渐变
        title="热销商品TOP10",
        template="plotly_white",
        height=500,
        width=400
    )
    fig_top10.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_top10, use_container_width=True)
    st.markdown('<p class="data-source">数据来源：叮咚买菜商品销售数据库</p>', unsafe_allow_html=True)

with col_pro2:
    # 雷达图：漏斗指定绿色系梯度
    st.markdown(" ")
    radar_data = top10_products.head(5)
    fig_radar = go.Figure()
    # 雷达图配色：漏斗指定绿（lightest→deepest→lightest）
    radar_colors = [COLORS["lightest_green"], COLORS["light_green"], COLORS["mid_green"], COLORS["dark_green"], COLORS["deepest_green"]]
    theta_labels = ["月销占比", "客单价占比", "复购率", "毛利率"]
    for idx, row in radar_data.iterrows():
        r_vals = [
            row['月销万件'] / top10_products['月销万件'].max() * 100,
            row['客单价元'] / top10_products['客单价元'].max() * 100,
            row['复购率'],
            row['毛利率']
        ]
        fig_radar.add_trace(go.Scatterpolar(
            r=r_vals,
            theta=theta_labels,
            fill='toself',
            name=row['商品名称'],
            line=dict(color=radar_colors[idx]),
            fillcolor=radar_colors[idx],
            opacity=0.7
        ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        template='plotly_white',
        height=500,
        width=400
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('<p class="data-source">数据来源：叮咚买菜商品运营数据库</p>', unsafe_allow_html=True)

st.markdown("""
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;叮咚买菜热销商品TOP10均为生鲜刚需高频品类，土鸡蛋以25万件月销居首，纯牛奶、西红柿紧随其后，月销分别达22万件、18万件，前十商品月销均在9万件以上，客单价集中在7-25元区间，复购率普遍超68%，毛利率介于12%-23%。这类商品能成为爆款，核心因贴合城市家庭日常采购需求，且具备高性价比、高使用频次的特征，其中土鸡蛋、纯牛奶复购率超80%，正是依托生鲜食材的刚需属性与平台品控保障。
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;同时，西兰花、生菜等蔬菜毛利率超19%，体现出生鲜核心品类的盈利优势。未来可围绕TOP10爆款打造品类组合装，结合用户消费习惯推出“早餐食材包”“家常菜组合”等定制化套餐，同时针对高复购商品强化产地直采以降低成本，还可基于爆款品类的用户画像，拓展同类型高性价比新品，进一步提升核心刚需品类的销售规模与用户粘性。
<br>
""", unsafe_allow_html=True)

st.divider()

# ===================== 6. 核心结论与业务建议（漏斗指定绿色系信息框） =====================
st.subheader("6. 结论与建议")
st.write("""
### 6.1 经营结论
1. **增长质量良好**：UV、GMV、营收保持8%以上同比增长，盈利水平持续提升，已进入稳健盈利阶段；
2. **用户基础稳固**：日活规模、留存水平均高于行业均值，但新用户转化和复购仍有优化空间；
3. **商品结构合理**：生鲜核心品类占比超60%，预制菜等新品类增长迅速，但下沉市场覆盖不足；
4. **效率优势显著**：前置仓模式配送时效行业领先，供应链周转效率优于传统商超30%以上。

### 6.2 落地性业务建议
""")

# 业务建议卡片（漏斗绿色系4宫格，全报告统一）
col_a1, col_a2, col_a3, col_a4 = st.columns(4)
with col_a1:
    st.markdown("""
    <div class="custom-info-1">
        <strong>🎯 用户运营优化</strong>
        <ul>
            <li>新用户首单复购率提升至40%</li>
            <li>低留存用户触达频次翻倍</li>
            <li>建立新用户专属导购体系</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_a2:
    st.markdown("""
    <div class="custom-info-2">
        <strong>📦 供应链效率提升</strong>
        <ul>
            <li>蔬菜直采规模扩大至90%</li>
            <li>预制菜新品类SKU翻倍</li>
            <li>库存周转天数缩短至2.5天</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_a3:
    st.markdown("""
    <div class="custom-info-3">
        <strong>🛒 商品结构优化</strong>
        <ul>
            <li>蔬菜品类推出组合装/礼盒</li>
            <li>拓展水果切配、半成品等新品</li>
            <li>高损耗品类优化仓储条件</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_a4:
    st.markdown("""
    <div class="custom-info-4">
        <strong>🚀 市场拓展策略</strong>
        <ul>
            <li>核心城市前置仓加密布局</li>
            <li>加大下沉市场配送投入</li>
            <li>拓展早餐、夜宵场景消费</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Blinkit Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

df = pd.read_excel("cleaned_blinkit.xlsx")

# ---------------- CLEAN COLUMN NAMES ----------------

df.columns = df.columns.str.strip().str.lower()

# ---------------- FIX SALES COLUMN ----------------

df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
df = df.dropna(subset=['sales'])

# ---------------- SIDEBAR STYLE ----------------

st.markdown("""
<style>

[data-testid="stSidebar"]{
    background-color:#d4a900;
}

[data-testid="stSidebar"] *{
    color:black;
}

.main-title{
    color:green;
    font-size:45px;
    font-weight:bold;
    text-align:center;
}

.kpi-card{
    background-color:#f4c400;
    padding:20px;
    border-radius:12px;
    height:170px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    box-shadow:2px 2px 10px rgba(0,0,0,0.3);
    margin-bottom:10px;
}

.kpi-title{
    font-size:20px;
    font-weight:bold;
    color:black;
}

.kpi-value{
    font-size:38px;
    font-weight:bold;
    color:black;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.markdown(
    "<h1 style='color:black;'>Blinkit</h1>",
    unsafe_allow_html=True
)

st.sidebar.markdown("### India's Last Minute App")
st.sidebar.markdown("---")
st.sidebar.header("FILTER PANEL")

# ---------------- FILTERS ----------------

item_type = st.sidebar.multiselect(
    "Item Type",
    options=df['item_type'].dropna().unique(),
    default=df['item_type'].dropna().unique()
)

outlet_type = st.sidebar.multiselect(
    "Outlet Type",
    options=df['outlet_type'].dropna().unique(),
    default=df['outlet_type'].dropna().unique()
)

outlet_size = st.sidebar.multiselect(
    "Outlet Size",
    options=df['outlet_size'].dropna().unique(),
    default=df['outlet_size'].dropna().unique()
)

outlet_location = st.sidebar.multiselect(
    "Outlet Location",
    options=df['outlet_location_type'].dropna().unique(),
    default=df['outlet_location_type'].dropna().unique()
)

# ---------------- FILTER DATA ----------------

filtered_df = df[
    (df['item_type'].isin(item_type)) &
    (df['outlet_type'].isin(outlet_type)) &
    (df['outlet_size'].isin(outlet_size)) &
    (df['outlet_location_type'].isin(outlet_location))
]

# ---------------- KPIs ----------------

total_sales = filtered_df['sales'].sum()
avg_sales = filtered_df['sales'].mean()
total_items = filtered_df.shape[0]
rating = filtered_df['rating'].mean()

# ---------------- TITLE ----------------

st.markdown(
    "<h1 class='main-title'>🛒 Blinkit Sales Analytics Dashboard</h1>",
    unsafe_allow_html=True
)

st.write("")

# ---------------- KPI SECTION ----------------

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">$ {total_sales/1000000:.2f}M</div>
        <div class="kpi-title">Total Sales</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{rating:.2f}</div>
        <div class="kpi-title">Average Rating</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{total_items/1000:.2f}K</div>
        <div class="kpi-title">No of Items</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">₹ {avg_sales:.2f}</div>
        <div class="kpi-title">Average Sales</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- CHART ROW 1 ----------------

c1, c2 = st.columns(2)

with c1:
    fat_chart = filtered_df.groupby(
        ['outlet_location_type','item_fat_content'],
        as_index=False
    )['sales'].sum()

    fig1 = px.bar(
        fat_chart,
        x='sales',
        y='outlet_location_type',
        color='item_fat_content',
        orientation='h',
        title='FAT BY OUTLET'
    )

    st.plotly_chart(fig1, use_container_width=True)

with c2:
    item_chart = filtered_df.groupby(
        'item_type',
        as_index=False
    )['sales'].sum()

    fig2 = px.bar(
        item_chart.sort_values(by='sales', ascending=False).head(10),
        x='sales',
        y='item_type',
        orientation='h',
        color='sales',
        title='ITEM TYPE'
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------- CHART ROW 2 ----------------

c3, c4 = st.columns(2)

with c3:
    fat_sales = filtered_df.groupby(
        'item_fat_content',
        as_index=False
    )['sales'].sum()

    fig3 = px.pie(
        fat_sales,
        names='item_fat_content',
        values='sales',
        hole=0.5,
        title='FAT CONTENT'
    )

    st.plotly_chart(fig3, use_container_width=True)

with c4:
    outlet_size_chart = filtered_df.groupby(
        'outlet_size',
        as_index=False
    )['sales'].sum()

    fig4 = px.pie(
        outlet_size_chart,
        names='outlet_size',
        values='sales',
        title='OUTLET SIZE'
    )

    st.plotly_chart(fig4, use_container_width=True)

# ---------------- CHART ROW 3 ----------------

c5, c6 = st.columns(2)

with c5:
    location_chart = filtered_df.groupby(
        'outlet_location_type',
        as_index=False
    )['sales'].sum()

    fig5 = px.bar(
        location_chart,
        x='outlet_location_type',
        y='sales',
        color='outlet_location_type',
        title='OUTLET LOCATION'
    )

    st.plotly_chart(fig5, use_container_width=True)

with c6:
    year_chart = filtered_df.groupby(
        'outlet_establishment_year',
        as_index=False
    )['sales'].sum()

    fig6 = px.line(
        year_chart,
        x='outlet_establishment_year',
        y='sales',
        markers=True,
        title='OUTLET ESTABLISHMENT'
    )

    st.plotly_chart(fig6, use_container_width=True)

# ---------------- TABLE ----------------

st.subheader("SALES DETAIL")

table = filtered_df.groupby(
    'outlet_type',
    as_index=False
).agg({
    'sales':'sum',
    'item_identifier':'count'
})

table.columns = ['Outlet Type', 'Total Sales', 'No of Items']

st.dataframe(table, use_container_width=True)

# ---------------- DATA PREVIEW ----------------

st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20))
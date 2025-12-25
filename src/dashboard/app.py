import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# --- 1. SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from src.core.database import DatabaseManager
from src.analyzers.price_analyzer import PriceAnalyzer
from src.analyzers.market_analyzer import MarketAnalyzer
from src.analyzers.neighborhood_analyzer import NeighborhoodAnalyzer
from src.analyzers.comparative_analyzer import ComparativeAnalyzer

# --- 2. PAGE CONFIG ---
st.set_page_config(
    page_title="PropTech Analytics",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. CUSTOM CSS (Clean & Bright) ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    
    /* Card Styling */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetric"]:hover {
        border-color: #2563EB;
        transform: translateY(-2px);
        transition: all 0.2s ease;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid #F3F4F6; }
    .stTabs [aria-selected="true"] { color: #2563EB !important; border-bottom-color: #2563EB !important; }
    
    /* Map Container */
    .mapboxgl-canvas { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# --- 4. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        db = DatabaseManager()
        p_analyzer = PriceAnalyzer(db)
        m_analyzer = MarketAnalyzer(db)
        n_analyzer = NeighborhoodAnalyzer(db)
        c_analyzer = ComparativeAnalyzer(db)
        
        df = p_analyzer.get_dataframe()
        market_health = m_analyzer.get_market_health()
        neighborhood_stats = n_analyzer.compare_zip_codes()
        deals = c_analyzer.find_deals(discount_threshold=0.10)
        
        # Safety fills
        df['bedrooms'] = df['bedrooms'].fillna(0)
        df['square_feet'] = df['square_feet'].fillna(0)
        df['price'] = df['price'].fillna(0)
        
        return df, market_health, neighborhood_stats, deals
    except Exception:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df, market_health, neighborhood_stats, deals = load_data()

if df.empty:
    st.warning("⚠️ No data available. Please run the pipeline script.")
    st.stop()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("🎛️ Controls")
    st.markdown("###")
    
    cities = sorted(df['city'].unique())
    selected_cities = st.multiselect("📍 Select Cities", cities, default=cities[:3])
    
    min_p, max_p = int(df['price'].min()), int(df['price'].max())
    price_range = st.slider("💰 Price Budget", min_p, max_p, (min_p, max_p))
    
    st.divider()
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Report CSV", csv, "real_estate_report.csv", "text/csv", type="primary")

# Apply Filters
filtered_df = df[
    (df['city'].isin(selected_cities)) & 
    (df['price'].between(price_range[0], price_range[1]))
]

# --- 6. HEADER & METRICS ---
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("🏙️ PropTech Commander")
    st.caption(f"Real-Time Intelligence | {len(filtered_df)} Listings Active")

st.markdown("---")

m1, m2, m3, m4 = st.columns(4)
avg_price = filtered_df['price'].mean()
global_avg = df['price'].mean()
delta_val = round((avg_price - global_avg) / global_avg * 100, 1)

m1.metric("Properties Found", len(filtered_df))
m2.metric("Avg Price", f"${avg_price:,.0f}", delta=f"{delta_val}% vs Market")
m3.metric("Median Size", f"{filtered_df['square_feet'].median():,.0f} sqft")
m4.metric("Lowest Price", f"${filtered_df['price'].min():,.0f}")

st.markdown("###")

# --- 7. MAIN TABS ---
# WE ADDED "🗺️ Map Explorer" HERE
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Map Explorer", "📊 Market Visuals", "💎 Deal Hunter", "🏥 Health Check"])

# TAB 1: MAP EXPLORER (NEW!)
with tab1:
    st.subheader("📍 Geospatial View")
    
    # Filter for rows that actually have coordinates
    map_df = filtered_df.dropna(subset=['latitude', 'longitude'])
    
    if not map_df.empty:
        # Create a professional Mapbox scatter plot
        fig_map = px.scatter_mapbox(
            map_df,
            lat="latitude",
            lon="longitude",
            color="price",
            size="square_feet",
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=15,
            zoom=10,
            hover_name="address",
            hover_data=["price", "bedrooms", "city"],
            mapbox_style="open-street-map", # Free open source map style
            height=600
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("No GPS coordinates found for the selected properties. (Try running the pipeline again to fetch more coordinates)")

# TAB 2: VISUALS
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Price Distribution")
        fig = px.histogram(filtered_df, x="price", color="city", nbins=20, template="plotly_white", color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Value Map")
        plot_df = filtered_df.copy()
        plot_df['size_bubble'] = plot_df['bedrooms'].apply(lambda x: max(x, 2))
        fig = px.scatter(plot_df, x="square_feet", y="price", color="city", size="size_bubble", template="plotly_white", color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: DEALS
with tab3:
    st.subheader("🎯 Top Value Opportunities")
    active_deals = deals[deals['city'].isin(selected_cities)] if not deals.empty else pd.DataFrame()
    if not active_deals.empty:
        st.dataframe(
            active_deals,
            column_config={
                "price": st.column_config.NumberColumn(format="$%d"),
                "market_diff_pct": st.column_config.ProgressColumn("Discount Score", format="%.1f%%", min_value=-0.3, max_value=0),
                "url": st.column_config.LinkColumn("Link")
            },
            use_container_width=True
        )
    else:
        st.info("No deals found in this selection.")

# TAB 4: HEALTH
with tab4:
    h1, h2 = st.columns(2)
    with h1:
        st.subheader("Inventory Levels")
        st.bar_chart(market_health['Inventory Count'], color="#2563EB")
    with h2:
        st.subheader("Market Volatility")
        st.bar_chart(market_health['Price Volatility'], color="#10B981")
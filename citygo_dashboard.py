
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PALETTE  (deep blues · teals · soft corals)
# ─────────────────────────────────────────────
PAL = {
    "navy":       "#0D2B45",
    "blue":       "#1A4F72",
    "teal":       "#1D9E75",
    "teal_light": "#5DCAA5",
    "coral":      "#D85A30",
    "coral_light":"#F0997B",
    "amber":      "#BA7517",
    "slate":      "#4A5568",
    "muted":      "#718096",
    "bg":         "#F7F9FC",
    "card_bg":    "#FFFFFF",
}

CHART_COLORS = [
    PAL["teal"], PAL["blue"], PAL["coral"],
    PAL["amber"], PAL["teal_light"], PAL["coral_light"],
]

PLOTLY_LAYOUT = dict(
    font_family="'Inter', 'Segoe UI', sans-serif",
    font_color=PAL["navy"],
    font_size=14,
    title_font_size=16,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_size=12),
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CityGo Analytics",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
    .main { background: #F7F9FC; }
    [data-testid="stSidebar"] { background: #0D2B45; }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }

    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        border-left: 4px solid var(--accent);
        box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    }
    .kpi-label  { font-size: 14px; color: #718096; font-weight: 500; margin-bottom: 6px; letter-spacing:.04em; line-height: 1.4; }
    .kpi-value  { font-size: 32px; font-weight: 700; color: #0D2B45; line-height: 1.2; margin-bottom: 8px; }
    .kpi-delta  { font-size: 14px; margin-top: 4px; line-height: 1.4; }
    .positive   { color: #1D9E75; }
    .negative   { color: #D85A30; }
    .neutral    { color: #718096; }

    .section-header {
        font-size: 18px; font-weight: 600; color: #1A4F72;
        letter-spacing: .08em; text-transform: uppercase;
        border-bottom: 2px solid #1D9E75;
        padding-bottom: 8px; margin-bottom: 20px;
        line-height: 1.3;
    }
    .insight-card {
        background: white;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 12px;
        border-left: 3px solid var(--accent, #1D9E75);
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .insight-num  { font-size: 12px; font-weight: 700; color: #1D9E75; margin-bottom: 6px; letter-spacing: 0.5px; }
    .insight-text { font-size: 15px; color: #2D3748; line-height: 1.6; }
    .chart-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    }

    /* Improve sidebar readability */
    [data-testid="stSidebar"] h1 { font-size: 20px !important; margin-bottom: 4px !important; }
    [data-testid="stSidebar"] h2 { font-size: 16px !important; margin-bottom: 8px !important; }
    [data-testid="stSidebar"] h3 { font-size: 14px !important; margin-bottom: 12px !important; }
    [data-testid="stSidebar"] p { font-size: 14px !important; line-height: 1.5 !important; }

    /* Improve main content readability */
    .main h4 { font-size: 16px !important; font-weight: 600 !important; margin-bottom: 16px !important; line-height: 1.4 !important; }

    /* Footer improvements */
    .main p:last-child { font-size: 14px !important; line-height: 1.5 !important; }

    /* Dataframe styling */
    .stDataFrame { font-size: 14px !important; }
    .stDataFrame th { font-size: 14px !important; font-weight: 600 !important; padding: 12px 8px !important; }
    .stDataFrame td { font-size: 14px !important; padding: 10px 8px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA  (replace this block with: df = pd.read_csv("citygo_trips.csv"))
# ─────────────────────────────────────────────
@st.cache_data
def generate_data(n: int = 1_000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    vehicle_types = ["Economy", "Premium", "Shared", "SUV"]
    weights       = [0.40, 0.25, 0.20, 0.15]

    df = pd.DataFrame({
        "trip_id":      range(1, n + 1),
        "rider_id":     rng.integers(1, 200, n),
        "driver_id":    rng.integers(1, 80, n),
        "vehicle_type": rng.choice(vehicle_types, n, p=weights),
        "trip_fare":    np.clip(rng.normal(35.63, 14, n), 5, 95).round(2),
        "day_type":     rng.choice(["Weekday", "Weekend"], n, p=[0.65, 0.35]),
        "wait_time":    np.clip(rng.exponential(6, n), 1, 30).round(1),
        "trip_duration":np.clip(rng.normal(41.5, 15, n), 5, 120).round(1),
    })

    # Ratings: 18.1% unrated
    ratings = rng.choice(
        ["1","2","3","4","5","Not given"], n,
        p=[0.03, 0.05, 0.12, 0.35, 0.26, 0.19],
    )
    df["rating"] = ratings

    # Commission model
    df["commission_rate"]    = np.where(df["trip_fare"] > 25, 0.25, 0.15)
    df["commission_revenue"] = (df["trip_fare"] * df["commission_rate"]).round(2)
    df["fare_tier"]          = np.where(df["trip_fare"] > 25, "> $25 (25% commission)", "≤ $25 (15% commission)")

    return df


df = generate_data()

# ─── derived metrics ───────────────────────────────────────
total_revenue   = df["commission_revenue"].sum()
gross_fare      = df["trip_fare"].sum()
avg_fare        = df["trip_fare"].mean()
avg_duration    = df["trip_duration"].mean()
unrated_pct     = (df["rating"] == "Not given").mean() * 100
pct_above_25    = (df["trip_fare"] > 25).mean() * 100

rated_df        = df[df["rating"] != "Not given"].copy()
rated_df["rating_num"] = pd.to_numeric(rated_df["rating"])
driver_stats    = (
    rated_df.groupby("driver_id")["rating_num"]
    .agg(trips="count", avg_rating="mean")
    .reset_index()
)
bonus_eligible  = driver_stats[(driver_stats["trips"] > 15) & (driver_stats["avg_rating"] > 4.2)]

top3_riders     = df["rider_id"].value_counts().nlargest(3).reset_index()
top3_riders.columns = ["rider_id", "trips"]
top5_drivers    = df["driver_id"].value_counts().nlargest(5).reset_index()
top5_drivers.columns = ["driver_id", "trips"]


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("##  CityGo Analytics")
    st.markdown("*Internal BI Dashboard — v1.0*")
    st.markdown("---")

    # Filters
    st.markdown("### Filters")
    day_filter  = st.multiselect("Day type",  ["Weekday", "Weekend"],    default=["Weekday","Weekend"])
    veh_filter  = st.multiselect("Vehicle",   df["vehicle_type"].unique(), default=list(df["vehicle_type"].unique()))
    fare_range  = st.slider("Fare range ($)", float(df["trip_fare"].min()), float(df["trip_fare"].max()), (5.0, 95.0))

    st.markdown("---")
    st.markdown("### Insights & Actions")

    insights = [
        ("01", "#1D9E75", "Focus surge pricing on Economy rides — 68% of trips already exceed $25, maximising the 25% commission tier."),
        ("02", "#1A4F72", f"Activate bonus program for {len(bonus_eligible)} elite drivers (rating > 4.2, > 15 trips). Retention ROI > cost."),
        ("03", "#D85A30", "Deploy 20% discount vouchers to top-3 frequent riders. Their loyalty drives predictable demand."),
        ("04", "#BA7517", f"Close the {unrated_pct:.1f}% feedback gap with post-ride rating nudges — data-blind on 1-in-5 trips."),
    ]
    for num, color, text in insights:
        st.markdown(f"""
        <div class="insight-card" style="--accent:{color}">
            <div class="insight-num">RECOMMENDATION {num}</div>
            <div class="insight-text">{text}</div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
mask = (
    df["day_type"].isin(day_filter) &
    df["vehicle_type"].isin(veh_filter) &
    df["trip_fare"].between(*fare_range)
)
fdf = df[mask]

if fdf.empty:
    st.warning("No trips match the current filter selection.")
    st.stop()

f_revenue  = fdf["commission_revenue"].sum()
f_avg_fare = fdf["trip_fare"].mean()
f_avg_dur  = fdf["trip_duration"].mean()
f_unrated  = (fdf["rating"] == "Not given").mean() * 100


# ─────────────────────────────────────────────
# SECTION 1 — KPI STRIP
# ─────────────────────────────────────────────
st.markdown('<p class="section-header">Executive Overview</p>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

def kpi_card(col, label, value, delta_text, delta_type, accent):
    col.markdown(f"""
    <div class="kpi-card" style="--accent:{accent}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta {delta_type}">{delta_text}</div>
    </div>""", unsafe_allow_html=True)

kpi_card(k1, "Net Revenue (filtered)", f"${f_revenue:,.0f}", f"25%/15% commission model", "neutral", PAL["teal"])
kpi_card(k2, "Avg Trip Fare",          f"${f_avg_fare:.2f}", f"vs ${avg_fare:.2f} baseline", "positive" if f_avg_fare >= avg_fare else "negative", PAL["blue"])
kpi_card(k3, "Avg Trip Duration",      f"{f_avg_dur:.1f} min", f"vs {avg_duration:.1f} min baseline", "neutral", PAL["coral"])
kpi_card(k4, "Unrated Trips",          f"{f_unrated:.1f}%", "⚠ Feedback blind-spot" if f_unrated > 15 else "Within threshold", "negative" if f_unrated > 15 else "positive", PAL["amber"])

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SECTION 2 — REVENUE & FINANCIALS
# ─────────────────────────────────────────────
st.markdown('<p class="section-header">Revenue & Financials</p>', unsafe_allow_html=True)

col_a, col_b, col_c = st.columns([1, 1.5, 1.5])

# — Donut: revenue split by tier ——————————————
with col_a:
    tier_rev = fdf.groupby("fare_tier")["commission_revenue"].sum().reset_index()
    fig_donut = px.pie(
        tier_rev, values="commission_revenue", names="fare_tier",
        hole=0.58,
        color_discrete_sequence=[PAL["teal"], PAL["coral"]],
        title="Revenue by fare tier",
    )
    fig_donut.update_traces(textinfo="percent+label", textfont_size=13,
                            marker=dict(line=dict(color="white", width=2)))
    fig_donut.update_layout(**PLOTLY_LAYOUT, showlegend=False,
                            annotations=[dict(text=f"${f_revenue/1000:.0f}K", x=0.5, y=0.5,
                                              font_size=20, font_color=PAL["navy"], showarrow=False)])
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# — Bar: avg fare by vehicle type ————————————
with col_b:
    veh_fare = (
        fdf.groupby(["vehicle_type", "day_type"])["trip_fare"]
        .mean().reset_index()
        .rename(columns={"trip_fare": "avg_fare"})
    )
    fig_bar = px.bar(
        veh_fare, x="vehicle_type", y="avg_fare", color="day_type",
        barmode="group",
        color_discrete_sequence=[PAL["blue"], PAL["teal_light"]],
        title="Avg fare by vehicle & day type",
        labels={"avg_fare": "Avg Fare ($)", "vehicle_type": "Vehicle", "day_type": "Day"},
    )
    fig_bar.update_layout(**PLOTLY_LAYOUT)
    fig_bar.update_yaxes(gridcolor="#EDF2F7", gridwidth=0.5)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# — Scatter: fare vs duration ————————————————
with col_c:
    sample = fdf.sample(min(500, len(fdf)), random_state=1)
    fig_scatter = px.scatter(
        sample, x="trip_duration", y="trip_fare",
        color="vehicle_type",
        color_discrete_sequence=CHART_COLORS,
        opacity=0.65, size_max=7,
        title="Fare vs trip duration",
        labels={"trip_duration": "Duration (min)", "trip_fare": "Fare ($)", "vehicle_type": "Vehicle"},
        trendline="ols",
    )
    fig_scatter.add_hline(y=25, line_dash="dot", line_color=PAL["coral"],
                          annotation_text="$25 threshold", annotation_position="top left")
    fig_scatter.update_layout(**PLOTLY_LAYOUT)
    fig_scatter.update_yaxes(gridcolor="#EDF2F7", gridwidth=0.5)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SECTION 3 — OPERATIONS & DRIVER PERFORMANCE
# ─────────────────────────────────────────────
st.markdown('<p class="section-header">Operations & Driver Performance</p>', unsafe_allow_html=True)

col_d, col_e, col_f = st.columns([1.2, 1.6, 1.2])

# — Horizontal bar: top 5 drivers ————————————
with col_d:
    t5 = fdf["driver_id"].value_counts().nlargest(5).reset_index()
    t5.columns = ["driver_id", "trips"]
    t5["label"] = "Driver " + t5["driver_id"].astype(str)
    fig_drivers = px.bar(
        t5, x="trips", y="label", orientation="h",
        color="trips",
        color_continuous_scale=["#E1F5EE", PAL["teal"]],
        title="Top 5 drivers by trips",
        labels={"trips": "Total trips", "label": ""},
        text="trips",
    )
    fig_drivers.update_traces(textposition="outside")
    fig_drivers.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False,
                              yaxis=dict(autorange="reversed"))
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_drivers, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# — Scatter: driver bonus eligibility ————————
with col_e:
    rated_fdf = fdf[fdf["rating"] != "Not given"].copy()
    rated_fdf["rating_num"] = pd.to_numeric(rated_fdf["rating"])
    ds = (
        rated_fdf.groupby("driver_id")["rating_num"]
        .agg(trips="count", avg_rating="mean")
        .reset_index()
    )
    ds["eligible"] = (ds["trips"] > 15) & (ds["avg_rating"] > 4.2)
    ds["status"]   = ds["eligible"].map({True: "Bonus eligible ⭐", False: "Standard"})

    fig_bonus = px.scatter(
        ds, x="trips", y="avg_rating",
        color="status",
        color_discrete_map={"Bonus eligible ⭐": PAL["teal"], "Standard": "#CBD5E0"},
        size="trips", size_max=14,
        title="Driver bonus eligibility map",
        labels={"trips": "# Trips completed", "avg_rating": "Avg rating"},
        hover_data={"driver_id": True, "eligible": False},
    )
    fig_bonus.add_hline(y=4.2, line_dash="dash", line_color=PAL["coral"],
                        annotation_text="Rating threshold 4.2")
    fig_bonus.add_vline(x=15,  line_dash="dash", line_color=PAL["blue"],
                        annotation_text="15 trips")
    fig_bonus.update_layout(**PLOTLY_LAYOUT)
    fig_bonus.update_yaxes(gridcolor="#EDF2F7", gridwidth=0.5)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_bonus, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# — Donut + table: weekend fleet mix & loyalty riders ——
with col_f:
    wknd = fdf[fdf["day_type"] == "Weekend"]
    wknd_veh = wknd["vehicle_type"].value_counts().reset_index()
    wknd_veh.columns = ["vehicle_type", "count"]
    fig_wknd = px.pie(
        wknd_veh, values="count", names="vehicle_type",
        hole=0.5,
        color_discrete_sequence=CHART_COLORS,
        title="Weekend fleet mix",
    )
    fig_wknd.update_traces(textinfo="percent+label", textfont_size=12,
                           marker=dict(line=dict(color="white", width=2)))
    fig_wknd.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_wknd, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# — Bottom row: loyalty riders ——————————————
st.markdown("#### 🎟 Top 3 Loyalty Riders — 20% Discount Voucher Candidates")
r3 = fdf["rider_id"].value_counts().nlargest(3).reset_index()
r3.columns = ["rider_id", "trips"]
r3["trip_share (%)"] = (r3["trips"] / len(fdf) * 100).round(2)
r3["total_spend ($)"] = r3["rider_id"].apply(
    lambda rid: fdf[fdf["rider_id"] == rid]["trip_fare"].sum()
).round(2)
r3["voucher_value ($)"] = (r3["total_spend ($)"] * 0.20).round(2)
r3.index = [" 1st", "2nd", " 3rd"]
r3["rider_id"] = "Rider " + r3["rider_id"].astype(str)
st.dataframe(r3.rename(columns={"rider_id": "Rider"}), use_container_width=True)

# ─── footer ────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;font-size:14px;color:#A0AEC0;line-height:1.5;'>"
    "CityGo Analytics Dashboard · Built with Streamlit & Plotly · "
    "Data: citygo_trips.csv · Commission model: 25% (fare > $25) / 15% (fare ≤ $25)"
    "</p>",
    unsafe_allow_html=True,
)

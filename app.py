import streamlit as st
from data_processor import get_integrated_metrics
from forecaster import DualForecaster
import visuals as vis

st.set_page_config(page_title="SaaS Strategic Forecast Model", layout="wide")
metrics = get_integrated_metrics()

st.title("⚖️ Revenue Strategy: Trend vs. Predictive Model")
st.markdown("""
By comparing the **Organic Trend** (Natural Growth) against our **Predictive Model** (Active Strategy), 
we can quantify the exact 'Revenue Lift' our decisions create.
""")

# Sidebar
st.sidebar.header("Decision Levers")
p_adj = st.sidebar.slider("Pricing/Contract Optimization (%)", -10, 50, 0) / 100
s_adj = st.sidebar.slider("Growth Spend Intensity (%)", -50, 300, 0) / 100

# Run
engine = DualForecaster(metrics)
comparison_df = engine.run_comparison(price_mod=p_adj, spend_mod=s_adj)

# Visualization
st.plotly_chart(vis.plot_trend_vs_prediction(metrics['history_df'], comparison_df), use_container_width=True)

# THE TEST: Variance Analysis
st.divider()
trend_end = comparison_df['Organic_Trend'].iloc[-1]
pred_end = comparison_df['Predictive_Simulation'].iloc[-1]
lift = pred_end - trend_end

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Strategic Lift", f"${lift:,.0f}", f"{(lift/trend_end):+.1%}")
    st.caption("Revenue added (or lost) compared to doing nothing.")

with col2:
    if lift > 0:
        st.success("✅ STRATEGY VALIDATED: Your simulation outperforms the historical trend.")
    else:
        st.error("🚨 STRATEGY RISK: Your settings are currently diluting the natural growth of the business.")
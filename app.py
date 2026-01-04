import streamlit as st
from data_processor import get_business_actuals
from forecaster import StrategicForecaster
import plotly.graph_objects as go

st.set_page_config(page_title="Executive Revenue Strategy", layout="wide")

actuals = get_business_actuals()

# Header
st.title("Business Growth Strategy Simulator")
st.markdown("This tool allows you to simulate the financial outcome of changes to your product pricing and marketing investments.")

# Section 1: Business Overview
st.markdown("### Where the Business Stands Today")
c1, c2, c3 = st.columns([1, 1, 2])

with c1:
    st.metric("Total Yearly Revenue", f"${actuals['yearly_revenue']:,.0f}")
    st.metric("Cost to Acquire a Customer", f"${actuals['cost_per_customer']:,.0f}")

with c2:
    st.metric("Profitability Score", f"{actuals['profit_score']:.1f}x")
    st.write(f"For every $1.00 spent on marketing, we earn ${actuals['profit_score']:.2f} in total customer value.")

with c3:
    st.markdown("**Current Product Mix**")
    st.table(actuals['products'].style.format({"Monthly Price": "${:,.0f}", "Annual Revenue": "${:,.0f}"}))

st.markdown("---")

# Section 2: Strategy Levers (Sidebar)
st.sidebar.header("Pricing Strategy per Product")
p_basic = st.sidebar.slider("Basic Plan Price Change (%)", -10, 50, 0) / 100
p_pro = st.sidebar.slider("Pro Plan Price Change (%)", -10, 50, 0) / 100
p_ent = st.sidebar.slider("Enterprise Plan Price Change (%)", -10, 50, 0) / 100

st.sidebar.markdown("---")
st.sidebar.header("Marketing Investment")
budget_lever = st.sidebar.slider("Change Marketing Budget (%)", -50, 200, 0) / 100

# Section 3: Strategic Comparison
engine = StrategicForecaster(actuals)
price_mods = {'Basic': p_basic, 'Pro': p_pro, 'Enterprise': p_ent}
forecast_df = engine.run_simulation(12, price_mods, budget_lever)

st.markdown("### Strategic Growth Prediction")
st.markdown("The blue line shows the result of your strategy. The dashed gray line shows where the business would go if no changes were made.")

# Chart Logic
fig = go.Figure()
fig.add_scatter(x=actuals['history']['Month'], y=actuals['history']['Revenue'], name="Historical Revenue", line=dict(color="black", width=2))
future_labels = [f"Month +{m}" for m in forecast_df['Month']]
fig.add_scatter(x=future_labels, y=forecast_df['Status Quo'], name="Status Quo (No Change)", line=dict(color="gray", dash='dash'))
fig.add_scatter(x=future_labels, y=forecast_df['Strategic Strategy'], name="Strategic Prediction", line=dict(color="#00CC96", width=4))
fig.update_layout(template="plotly_white", yaxis_tickprefix="$")
st.plotly_chart(fig, use_container_width=True)

# Section 4: Summary Comparison
st.markdown("---")
st.markdown("### Strategy Comparison")
col_a, col_b, col_c = st.columns(3)

status_quo_final = forecast_df.iloc[-1]['Status Quo'] * 12
strategic_final = forecast_df.iloc[-1]['Strategic Strategy'] * 12
variance = strategic_final - status_quo_final

col_a.metric("Status Quo Yearly Revenue", f"${status_quo_final:,.0f}")
col_b.metric("Strategic Yearly Revenue", f"${strategic_final:,.0f}")
col_c.metric("Revenue Impact of Strategy", f"${variance:,.0f}", f"{(variance/status_quo_final):.1%}")

st.markdown(f"""
**Summary:** By adjusting your product pricing and marketing budget, you are projected to generate an additional 
**${variance:,.0f}** in yearly revenue compared to your current growth trajectory.
""")
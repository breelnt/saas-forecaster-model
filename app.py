import streamlit as st
from data_processor import get_business_actuals
from forecaster import BusinessForecaster
import visuals as vis  # <--- Importing your design file

# Page Configuration
st.set_page_config(page_title="Business Growth Simulator", layout="wide")

# 1. Load historical numbers
try:
    actuals = get_business_actuals()
except:
    st.error("Missing data files. Please check your repository for customers.csv, revenue.csv, and subscriptions.csv.")
    st.stop()

# 2. Header and Introduction
st.title("Business Growth Simulator")
st.markdown("""
This tool shows exactly how much money the business is making today and predicts 
where we will be in one year based on your decisions.
""")

# 3. Where the Business Stands Today
st.markdown("### Where the Business Stands Today")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Yearly Revenue", f"${actuals['yearly_revenue']:,.0f}")
c2.metric("Profitability Score", f"{actuals['profit_score']:.1f}x")
c3.metric("Cost per New Customer", f"${actuals['cost_per_customer']:,.0f}")
c4.metric("Customer Loss Rate", f"{actuals['loss_rate']:.1%}")

st.markdown("---")

# 4. Strategic Levers (Sidebar)
st.sidebar.header("Business Strategy")
st.sidebar.markdown("Adjust these sliders to see how your choices impact the bottom line.")

price_lever = st.sidebar.slider("Increase Prices by (%)", 0, 50, 0) / 100
spend_lever = st.sidebar.slider("Increase Marketing Budget by (%)", 0, 200, 0) / 100

# 5. Run the Prediction
engine = BusinessForecaster(actuals)
forecast_df = engine.predict(12, price_lever, spend_lever)

# 6. Display the Chart from visuals.py
st.markdown("### Predicted Growth")
# We call the function from our visuals.py file here
st.plotly_chart(vis.plot_growth_forecast(forecast_df), use_container_width=True)

# 7. Monthly Breakdown
st.markdown("### Month-by-Month Breakdown")
st.markdown("This table shows exactly how we get from our starting revenue to our goal.")

st.dataframe(forecast_df.style.format({
    "Revenue at Start": "${:,.0f}",
    "Marketing Investment": "${:,.0f}",
    "New Sales Revenue": "${:,.0f}",
    "Lost Sales Revenue": "${:,.0f}",
    "Revenue at End": "${:,.0f}"
}), use_container_width=True)

# 8. Final Executive Summary
st.markdown("---")
final_yearly = forecast_df.iloc[-1]['Revenue at End'] * 12
growth_total = final_yearly - actuals['yearly_revenue']

st.markdown(f"""
### The Bottom Line
Under this plan, your yearly revenue is predicted to grow from 
**${actuals['yearly_revenue']:,.0f}** to **${final_yearly:,.0f}**. 
This is an increase of **${growth_total:,.0f}** over the next 12 months.
""")
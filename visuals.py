import plotly.graph_objects as go

def plot_comparison_chart(history_df, forecast_df):
    fig = go.Figure()

    # 1. Past Performance
    fig.add_scatter(x=history_df['Month'], y=history_df['Revenue'], 
                    name="Past Revenue", line=dict(color="black", width=3))

    # 2. Future: Status Quo (The Simple Trend)
    future_dates = [f"Month +{m}" for m in forecast_df['Month']]
    fig.add_scatter(x=future_dates, y=forecast_df['Status Quo'], 
                    name="Organic Trend (Status Quo)", 
                    line=dict(color="gray", dash='dash'))

    # 3. Future: Strategic Strategy (The Prediction)
    fig.add_scatter(x=future_labels, y=forecast_df['Strategic Strategy'], 
                    name="Strategic Prediction", 
                    line=dict(color="#2E86C1", width=4))

    fig.update_layout(
        title="Revenue Forecast: Status Quo vs. Strategic Prediction",
        template="plotly_white",
        yaxis_tickprefix="$",
        hovermode="x unified"
    )
    return fig
import plotly.graph_objects as go

def plot_trend_vs_prediction(history_df, forecast_df):
    fig = go.Figure()

    # Historical Actuals
    fig.add_scatter(x=history_df['Month'], y=history_df['Revenue'], 
                    name="Actuals (History)", line=dict(color="black", width=4))

    # Labels for the future months
    future_labels = [f"Month +{m}" for m in forecast_df['Month']]

    # PATH A: Simple Trend
    fig.add_scatter(x=future_labels, y=forecast_df['Organic_Trend'], 
                    name="Organic Trend (Status Quo)", 
                    line=dict(color="gray", dash='dash'))

    # PATH B: Predictive Model
    fig.add_scatter(x=future_labels, y=forecast_df['Predictive_Simulation'], 
                    name="Predictive Simulation (Active Strategy)", 
                    line=dict(color="#00CC96", width=3))

    fig.update_layout(title="Strategic Gap Analysis: Trend vs. Prediction",
                      template="plotly_white", hovermode="x unified")
    return fig
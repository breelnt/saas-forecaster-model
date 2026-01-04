import pandas as pd

class DualForecaster:
    def __init__(self, metrics):
        self.metrics = metrics

    def run_comparison(self, months=24, price_mod=0.0, spend_mod=0.0):
        # Initial States
        mrr_trend = self.metrics['current_mrr']
        mrr_pred = self.metrics['current_mrr']
        
        # Predictive Adjustments
        adj_arpu = self.metrics['avg_arpu'] * (1 + price_mod)
        adj_churn = self.metrics['base_churn'] + (price_mod * 0.05)
        adj_cac = self.metrics['avg_cac'] * (1 + (spend_mod * 0.4))
        budget = (mrr_pred * 0.15) * (1 + spend_mod) # Budget as 15% of Revenue

        data = []
        for m in range(1, months + 1):
            # PATH A: The Simple Organic Trend (Status Quo)
            mrr_trend = mrr_trend * (1 + self.metrics['organic_momentum'])
            
            # PATH B: The Predictive Model (Strategic Intervention)
            new_rev = (budget / adj_cac) * adj_arpu
            loss = mrr_pred * adj_churn
            mrr_pred = mrr_pred + new_rev - loss
            
            data.append({
                "Month": m,
                "Organic_Trend": mrr_trend,
                "Predictive_Simulation": mrr_pred
            })
            
        return pd.DataFrame(data)
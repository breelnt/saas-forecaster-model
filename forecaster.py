import pandas as pd

class StrategicForecaster:
    def __init__(self, actuals):
        self.a = actuals

    def run_simulation(self, months, price_mods, budget_change):
        # Setup starting points
        mrr_trend = self.a['monthly_revenue']
        mrr_pred = self.a['monthly_revenue']
        
        # Strategy Logic
        # We assume marketing spend is split across products
        budget = (self.a['monthly_revenue'] * 0.15) * (1 + budget_change)
        
        # Calculate a weighted new price based on the product mix and specific sliders
        # price_mods is a dict: {'Basic': 0.1, 'Pro': 0.05, ...}
        current_weights = self.a['products'].set_index('Product')['Annual Revenue']
        current_weights = current_weights / current_weights.sum()
        
        avg_price_mod = sum([price_mods[p] * current_weights.get(p, 0) for p in price_mods])
        new_avg_price = self.a['products']['Monthly Price'].mean() * (1 + avg_price_mod)
        
        # Risk factors
        new_loss_rate = self.a['loss_rate'] + (avg_price_mod * 0.1) # Aggressive pricing increases loss
        new_cac = self.a['cost_per_customer'] * (1 + (budget_change * 0.4))

        results = []
        for m in range(1, months + 1):
            # Path 1: Simple Organic Trend (Status Quo)
            mrr_trend = mrr_trend * (1 + self.a['momentum'])
            
            # Path 2: Strategic Prediction
            new_sales = (budget / new_cac) * new_avg_price
            losses = mrr_pred * new_loss_rate
            mrr_pred = mrr_pred + new_sales - losses
            
            results.append({
                "Month": m,
                "Status Quo": mrr_trend,
                "Strategic Strategy": mrr_pred
            })
        return pd.DataFrame(results)
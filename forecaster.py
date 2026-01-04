import pandas as pd

class BusinessForecaster:
    def __init__(self, actuals):
        self.data = actuals

    def predict(self, months, price_change, budget_change):
        # Apply logic
        new_price = self.data['avg_bill'] * (1 + price_change)
        new_cost_per_customer = self.data['cost_per_customer'] * (1 + (budget_change * 0.4))
        monthly_budget = (self.data['monthly_revenue'] * 0.20) * (1 + budget_change)
        new_loss_rate = self.data['loss_rate'] + (price_change * 0.05)
        
        running_rev = self.data['monthly_revenue']
        forecast = []
        
        for m in range(1, months + 1):
            start_rev = running_rev
            customers_gained = monthly_budget / new_cost_per_customer
            revenue_gained = customers_gained * new_price
            revenue_lost = start_rev * new_loss_rate
            end_rev = start_rev + revenue_gained - revenue_lost
            
            forecast.append({
                "Month": f"Month {m}",
                "Revenue at Start": round(start_rev, 0),
                "Marketing Investment": round(monthly_budget, 0),
                "New Sales Revenue": round(revenue_gained, 0),
                "Lost Sales Revenue": round(revenue_lost, 0),
                "Revenue at End": round(end_rev, 0)
            })
            running_rev = end_rev
            
        return pd.DataFrame(forecast)
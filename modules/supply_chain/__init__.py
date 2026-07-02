class SupplyChainManager:
    def __init__(self):
        self.suppliers = {}
        self.inventory = {}

    def calculate_reorder(self, current_stock: int, daily_sales: float, lead_time_days: int, safety_days: int = 7) -> dict:
        safety_stock = int(daily_sales * safety_days)
        reorder_point = int(daily_sales * lead_time_days + safety_stock)
        suggested_order = max(reorder_point * 2 - current_stock, 0)

        return {
            "current_stock": current_stock,
            "daily_sales": daily_sales,
            "safety_stock": safety_stock,
            "reorder_point": reorder_point,
            "suggested_order": suggested_order,
            "urgency": "紧急" if current_stock <= safety_stock else ("关注" if current_stock <= reorder_point else "充足"),
        }

    def suggest_batch_plan(self, monthly_forecast: int, production_capacity: int) -> dict:
        batches = []
        remaining = monthly_forecast
        batch_num = 1
        while remaining > 0:
            batch_size = min(production_capacity, remaining)
            batches.append({"batch": batch_num, "quantity": batch_size})
            remaining -= batch_size
            batch_num += 1

        return {
            "total_forecast": monthly_forecast,
            "batches": batches,
            "total_batches": len(batches),
        }

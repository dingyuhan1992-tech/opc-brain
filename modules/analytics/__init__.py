from ai.engine import engine
from ai.prompts import SALES_ANALYSIS, COMPETITOR_ANALYSIS, INVENTORY_FORECAST


class SalesAnalyzer:
    def analyze(self, sales_data: list, product_name: str = "") -> dict:
        data_str = "\n".join([
            f"日期：{d.get('date')} | 销量：{d.get('sales_volume')} | 销售额：{d.get('sales_amount')} | 浏览量：{d.get('views')} | 收藏：{d.get('favorites')}"
            for d in sales_data
        ])
        prompt = f"产品：{product_name}\n\n销售数据：\n{data_str}"
        return engine.chat_json(SALES_ANALYSIS, prompt)


class CompetitorAnalyzer:
    def analyze(self, product_info: dict, competitor_data: list) -> dict:
        prompt = f"""我的产品：
名称：{product_info.get('name')}
功效：{product_info.get('benefits')}
价格：{product_info.get('price')}
成分：{product_info.get('ingredients')}

竞品数据：
{chr(10).join([f"- {c.get('name')}: 价格{c.get('price')}, 月销{c.get('monthly_sales')}, 评分{c.get('rating')}, 卖点:{c.get('selling_points')}" for c in competitor_data])}"""
        return engine.chat_json(COMPETITOR_ANALYSIS, prompt)


class InventoryForecaster:
    def forecast(self, sales_history: list, product_name: str = "") -> dict:
        data_str = "\n".join([
            f"月份：{d.get('month')} | 销量：{d.get('sales')}"
            for d in sales_history
        ])
        prompt = f"产品：{product_name}\n历史销售数据：\n{data_str}"
        return engine.chat_json(INVENTORY_FORECAST, prompt)

from ai.engine import engine


class MarketingEngine:
    def generate_promotion_plan(self, product_name: str, platform: str, budget: float, target: str) -> dict:
        prompt = f"""为以下产品制定推广计划：
产品：{product_name}
平台：{platform}
预算：{budget}元
目标：{target}

请提供推广方案，包含：
1. 推广渠道选择
2. 内容策略
3. 投放时间规划
4. 预算分配
5. KPI 预期

输出 JSON 格式。"""
        return engine.chat_json("你是一位资深的电商营销专家。", prompt)

    def generate_kol_outreach(self, product_name: str, kol_type: str, platform: str) -> str:
        prompt = f"""产品：{product_name}
KOL 类型：{kol_type}（宠物类博主/萌宠达人/宠物医生等）
平台：{platform}

请生成一份 KOL 合作邀请文案，要求：
1. 突出产品卖点
2. 说明合作方式
3. 体现对 KOL 的尊重和诚意"""
        return engine.chat("你是一位品牌商务负责人，擅长与 KOL 沟通合作。", prompt)

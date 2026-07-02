from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone

from ai.engine import engine
from modules.product.optimizer import ProductOptimizer
from modules.customer.chatbot import CustomerServiceBot
from modules.analytics import SalesAnalyzer, CompetitorAnalyzer, InventoryForecaster
from modules.customer.marketing import MarketingEngine
from modules.content import ContentGenerator
from modules.product.image import ImageOptimizer
from modules.supply_chain import SupplyChainManager

router = APIRouter(prefix="/api/v1")
optimizer = ProductOptimizer()
chatbot = CustomerServiceBot()
sales_analyzer = SalesAnalyzer()
competitor_analyzer = CompetitorAnalyzer()
inventory_forecaster = InventoryForecaster()
marketing = MarketingEngine()
content_gen = ContentGenerator()
image_opt = ImageOptimizer()
supply_chain = SupplyChainManager()


# ============ 商品优化 ============

class ProductInfo(BaseModel):
    name: str
    category: Optional[str] = "宠物保健品"
    ingredients: Optional[str] = ""
    pet_type: Optional[str] = "犬/猫"
    benefits: Optional[str] = ""
    specification: Optional[str] = ""
    price_range: Optional[str] = ""
    brand_name: Optional[str] = ""
    selling_points: Optional[str] = ""
    age_range: Optional[str] = "全年龄段"
    usage: Optional[str] = ""
    platform: Optional[str] = "淘宝"


@router.post("/product/optimize-title")
async def optimize_title(info: ProductInfo):
    result = optimizer.optimize_title(info.model_dump())
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/product/generate-detail")
async def generate_detail(info: ProductInfo):
    result = optimizer.generate_detail_page(info.model_dump())
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/product/generate-social")
async def generate_social(info: ProductInfo):
    result = optimizer.generate_social_content(info.model_dump())
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/product/optimize-image")
async def optimize_image(info: ProductInfo):
    result = image_opt.suggest_optimization(info.name, info.category, info.platform)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


# ============ 智能客服 ============

class CustomerQuery(BaseModel):
    question: str
    customer_name: Optional[str] = "亲"
    conversation_id: Optional[str] = None


@router.post("/customer/chat")
async def customer_chat(query: CustomerQuery):
    reply = chatbot.get_response(query.question, query.customer_name, query.conversation_id)
    return {"reply": reply}


@router.post("/customer/analyze-sentiment")
async def analyze_sentiment(data: dict):
    sentiment = chatbot.analyze_sentiment(data.get("message", ""))
    return {"sentiment": sentiment}


# ============ 数据分析 ============

class SalesDataInput(BaseModel):
    product_name: Optional[str] = ""
    data: List[dict]


@router.post("/analytics/sales")
async def analyze_sales(input_data: SalesDataInput):
    result = sales_analyzer.analyze(input_data.data, input_data.product_name)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


class CompetitorInput(BaseModel):
    product: ProductInfo
    competitors: List[dict]


@router.post("/analytics/competitor")
async def analyze_competitor(input_data: CompetitorInput):
    result = competitor_analyzer.analyze(input_data.product.model_dump(), input_data.competitors)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


class InventoryInput(BaseModel):
    product_name: Optional[str] = ""
    sales_history: List[dict]


@router.post("/analytics/forecast")
async def forecast_inventory(input_data: InventoryInput):
    result = inventory_forecaster.forecast(input_data.sales_history, input_data.product_name)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


# ============ 营销推广 ============

class MarketingInput(BaseModel):
    product_name: str
    platform: str = "抖音"
    budget: float = 10000
    target: str = "提升品牌知名度"


@router.post("/marketing/plan")
async def marketing_plan(input_data: MarketingInput):
    result = marketing.generate_promotion_plan(
        input_data.product_name, input_data.platform, input_data.budget, input_data.target
    )
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


class KOLInput(BaseModel):
    product_name: str
    kol_type: str = "宠物类博主"
    platform: str = "小红书"


@router.post("/marketing/kol-outreach")
async def kol_outreach(input_data: KOLInput):
    result = marketing.generate_kol_outreach(input_data.product_name, input_data.kol_type, input_data.platform)
    return {"content": result}


# ============ 内容生成 ============

class ContentInput(BaseModel):
    product_name: str
    platform: str = "抖音"
    audience: str = "养宠人群"
    duration: str = "60秒"
    style: str = "科普评测"


@router.post("/content/ad-copy")
async def ad_copy(input_data: ContentInput):
    result = content_gen.generate_ad_copy(input_data.product_name, input_data.platform, input_data.audience)
    return {"content": result}


@router.post("/content/video-script")
async def video_script(input_data: ContentInput):
    result = content_gen.generate_video_script(input_data.product_name, input_data.duration, input_data.style)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


# ============ 供应链 ============

class SupplyInput(BaseModel):
    current_stock: int
    daily_sales: float
    lead_time_days: int = 15
    safety_days: int = 7


@router.post("/supply/reorder")
async def reorder_calc(input_data: SupplyInput):
    return supply_chain.calculate_reorder(
        input_data.current_stock, input_data.daily_sales,
        input_data.lead_time_days, input_data.safety_days
    )


class BatchInput(BaseModel):
    monthly_forecast: int
    production_capacity: int


@router.post("/supply/batch-plan")
async def batch_plan(input_data: BatchInput):
    return supply_chain.suggest_batch_plan(input_data.monthly_forecast, input_data.production_capacity)


# ============ AI 自由对话 ============

class ChatInput(BaseModel):
    prompt: str
    system: Optional[str] = "你是一个专业的宠物保健品行业AI助手。"


@router.post("/ai/chat")
async def ai_chat(input_data: ChatInput):
    result = engine.chat(input_data.system, input_data.prompt)
    return {"reply": result}


# ============ 品牌健康度 ============

@router.get("/brand/health")
async def brand_health():
    return {
        "status": "healthy",
        "metrics": {
            "total_products": 0,
            "active_listings": 0,
            "total_sales": 0,
            "avg_rating": 0,
        },
        "suggestions": [
            "添加您的第一个产品开始使用 OPC Brain",
            "配置电商平台 API 以实现数据自动同步",
        ],
    }

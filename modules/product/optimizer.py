import json
import os
from datetime import datetime, timezone

from ai.engine import engine
from ai.prompts import (
    PRODUCT_TITLE_OPTIMIZATION,
    PRODUCT_DETAIL_GENERATION,
    SOCIAL_MEDIA_COPY,
)
from database.models import Product, ProductDetail, GeneratedContent, Brand
from database.db import SessionLocal


class ProductOptimizer:
    def optimize_title(self, product_info: dict) -> dict:
        prompt = f"""产品名称：{product_info.get('name')}
产品品类：{product_info.get('category')}
核心成分：{product_info.get('ingredients')}
适用宠物：{product_info.get('pet_type', '犬/猫')}
主要功效：{product_info.get('benefits')}
目标平台：{product_info.get('platform', '淘宝')}"""
        return engine.chat_json(PRODUCT_TITLE_OPTIMIZATION, prompt)

    def generate_detail_page(self, product_info: dict) -> dict:
        prompt = f"""产品名称：{product_info.get('name')}
品牌：{product_info.get('brand_name')}
产品功效：{product_info.get('benefits')}
核心成分：{product_info.get('ingredients')}
规格：{product_info.get('specification')}
适用宠物：{product_info.get('pet_type', '犬/猫')}
适用年龄：{product_info.get('age_range', '全年龄段')}
使用方法：{product_info.get('usage')}
价格区间：{product_info.get('price_range')}"""
        return engine.chat_json(PRODUCT_DETAIL_GENERATION, prompt)

    def generate_social_content(self, product_info: dict) -> dict:
        prompt = f"""产品名称：{product_info.get('name')}
品牌：{product_info.get('brand_name')}
主要功效：{product_info.get('benefits')}
核心成分：{product_info.get('ingredients')}
价格：{product_info.get('price_range')}
卖点：{product_info.get('selling_points', '天然安全，效果显著')}"""
        return engine.chat_json(SOCIAL_MEDIA_COPY, prompt)

    def save_optimized_content(self, product_id: int, content_type: str, platform: str, content: dict):
        db = SessionLocal()
        try:
            gc = GeneratedContent(
                product_id=product_id,
                content_type=content_type,
                platform=platform,
                content=json.dumps(content, ensure_ascii=False),
                created_at=datetime.now(timezone.utc),
            )
            db.add(gc)
            db.commit()
        finally:
            db.close()

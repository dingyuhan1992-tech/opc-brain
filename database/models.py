from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from database.db import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    logo = Column(String(500))
    description = Column(Text)
    slogan = Column(String(500))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    name = Column(String(300), nullable=False)
    subtitle = Column(String(500))
    category = Column(String(100))
    ingredients = Column(Text)
    specification = Column(String(200))
    price = Column(Float)
    cost_price = Column(Float)
    stock = Column(Integer, default=0)
    status = Column(String(20), default="draft")  # draft, active, discontinued
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    brand = relationship("Brand", back_populates="products")
    platform_listings = relationship("PlatformListing", back_populates="product")
    product_details = relationship("ProductDetail", back_populates="product")
    sales_data = relationship("SalesData", back_populates="product")


class ProductDetail(Base):
    __tablename__ = "product_details"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    version = Column(Integer, default=1)
    title = Column(String(500))
    description = Column(Text)
    highlights = Column(JSON)
    images = Column(JSON)
    seo_keywords = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    product = relationship("Product", back_populates="product_details")


class PlatformListing(Base):
    __tablename__ = "platform_listings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    platform = Column(String(50), nullable=False)  # taobao, douyin, xiaohongshu, wechat
    platform_product_id = Column(String(200))
    platform_url = Column(String(500))
    title = Column(String(500))
    price = Column(Float)
    status = Column(String(20), default="pending")  # pending, listed, paused, error
    last_sync_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    product = relationship("Product", back_populates="platform_listings")


class SalesData(Base):
    __tablename__ = "sales_data"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    platform = Column(String(50))
    date = Column(DateTime)
    sales_volume = Column(Integer, default=0)
    sales_amount = Column(Float, default=0)
    views = Column(Integer, default=0)
    favorites = Column(Integer, default=0)
    reviews_count = Column(Integer, default=0)
    avg_rating = Column(Float, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    product = relationship("Product", back_populates="sales_data")


class CustomerMessage(Base):
    __tablename__ = "customer_messages"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50))
    customer_id = Column(String(200))
    customer_name = Column(String(200))
    content = Column(Text)
    reply = Column(Text)
    intent = Column(String(100))
    sentiment = Column(String(20))
    is_auto_replied = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    replied_at = Column(DateTime)


class MarketingCampaign(Base):
    __tablename__ = "marketing_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300))
    platform = Column(String(50))
    type = Column(String(50))  # promotion, social_media, KOL, etc.
    content = Column(Text)
    budget = Column(Float)
    actual_cost = Column(Float)
    roi = Column(Float)
    status = Column(String(20), default="planning")
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class GeneratedContent(Base):
    __tablename__ = "generated_contents"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    content_type = Column(String(50))  # title, description, social_post, script, etc.
    platform = Column(String(50))
    content = Column(Text)
    version = Column(Integer, default=1)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

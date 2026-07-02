from datetime import datetime, timezone
from database.db import SessionLocal
from database.models import PlatformListing, Product


class PlatformManager:
    def __init__(self):
        self.platforms = {}

    def register_platform(self, name: str, config: dict):
        self.platforms[name] = config

    def sync_all(self):
        results = []
        for platform_name in self.platforms:
            try:
                result = self._sync_platform(platform_name)
                results.append({"platform": platform_name, "status": "success", "data": result})
            except Exception as e:
                results.append({"platform": platform_name, "status": "error", "error": str(e)})
        return results

    def _sync_platform(self, platform: str):
        return {"platform": platform, "synced_at": datetime.now(timezone.utc).isoformat(), "products_count": 0}

    def get_listing_status(self, platform: str) -> list:
        db = SessionLocal()
        try:
            listings = db.query(PlatformListing).filter(PlatformListing.platform == platform).all()
            return [
                {
                    "id": l.id,
                    "product_name": l.product.name if l.product else "未知",
                    "platform_product_id": l.platform_product_id,
                    "price": l.price,
                    "status": l.status,
                    "last_sync": l.last_sync_at.isoformat() if l.last_sync_at else None,
                }
                for l in listings
            ]
        finally:
            db.close()

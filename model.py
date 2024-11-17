from tortoise import fields
from tortoise.models import Model
import asyncio


class Symbol(Model):
    id = fields.IntField(pk=True)
    symbol = fields.CharField(max_length=100, unique=True)
    status = fields.CharField(max_length=50)
    base_asset = fields.CharField(max_length=50, index=True)
    quote_asset = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "symbol"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "symbol": self.symbol,
            "status": self.status,
            "baseAsset": self.base_asset,
            "quoteAsset": self.quote_asset,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
        }


class Announcement(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=500, unique=True)
    url = fields.CharField(max_length=500)
    url_hash = fields.CharField(max_length=50, index=True)
    time = fields.DateField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "announcement"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "urlHash": self.url_hash,
            "time": self.time.isoformat(),
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
        }

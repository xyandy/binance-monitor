from tortoise import fields
from tortoise.models import Model
import asyncio
from datetime import datetime, timezone, timedelta


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
            # "createdAt": self.created_at.isoformat(),
            # "updatedAt": self.updated_at.isoformat(),
        }


class Announcement(Model):
    id = fields.IntField(pk=True)
    article_id = fields.IntField(index=True)
    article_code = fields.CharField(max_length=50, index=True)
    article_title = fields.CharField(max_length=500)
    release_date = fields.BigIntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "announcement"

    def to_dict(self) -> dict:
        # 将 release_date (毫秒时间戳) 转换为东八区时间
        tz = timezone(timedelta(hours=8))
        time = datetime.fromtimestamp(self.release_date / 1000, tz).strftime('%Y-%m-%d %H:%M:%S')
        return {
            "id": self.id,
            "articleId": self.article_id,
            "articleCode": self.article_code,
            "articleTitle": self.article_title,
            "releaseDate": self.release_date,
            "time": time,
            # "createdAt": self.created_at.isoformat(),
            # "updatedAt": self.updated_at.isoformat(),
        }

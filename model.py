from tortoise import fields
from tortoise.models import Model
import asyncio


class Symbol(Model):
    id = fields.IntField(pk=True)
    symbol = fields.CharField(max_length=100, unique=True)
    status = fields.CharField(max_length=50)
    baseAsset = fields.CharField(max_length=50, index=True)
    quoteAsset = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "symbol"

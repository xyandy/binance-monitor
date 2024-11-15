import httpx
from typing import List
import json

from config import LOGGER, URL
from model import Symbol


async def get_exchange_info(url: str, timeout: float = 30.0) -> List[Symbol]:
    try:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(url, timeout=timeout)
            response.raise_for_status()

            data = response.json()
            symbols = data.get("symbols", [])
            return [
                Symbol(
                    symbol=s["symbol"],
                    base_asset=s["baseAsset"],
                    quote_asset=s["quoteAsset"],
                    status=s["status"],
                )
                for s in symbols
            ]
    except Exception as e:
        message = f"fail to exchange info: {str(e)}"
        LOGGER.error(message)
        return []


async def monitor_exchange_api():
    symbols = await Symbol.all()
    symbol_set = set(s.symbol for s in symbols)
    LOGGER.info(f"db symbol size: {len(symbol_set)}")

    exchange_info = await get_exchange_info(URL)
    if not exchange_info or len(exchange_info) == 0:
        LOGGER.info("exchange info is empty")
        return
    
    LOGGER.info(f"exchange info size: {len(exchange_info)}")
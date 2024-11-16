import json
import httpx
from typing import List

from config import LOGGER, URL
from model import Symbol
from util import send_email


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

    notify_list = []
    for s in exchange_info:
        if s.symbol not in symbol_set:
            await s.save()
            notify_list.append(s)

    if len(notify_list) > 0:
        symbol_dicts = [
            {
                "symbol": s.symbol,
                "baseAsset": s.base_asset,
                "quoteAsset": s.quote_asset,
                "status": s.status
            } for s in notify_list
        ]
        content = json.dumps(symbol_dicts, indent=2)
        send_email(f"binance add new api", content)
        LOGGER.info(f"notify list: {content}")

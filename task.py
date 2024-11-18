import json
import httpx
import asyncio
from typing import List
from datetime import datetime
from crawl4ai import AsyncWebCrawler


from config import LOGGER, EXCHANGE_API_URL, ANNOUNCEMENT_URL
from model import Symbol, Announcement
from util import send_email, extract_announcements, url_to_hash, parse_proxy_file
from random import choice


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

    exchange_info = await get_exchange_info(EXCHANGE_API_URL)
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
                "status": s.status,
            }
            for s in notify_list
        ]
        content = json.dumps(symbol_dicts, indent=2)
        send_email(f"binance add new token", content)
        LOGGER.info(f"notify list: {content}")


async def get_announcement(url: str, timeout: float = 60000):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    # 读取并随机选择一个代理
    proxies = [
        {
            "proxy": "http://198.23.239.134:6540",
            "username": "tmwyubph",
            "password": "7esnvu6mjsvz",
        },
        {
            "proxy": "http://207.244.217.165:6712",
            "username": "tmwyubph",
            "password": "7esnvu6mjsvz",
        },
        {
            "proxy": "http://107.172.163.27:6543",
            "username": "tmwyubph",
            "password": "7esnvu6mjsvz",
        },
        {
            "proxy": "http://64.137.42.112:5157",
            "username": "tmwyubph",
            "password": "7esnvu6mjsvz",
        },
        {
            "proxy": "http://173.211.0.148:6641",
            "username": "tmwyubph",
            "password": "7esnvu6mjsvz",
        },
        {
            "proxy": "http://161.123.152.115:6360",
            "username": "tmwyubph",
            "password": "7esnvu6mjsvz",
        },
        {
            "proxy": "http://167.160.180.203:6754",
            "username": "tmwyubph",
            "password": "7esnvu6mjsvz",
        },
        {
            "proxy": "http://154.36.110.199:6853",
            "username": "tmwyubph",
            "password": "7esnvu6mjsvz",
        },
        {
            "proxy": "http://173.0.9.70:5653",
            "username": "tmwyubph",
            "password": "7esnvu6mjsvz",
        },
        {
            "proxy": "http://173.0.9.209:5792",
            "username": "tmwyubph",
            "password": "7esnvu6mjsvz",
        },
    ]
    proxy = choice(proxies)
    proxy_config = {
        "proxy": proxy["proxy"],
        "username": proxy["username"],
        "password": proxy["password"],
    }

    try:
        async with AsyncWebCrawler() as crawler:
            page = await crawler.arun(
                url=url,
                headers=headers,
                proxy=proxy_config,  # 添加代理配置
                page_timeout=timeout,
                wait_until="networkidle",
                wait_time=5000,
            )
            if not page:
                raise Exception("page is null")
            filteredLinks = extract_announcements(page.links)
            return filteredLinks
    except Exception as e:
        message = f"fail to get announcement: {str(e)}"
        LOGGER.error(message)
        return []


async def monitor_announcement():
    db_announcements = await Announcement.all()
    announcement_set = set(a.url_hash for a in db_announcements)
    LOGGER.info(f"db announcement size: {len(announcement_set)}")

    announcements = await get_announcement(ANNOUNCEMENT_URL)
    if not announcements or len(announcements) == 0:
        LOGGER.info("announcement is empty")
        return
    LOGGER.info(f"announcement size: {len(announcements)}")

    notify_list = []
    for a in announcements:
        url_hash = url_to_hash(a["href"])
        if url_hash not in announcement_set:
            date_obj = datetime.strptime(a["time"], "%Y-%m-%d").date()
            await Announcement.create(
                title=a["text"],
                url=a["href"],
                url_hash=url_hash,
                time=date_obj,
            )
            notify_list.append(a)

    if len(notify_list) > 0:
        content = json.dumps(notify_list, indent=2)
        send_email(f"binance add new announcement", content)
        LOGGER.info(f"notify list: {content}")


if __name__ == "__main__":
    asyncio.run(get_announcement(ANNOUNCEMENT_URL))

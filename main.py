import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from contextlib import asynccontextmanager
from tortoise import Tortoise

# local dependency
from config import LOGGER, PORT, TORTOISE_ORM
from task import monitor_exchange_api
from model import Symbol

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init db
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    LOGGER.info("Sqlite connected")
    # add cronjob
    scheduler.add_job(
        monitor_exchange_api, "interval", minutes=1, max_instances=1, coalesce=True
    )
    scheduler.start()

    yield

    scheduler.shutdown()
    await Tortoise.close_connections()


app = FastAPI(title="binance-monitor", lifespan=lifespan)


@app.get("/symbols")
async def get_symbols(symbol: str | None = None) -> List[dict]:
    try:
        if symbol:
            symbols = await Symbol.filter(symbol=symbol)
        else:
            symbols = await Symbol.all()

        return [
            {
                "symbol": s.symbol,
                "baseAsset": s.base_asset,
                "quoteAsset": s.quote_asset,
                "status": s.status,
            }
            for s in symbols
        ]
    except Exception as e:
        message = f"fail to get symbols: {str(e)}"
        LOGGER.error(message)
        raise HTTPException(status_code=500, detail=message)


@app.delete("/symbols/{symbol}")
async def delete_symbol(symbol: str) -> dict:
    try:
        symbol_obj = await Symbol.get_or_none(symbol=symbol)
        if not symbol_obj:
            raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")

        await symbol_obj.delete()
        return {"message": f"Symbol {symbol} deleted successfully"}
    except Exception as e:
        message = f"fail to delete symbol {symbol}: {str(e)}"
        LOGGER.error(message)
        raise HTTPException(status_code=500, detail=message)


@app.get("/tokens")
async def get_tokens() -> List[str]:
    symbols = await Symbol.all()
    unique_tokens = set(s.base_asset for s in symbols)
    return list(unique_tokens)


if __name__ == "__main__":
    port = PORT
    uvicorn.run(app, host="0.0.0.0", port=port)
    LOGGER.info(f"server listens on {port}")

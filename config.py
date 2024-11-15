import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)

LOGGER = logging.getLogger(__name__)

PORT = 28000

TORTOISE_ORM = {
    "connections": {"default": "sqlite://sqlite/symbol.db3"},
    "apps": {
        "models": {
            "models": ["model"],
            "default_connection": "default",
        },
    },
}

URL = "https://api.binance.com/api/v3/exchangeInfo"

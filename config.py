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

EMIAL_CONFIG = {
    "host": "smtp.gmail.com",
    "port": 587,
    "sender": "xy913741894@gmail.com",
    "sender_name": "binance-monitor",
    "password": "cpbhlrkhziqejewx",
    "receiver": "xy913741894@qq.com",
}

EXCHANGE_API_URL = "https://api.binance.com/api/v3/exchangeInfo"
ANNOUNCEMENT_API_URL = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=48&pageNo=1&pageSize=5"

# ANNOUNCEMENT_URL = "https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48"

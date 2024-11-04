from src.config import settings
from connectors.redis_conn import RedisConnector

redis_connector = RedisConnector(url=settings.REDIS_URL)
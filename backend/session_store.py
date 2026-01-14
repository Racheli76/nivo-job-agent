import json
from typing import Any, Optional, Dict
from config import settings
import time

try:
    import redis.asyncio as aioredis
except Exception:
    aioredis = None


class BaseSessionStore:
    async def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    async def set(self, session_id: str, value: Dict[str, Any]) -> None:
        raise NotImplementedError

    async def delete(self, session_id: str) -> None:
        raise NotImplementedError


class InMemorySessionStore(BaseSessionStore):
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    async def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._store.get(session_id)

    async def set(self, session_id: str, value: Dict[str, Any]) -> None:
        self._store[session_id] = value

    async def delete(self, session_id: str) -> None:
        self._store.pop(session_id, None)


class RedisSessionStore(BaseSessionStore):
    def __init__(self, url: str):
        if not aioredis:
            raise RuntimeError('redis.asyncio not available')
        self._client = aioredis.from_url(url, decode_responses=True)

    async def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        raw = await self._client.get(session_id)
        if not raw:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return None

    async def set(self, session_id: str, value: Dict[str, Any]) -> None:
        await self._client.set(session_id, json.dumps(value))

    async def delete(self, session_id: str) -> None:
        await self._client.delete(session_id)


# choose store based on config
if settings.redis_url and aioredis:
    try:
        session_store: BaseSessionStore = RedisSessionStore(settings.redis_url)
    except Exception:
        session_store = InMemorySessionStore()
else:
    session_store = InMemorySessionStore()

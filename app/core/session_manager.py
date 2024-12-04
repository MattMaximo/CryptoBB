from typing import Optional
import aiohttp
from contextlib import asynccontextmanager

class SessionManager:
    _instance = None
    _session: Optional[aiohttp.ClientSession] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    async def get_session(cls, headers: dict = None) -> aiohttp.ClientSession:
        if cls._session is None or cls._session.closed:
            cls._session = aiohttp.ClientSession(headers=headers)
        return cls._session

    @classmethod
    async def close_session(cls):
        if cls._session and not cls._session.closed:
            await cls._session.close()
            cls._session = None

    @classmethod
    @asynccontextmanager
    async def get_session_context(cls, headers: dict = None):
        session = await cls.get_session(headers)
        try:
            yield session
        finally:
            pass  # We don't close the session here as it's reused 
import aiohttp
import asyncio
from typing import Optional

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; aiohttp-crawler/1.0; +https://yourdomain.com/bot)"
}

async def fetch(url: str, session: Optional[aiohttp.ClientSession] = None, timeout: int = 5) -> str:
    """
    异步请求网页，返回文本内容（HTML等）
    如果传入session，则复用该session，提升效率；否则内部创建新session。

    参数:
      - url: 目标URL
      - session: aiohttp.ClientSession对象（可选）
      - timeout: 超时时间，单位秒

    返回:
      - str: 响应文本内容

    抛出:
      - aiohttp.ClientError或asyncio.TimeoutError等异常
    """
    close_session = False
    if session is None:
        session = aiohttp.ClientSession(headers=DEFAULT_HEADERS)
        close_session = True

    try:
        async with session.get(url, timeout=timeout) as response:
            response.raise_for_status()  # 抛出状态异常
            return await response.text()
    finally:
        if close_session:
            await session.close()

import aiohttp
import asyncio
import logging
from typing import Optional
from utils.config import load_config

class AsyncFetcher:
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (compatible; aiohttp-crawler/1.0; +https://yourdomain.com/bot)"
    }

    def __init__(self, headers: Optional[dict] = None):
        self.headers = headers or self.DEFAULT_HEADERS
        self.config = load_config()
        self.timeout = self.config.get("timeout", 10)
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(__name__)
        self._setup_logger()

    def _setup_logger(self):
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        self.logger.debug("AsyncFetcher: 创建新的 ClientSession")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
            self.logger.debug("AsyncFetcher: 关闭 ClientSession")
            self.session = None

    async def fetch(self, url: str) -> str:
        """
        异步请求网页，返回文本内容

        参数:
          - url: 目标URL

        返回:
          - str: 响应文本内容

        抛出:
          - aiohttp.ClientError或asyncio.TimeoutError等异常
        """
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=self.headers)
            auto_close = True
            self.logger.debug("fetch: 创建临时 ClientSession")
        else:
            auto_close = False

        try:
            self.logger.info(f"开始请求: {url}")
            async with self.session.get(url, timeout=self.timeout) as response:
                response.raise_for_status()
                text = await response.text()
                self.logger.info(f"请求成功: {url} [状态码: {response.status}]")
                return text
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            self.logger.error(f"请求失败: {url} - 错误: {e}")
            raise
        finally:
            if auto_close and self.session:
                await self.session.close()
                self.logger.debug("fetch: 关闭临时 ClientSession")
                self.session = None

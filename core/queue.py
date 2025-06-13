import asyncio
import logging
import re
from typing import Tuple, Optional

from urllib.parse import urldefrag
from utils.config import load_config


class Deduplicator:
    def __init__(self):
        self.visited = set()
        self.config = load_config()

    def normalize(self, url: str) -> str:
        """
        去除 fragment，标准化 URL
        """
        clean_url, _ = urldefrag(url)
        return clean_url

    def is_seen(self, url: str) -> bool:
        url = self.normalize(url)
        if self.config.get("url_disallow_patterns", []):
            for pattern in self.config["url_disallow_patterns"]:
                if re.search(pattern, url):
                    return True
        return url in self.visited

    def mark_seen(self, url: str):
        url = self.normalize(url)
        self.visited.add(url)


# 设置 logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class QueueManager:
    def __init__(self, config: dict = load_config()):
        self.queue = asyncio.PriorityQueue()
        self.seen = Deduplicator()
        self.config = config or {}
        self.start_urls  = self.config.get("start_urls", [])
        logger.debug("QueueManager 初始化完成。")

    async def async_init(self, initial_urls: list[str] = None):
        if  initial_urls is None:
            initial_urls = self.start_urls
        for url in initial_urls:
            await self.add_url(url)
        logger.info("初始 URL 添加完成。")

    def _get_url_priority(self, url: str) -> int:
        """
        匹配规则并返回优先级，默认 0，优先级数值越小越优先
        """
        rules = self.config.get("priority_rules", [])
        for rule in rules:
            pattern = rule.get("pattern")
            priority = rule.get("priority", 0)
            if pattern and re.search(pattern, url):
                logger.debug(f"URL 匹配规则: {pattern}，设定优先级: {priority}")
                return -priority  # PriorityQueue 越小越优先
        return 0

    async def add_url(self, url: str, meta: Optional[dict] = None):
        """
        添加 URL 到队列中，带优先级和去重
        """
        if self.seen.is_seen(url):
            logger.debug(f"已跳过重复 URL: {url}")
            return

        priority = self._get_url_priority(url)
        await self.queue.put((priority, url, meta or {}))
        self.seen.mark_seen(url)
        logger.info(f"添加 URL: {url}，优先级: {priority}")

    async def get_url(self) -> Tuple[int, str, dict]:
        """
        获取下一个待处理的 URL
        """
        item = await self.queue.get()
        logger.debug(f"获取 URL: {item[1]}，优先级: {item[0]}")
        return item

    def is_empty(self) -> bool:
        """
        检查队列是否为空
        """
        empty = self.queue.empty()
        logger.debug(f"队列是否为空: {empty}")
        return empty

    def task_done(self):
        """
        当前任务处理完成
        """
        self.queue.task_done()
        logger.debug("标记当前任务已完成。")

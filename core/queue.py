import asyncio
from typing import Tuple, Optional
from core.deduplicator import Deduplicator
from core.rules import get_url_priority

class QueueManager:
    def __init__(self, config: dict = None):
        self.queue = asyncio.PriorityQueue()
        self.seen = Deduplicator()
        self.config = config or {}

    async def add_url(self, url: str, meta: Optional[dict] = None):
        """
        添加 URL 到队列中，带优先级和去重
        """
        if self.seen.is_seen(url):
            return
        priority = get_url_priority(url, self.config.get("priority_rules", []))
        await self.queue.put((priority, url, meta or {}))
        self.seen.mark_seen(url)

    async def get_url(self) -> Tuple[int, str, dict]:
        """
        获取下一个待处理的 URL
        """
        return await self.queue.get()

    def is_empty(self) -> bool:
        """
        检查队列是否为空
        """
        return self.queue.empty()

    def task_done(self):
        """
        当前任务处理完成
        """
        self.queue.task_done()

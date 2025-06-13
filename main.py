import asyncio
from core.queue import QueueManager
from core.fetcher import AsyncFetcher
from core.extractor import DataExtractor
from core.discover import LinkDiscover
from core.saver import DataSaver

async def main():
    queue = QueueManager()
    extractor = DataExtractor()
    saver = DataSaver()
    discover = LinkDiscover()
    # 加载url队列
    await queue.async_init()
    # 创建异步抓取器
    async with AsyncFetcher() as fetcher:
        while not queue.is_empty():
            priority, url, meta = await queue.get_url()
            try:
                # 获取返回文本
                html = await fetcher.fetch(url)
                #  提取数据
                data = extractor.extract(html, url)
                #  保存数据
                await saver.save(data, url)
                #  发现新的链接
                links = discover.extract_links(html, url)
                for link in links:
                    # 添加到队列
                    await queue.add_url(link)
            except Exception as e:
                print(f"Error processing {url}: {e}")
            queue.task_done()

if __name__ == "__main__":
    asyncio.run(main())

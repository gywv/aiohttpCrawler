import asyncio
from core.queue import QueueManager
from core.fetcher import AsyncFetcher
from core.extractor import DataExtractor
from core.discover import LinkDiscover
from core.saver import DataSaver
from utils.config import load_config

config = load_config()
CONCURRENT_REQUESTS = config.get("concurrent_requests", 10)


async def worker(queue, fetcher, extractor, saver, discover, semaphore):
    while True:
        item = await queue.get_url()
        priority, url, meta = item
        if url is None:
            # queue.task_done()
            break  # 退出循环
        try:
            async with semaphore:
                html = await fetcher.fetch(url)
            data = extractor.extract(html, url)
            await saver.save(data, url)
            links = discover.extract_links(html, url)
            for link in links:
                await queue.add_url(link)
        except Exception as e:
            print(f"Error processing {url}: {e}")
        finally:
            queue.task_done()


async def main():
    queue = QueueManager()
    extractor = DataExtractor()
    saver = DataSaver()
    discover = LinkDiscover()
    await queue.async_init()

    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async with AsyncFetcher() as fetcher:
        tasks = [asyncio.create_task(worker(queue, fetcher, extractor, saver, discover, semaphore)) for _ in range(CONCURRENT_REQUESTS)]

        # 等待所有URL任务完成
        await queue.join()

        # 添加哨兵值通知 worker 退出
        for _ in range(CONCURRENT_REQUESTS):
            await queue.add_url(None)  # 哨兵

        # 等待所有 worker 退出
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

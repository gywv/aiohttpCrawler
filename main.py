import asyncio
from core.queue import QueueManager
from core.fetcher import AsyncFetcher
from core.extractor import DataExtractor
from core.discover import LinkDiscover
from core.saver import DataSaver
from utils.config import load_config

cofig = load_config()
CONCURRENT_REQUESTS = cofig.get("concurrent_requests", 10)


async def worker(queue, fetcher, extractor, saver, discover, semaphore):
    while True:
        try:
            priority, url, meta = await queue.get_url()
        except asyncio.QueueEmpty:
            break

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
        tasks = [worker(queue, fetcher, extractor, saver, discover, semaphore) for _ in range(CONCURRENT_REQUESTS)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

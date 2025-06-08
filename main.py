import asyncio
import aiohttp
import yaml
import traceback

from core.queue import QueueManager
from core.fetcher import fetch
from core.extractor import DataExtractor
from core.discover import LinkDiscover
from core.saver import DataSaver
from utils.log import setup_logger
from utils.config import load_config 

async def main():
    
    try:
        config = load_config()
    except FileNotFoundError:
        print("配置文件 config.yaml 不存在，请检查文件路径。")
        input("按任意键退出...")
        return
    except yaml.YAMLError as e:
        print(f"配置文件格式错误: {e}")
        input("按任意键退出...")
        return

    logger = setup_logger(log_level=config.get("log_level", "INFO"))

    queue = QueueManager(config)
    extractor = DataExtractor(config)
    saver = DataSaver(config)
    discover = LinkDiscover(config)

    logger.info("初始化队列...")
    for url in config["start_urls"]:
        await queue.add_url(url)
        logger.info(f"添加初始URL: {url}")

    async with aiohttp.ClientSession() as session:
        while not queue.is_empty():
            priority, url, meta = await queue.get_url()
            logger.info(f"开始处理: {url} (priority={priority})")

            try:
                html = await fetch(url, session, timeout=config.get("fetch_timeout", 5))
                data = extractor.extract(html, url)
                await saver.save(data, url)
                logger.info(f"保存数据成功: {url}")

                links = discover.extract_links(html, url)
                logger.info(f"发现 {len(links)} 个新链接")
                for link in links:
                    await queue.add_url(link)

            except Exception as e:
                logger.error(f"处理失败: {url}")
                logger.error(traceback.format_exc())

            queue.task_done()


if __name__ == "__main__":
    asyncio.run(main())

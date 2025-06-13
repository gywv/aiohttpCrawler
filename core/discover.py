import re
import logging
from typing import List, Optional
from urllib.parse import urljoin, urlparse
from lxml import html as lxml_html
from utils.config import load_config

# 初始化 logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class LinkDiscover:
    def __init__(self, config: Optional[dict] = None):
        self.config = load_config()
        self.selector = "a[href]"
        self.allowed_domains = self.config.get("allowed_domains", [])
        self.exclude_patterns = [re.compile(p) for p in self.config.get("exclude_patterns", [])]

        logger.info("LinkDiscover 初始化完成。")
        logger.debug(f"使用选择器: {self.selector}，允许域名: {self.allowed_domains}，排除模式: {[p.pattern for p in self.exclude_patterns]}")

    def extract_links(self, page_html: str, base_url: str) -> List[str]:
        """
        提取页面中的所有符合规则的链接，补全相对 URL
        """
        try:
            tree = lxml_html.fromstring(page_html)
            tree.make_links_absolute(base_url)
        except Exception as e:
            logger.error(f"[HTML解析失败] base_url: {base_url}，错误: {str(e)}")
            return []

        links = []
        elements = tree.cssselect(self.selector)
        logger.debug(f"选择器匹配元素数: {len(elements)}")

        for el in elements:
            href = el.get("href")
            if not href:
                continue
            href = href.strip()
            if self._is_valid(href):
                links.append(href)
            else:
                logger.debug(f"被过滤链接: {href}")

        logger.info(f"从 {base_url} 提取到有效链接数: {len(links)}")
        return links

    def _is_valid(self, url: str) -> bool:
        if url.startswith(("javascript:", "mailto:", "tel:", "#")):
            return False

        if self.allowed_domains:
            domain = urlparse(url).netloc
            if domain not in self.allowed_domains:
                return False

        for pattern in self.exclude_patterns:
            if pattern.search(url):
                return False

        return True

from typing import List, Optional
from urllib.parse import urljoin, urlparse
from lxml import html as lxml_html
import re

class LinkDiscover:
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        # 默认提取规则：所有 <a> 标签 href 属性
        self.selector = self.config.get("link_selector", "a[href]")
        self.allowed_domains = self.config.get("allowed_domains", [])
        self.exclude_patterns = [re.compile(p) for p in self.config.get("exclude_patterns", [])]

    def extract_links(self, page_html: str, base_url: str) -> List[str]:
        """
        提取页面中的所有符合规则的链接，补全相对 URL
        """
        tree = lxml_html.fromstring(page_html)
        tree.make_links_absolute(base_url)  # 先自动补全所有链接

        links = []
        elements = tree.cssselect(self.selector)
        for el in elements:
            href = el.get("href")
            if not href:
                continue
            href = href.strip()
            if self._is_valid(href):
                links.append(href)
        return links

    def _is_valid(self, url: str) -> bool:
        # 过滤掉 javascript:, mailto:, tel: 等非 http(s) 链接
        if url.startswith(("javascript:", "mailto:", "tel:", "#")):
            return False

        # 过滤域名白名单
        if self.allowed_domains:
            domain = urlparse(url).netloc
            if domain not in self.allowed_domains:
                return False

        # 过滤排除规则
        for pattern in self.exclude_patterns:
            if pattern.search(url):
                return False

        return True

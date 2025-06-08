import re
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

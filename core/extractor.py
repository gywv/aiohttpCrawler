import re
import logging
from typing import Dict, Optional, List, Any
from lxml import html as lxml_html
from lxml.etree import XMLSyntaxError
from utils.config import load_config

# 配置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 可调整为 DEBUG 以查看更详细信息

# 控制台输出格式
console_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s')
console_handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(console_handler)


class DataExtractor:
    def __init__(self, config: Optional[Dict] = load_config()):
        """
        config 示例格式:
        {
            "data_extraction": [
                {"title": "css:h1.article-title"},
                {"date": "xpath://div[@class='date']/text()"},
                {"content": "css:div.article-body"},
                {"emails": "re:\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"}
            ]
        }
        """
        extraction = config.get("data_extraction", []) if config else []
        self.rules = self._normalize_rules(extraction)
        logger.info("DataExtractor 初始化完成，提取规则: %s", self.rules)

    def _normalize_rules(self, extraction: Any) -> Dict[str, str]:
        """
        统一规则格式为一个字典 {field: rule}
        """
        if isinstance(extraction, dict):
            return extraction
        elif isinstance(extraction, list):
            combined_rules = {}
            for item in extraction:
                if isinstance(item, dict):
                    combined_rules.update(item)
            return combined_rules
        return {}

    def _parse_html(self, page_html: str, url: str):
        """
        将HTML解析为DOM树，并处理异常
        """
        try:
            tree = lxml_html.fromstring(page_html)
            tree.make_links_absolute(url)
            logger.debug("HTML 解析成功: %s", url)
            return tree
        except XMLSyntaxError as e:
            logger.error("[HTML解析失败] URL: %s，错误信息: %s", url, str(e))
            return None

    def _extract_by_rule(self, tree, page_html: str, rule: str) -> List[str]:
        """
        根据规则提取字段值
        """
        values = []
        logger.debug("执行提取规则: %s", rule)

        if rule.startswith("css:"):
            selector = rule[4:]
            elements = tree.cssselect(selector)
            values = [el.text_content().strip() for el in elements if el.text_content().strip()]
            logger.debug("CSS提取 [%s]: %d 条结果", selector, len(values))

        elif rule.startswith("xpath:"):
            xpath_expr = rule[6:]
            elements = tree.xpath(xpath_expr)
            for el in elements:
                val = el.strip() if isinstance(el, str) else el.text_content().strip()
                if val:
                    values.append(val)
            logger.debug("XPath提取 [%s]: %d 条结果", xpath_expr, len(values))

        elif rule.startswith("re:"):
            pattern = rule[3:]
            try:
                matches = re.findall(pattern, page_html)
                values = [m.strip() for m in matches if m.strip()]
                logger.debug("正则提取 [%s]: %d 条结果", pattern, len(values))
            except re.error as e:
                logger.warning("[正则表达式错误] pattern: %s，错误信息: %s", pattern, str(e))

        else:
            logger.warning("[未知规则] rule: %s", rule)

        return values

    def extract(self, page_html: str, url: str) -> Dict[str, List[str]]:
        """
        提取页面数据
        """
        logger.info("开始提取 URL: %s", url)
        tree = self._parse_html(page_html, url)
        if not tree:
            logger.warning("提取失败：HTML树构建失败")
            return {}

        result: Dict[str, List[str]] = {}

        for field, rule in self.rules.items():
            values = self._extract_by_rule(tree, page_html, rule)
            result[field] = values
            logger.debug("字段 [%s] 提取结果: %s", field, values)

        result["url"] = [url]  # 保留来源网址
        logger.info("提取完成: %s", url)
        return result

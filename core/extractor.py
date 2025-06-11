import re
from typing import Dict, Optional, List, Any
from lxml import html as lxml_html

class DataExtractor:
    def __init__(self, config: Optional[Dict] = None):
        """
        config示例格式:
        {
            "data_extraction": {
                "title": "css:h1.article-title",
                "date": "xpath://div[@class='date']/text()",
                "content": "css:div.article-body",
                "emails": "re:\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
            }
        }
        """
        self.rules = config.get("data_extraction", {}) if config else {}

    def extract(self, page_html: str, url: str) -> Dict[str, List[str]]:
        """
        根据配置规则提取字段数据
        返回字典：{field: [value1, value2, ...], ...}

        所有字段统一返回为列表，匹配不到则为空列表。
        """
        tree = lxml_html.fromstring(page_html)
        result: Dict[str, List[str]] = {}

        for field, rule in self.rules.items():
            values: List[str] = []

            if rule.startswith("css:"):
                selector = rule[4:]
                elems = tree.cssselect(selector)
                values = [elem.text_content().strip() for elem in elems if elem.text_content().strip()]
            elif rule.startswith("xpath:"):
                xpath_expr = rule[6:]
                elems = tree.xpath(xpath_expr)
                for elem in elems:
                    if isinstance(elem, str):
                        val = elem.strip()
                    else:
                        val = elem.text_content().strip()
                    if val:
                        values.append(val)
            elif rule.startswith("re:"):
                pattern = rule[3:]
                matches = re.findall(pattern, page_html)
                values = [match.strip() for match in matches if match.strip()]
            else:
                # 默认按 CSS selector 处理
                elems = tree.cssselect(rule)
                values = [elem.text_content().strip() for elem in elems if elem.text_content().strip()]

            result[field] = values

        result["url"] = [url]
        return result

from typing import Dict, Optional
from lxml import html as lxml_html

class DataExtractor:
    def __init__(self, config: Optional[Dict] = None):
        """
        config示例格式:
        {
            "data_extraction": {
                "title": "css:h1.article-title",
                "date": "xpath://div[@class='date']/text()",
                "content": "css:div.article-body"
            }
        }
        """
        self.rules = config.get("data_extraction", {}) if config else {}

    def extract(self, page_html: str, url: str) -> Dict:
        """
        根据配置规则提取字段数据
        返回字典：{field: value, ...}

        如果某字段没匹配上，返回空字符串
        """
        tree = lxml_html.fromstring(page_html)
        result = {}

        for field, rule in self.rules.items():
            if rule.startswith("css:"):
                selector = rule[4:]
                elems = tree.cssselect(selector)
                text = elems[0].text_content().strip() if elems else ""
            elif rule.startswith("xpath:"):
                xpath_expr = rule[6:]
                elems = tree.xpath(xpath_expr)
                if isinstance(elems, list) and elems:
                    if isinstance(elems[0], str):
                        text = elems[0].strip()
                    else:
                        text = elems[0].text_content().strip()
                else:
                    text = ""
            else:
                # 默认按css selector处理
                elems = tree.cssselect(rule)
                text = elems[0].text_content().strip() if elems else ""

            result[field] = text
            result["url"] = url


        # 你可以在这里加入字段后处理，如日期格式化、数据清洗等

        return result

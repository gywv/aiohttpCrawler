import re

def get_url_priority(url: str, rules: list) -> int:
    """
    匹配规则并返回优先级，默认 0，优先级数值越小越优先
    """
    for rule in rules:
        pattern = rule.get("pattern")
        priority = rule.get("priority", 0)
        if re.search(pattern, url):
            return -priority  # PriorityQueue: 越小越优先
    return 0

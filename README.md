
# 🕸️ Async Web Crawler（异步网页爬虫）

一个基于 Python `asyncio` 和 `aiohttp` 的高性能可配置爬虫框架。支持并发抓取、链接发现、内容提取与保存，结构清晰、模块化，适合学习与二次开发。

---

## 📦 项目结构

```
crawler/
├── main.py                # 程序主入口
├── core/
│   ├── fetcher.py         # 网页下载器（异步）
│   ├── extractor.py       # 数据提取器（支持 CSS/XPath/正则）
│   ├── discover.py        # 链接提取与过滤
│   ├── saver.py           # 数据保存（JSON 或 TXT）
│   └── queue.py           # URL 队列与去重逻辑
├── utils/
│   └── config.py          # 配置加载器
├── config.yaml            # 配置文件（需用户自定义）
└── data/                  # 默认数据保存目录
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install aiohttp lxml pyyaml
```

### 2. 编写配置文件 `config.yaml`

示例内容如下：

```yaml
start_urls:
  - https://example.com

allowed_domains:
  - example.com

exclude_patterns:
  - "\\.pdf$"

concurrent_requests: 5
timeout: 10

data_extraction:
  - title: "css:h1"
  - content: "css:div.article"
  - date: "xpath://div[@class='date']/text()"
  - emails: "re:\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"

save_dir: "data"
save_as: "json"
file_prefix: "result"

priority_rules:
  - pattern: "news"
    priority: 10
```

### 3. 启动爬虫

```bash
python main.py
```

---

## 🔍 功能说明

| 模块            | 作用                           |
| ------------- | ---------------------------- |
| **main.py**   | 控制任务调度与协程执行                  |
| **fetcher**   | 发送异步 HTTP 请求，自动处理超时与异常       |
| **extractor** | 从网页中提取内容，支持 CSS、XPath 和正则表达式 |
| **discover**  | 从页面中提取链接，自动排除无效或重复 URL       |
| **queue**     | 使用优先队列实现任务管理，支持去重与优先级设置      |
| **saver**     | 按配置保存为 JSON 文件或 TXT 文本       |
| **config**    | 加载 YAML 配置文件，集中管理参数          |



## ✅ 特点亮点

* ✅ **全异步架构**：利用 `asyncio` + `aiohttp`，高并发低资源占用
* ✅ **模块化设计**：每个功能独立，便于扩展与维护
* ✅ **配置驱动**：无需改代码，修改 YAML 文件即可控制行为
* ✅ **去重机制**：自动防止重复抓取
* ✅ **日志详实**：内置 `logging`，方便调试和追踪



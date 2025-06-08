
# 🚀 Async Web Crawler

一个基于 `aiohttp` 异步框架构建的轻量级网页爬虫，支持链接发现、数据提取、去重、优先级调度与数据保存等功能。适用于定向抓取、内容监控等场景。

---

## 🌟 特性 Features

* ✅ **异步请求**：使用 `aiohttp` 实现高效非阻塞网页抓取。
* ✅ **自动发现链接**：通过配置化规则发现网页中的子链接。
* ✅ **URL 去重**：避免重复访问，提高效率。
* ✅ **优先级调度**：支持通过正则表达式设置抓取优先级。
* ✅ **自定义数据提取**：支持 `CSS Selector` 与 `XPath` 配置提取字段。
* ✅ **本地保存数据**：以 `JSON` 文件格式存储提取结果。
* ✅ **配置驱动**：所有抓取逻辑与参数均通过 `config.yaml` 配置。

---

## 📁 项目结构

```
crawler/
├── core/
│   ├── deduplicator.py    # URL 去重管理器
│   ├── discover.py        # 链接发现模块
│   ├── extractor.py       # 数据提取器
│   ├── fetcher.py         # 网页请求器（异步）
│   ├── queue.py           # URL 队列管理器（带优先级）
│   ├── rules.py           # 优先级规则处理
│   ├── saver.py           # 数据保存器
├── utils/
│   ├── config.py          # 配置加载器
│   ├── log.py             # 日志系统
├── config.yaml            # 配置文件
├── main.py                # 程序入口
```

---

## 🚀 快速开始

### 1. 安装依赖

建议使用 Python 3.8 及以上版本。

```bash
pip install aiohttp lxml PyYAML
```

### 2. 编辑配置文件

在 `config.yaml` 中设置起始 URL、提取规则、域名白名单等：

```yaml
start_urls:
  - "https://example.com"

allowed_domains:
  - "example.com"

data_extraction:
  title: "css:h1.title"
  content: "css:div.content"

priority_rules:
  - pattern: ".*post.*"
    priority: 10
```

### 3. 启动爬虫

```bash
python main.py
```

---

## ⚙️ 配置说明

配置文件 `config.yaml` 支持以下字段：

| 字段                | 类型   | 说明                          |
| ----------------- | ---- | --------------------------- |
| `start_urls`      | list | 初始抓取入口                      |
| `allowed_domains` | list | 允许抓取的域名                     |
| `priority_rules`  | list | 优先级设置，正则匹配 URL，数字越大越优先      |
| `data_extraction` | dict | 字段提取规则，支持 `css:` 和 `xpath:` |
| `save_dir`        | str  | 数据保存目录                      |
| `save_as`         | str  | 保存格式（目前仅支持 `json`）          |
| `log_level`       | str  | 日志等级（如 `INFO`, `DEBUG`）     |
| `fetch_timeout`   | int  | 单个请求的超时时间（秒）                |

---

## 🔧 示例提取规则

```yaml
data_extraction:
  title: "css:h1.article-title"
  author: "css:span.author"
  date: "xpath://div[@class='meta']/time/text()"
```

---

## 📌 注意事项

* 本项目不自动遵守 `robots.txt`，请在合法合规前提下使用。
* 若抓取大量页面，建议使用代理池与异常重试机制进行增强。
* 多条数据不会写入一个文件，每条记录单独保存在一个 JSON 文件中。

---

## 📄 License

MIT License





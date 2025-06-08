# utils/log.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os

_logger_cache = {}

def setup_logger(
    name: str = "aiohttp_crawler",
    log_level: str = "INFO",
    log_dir: str = "logs",
    log_file: str = "crawler.log",
    when: str = "midnight",
    backup_count: int = 7,
) -> logging.Logger:
    """
    创建并返回一个配置好的 Logger 对象，确保全局唯一。
    """
    if name in _logger_cache:
        return _logger_cache[name]

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 控制台 handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # 文件 handler
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, log_file)
        fh = TimedRotatingFileHandler(log_path, when=when, backupCount=backup_count, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    _logger_cache[name] = logger
    return logger

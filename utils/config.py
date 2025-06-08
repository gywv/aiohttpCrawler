# utils/config.py
import yaml
import os

_config_cache = None

def load_config(config_path="config.yaml"):
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        try:
            _config_cache = yaml.safe_load(f)
            return _config_cache
        except yaml.YAMLError as e:
            raise ValueError(f"配置文件格式错误: {e}")

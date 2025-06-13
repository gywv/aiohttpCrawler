import json
import os
import logging
from typing import Dict, Optional, Union

# 配置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 根据需要改为 DEBUG

# 控制台输出格式
console_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s')
console_handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(console_handler)


class DataSaver:
    def __init__(self, config: Optional[Dict] = None):
        """
        config 示例：
        {
            "save_dir": "data",
            "save_as": "json",  # 支持 "json" 或 "txt"
            "file_prefix": "result"  # 文件名前缀
        }
        """
        self.config = config or {}
        self.save_dir = self.config.get("save_dir", "data")
        self.save_as = self.config.get("save_as", "json")
        self.file_prefix = self.config.get("file_prefix", "result")

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            logger.info("创建保存目录: %s", self.save_dir)

        self._file_index = 0  # 用于 JSON 文件命名
        logger.info("DataSaver 初始化完成。保存格式: %s，目录: %s", self.save_as, self.save_dir)

    async def save(self, data: Union[Dict, str], url: Optional[str] = None):
        """
        保存数据到文件。
        - JSON 模式：每条数据一个文件。
        - TXT 模式：所有数据追加保存到一个文件中。
        """
        try:
            if self.save_as == "json":
                await self._save_json(data, url)
            elif self.save_as == "txt":
                await self._save_txt(data, url)
            else:
                logger.error("不支持的保存格式: %s", self.save_as)
                raise NotImplementedError(f"Save format '{self.save_as}' not implemented yet.")
        except Exception as e:
            logger.exception("保存数据时出错: %s", str(e))

    async def _save_json(self, data: Dict, url: Optional[str] = None):
        filename = f"{self.file_prefix}_{self._file_index}.json"
        self._file_index += 1

        filepath = os.path.join(self.save_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info("数据已保存为 JSON: %s", filepath)
        except Exception as e:
            logger.error("保存 JSON 文件失败: %s，错误: %s", filepath, str(e))
            raise

    async def _save_txt(self, data: Union[Dict, str], url: Optional[str] = None):
        filename = f"{self.file_prefix}.txt"
        filepath = os.path.join(self.save_dir, filename)

        if isinstance(data, dict):
            data_str = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            data_str = str(data)

        try:
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(data_str + "\n\n")
            logger.info("数据已追加保存为 TXT: %s", filepath)
        except Exception as e:
            logger.error("保存 TXT 文件失败: %s，错误: %s", filepath, str(e))
            raise

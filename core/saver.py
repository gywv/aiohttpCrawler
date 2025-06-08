import json
import os
from typing import Dict, Optional

class DataSaver:
    def __init__(self, config: Optional[Dict] = None):
        """
        config 示例：
        {
            "save_dir": "data",
            "save_as": "json",  # 未来可以支持 txt、csv 等
            "file_prefix": "result"  # 文件名前缀
        }
        """
        self.config = config or {}
        self.save_dir = self.config.get("save_dir", "data")
        self.save_as = self.config.get("save_as", "json")
        self.file_prefix = self.config.get("file_prefix", "result")

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        # 用于给文件命名
        self._file_index = 0

    async def save(self, data: Dict, url: Optional[str] = None):
        """
        保存一条数据到文件，文件名自动生成
        """
        if self.save_as == "json":
            await self._save_json(data, url)
        else:
            raise NotImplementedError(f"Save format '{self.save_as}' not implemented yet.")

    async def _save_json(self, data: Dict, url: Optional[str] = None):
        # 简单起见，每条数据保存为一个 json 文件，文件名基于自增计数
        filename = f"{self.file_prefix}_{self._file_index}.json"
        self._file_index += 1

        filepath = os.path.join(self.save_dir, filename)
        # 异步写文件（aiofiles也可以用，但这里同步足够）
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

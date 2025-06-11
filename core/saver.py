import json
import os
from typing import Dict, Optional, Union

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

        self._file_index = 0  # 用于 JSON 文件命名

    async def save(self, data: Union[Dict, str], url: Optional[str] = None):
        """
        保存数据到文件。
        - JSON 模式：每条数据一个文件。
        - TXT 模式：所有数据追加保存到一个文件中。
        """
        if self.save_as == "json":
            await self._save_json(data, url)
        elif self.save_as == "txt":
            await self._save_txt(data, url)
        else:
            raise NotImplementedError(f"Save format '{self.save_as}' not implemented yet.")

    async def _save_json(self, data: Dict, url: Optional[str] = None):
        filename = f"{self.file_prefix}_{self._file_index}.json"
        self._file_index += 1

        filepath = os.path.join(self.save_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    async def _save_txt(self, data: Union[Dict, str], url: Optional[str] = None):
        """
        以文本形式保存，所有数据都写入同一个txt文件中（追加模式）。
        每条数据之间空一行。
        """
        filename = f"{self.file_prefix}.txt"
        filepath = os.path.join(self.save_dir, filename)

        # 如果是字典，先转换为 JSON 字符串格式，便于可读性
        if isinstance(data, dict):
            data_str = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            data_str = str(data)

        with open(filepath, "a", encoding="utf-8") as f:
            f.write(data_str + "\n\n")

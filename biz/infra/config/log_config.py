import json
import logging
from datetime import datetime
from pathlib import Path


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "@timestamp": datetime.now().isoformat() + "Z",
            "caller": f"{Path(record.pathname).name}:{record.lineno}",  # 只记录文件名和行号
            "content": record.getMessage(),
            "level": record.levelname
        }
        return json.dumps(log_record, ensure_ascii=False)


def log_init():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = JsonFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

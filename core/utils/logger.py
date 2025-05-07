import psutil

from core.logger import logger


class Logger:
    async def log_memory_usage(self, file):
        memory_info = psutil.virtual_memory()
        total_memory = round(memory_info.total / (1024 ** 3), 1)
        used_memory = round(memory_info.used / (1024 ** 3), 1)
        percent_used = memory_info.percent
        logger.info(f"FILE: {file} | Ram usage: {used_memory}/{total_memory} GB ({percent_used}%)")

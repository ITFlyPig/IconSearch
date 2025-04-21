from loguru import logger
import os

def init_logger(log_dir: str, log_name: str):
    # 配置日志
    logger.add(
        os.path.join(log_dir, f"{log_name}"+"_{time}.log"),  # 动态日志路径
        rotation=10 * 1024 * 1024,  # 每 10MB 轮转一个新文件
        retention=10,  # 最多保留 10 个文件
        format="{time} | {level} | {message}",
        level="INFO",  # 日志级别
        # compression="zip"  # 可选：压缩旧日志文件
    )


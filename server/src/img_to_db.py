import os.path

from loguru import logger
from server.src.ai_model import AiModel
from server.src.db import VectorDB

class ImgDirHandler:
    def __init__(self, vector_db: VectorDB, model: AiModel):
        self.vector_db = vector_db
        self.model = model

    def handle_dir(self, dir_path: str):
        """
        处理目录
        :return:
        """
        logger.info(f'handle dir:{dir_path}')
        # 获取目录下的所有文件和子目录
        files = os.listdir(dir_path)
        # 遍历文件
        for file in files:
            file_path = os.path.join(dir_path, file)
            if not os.path.isfile(file_path):
                continue
            image_features = self.model.to_vector(file_path)
            if image_features is None:
                logger.info(f'parse file:{file_path} vector error')
                continue
            self.vector_db.save(image_features, file_path)
        logger.info(f'handle dir:{dir_path} done')


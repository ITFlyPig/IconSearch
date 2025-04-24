import os
import uuid

from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest


class VectorDB:
    def __init__(self, host: str, port: int, collection_name: str, size: int):
        self.host = host
        self.port = port
        self.size = size
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(host=self.host, port=self.port)
        self._get_or_create_collection(collection_name, self.size)

    def _get_or_create_collection(self, collection_name: str, size: int):
        """
        创建集合
        :param collection_name:
        :param size:
        :return:
        """
        # try:
        #     collection = self.qdrant_client.get_collection(collection_name=collection_name)
        #     if collection is not None:
        #         return
        # except Exception as e: # 集合不存在
        #     pass
        self.qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=rest.VectorParams(size=size, distance=rest.Distance.COSINE),
        )

    def save(self, img_vector, img_path: str) -> bool:
        """
        将给定的图片和向量保存到数据库
        :param img_vector:
        :param img_path:
        :return:
        """
        file_name = os.path.basename(img_path)
        point_id = str(uuid.uuid4())
        # 打印调试信息
        point = rest.PointStruct(
            id=point_id,
            vector=img_vector,
            payload={'file_name': file_name, 'img_path': img_path}
        )
        logger.info(f'Attempting to insert: {img_path}')
        try:
            response = self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            if response.status == rest.UpdateStatus.COMPLETED:
                logger.info(f'Successfully stored image: {img_path} in Qdrant, response: {response}')
                return True
            else:
                logger.error(f'Failed to store image: {img_path} in Qdrant, response: {response}')
                return False
        except Exception as e:
            logger.error(f'Failed to store image: {img_path} in Qdrant, error:{e}')
            return False
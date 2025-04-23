from common.log import init_logger
from server.src.ai_model import AiModel
from server.src.config import Config
from server.src.db import VectorDB
from server.src.icon_search_server import start_search_server
from server.src.img_to_db import ImgDirHandler

if __name__ == '__main__':
    config = Config.from_yaml('server/conf/conf.yaml')
    init_logger(config.log.dir, config.log.name)
    # 启动时全量扫描一次图片目录，解析图片为向量，保存到数据库
    model = AiModel()
    qdrant_conf = config.qdrant
    vector_db = VectorDB(qdrant_conf.hot, qdrant_conf.port, qdrant_conf.collection_name, model.open_ai_model.visual.output_dim)
    img_dir_handler = ImgDirHandler(vector_db, model)
    img_dir_handler.handle_dir(config.image.origin_dir)
    # 启动监听，有新图片时，解析图片为向量，保存到数据库 TODO

    # 启动web搜索服务
    start_search_server(model, vector_db)



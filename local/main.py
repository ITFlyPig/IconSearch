import json

from loguru import logger

from common.log import init_logger
from local.src.cache import VectorDrawableCache
from local.src.config import Config
from local.src.image import delete_all_images, collect_images, handle_images

if __name__ == '__main__':
    config = Config.from_yaml('./conf/conf.yaml')
    init_logger(config.log.dir, config.log.name)
    # 删除之前收集的所有图片和所有处理好的图片
    delete_all_images(config.image.origin_save_dir)
    delete_all_images(config.image.handled_dir)
    # 收集图片
    move_count = collect_images(config.image.origin_dir, config.image.origin_save_dir)
    logger.info(f'move {move_count} files to {config.image.origin_save_dir}')
    # 将图片中的vector drawable、 svg转为一般的图片格式，并保存到新的文件目录中
    handle_images(config.image.origin_save_dir, config.image.handled_dir)
    # 将处理好的图片同步到服务器





import os
import shutil
import time

from loguru import logger
import xml.etree.ElementTree as ET
import cairosvg

from local.src.cache import VectorDrawableCache
from local.src.vector_drawable_converter import KimiConverter

# 图片后缀集合
image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}

def is_image_file(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower() in image_extensions


def is_xml_file(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower() == '.xml'


def is_vector_drawable(file_path):
    try:
        # 解析XML文件
        tree = ET.parse(file_path)
        root = tree.getroot()
        # 检查根元素是否为<vector>
        if root.tag == 'vector':
            return True
        else:
            return False
    except ET.ParseError:
        # 如果文件不是有效的XML，返回False
        return False
    except Exception as e:
        # 处理其他异常
        logger.error(f"is_vector_drawable exception, file_path:{file_path} error: {e}")
        return False
def move_to(f_path: str, to_dir: str):
    f_name = f_path.split('/')[-1]
    shutil.copy(f_path, os.path.join(to_dir, f_name))

def copy_to(f_path: str, to_dir: str):
    f_name = f_path.split('/')[-1]
    shutil.copy(f_path, os.path.join(to_dir, f_name))


def delete_all_images(directory):
    """删除指定目录下的所有文件"""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)  # 删除文件或符号链接
        except Exception as e:
            logger.error(f"delete_all_images exception, file_path:{file_path} error: {e}")

def collect_images(from_dir: str, to_dir: str) -> int:
    """收集指定目录下的所有图片文件路径"""
    move_count = 0  # 初始化移动计数器

    for filename in os.listdir(from_dir):
        file_path = os.path.join(from_dir, filename)
        if os.path.isdir(file_path):
            dir_name = get_dir_name(file_path)
            if is_hidden_dir(dir_name) or is_build_dir(dir_name):
                continue
            move_count += collect_images(file_path, to_dir)
        else:
            from_dir_name = get_dir_name(from_dir)
            if from_dir_name.startswith("drawable"): # drawable目录下面的图片类文件
                if is_image_file(file_path) or is_vector_drawable(file_path):
                    move_to(file_path, to_dir)
                    move_count += 1
                    logger.info(f'move {file_path} to {to_dir}')
    return move_count

def get_dir_name(path: str):
    return path.split('/')[-1]

def is_hidden_dir(dir_name: str):
    return dir_name.startswith('.')

def is_drawable_dir(dir_name: str):
    return dir_name.startswith('drawable')

def is_build_dir(dir_name: str):
    return dir_name == "build"

converter = KimiConverter()
def vd_to_svg(vd_path: str, svg_path: str):
    global converter
    converter.convert(vd_path, svg_path)


cache = VectorDrawableCache("./img/cache")
def handle_images(from_dir: str, to_dir: str):
    for filename in os.listdir(from_dir):
        file_path = os.path.join(from_dir, filename)
        if os.path.isfile(file_path):
            if is_image_file(file_path): # 图片直接移动
                move_to(file_path, to_dir)
                logger.info(f'move {file_path} to {to_dir}')
            elif is_vector_drawable(file_path): # vector drawable处理后再移动
                # 尝试从cache获取
                global cache
                cache_png_path = cache.get_cache_png(file_path)
                if os.path.exists(cache_png_path):
                   copy_to(cache_png_path, to_dir)
                   logger.info(f'get cache png success, cache_png_path:{cache_png_path}, file_path:{file_path}, to_dir:{to_dir}')
                   continue

                # 转为svg
                svg_path = os.path.join(to_dir, filename.split('.')[0] + '.svg')
                vd_to_svg(file_path, svg_path)
                if not os.path.exists(svg_path):
                    continue
                svg_size = os.path.getsize(svg_path)
                if svg_size <= 0:
                    logger.error(f'vector drawable to svg error, vd_path:{file_path}')
                    continue
                logger.info(f'vector drawable to svg success, vd_path:{file_path}, svg_path:{svg_path}')
                # # api调用限制，1分钟最多200次
                # time.sleep(1)

                # 转为 png
                png_path = os.path.join(to_dir, filename.split('.')[0] + '.png')
                cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=100, output_height=100)
                png_size = os.path.getsize(png_path)
                if png_size <= 0:
                    logger.error(f'svg to png error, svg_path:{svg_path}')
                    continue
                logger.info(f'svg to png success, png_path:{png_path}, svg_path:{svg_path}')
                # 保存到cache
                cache.save(svg_path, png_path)


import os.path
from dataclasses import dataclass


class VectorDrawableCache:
    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def build_cache(self, from_dir: str):
        """
        从给定目录构建cache
        :param from_dir: 构建cache的来源目录
        :return:
        """
        # 收集所有的png和svg
        all_files = {}
        for file_name in os.listdir(from_dir):
            file_path = os.path.join(from_dir, file_name)
            if os.path.isdir(file_path):
                continue

            # 收集png和svg
            pure_file_name = file_name.split(".")[0]
            if file_name.endswith(".png"):
                image_pair = all_files.get(pure_file_name)
                if image_pair is None:
                    image_pair = ImagePair(file_path, "")
                    all_files[pure_file_name] = image_pair
                else:
                    image_pair.svg_path = file_path
            if file_name.endswith(".svg"):
                image_pair = all_files.get(pure_file_name)
                if image_pair is None:
                    image_pair = ImagePair("", file_path)
                    all_files[pure_file_name] = image_pair
                else:
                    image_pair.svg_path = file_path

        # 将png有对应的svg的文件复制到cache中
        for _, image_pair in all_files.items():
            if image_pair.png_path != "" and image_pair.svg_path != "":
                self.save(image_pair.svg_path, image_pair.png_path)
    def get_cache_png(self, vector_drawable_path: str) -> str:
        """
        获取已经处理过的vector drawable对应的png
        :param vector_drawable_path: vector drawable 路径
        :return:
        """
        if vector_drawable_path == "":
            return ""
        vd_name = os.path.basename(vector_drawable_path)
        pure_vd_name = vd_name.split(".")[0]
        cache_png_path = os.path.join(self.cache_dir, pure_vd_name + ".png")
        if os.path.exists(cache_png_path):
            return cache_png_path
        else:
            return ""
    def save(self, svg_path: str, png_path: str):
        png_name = os.path.basename(png_path)
        svg_name = os.path.basename(svg_path)
        cache_png_path = os.path.join(self.cache_dir, png_name)
        cache_svg_path = os.path.join(self.cache_dir, svg_name)
        os.system(f"cp {svg_path} {cache_svg_path}")
        os.system(f"cp {png_path} {cache_png_path}")

@dataclass
class ImagePair:
    png_path: str
    svg_path: str
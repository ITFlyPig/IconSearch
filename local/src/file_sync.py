import os

from fabric import Connection
from loguru import logger

# 配置远程服务器信息
g_host = ''
g_user = ''
g_password = ''

class FileSync:
    def __init__(self, host, user, password):
        self.conn = Connection(host=host, user=user, connect_kwargs={'password': password})
        self.conn: Connection
        self.host = host
        self.user = user
        self.password = password


    def put(self, local_dir, remote_dir):
        """
        上传文件
        :param local_dir: 本地文件目录
        :param remote_dir: 远程文件目录
        :return:
        """
        self.conn.put(local_dir, remote_dir)

    def close(self):
        self.conn.close()

    def rm_remote_dir(self, remote_dir):
        """
        删除远程目录
        :param remote_dir: 远程目录
        :return:
        """
        self.conn.run(f'rm -rf {remote_dir}')

    def mk_remote_dir(self, remote_dir):
        """
        创建远程目录
        :param remote_dir: 远程目录
        :return:
        """
        self.conn.run(f'mkdir -p {remote_dir}')


def sync_all_img(local_dir, remote_dir):
    """
    同步本地图片到远程
    :param local_dir:
    :param remote_dir:
    :return:
    """
    logger.info(f"start sync img: local_dir:{local_dir}, remote_dir:{remote_dir}")
    fs = FileSync(g_host, g_user, g_password)
    fs.rm_remote_dir(remote_dir)
    fs.mk_remote_dir(remote_dir)
    count = 0
    files = os.listdir(local_dir)
    for img in files:
        img_path = os.path.join(local_dir, img)
        fs.put(img_path, remote_dir)
        count = count + 1
        logger.info(f"sync img: {img_path} cur:{count} total:{len(files)}")
    fs.close()
    logger.info(f"end sync img: local_dir:{local_dir}, remote_dir:{remote_dir} success count: {count}, total: {len(files)}")
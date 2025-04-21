from typing import Callable

from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

class ImgEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:  # 只监听文件，不监听目录
            print(f"新文件创建: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"文件修改: {event.src_path}")

def watch_dir(dir_path: str, on_change: Callable[[FileSystemEvent], None], on_created: Callable[[FileSystemEvent], None]):
    """
    监听图片目录下文件的创建和修改
    :param dir_path:  监听的目录
    :param on_change: 文件修改
    :param on_created: 文件创建
    :return:
    """
    observer = Observer()
    handler = FileSystemEventHandler()
    handler.on_created = on_created
    handler.on_modified = on_change
    observer.schedule(handler, dir_path, recursive=True)
    observer.start()
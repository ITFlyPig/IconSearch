import yaml
from dataclasses import dataclass

@dataclass
class LogConfig:
    name: str
    dir: str

@dataclass
class ImageConfig:
    origin_dir: str
    origin_save_dir: str
    handled_dir: str

@dataclass
class Config:
    log: LogConfig
    image: ImageConfig

    @classmethod
    def from_yaml(cls, file_path: str) -> 'Config':
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return cls(
                log=LogConfig(**data['log']),
                image=ImageConfig(**data['image']),
            )




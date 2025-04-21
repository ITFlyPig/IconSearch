import yaml
from dataclasses import dataclass

@dataclass
class LogConfig:
    name: str
    dir: str

@dataclass
class ImageConfig:
    origin_dir: str

@dataclass
class QdrantConfig:
    hot: str
    port: int
    collection_name: str

@dataclass
class Config:
    log: LogConfig
    image: ImageConfig
    qdrant: QdrantConfig

    @classmethod
    def from_yaml(cls, file_path: str) -> 'Config':
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return cls(
                log=LogConfig(**data['log']),
                image=ImageConfig(**data['image']),
                qdrant=QdrantConfig(**data['qdrant']),
            )




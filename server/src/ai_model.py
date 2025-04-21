import os

from PIL import Image
import torch
import open_clip

class AiModel:
    def __init__(self):
        self.open_ai_model = open_clip.create_model('ViT-B-32', pretrained='openai', quick_gelu=True)
        self.preprocess = open_clip.image_transform(self.open_ai_model.visual.image_size, is_train=False)

    def get_model(self):
        return self.open_ai_model

    def get_preprocess(self):
        return self.preprocess

    def to_vector(self, img_path: str):
        """
        将图片转为向量
        :param img_path:
        :return:
        """
        if img_path is None or img_path == '' or os.path.exists(img_path) == False:
            return None
        image = Image.open(img_path).convert('RGB')
        image = self.preprocess(image).unsqueeze(0)  # Add batch dimension
        # 获取图片向量
        with torch.no_grad():
            image_features = self.open_ai_model.encode_image(image).numpy().flatten().tolist()
            return image_features

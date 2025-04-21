import json
import os.path
from abc import ABC, abstractmethod

from loguru import logger
from openai import OpenAI

from local.src.cache import VectorDrawableCache


# 抽象类，将VectorDrawable转换为SVG
class VectorDrawableConverter(ABC):
    @abstractmethod
    def convert(self, vd_path: str, svg_path: str):
        """
        将VectorDrawable转换为SVG
        :param vd_path: VectorDrawable路径
        :param svg_path: 输出的svg路径
        :return:
        """
        pass


# 使用kimi模型来转换
class KimiConverter(VectorDrawableConverter):
    def __init__(self):
        self.kimi_client = OpenAI(
            api_key="sk-OoajQ4zCOS7e3IgJObzs6QrNf7anB1XJmiA607385USEzHif",
            base_url="https://api.moonshot.cn/v1",
        )
        self.system_prompt = """
    你是月之暗面（Kimi）只能转换器，你负责将用户输入的Vector Drawable转为svg。请参考文档内容回复用户的问题，你的回答可以是说明、转换后的svg内容。

    请使用如下 JSON 格式输出你的回复：

    {
        "desc": "说明",
        "svg": "svg的内容",
    }

    注意，请将说明信息放置在 `desc` 字段中，将Vector Drawable转为svg后的内容放在 `svg` 字段中。
    """

    def convert(self, vd_path: str, svg_path: str):
        vd_content = open(vd_path, "r").read()
        completion = self.kimi_client.chat.completions.create(
            model="moonshot-v1-8k",
            # model="moonshot-v1-32k",
            # model="moonshot-v1-128k",
            messages=[
                {"role": "system",
                 "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
                {"role": "system", "content": self.system_prompt},  # <-- 将附带输出格式的 system prompt 提交给 Kimi
                {"role": "user", "content": f"请转换以下的vector drawable为 svg\n{vd_content}"}
            ],
            temperature=0.3,
            response_format={"type": "json_object"},  # <-- 使用 response_format 参数指定输出格式为 json_object
        )
        try:
            content = json.loads(completion.choices[0].message.content)
        except Exception as e:
            logger.error(f"kimi convert exception, vd_path:{vd_path} error: {e} resp: {completion.choices[0].message.content}")
            return
        if "svg" in content:
            open(svg_path, "w").write(content["svg"])

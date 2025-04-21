import os
import uuid

from flask import Flask, request, render_template, send_from_directory
from loguru import logger
from PIL import Image
import torch

from server.src.ai_model import AiModel
from server.src.db import VectorDB

app = Flask(__name__, template_folder='../templates')

_model: AiModel = None
_vector_db: VectorDB = None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/origin_img/<filename>')
def origin_img(filename):
    return send_from_directory('../../local/img/handled', filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        image_path = save_file(file)
        # 加载图片并进行预处理
        image = Image.open(image_path).convert('RGB')
        image = _model.preprocess(image).unsqueeze(0)  # Add batch dimension

        # 获取图片向量
        with torch.no_grad():
            image_features = _model.open_ai_model.encode_image(image).numpy().flatten().tolist()

        # 在Qdrant中搜索相似图片
        search_result = _vector_db.qdrant_client.search(
            collection_name=_vector_db.collection_name,
            query_vector=image_features,
            limit=5  # 设置返回的结果数量
        )

        # 获取相似图片的文件名
        similar_images = [hit.payload['file_name'] for hit in search_result]
        logger.info(f'similar images: {similar_images}')
        return render_template('result.html', images=similar_images)
    return "File not allowed", 400


def allowed_file(filename):
    return '.' in filename and filename.lower().rsplit('.', 1)[1] in {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp'}

UPLOAD_FOLDER = './uploads' # 设置上传图片的文件夹
def save_file(file):
    filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file.save(file_path)
    return file_path

def start_search_server(model: AiModel, vector_db: VectorDB):
    logger.info('start search server')
    logger.info(f'template folder: {app.template_folder}, root_path: {app.root_path}')
    global _model
    _model = model
    global _vector_db
    _vector_db = vector_db
    app.run(host='0.0.0.0', port=8099, debug=True)

from flask import Flask, request, abort, Response, jsonify 
from views.save_image import ImageSaver
from views.model import Model
from os.path import join, dirname
from os import getenv
from dotenv import load_dotenv
from utils import has_dependencies, create_directory

dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = getenv('UPLOAD_DIRECTORY', 'app/persistent/')
create_directory(app.config['UPLOAD_FOLDER'])

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        if not has_dependencies(request, True):
            return Response("Wrong query", status=400)
        image_handler = ImageSaver()
        image = request.files['image']
        token = request.values['token']
        label = request.values['label']
        return image_handler.save_image(image, token, label)

@app.route('/api/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        if not has_dependencies(request, False):
            return Response("Wrong query", status=400)
        model = Model()
        image_handler = ImageSaver()
        image = request.files['image']
        token = request.values['token']
        response = image_handler.save_image(image, token)
        if response.status_code != 201:
            return Response("Couldn't save image", status=400)
        hashed_path = image_handler.hashed_path(image, token)
        image = model.process_image(hashed_path)
        top_prob, top_class = model.predict_classes(image)
        response_object = {
            'prob': top_prob,
            'class': top_class
        }
        image_handler.delete_image(hashed_path)
        return jsonify(response_object), 201

if __name__ == '__main__':
    app.run(
        debug = getenv('DEV_MODE', True),
        port = getenv('PORT', 5000)
        )
from flask import Flask, request, abort
from views.save_image import ImageSaver
from os.path import join, dirname
from os import getenv
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = getenv('UPLOAD_DIRECTORY', None)

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files or 'token' not in request.values:
            abort(400)
        elif request.values['token'] == "":
            abort(400)  
        image_handler = ImageSaver()
        image = request.files['image']
        token = request.values['token']
        return image_handler.save_image(image, token)


if __name__ == '__main__':
    app.run(
        debug = getenv('DEV_MODE', True),
        port = getenv('PORT', 5000)
        )
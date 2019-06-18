from flask import Flask, request, abort
from werkzeug.utils import secure_filename
from views.save_image import ImageSaver
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_DIRECTORY', None)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'image' not in request.files:
            abort(400)
        image_handler = ImageSaver()
        image = request.files['image']
        return image_handler.save_image(image)


if __name__ == '__main__':
    app.run(
        debug = os.getenv('DEV_MODE', True),
        port = os.getenv('PORT', 5000)
        )
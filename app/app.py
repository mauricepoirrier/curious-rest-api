from flask import Flask, request, abort
from werkzeug.utils import secure_filename
from views.save_image import ImageSaver


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'persistent/'

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'image' not in request.files:
            abort(400)
        image_handler = ImageSaver()
        image = request.files['image']
        return image_handler.save_image(image)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
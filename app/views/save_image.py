from os import path
from werkzeug.utils import secure_filename
from flask import current_app as app
from flask import Response
from flask_hashing import Hashing



class ImageSaver():
    def __init__(self):
        self.hashing = Hashing()
        self.extensions = set(['png', 'jpg', 'jpeg'])
    
    def save_image(self, image):
        if not self.check_extensions(image.filename):
            abort(400)
        filename = secure_filename(image.filename)
        hashed_name= self.hashing.hash_value(filename.split('.')[0], salt='secret') \
            +'.'+ filename.split('.')[1]
        image.save(path.join(app.config['UPLOAD_FOLDER'], hashed_name))
        return Response("Created", status=201)
    
    def check_extensions(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.extensions
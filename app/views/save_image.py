from os import path, remove
from werkzeug.utils import secure_filename
from flask import current_app as app
from flask import Response
from flask_hashing import Hashing


class ImageSaver():
    def __init__(self):
        self.hashing = Hashing()
        self.extensions = set(['png', 'jpg', 'jpeg'])
    
    def save_image(self, image, token):
        '''
        Recieves an image from form and a user token
        Returns a http response
        '''
        if not self.check_extensions(image.filename):
            abort(400)
        hashed_path = self.hashed_path(image, token)
        image.save(hashed_path)
        return Response("Created", status=201)
    
    def hashed_path(self, image, token):
        '''
        Recieves an image object and a token
        Returns hashed path of object
        '''
        filename = secure_filename(image.filename)
        hashed_name= self.hashing.hash_value(filename.split('.')[0], salt=token) \
            +'.'+ filename.split('.')[1]
        return path.join(app.config['UPLOAD_FOLDER'], hashed_name)

    def check_extensions(self, filename):
        '''
        Recieves a filename
        Returns if file has extension permited
        '''
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.extensions
    
    def delete_image(self, image_path):
        '''
        Recieves a path of a file already hashed
        Returns True if file had deleted
        '''
        if path.exists(image_path):
            remove(image_path)
            return True
        return False

        
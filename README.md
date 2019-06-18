# REST API for Curious AI

Project involves to create a RESTFUL API with use case:
- Upload pictures and store them
- Upload pictures and predict from a model

This project uses PyTorch densenet161 as example. Does the image proccesing for that specific pre-trained model.
Model could be change on enviroment and the width and height of image too.

## Endpoints
As it had been said, this project has 2 endpoints.
Uploading an image
```
URL: localhost:5000/api/upload
Content-type: form-data
Body:
    > image: image with extension .jpeg, .jpg or .png
    > token: secret of a user for saving method
```
Prediction on image
```
URL: localhost:5000/api/predict
Content-type: form-data
Body:
    > image: image with extension .jpeg, .jpg or .png
    > token: secret of a user for saving method

```
## Installation
```bash
pip install -r requirements.txt
``` 

## Enviroment
Project does use an .env with the following variables
```
UPLOAD_DIRECTORY='path/to/directory/' default='app/persistent/'
DEV_MODE=True default
PORT=5000 default
MODEL_PATH='path/to/model' default='app/models'
WIDTH=224
HEIGHT=224
```
## Running
Running on root folder of the project
```bash
python app/app.py
```

## Tests
Running on root folder of the project
```bash
pytest
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

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
Project uses PyTorch and other packages, to install run the followings commands
```bash
pip install -r requirements.txt
pip install https://download.pytorch.org/whl/cu100/torch-1.1.0-cp37-cp37m-linux_x86_64.whl
pip install https://download.pytorch.org/whl/cu100/torchvision-0.3.0-cp37-cp37m-linux_x86_64.whl
``` 
Note that could be other versions as pip is currently not working for PyTorch.

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
Running on root folder of the project and set the FLASK APP as following
Windows
```
set FLASK_APP=app/app.py
```
Unix
```bash
export FLASK_APP=app/app.py
```
then run
```
flask run
```

## Tests
Running on root folder of the project
```bash
pytest
```

## Docker
Project has a dockefile running a not standart PyTorch image.
To build the image
```bash
docker build -t curious_api .
```
To run the container
```bash
docker run -p 5000:5000 curious_api
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

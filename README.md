# REST API for Curious AI

Project involves to create a RESTFUL API with use case:
- Upload pictures and store them
- Upload pictures and predict from a model

## Installation
```bash
pip install requirements
``` 

## Enviroment
Project does use an .env with the following variables
```
UPLOAD_DIRECTORY='path/to/directory/' default='app/persistent/'
DEV_MODE=True default
PORT=5000 default
MODEL_PATH='path/to/model' default='app/models'
```
## Running
```bash
python app
```

## Tests
```bash
python test
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

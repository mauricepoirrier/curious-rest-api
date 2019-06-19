FROM anibali/pytorch:cuda-10.0

#RUN pip install https://download.pytorch.org/whl/cu100/torch-1.1.0-cp37-cp37m-linux_x86_64.whl

#RUN pip install https://download.pytorch.org/whl/cu100/torchvision-0.3.0-cp37-cp37m-linux_x86_64.whl

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY . /src

WORKDIR /src

ENV UPLOAD_DIRECTORY='app/persistent/'
ENV DEV_MODE=True
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP='app/app.py'
RUN sudo chmod -R 777 .

CMD ["flask", "run", "--host=0.0.0.0"]

# docker build -t curious_api .
# docker run -p 5000:5000 curious_api
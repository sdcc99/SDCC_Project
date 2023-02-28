FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y g++
RUN apt-get update && apt-get install -y cmake
RUN apt-get update && apt-get install -y libpng-dev
RUN apt-get update && apt-get install -y libopenblas-dev
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip
RUN pip install dlib

WORKDIR /face_rec

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]

FROM python:3.7.9

RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx \
    && apt-get install ffmpeg libsm6 libxext6  -y \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt
COPY . /src
CMD ["python","app.py"]
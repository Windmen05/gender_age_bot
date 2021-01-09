FROM python:3.7.9

RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN apt-get update ##[edited]
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /src
CMD ["python","app.py"]
FROM python:3.7.9

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
CMD ["python","app.py"]
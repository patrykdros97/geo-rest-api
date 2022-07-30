FROM python:3

WORKDIR /usr/src/app

RUN apt-get update\
    && apt-get upgrade -y\
    && apt-get install -y sqlite3 libsqlite3-dev gcc g++

COPY requirements.txt ./requirements.txt
COPY app.py ./app.py
COPY ./geo_app ./geo_app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "app.py"]
FROM python:3.7.7-slim-buster
MAINTAINER Robert Murray

COPY requirements.txt /


RUN apt update
RUN apt-get install -y wget gcc g++ make cmake tk
RUN pip install -r /requirements.txt

RUN mkdir src
COPY src/ src/
WORKDIR src

ENTRYPOINT ["python", "main.py"]
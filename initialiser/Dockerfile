FROM python:3.10-slim-buster

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY initialise_masterdata.py .


CMD sleep infinity
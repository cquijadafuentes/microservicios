# Use an official Python runtime as a parent image
FROM python:2.7-slim
WORKDIR /app
ADD . /app
RUN apt-get update -y && apt-get install libssl-dev -y
RUN apt-get install default-libmysqlclient-dev build-essential -y
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flask-sqlalchemy
RUN export FLASK_APP=/app/app/run.py
RUN export FLASK_CONFIG=development
EXPOSE 5000
CMD ["flask", "run"]
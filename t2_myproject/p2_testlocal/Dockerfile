# Use an official Python runtime as a parent image
FROM python:2.7-slim
WORKDIR /app
ADD . /app
RUN pip install --trusted-host pypi.python.org Flask
RUN export FLASK_APP=run.py
CMD ["for i in $(seq 1 10); do echo "$i - Hello work!"; done"]
CMD ["flask", "run"]

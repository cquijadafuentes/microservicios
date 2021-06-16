# Use an official Python runtime as a parent image
FROM python:2.7-slim
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --trusted-host pypi.python.org Flask
EXPOSE 5000
CMD ["for i in $(seq 1 10); do echo "$i - Hello work!"; done"]
CMD ["./rf.sh"]

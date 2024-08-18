# Pulling the official Python 3.12.5 image from the Docker Hub
FROM python:3.12.5-slim

# set PYTHONPATH environment variable
ENV PYTHONPATH=/app/:$PYTHONPATH

# default working directory in the container
WORKDIR /app

# copy requirements file into the container
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy everything to container workdir
COPY . .

# execute the script
CMD python /app/src/main.py
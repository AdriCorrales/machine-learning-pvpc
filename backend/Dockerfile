# pull official base image
FROM python:3.10.0

COPY . /app
# FROM python:3.7.7-slim-stretch # for Raspberry

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app

EXPOSE 5001

RUN chmod +x ./start.sh
CMD ["./start.sh"]
# start by pulling the python image
#FROM python:3.8-alpine
#COPY ./requirements.txt /app/requirements.txt
#WORKDIR /app
#RUN /usr/local/bin/python -m pip install --upgrade pip

#COPY . /app
#ENTRYPOINT [ "python" ]
FROM python:3.10-slim
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install Flask gunicorn
RUN pip install -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 __init__:start
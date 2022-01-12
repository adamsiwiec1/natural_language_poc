FROM python:3.10-slim
ENV PYTHONUNBUFFERED True
ENV APP_HOME /
WORKDIR $APP_HOME
COPY . ./
RUN pip install pipenv
RUN pip install Flask gunicorn
RUN pip install -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 natural_language_poc.__init__:start
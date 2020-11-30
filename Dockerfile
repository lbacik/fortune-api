FROM python:3.9

ENV FORTUNES=/usr/share/games/fortunes

RUN apt-get -y update && apt-get -y install \
    fortune\
    fortunes

COPY . /opt/project
WORKDIR /opt/project

RUN pip install -r requirements.txt

EXPOSE 8080

CMD uwsgi --ini config.ini

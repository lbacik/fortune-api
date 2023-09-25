FROM debian:11 as base

# hadolint ignore=DL3008,DL3015
RUN apt-get -y update && apt-get -y install \
    fortunes \
    fortunes-off \
    fortune-anarchism \
    fortunes-bg \
    fortunes-bofh-excuses \
    fortunes-br \
    fortunes-cs \
    fortunes-de \
    fortunes-debian-hints \
    fortunes-es \
    fortunes-es-off \
    fortunes-fr \
    fortunes-ga \
    fortunes-it \
    fortunes-it-off \
    fortunes-mario \
    fortunes-pl \
    fortunes-ru \
    fortunes-zh

FROM python:3.9

ENV FORTUNES=/usr/share/games/fortunes
ENV CORS=yes

COPY --from=base /usr/share/games/fortunes /usr/share/games/fortunes

COPY . /opt/project
WORKDIR /opt/project

# hadolint ignore=DL3042
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uwsgi", "--ini", "config.ini"]


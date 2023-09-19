FROM debian:12 as base

# hadolint ignore=DL3008,DL3015
RUN apt-get -y update && apt-get -y install \
    fortune-anarchism \
    fortune-mod \
    fortunes-bg \
    fortunes-bofh-excuses \
    fortunes-br \
    fortunes-cs \
    fortunes-de \
    fortunes-debian-hints \
    fortunes-eo \
    fortunes-es-off \
    fortunes-es \
    fortunes-ga \
    fortunes-it-off \
    fortunes-it \
    fortunes-mario \
    fortunes-min \
    fortunes-pl \
    fortunes-ru \
    fortunes-zh \
    fortunes

FROM python:3.11

ENV FORTUNES=/usr/share/games/fortunes

COPY --from=base /usr/share/games/fortunes /usr/share/games/fortunes
COPY . /opt/project
WORKDIR /opt/project

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ~/.local/bin/poetry config virtualenvs.create false  \
    && ~/.local/bin/poetry install --no-dev --no-root --no-interaction --no-ansi

EXPOSE 8080

ENV PYTHONPATH='./src'

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "lfortune_api.restapi.app:api"]


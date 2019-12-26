FROM python:3.6-alpine

ENV FLASK_APP views.py

USER root
RUN apk add build-base

RUN adduser -D eric
USER eric

WORKDIR /home/eric

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

COPY app.py models.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

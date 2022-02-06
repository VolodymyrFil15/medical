FROM python:3.10.2

ENV APP_DIR=/app
COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -U pip setuptools wheel \
 && pip install --no-cache-dir -U -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt


COPY . $APP_DIR/

WORKDIR $APP_DIR

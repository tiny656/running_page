FROM nikolaik/python-nodejs:python3.10-nodejs14-slim

WORKDIR /root/running_page
COPY . /root/running_page/

RUN apt-get update \
        && apt-get install -y --no-install-recommends git \
        && apt-get purge -y --auto-remove \
        && rm -rf /var/lib/apt/lists/* \
        && pip3 install -r requirements.txt  \
        && yarn install \
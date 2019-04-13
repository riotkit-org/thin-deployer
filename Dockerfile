FROM docker:latest

RUN set -x\
    && apk add --update python3 bash make curl wget grep sudo git \
    && apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev gcc python3-dev \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && pip3 install --upgrade pip \
    && pip3 install 'docker-compose' \
    && docker --version \
    && docker-compose --version \
    && addgroup -g 1800 -S deployer \
    && adduser -u 1800 -D -S -G deployer deployer \
    && apk del --virtual .build-deps gcc musl-dev libffi-dev openssl-dev gcc python3-dev \
    && rm -rf /var/cache/apk/*

#
# Build the application, run tests to verify
#
ADD ./ /app
RUN set -x \
    && cd /app \
    && cp ./tests/.deployer.yml /root/.deployer.yml \
    && make install_dependencies install_as_python_package test PIP_BIN=pip3 \
    && mkdir /deployer-root

EXPOSE 8012
WORKDIR "/deployer-root"

ENTRYPOINT thin-deployer

FROM docker:latest

RUN set -x\
    && apk add --update python3 bash make curl wget grep sudo \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && pip3 install 'docker-compose' \
    && docker --version \
    && docker-compose --version

#
# Build the application, run tests to verify
#
ADD ./ /app
RUN set -x \
    && cd /app \
    && cp ./tests/.deployer.yml /root/.deployer.yml \
    && make install_dependencies test \
    && mkdir /deployer-root

EXPOSE 8012
WORKDIR "/deployer-root"

ENTRYPOINT /bin/bash -c 'cd /app && ./bin/deployer.py'

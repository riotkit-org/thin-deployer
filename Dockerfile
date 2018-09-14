FROM docker:latest

RUN apk add --update python3 bash make curl wget grep \
    && ln -s /usr/bin/python3 /usr/bin/python

#
# Build the application, run tests to verify
#
ADD ./ /app
RUN cd /app \
    && cp ./tests/.deployer.yml /root/.deployer.yml \
    && make install_dependencies test

EXPOSE 8012

ENTRYPOINT /bin/bash -c 'cd /app && ./bin/deployer.py'


.SILENT:
IS_ENV_PRESENT=$(shell test -e .env && echo -n yes)

ifeq ($(IS_ENV_PRESENT), yes)
	include .env
	export $(shell sed 's/=.*//' .env)
endif

# Colors
COLOR_RESET   = \033[0m
COLOR_INFO    = \033[32m
COLOR_COMMENT = \033[33m

## This help screen
help:
	printf "${COLOR_COMMENT}Usage:${COLOR_RESET}\n"
	printf " make [target]\n\n"
	printf "${COLOR_COMMENT}Available targets:${COLOR_RESET}\n"
	awk '/^[a-zA-Z\-\_0-9\.@]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf " ${COLOR_INFO}%-16s${COLOR_RESET}\t\t%s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

## Run with test configuration
run:
	./bin/deployer.py --configuration=./tests/.deployer.yml

## Install requirements
install_dependencies:
	pip3 install -r ./requirements.txt

## Run unit tests
test:
	python3 -m unittest discover -s ./tests

## Build PyPI package
build:
	python3 ./setup.py build

## Build PyPI package
install_as_python_package:
	python3 ./setup.py install

## Build and run a Docker container
container: build_container run_container

## Build Docker container
build_container:
	sudo docker build . -t wolnosciowiec/thin-deployer

## Push Docker container to the registry
push_container:
	sudo docker push wolnosciowiec/thin-deployer

## Run Docker container
run_container:
	sudo docker run -p 8012:8012 --rm --name thin-deployer wolnosciowiec/thin-deployer

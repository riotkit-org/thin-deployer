
run:
	./bin/deployer.py

install_dependencies:
	pip3 install -r ./requirements.txt

test:
	python3 -m unittest discover -s ./tests

container: build_container run_container

build_container:
	sudo docker build . -t wolnosciowiec/thin-deployer

push_container:
	sudo docker push wolnosciowiec/thin-deployer

run_container:
	sudo docker run --rm --name thin-deployer wolnosciowiec/thin-deployer


run:
	./bin/deployer.py

install_dependencies:
	pip3 install -r ./requirements.txt

test:
	python3 -m unittest discover -s ./tests

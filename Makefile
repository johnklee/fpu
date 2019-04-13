.PHONY: init test lint dist

all: init test lint

init:
	pip3 install -r requirements.txt

test:
	pytest tests

dist:
	python3 setup.py sdist

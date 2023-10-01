.PHONY: init test lint dist

all: init test lint

init:
	pip install -r requirements.txt

test:
	- coverage run -m pytest tests
	coverage report

dist: init test
	rm -f dist/*
	python3 setup.py sdist bdist_wheel

lint:
	flake8 fpu

upload: dist
	twine upload --skip-existing dist/*

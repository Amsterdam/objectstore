.PHONY: release dist build test coverage clean distclean

PYTHON = python3

release: test dist
	twine upload dist/*

dist:
	$(PYTHON) setup.py sdist bdist_wheel

build:
	$(PYTHON) setup.py build

test:
	$(PYTHON) setup.py test

clean:
	rm -rf dist/*

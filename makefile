
.DEFAULT_GOAL := init

MAIN=geminidata-service.py

SYS_PYTHON=$(shell which python3)
VENV_PATH=./
VENV_NAME=venv
VENV=$(VENV_PATH)$(VENV_NAME)
PIP=$(VENV)/bin/pip
PSERVE=$(VENV)/bin/pserve
PYTHON=$(VENV)/bin/python

init:
	test -e $(PYTHON) || \
    { echo "Creating virtual env: $(VENV)"; $(SYS_PYTHON) -m venv $(VENV_NAME) && \
      test -r requirements.txt && $(PIP) install -r requirements.txt && touch $(VENV)/.installed ; } || \
    { test -f $(VENV)/.installed || \
      test -r requirements.txt && $(PIP) install -r requirements.txt && touch $(VENV)/.installed ; }

test:
	$(PYTHON) -m unittest

#install:
#	pip3 install -r requirements.txt || { echo "Wrong user or no pip3 most likly!" ; exit 1; }

run: init
	$(PYTHON) $(MAIN)

init-dev:
	test -e $(PYTHON) || \
    { echo "Creating virtual env: $(VENV)"; $(SYS_PYTHON) -m venv $(VENV_NAME) ; } && \
    $(PIP) install --upgrade pip setuptools pipreqs

update-deps:
	$(VENV)/bin/pipreqs --force ./

clean:
	find . -type d -name __pycache__ -not -path $(VENV) -exec rm -r {} \; 2>/dev/null && \
    echo "So fresh so clean..."

clean-venv:
	test -d ./venv &&  \
    rm -r ./venv || echo "./venv already clean!"

clean-all: clean clean-venv


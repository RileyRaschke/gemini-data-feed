
.DEFAULT_GOAL := init

MAIN=gemini-data-feed.py

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

run: init
	$(PYTHON) $(MAIN)

init-dev:
	test -e $(PYTHON) || \
    { echo "Creating virtual env: $(VENV)"; $(SYS_PYTHON) -m venv $(VENV_NAME) ; } && \
    $(PIP) install --upgrade pip setuptools pipreqs && \
    $(PIP) install "pyramid==1.10.4" waitress

install-dev:
	$(PIP) install -e ".[dev]"

update_deps:
	$(VENV)/bin/pipreqs --force ./

clean:
	find . -type d -name __pycache__ -not -path $(VENV) -exec rm -r {} \; 2>/dev/null && \
    echo "So fresh so clean..."

clean-venv:
	test -d ./venv &&  \
    rm -r ./venv || echo "./venv already clean!"

clean-all: clean clean-venv


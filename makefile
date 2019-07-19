
.DEFAULT_GOAL := init

MAIN=gemini-data-feed.py
CMDCLIENT=$(MAIN)

SYS_PYTHON=$(shell which python3)
VENV_PATH=./
VENV_NAME=venv
VENV=$(VENV_PATH)$(VENV_NAME)
PIP=$(VENV)/bin/pip
PSERVE=$(VENV)/bin/pserve
PYTHON=$(VENV)/bin/python

init:
	test -f $(VENV)/.installed || \
	test -e $(PYTHON) || \
		{ echo "Creating virtual env: $(VENV)"; $(SYS_PYTHON) -m venv $(VENV_NAME) && \
	      test -r requirements.txt && $(PIP) install -r requirements.txt && touch $(VENV)/.installed || \
		    echo "No requirements.txt to install"; exit 0 ; }

test:
	$(PYTHON) -m unittest

run: init
	$(PYTHON) $(MAIN)

init-dev:
	test -e $(PYTHON) || \
		{ echo "Creating virtual env: $(VENV)"; $(SYS_PYTHON) -m venv $(VENV_NAME) ; } && \
		$(PIP) install --upgrade pip setuptools pipreqs #&& \
		#$(PIP) install "pyramid==1.10.4" waitress

#install-dev:
#	$(PIP) install -e ".[dev]"

update_deps:
	$(VENV)/bin/pipreqs ./

clean:
	find . -type d -name __pycache__ -exec rm -r {} \; && \
	test -d ./venv &&  \
	  rm -r ./venv


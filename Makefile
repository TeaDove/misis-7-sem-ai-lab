PYTHON ?= .venv/bin/python
PYTHON_JUP ?= .venv_jup/bin/python
PYTHON_PRE ?= ../.venv/bin/python

install:
	python3.10 -m venv .venv
	$(PYTHON) -m pip install poetry
	poetry update

	python3.10 -m venv .venv_jup
	$(PYTHON_JUP) -m pip install -r src/jup-requirements.txt

jup:
	$(PYTHON_JUP) -m jupyterlab

jup-darwin:
	$(PYTHON_JUP) -m jupyterlab --app-dir=/opt/homebrew/share/jupyter/lab

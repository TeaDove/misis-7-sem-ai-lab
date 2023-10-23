PYTHON ?= .venv/bin/python

download: 
	cd data && ./get_data.sh 

download-quick:
	cd data && ./get_data_quick.sh 

install:
	python3.10 -m venv .venv
	. .venv/bin/activate
	$(PYTHON) -m pip install -r ./src/requirements.txt

jup:
	. .venv/bin/activate
	$(PYTHON) -m jupyterlab

jup-darwin:
	. .venv/bin/activate
	$(PYTHON) -m jupyterlab --app-dir=/opt/homebrew/share/jupyter/lab

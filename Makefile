.PHONY: setup run clean

setup:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt

run:
	source venv/bin/activate && python weather_fetcher.py

clean:
	rm -rf venv __pycache__ *.pyc

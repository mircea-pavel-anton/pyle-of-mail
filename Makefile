run:
	@python3 src/main.py

clean:
	@rm -rf env/ *.log

venv:
	@python3 -m venv env/
	@echo "Virtual environment created. Activate it by running: source env/bin/activate"

install:
	pip install -r requirements.txt
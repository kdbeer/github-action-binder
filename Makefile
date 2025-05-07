# Create VENV
create_python_env:
	python3 -m venv venv

install: venv/bin/python
	venv/bin/pip install -r requirements.txt

update_env: install
	venv/bin/python main.py
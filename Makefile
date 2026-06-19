
run: install
	@echo "Running the application..."
	python3 main.py

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

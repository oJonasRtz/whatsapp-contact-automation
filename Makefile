
run: install
	@echo "Running the application..."
	python3 main.py

install:
	@echo "Installing dependencies..."
	@pip install -q -r requirements.txt

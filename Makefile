.PHONY: setup run test lint format docker-up docker-down generate-data train

setup:
	pip install -r requirements.txt
	python scripts/seed_database.py

run:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v

lint:
	flake8 .
	black --check .

format:
	black .

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

generate-data:
	python scripts/generate_synthetic_data.py

train:
	python scripts/train_models.py

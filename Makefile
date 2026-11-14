.PHONY: start install seed test run-backend run-frontend build-frontend docker-up docker-down clean

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest
UVICORN = $(VENV)/bin/uvicorn

start:
	@./start.sh

install:
	@echo "Creating virtual environment and installing dependencies..."
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r backend/requirements.txt
	cd frontend && npm install

seed:
	@echo "Seeding SkillPath database..."
	PYTHONPATH=. $(PYTHON) -m backend.app.seed.seed_runner

test:
	@echo "Running backend test suite..."
	PYTHONPATH=. $(PYTEST) backend/tests/ -v

run-backend:
	@echo "Starting SkillPath FastAPI backend on http://localhost:8000..."
	PYTHONPATH=. $(UVICORN) backend.app.main:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	@echo "Starting SkillPath React frontend on http://localhost:5173..."
	cd frontend && npm run dev

build-frontend:
	@echo "Building frontend production bundle..."
	cd frontend && npm run build

docker-up:
	@echo "Starting SkillPath with Docker Compose..."
	docker compose up --build -d

docker-down:
	@echo "Stopping Docker containers..."
	docker compose down

clean:
	@echo "Cleaning caches and builds..."
	rm -rf .pytest_cache
	rm -rf frontend/dist
	find . -type d -name "__pycache__" -exec rm -rf {} +


lint:
	ruff check .

lint-fix:
	ruff check . --fix

format:
	ruff format .

typecheck:
	mypy src

test:
	pytest

check: format lint typecheck test

run:
	uv run uvicorn garden_app.main:app --reload
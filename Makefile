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

check: lint test format typecheck
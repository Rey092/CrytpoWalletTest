install:
	pip install --upgrade pip
	pre-commit install # should be installed Globally. same with poetry


run:
	uvicorn config.app:app --reload


run_parser:
	python manage.py ethereum-blocks-parser

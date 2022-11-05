install:
	pip install --upgrade pip
	pre-commit install # should be installed Globally. same with poetry


run:
	uvicorn config.app:app --reload


init:
	python manage.py init


run_parser:
	python apps/network_ethereum/block_parser.py

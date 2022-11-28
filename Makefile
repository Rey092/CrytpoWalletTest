install:
	pip install --upgrade pip
	pre-commit install # should be installed Globally. same with poetry


init:
	python manage.py init


run:
	uvicorn api_service.config.app:app --workers 2


run_sio:
	uvicorn socketio_service.config.app:app --reload --port 8002


run_eth:
	python eth_network_service/eth_block_parser.py


run_ibay:
	uvicorn ibay_service.config.app:app --reload --port 8001


start_worker:
	celery -A api_service.config.celery worker --loglevel=info

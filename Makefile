format:
	sh scripts/format.sh

test:
	sh scripts/test.sh

mypy:
	python -m mypy --config-file ./app/pyproject.toml app

run:
	cd app && poetry run gunicorn app.main:app \
		--workers 4 \
		--worker-class uvicorn.workers.UvicornWorker \
		--bind 0.0.0.0:8000 \
		--config $(PWD)/gunicorn_conf.py

FROM dr2.parswitch.com/devops/python:3-10
WORKDIR /app/
ENV PYTHONPATH=/app

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Install Poetry version 1
RUN pip install poetry fastapi uvicorn gunicorn
RUN poetry config virtualenvs.create false
# Copy poetry.lock* in case it doesn't exist in the repo
RUN poetry export -f requirements.txt --without-hashes --output /app/requirements.txt
RUN pip install -r requirements.txt

# Install Poetry version 2
# RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
#     cd /usr/local/bin && \
#     ln -s /opt/poetry/bin/poetry && \
#     poetry config virtualenvs.create false

ENV C_FORCE_ROOT=1
COPY ./app/worker-start.sh /worker-start.sh

COPY ./app /app


CMD ["/bin/bash", "/worker-start.sh"]

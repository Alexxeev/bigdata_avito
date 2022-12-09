FROM python:slim-bullseye as builder

WORKDIR /app

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels flask elasticsearch

FROM python:slim-bullseye

WORKDIR /app

COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache /wheels/*

COPY __init__.py .
COPY controller.py .
COPY index.py .

CMD [ "python3", "controller.py" ]
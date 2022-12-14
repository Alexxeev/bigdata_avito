FROM python:slim-bullseye as builder

WORKDIR /app

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels flask elasticsearch scikit-learn pandas numpy

FROM python:slim-bullseye

WORKDIR /app

COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache /wheels/*

COPY ./modules/*.py .
COPY ./model/flatz.pkl ./model/flatz.pkl

CMD [ "python3", "controller.py" ]
FROM python:3.13-alpine

WORKDIR /home

COPY pyproject.toml .

COPY . .

RUN pip install --no-cache-dir -e .

CMD ["user_service"]

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --index-url https://pypi.org/simple \
    filelock typing-extensions setuptools sympy networkx jinja2 fsspec

RUN pip install --no-cache-dir --no-deps \
    torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir \
    --index-url https://pypi.org/simple \
    -r requirements.txt

COPY . .

RUN chmod +x start.sh

EXPOSE 8080

CMD ["./start.sh"]

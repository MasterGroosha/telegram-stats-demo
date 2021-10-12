# Сборочный образ, чтобы не тащить GCC (нужен для ciso* библиотеки)
# в прод-образ
FROM python:3.9-slim-buster as compile-image
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential gcc \
 && python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Прод-образ, куда копируются все собранные ранее зависимости
# Исходный image один и тот же, поэтому можно спокойно копировать
FROM python:3.9-slim-buster
COPY --from=compile-image /opt/venv /opt/venv
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"
COPY *.py /app/
CMD ["python", "-m", "bot"]

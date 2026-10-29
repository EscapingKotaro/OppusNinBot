FROM python:3.11-slim

# Системные зависимости ТОЛЬКО для pyzbar и opencv (без selenium/xvfb!)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libzbar0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Копируем и ставим зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Создаем нужные директории (чтобы shelve и ключи не падали с ошибкой)
RUN mkdir -p data keys video

# Запускаем бота напрямую, без xvfb-run
CMD ["python", "main.py"]
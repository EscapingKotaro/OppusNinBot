FROM python:3.11-slim

# Системные зависимости для pyzbar и opencv
# ВАЖНО: libgl1-mesa-glx заменен на libgl1 для совместимости с новым Debian
RUN apt-get update && apt-get install -y --no-install-recommends \
    libzbar0 \
    libgl1 \
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

# Копируем весь код
COPY . .

# Создаем нужные директории (чтобы shelve и ключи не падали с ошибкой)
RUN mkdir -p data keys video

# Запускаем бота напрямую, без xvfb-run (так как селениума нет)
CMD ["python", "main.py"]
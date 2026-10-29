# app/metrics.py
from prometheus_client import start_http_server, Counter, Gauge, Histogram
import threading
import time

# 1. Жив/не жив (Heartbeat)
BOT_ALIVE = Gauge('bot_alive', '1 если бот жив, обновляется каждые 30 сек')

# 2. Счетчик попыток активации по типам исхода
ACTIVATIONS_TOTAL = Counter(
    'activations_total',
    'Всего попыток отправки запроса на активацию Nintendo',
    ['status']  # success, busy, error, timeout, connection_error, unknown
)

# 3. Гистограмма времени выполнения запроса к API активации
ACTIVATIONS_DURATION = Histogram(
    'activations_duration_seconds',
    'Время выполнения запроса на активацию (сек)',
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

# 4. Размер очереди задач активации прямо сейчас
ACTIVATIONS_QUEUE_SIZE = Gauge(
    'activations_queue_size',
    'Количество задач активации в очереди (maks_tek)'
)

# 5. Итоговые статусы после проверки задач (из check_maks_tek)
ACTIVATION_CHECKS_TOTAL = Counter(
    'activation_checks_total',
    'Всего проверок статуса задач активации',
    ['final_status']  # success, failed, api_error, pending
)

def start_metrics_server(port: int = 9090):
    start_http_server(port)
    print(f"✅ Metrics server started on port {port}")

def start_heartbeat(interval: int = 30):
    def _beat():
        while True:
            BOT_ALIVE.set(1)
            time.sleep(interval)
    t = threading.Thread(target=_beat, daemon=True)
    t.start()
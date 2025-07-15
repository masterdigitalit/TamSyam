#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import requests
import datetime
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

LOCK = threading.Lock()

def generate_uuid1_from_time(dt: datetime.datetime,
                             clock_seq: int = None,
                             node: int = None) -> uuid.UUID:
    """
    Генерирует UUIDv1 по переданному времени dt.
    При отсутствии clock_seq и node берёт их из системы.
    """
    # Эпоха UUIDv1 — 15 октября 1582 UTC
    epoch_start = datetime.datetime(1582, 10, 15, tzinfo=datetime.timezone.utc)
    # Переводим dt в UTC и считаем 100‑нс интервалы
    dt_utc = dt.astimezone(datetime.timezone.utc)
    intervals = int((dt_utc - epoch_start).total_seconds() * 10**7)

    time_low = intervals & 0xFFFFFFFF
    time_mid = (intervals >> 32) & 0xFFFF
    time_hi_and_version = ((intervals >> 48) & 0x0FFF) | (1 << 12)  # версия 1

    # clock_seq и node
    if clock_seq is None:
        clock_seq = uuid.uuid1().clock_seq
    if node is None:
        node = uuid.getnode()

    # Собираем поля в UUID
    return uuid.UUID(fields=(
        time_low,
        time_mid,
        time_hi_and_version,
        (clock_seq >> 8) & 0x3F | 0x80,  # вариант
        clock_seq & 0xFF,
        node
    ))

def check_url(id_code: uuid.UUID,
              timeout: float = 5.0) -> bool:
    """
    Делает запрос к https://dc6.sherlock-report.at/r/<id_code>
    Возвращает True, если статус 200 (страница найдена).
    """
    url = f"https://dc6.sherlock-report.at/r/{id_code}"
    try:
        resp = requests.get(url, allow_redirects=False, timeout=timeout)
        if resp.status_code == 200:
            with LOCK:
                with open("found.txt", "a", encoding="utf-8") as f:
                    f.write(f"{id_code}\n")
                print(f"❗ Обнаружена страница: {url}")
            return True
    except requests.RequestException as e:
        print(f"⚠ Ошибка запроса {url}: {e}")
    return False

def worker(args_tuple):
    """
    Пакетный воркер для ThreadPoolExecutor.
    Получает (dt, clock_seq, node, timeout), генерирует uuid и проверяет URL.
    """
    dt, clock_seq, node, timeout = args_tuple
    uid = generate_uuid1_from_time(dt, clock_seq, node)
    check_url(uid, timeout)

def main():
    p = argparse.ArgumentParser(
        description="Генератор и сканер UUIDv1 для dc6.sherlock-report.at"
    )
    p.add_argument("--start", type=str, default="2023-01-01T00:00:00",
                   help="Стартовая дата (ISO), например 2023-01-01T00:00:00")
    p.add_argument("--end", type=str, default=None,
                   help="Конечная дата (ISO), по умолчанию – сейчас")
    p.add_argument("--step", type=float, default=1.0,
                   help="Шаг итерации в секундах (float)")
    p.add_argument("--delay", type=float, default=0.1,
                   help="Пауза между батчами запросов в секундах")
    p.add_argument("--timeout", type=float, default=5.0,
                   help="Timeout HTTP-запросов в секундах")
    p.add_argument("--workers", type=int, default=5,
                   help="Число потоков для одновременных запросов")
    p.add_argument("--clock-seq", type=int, default=None,
                   help="Зафиксированный clock_seq (по умолчанию – рандомный)")
    p.add_argument("--node", type=lambda x: int(x, 0), default=None,
                   help="Зафиксированный node (MAC, по умолчанию – системный)")
    args = p.parse_args()

    # Парсим даты
    dt_start = datetime.datetime.fromisoformat(args.start)
    dt_end = datetime.datetime.fromisoformat(args.end) if args.end else datetime.datetime.now()
    step_delta = datetime.timedelta(seconds=args.step)

    # Очищаем файл результатов
    open("found.txt", "w", encoding="utf-8").close()

    # Составляем список задач
    tasks = []
    current = dt_start
    while current <= dt_end:
        tasks.append((current, args.clock_seq, args.node, args.timeout))
        current += step_delta

    print(f"Всего итераций: {len(tasks)}")
    print(f"Запуск {args.workers} воркеров…")

    # Параллельно сканируем
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for i in range(0, len(tasks), args.workers):
            batch = tasks[i:i + args.workers]
            futures = [executor.submit(worker, t) for t in batch]
            # ждем завершения батча
            for _ in as_completed(futures):
                pass
            time.sleep(args.delay)

    print("Готово! Успешные UUID записаны в found.txt")

if __name__ == "__main__":
    main()

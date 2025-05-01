# attack.py
"""
Модуль для автоматизации атаки в игре. Содержит функции для:
- Поиска и вступления в бой
- Выбора противника
- Размещения войск
- Ожидания завершения боя
"""

from utils import find_and_click, hold_mouse_in_parallelogram
from config import DEPLOY_ZONE_1, DEPLOY_ZONE_2
from logger import log
import time
import random

def auto_attack():
    """
    Основная функция автоматической атаки.
    Выполняет полный цикл от поиска боя до завершения.
    
    Returns:
        bool: True если атака завершена успешно, False в случае ошибки
    """
    log("Начинаем автоатаку...")

    # 1. Этап вступления в бой
    if not find_and_click("C:/farmbot/images/attack.png"):
        log("Кнопка 'В бой' не найдена.")
        return False

    # Пауза для загрузки интерфейса
    time.sleep(2)
    
    # 2. Этап поиска соперника
    if not find_and_click("C:/farmbot/images/find_match.png"):
        log("Кнопка 'Подбор' не найдена.")
        return False

    # Ожидание подбора соперника
    time.sleep(5)

    # 3. Этап выбора противника (опциональный)
    # Случайное количество попыток найти другого противника
    for _ in range(random.randint(0, 5)):   
        if find_and_click("C:/farmbot/images/next_opponent.png", silent_errors=True):
            log("Следующий противник...")
            time.sleep(random.uniform(1, 2))  # Случайная пауза между действиями

    # 4. Подготовка к атаке
    # Случайная задержка перед атакой для имитации человеческого поведения
    delay = random.randint(0, 10)
    log(f"Ждём {delay} сек перед атакой...")
    time.sleep(delay)

    # 5. Выбор войск для атаки
    if not find_and_click("C:/farmbot/images/troop_icon.png"):
        log("Иконка юнита не найдена.")
        return False

    # 6. Размещение войск на поле боя
    log("Выпускаем войска...")
    # Первая зона размещения - короткое удержание
    hold_mouse_in_parallelogram(DEPLOY_ZONE_1, hold_time=1)
    # Вторая зона размещения - длинное удержание (основные силы)
    hold_mouse_in_parallelogram(DEPLOY_ZONE_2, hold_time=10)

    log("Войска выпущены. Ждём окончания боя...")

    # 7. Ожидание завершения боя
    wait_time = time.time() + 180  # Максимальное время ожидания - 3 минуты
    last_log_time = 0  # Время последнего лога
    check_interval = 5  # Интервал проверки завершения боя (сек)

    while time.time() < wait_time:
        try:
            # Проверка кнопки "Домой" - признак завершения боя
            if find_and_click("C:/farmbot/images/home_button.png", silent_all=True):
                log("Бой завершён, нажата кнопка 'Домой'.")
                return True
            
            # Логирование статуса не чаще чем раз в 30 секунд
            now = time.time()
            if now - last_log_time > 30:
                log("[INFO] Ожидание завершения боя...")
                last_log_time = now
                
        except Exception as e:
            # Логирование ошибок не чаще чем раз в 30 секунд
            now = time.time()
            if now - last_log_time > 30:
                log(f"[INFO] Ошибка при ожидании: {str(e)}")
                last_log_time = now
                
        time.sleep(check_interval)

    # 8. Завершение по таймауту
    log("Время боя истекло. Возвращаемся вручную.")
    # Последняя попытка найти кнопку "Домой"
    return find_and_click("C:/farmbot/images/home_button.png")
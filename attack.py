# attack.py
from utils import find_and_click, hold_mouse_in_parallelogram
from config import DEPLOY_ZONE_1, DEPLOY_ZONE_2
from logger import log
import time
import random

def auto_attack():
    log("Начинаем автоатаку...")

    # Важные элементы - логируем как обычно
    if not find_and_click("C:/farmbot/images/attack.png"):
        log("Кнопка 'В бой' не найдена.")
        return False

    time.sleep(2)
    if not find_and_click("C:/farmbot/images/find_match.png"):
        log("Кнопка 'Подбор' не найдена.")
        return False

    time.sleep(5)

    # Для менее важных элементов можно использовать silent_errors
    for _ in range(random.randint(0, 5)):   
        if find_and_click("C:/farmbot/images/next_opponent.png", silent_errors=True):
            log("Следующий противник...")
            time.sleep(random.uniform(1, 2))

    delay = random.randint(0, 10)
    log(f"Ждём {delay} сек перед атакой...")
    time.sleep(delay)

    if not find_and_click("C:/farmbot/images/troop_icon.png"):
        log("Иконка юнита не найдена.")
        return False

    log("Выпускаем войска...")
    hold_mouse_in_parallelogram(DEPLOY_ZONE_1, hold_time=1)
    hold_mouse_in_parallelogram(DEPLOY_ZONE_2, hold_time=10)

    log("Войска выпущены. Ждём окончания боя...")

    wait_time = time.time() + 180
    last_log_time = 0
    check_interval = 5

    while time.time() < wait_time:
        try:
            # Для периодических проверок используем silent_all
            if find_and_click("C:/farmbot/images/home_button.png", silent_all=True):
                log("Бой завершён, нажата кнопка 'Домой'.")
                return True
            
            # Логируем статус не чаще чем раз в 30 секунд
            now = time.time()
            if now - last_log_time > 30:
                log("[INFO] Ожидание завершения боя...")
                last_log_time = now
                
        except Exception as e:
            now = time.time()
            if now - last_log_time > 30:
                log(f"[INFO] Ошибка при ожидании: {str(e)}")
                last_log_time = now
                
        time.sleep(check_interval)

    log("Время боя истекло. Возвращаемся вручную.")
    # Последняя попытка - важное событие, логируем полностью
    return find_and_click("C:/farmbot/images/home_button.png")
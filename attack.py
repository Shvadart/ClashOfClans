# attack.py
from utils import find_and_click, hold_mouse_in_parallelogram
from config import DEPLOY_ZONE_1, DEPLOY_ZONE_2
from logger import log
import time
import random

def auto_attack():
    log("Начинаем автоатаку...")

    if not find_and_click("C:/farmbot/images/attack.png"):
        log("Кнопка 'В бой' не найдена.")
        return False

    time.sleep(2)
    if not find_and_click("C:/farmbot/images/find_match.png"):
        log("Кнопка 'Подбор' не найдена.")
        return False

    time.sleep(5)

    # Рандомно нажимаем "следующий противник" 0–5 раз
    for _ in range(random.randint(0, 5)):   
        if find_and_click("C:/farmbot/images/next_opponent.png"):
            log("Следующий противник...")
            time.sleep(random.uniform(1, 2))
        



    # Пауза перед началом атаки
    delay = random.randint(0, 15)
    log(f"Ждём {delay} сек перед атакой...")
    time.sleep(delay)

    # Кликаем по иконке юнита
    if not find_and_click("C:/farmbot/images/troop_icon.png"):
        log("Иконка юнита не найдена.")
        return False

    log("Выпускаем войска...")

    log("Зажимаем мышку в зоне 1 для выпуска юнитов...")
    hold_mouse_in_parallelogram(DEPLOY_ZONE_1, hold_time=1.5)

    log("Зажимаем мышку в зоне 2 для выпуска юнитов...")
    hold_mouse_in_parallelogram(DEPLOY_ZONE_2, hold_time=4)


    log("Войска выпущены. Ждём окончания боя...")

    wait_time = time.time() + 180  # 3 минуты
    last_log_time = 0

    while time.time() < wait_time:
        try:
            if find_and_click("C:/farmbot/images/home_button.png"):
                log("Бой завершён, нажата кнопка 'Домой'.")
                return True
        except Exception as e:
            now = time.time()
            if now - last_log_time > 30:
                log(f"[INFO] Кнопка 'Домой' пока не найдена...")
                last_log_time = now
        time.sleep(5)



    log("Время боя истекло. Возвращаемся вручную.")
    try:
        return find_and_click("C:/farmbot/images/home_button.png")
    except Exception as e:
        log(f"[ERROR] Не удалось вернуться домой вручную: {e}")
        return False

    

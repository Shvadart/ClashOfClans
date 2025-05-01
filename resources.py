# resources.py
"""
Модуль для работы с игровыми ресурсами. Функционал:
- Получение текущего количества ресурсов (золото, эликсир, самоцветы)
- Определение уровня ратуши
- Создание скриншотов игровых областей
- Логирование результатов
"""

from numbers_from_screenshotes import get_all_resources
from make_screenshot import make_screenshot
from config import GOLD_REGION, ELIXIR_REGION, GEMS_REGION
from logger import log
from utils import find_on_screen
import time
import os

def get_resources():
    """
    Получает текущее количество всех ресурсов игрока.
    
    Returns:
        tuple: (gold, elixir, gems) - количество каждого ресурса:
            - gold (int): количество золота
            - elixir (int): количество эликсира
            - gems (int): количество самоцветов
            
    Процесс:
    1. Делает скриншоты областей с ресурсами
    2. Распознает числа с изображений
    3. Логирует результаты
    """
    # Создаем скриншоты областей с ресурсами
    make_screenshot(GOLD_REGION, 'gold_region.png')
    make_screenshot(ELIXIR_REGION, 'elixir_region.png')
    make_screenshot(GEMS_REGION, 'gems_region.png')

    # Получаем количество ресурсов через OCR
    gold, elixir, gems = get_all_resources()
    
    # Логируем результаты
    log(f"Ресурсы: золото = {gold}, эликсир = {elixir}, гемы = {gems}")
    
    return gold, elixir, gems

def get_townhall_level():
    """
    Определяет уровень ратуши игрока.
    
    Returns:
        int or None: уровень ратуши (2-10) или None, если не удалось определить
        
    Алгоритм:
    1. Делает скриншот всей деревни
    2. Сравнивает с шаблонами ратуш разных уровней
    3. При необходимости повторяет попытки
    4. Запрашивает пользовательский ввод при неудаче
    """
    IMAGE_DIR = "C:/farmbot/images/"
    screenshot_path = os.path.join(IMAGE_DIR, "townhall_snapshot.png")
    attempts = 3  # Количество попыток распознавания
    delay_between = 2  # Задержка между попытками в секундах

    for attempt in range(attempts):
        # 1. Создаем скриншот деревни
        make_screenshot(region=None, filename=screenshot_path)
        screenshot = cv2.imread(screenshot_path)
        
        if screenshot is None:
            log("[ERROR] Скриншот деревни не загружен.")
            return None

        # 2. Проверяем все возможные уровни ратуши
        for level in range(2, 11):  # Уровни ратуши от 2 до 10
            for file in os.listdir(IMAGE_DIR):
                # Ищем файлы шаблонов для текущего уровня
                if file.startswith(f"townhall_{level}_") and file.endswith(".png"):
                    path = os.path.join(IMAGE_DIR, file)
                    template = cv2.imread(path)
                    
                    if template is None:
                        log(f"[ERROR] Не удалось загрузить шаблон: {path}")
                        continue

                    # Сравниваем скриншот с шаблоном
                    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)
                    
                    # Порог совпадения (0.87 = 87%)
                    threshold = 0.87
                    if max_val >= threshold:
                        log(f"✅ Найдена ратуша уровня {level} по шаблону {file}")
                        return level

        # 3. Если ратуша не найдена - пауза перед повторной попыткой
        if attempt < attempts - 1:
            log("🔁 Ратуша не найдена, повторная попытка...")
            time.sleep(delay_between)

    # 4. Если все попытки исчерпаны
    log("❌ Ратуша не найдена ни в одной из попыток.")
    
    # 5. Запрашиваем действия пользователя
    user_input = input("🔁 Добавь шаблон ратуши и нажми Enter (или введи 'stop' для выхода): ")
    if user_input.strip().lower() == "stop":
        log("🛑 Программа остановлена пользователем.")
        exit(0)
        
    # 6. Рекурсивный вызов после добавления шаблона
    return get_townhall_level()
# collect.py
"""
Модуль для автоматического сбора ресурсов в игре. Функционал:
- Поиск и сбор золота и эликсира на экране
- Несколько попыток поиска с прокруткой экрана
- Диагностика проблем при сборе
"""

from utils import find_any_and_click, find_any_on_screen, debug_screenshot
from logger import log
from config import IMAGE_DIR, CONFIDENCE, PAUSE_SHORT
import time
import os
import pyautogui

def collect_resources_if_visible():
    """
    Основная функция сбора ресурсов. Выполняет:
    1. Поиск ресурсов по шаблонам изображений
    2. Несколько попыток сбора
    3. Прокрутку экрана при необходимости
    4. Диагностику при неудаче
    
    Returns:
        bool: True если ресурсы были собраны, иначе False
    """
    # Группы изображений для разных типов ресурсов
    resource_groups = {
        'gold': [
            os.path.join(IMAGE_DIR, "collect_gold_sv.png"),  # Золото (вариант 1)
            os.path.join(IMAGE_DIR, "collect_gold_v.png")    # Золото (вариант 2)
        ],
        'elixir': [
            os.path.join(IMAGE_DIR, "collect_elixir_svs.png"),  # Эликсир (вариант 1)
            os.path.join(IMAGE_DIR, "collect_elixir_szfv.png")   # Эликсир (вариант 2)
        ]
    }

    collected = False  # Флаг успешного сбора
    max_attempts = 3   # Максимальное количество попыток сбора
    
    # Основной цикл попыток сбора
    for attempt in range(1, max_attempts + 1):
        log(f"Попытка сбора {attempt}/{max_attempts}...")
        
        # Перебираем все типы ресурсов
        for res_type, images in resource_groups.items():
            # Проверка существования файлов изображений
            if not any(os.path.exists(img) for img in images):
                log(f"⚠️ Нет изображений для {res_type}", silent=True)
                continue
                
            # Пытаемся найти и кликнуть по любому из изображений
            if find_any_and_click(images, pause=PAUSE_SHORT):
                log(f"💰 Собраны ресурсы ({res_type})")
                collected = True
                time.sleep(0.5)  # Короткая пауза между сборами

        # Если хотя бы что-то собрали - прерываем попытки
        if collected:
            break
            
        time.sleep(1)  # Пауза между попытками
        
        # Если после 2 попыток ничего не нашли - пробуем прокрутить экран
        if attempt == 2:
            try_scroll()

    # Если сбор не удался - запускаем диагностику
    if not collected:
        log("⚠️ Ресурсы не найдены. Диагностика...")
        run_diagnostics(resource_groups)
    
    return collected

def try_scroll():
    """
    Пытается прокрутить экран вверх для поиска ресурсов.
    Использует pyautogui для имитации drag-жеста.
    """
    log("Пробуем прокрутить экран...")
    try:
        # Перемещаем курсор в центр экрана
        pyautogui.moveTo(500, 300)
        # Имитируем перетаскивание вверх на 200 пикселей
        pyautogui.dragRel(0, -200, duration=0.5)
        time.sleep(1)  # Пауза после прокрутки
    except Exception as e:
        log(f"⚠️ Ошибка прокрутки: {str(e)}", silent=True)

def run_diagnostics(resource_groups):
    """
    Запускает диагностику причин неудачного сбора:
    1. Делает скриншот экрана
    2. Проверяет видимость шаблонов ресурсов
    
    Args:
        resource_groups (dict): Словарь с путями к изображениям ресурсов
    """
    # Создаем отладочный скриншот
    debug_screenshot()
    
    # Проверяем какие изображения видны на экране
    for res_type, images in resource_groups.items():
        visible = []
        for img in images:
            # Проверяем существование файла и его видимость на экране
            if os.path.exists(img) and find_any_on_screen(img, CONFIDENCE-0.1):
                visible.append(os.path.basename(img))  # Добавляем только имя файла
        
        if visible:
            log(f"🔍 Видимые изображения для {res_type}: {', '.join(visible)}")
        else:
            log(f"🔍 Для {res_type} ничего не найдено")

if __name__ == "__main__":
    # Точка входа при прямом запуске скрипта
    collect_resources_if_visible()
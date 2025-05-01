# builder.py
"""
Модуль для автоматизации строительства в игре. Содержит функции для:
- Открытия меню строителя
- Поиска новых доступных построек
- Проверки ресурсов
- Размещения зданий на карте
"""

from utils import find_and_click, find_on_screen, find_any_on_screen
from logger import log
from resources import get_resources, get_townhall_level
from decorators import with_resource_collection
from config import *
from utils import debug_screenshot
import time
import pyautogui
import json
import os

def build_new_structure():
    """
    Основная функция строительства новых зданий.
    Выполняет полный цикл от открытия меню строителя до подтверждения постройки.
    
    Returns:
        bool: True если здание успешно построено, False в случае ошибки
    """
    # Получаем текущее количество ресурсов
    gold, elixir, _ = get_resources()
    
    # 1. Открываем меню строителя
    log("Открываем меню строителя...")
    if not find_and_click(
            "C:/farmbot/images/builder_icon.png",
            confidence=0.8,  # Уровень уверенности для иконки строителя
            retry=5,         # Количество попыток
            silent_errors=True  # Не логируем ошибки поиска
        ):
            log("❌ Меню строителя не найдено после 5 попыток")
            return False

    # Пауза для загрузки интерфейса
    time.sleep(0.5)
    
    # 2. Поиск доступных новых построек
    new_found = False
    log(f"🔍 Ищем 'Новое' в регионе: {SEARCH_REGION}")
    debug_screenshot(region=SEARCH_REGION)  # Дебажный скриншот
    
    # Проверяем несколько вариантов изображения "Новое"
    for new_img in [
        "C:/farmbot/images/new1.png",
        "C:/farmbot/images/new2.png",
        "C:/farmbot/images/new3.png",
        "C:/farmbot/images/new4.png",
        "C:/farmbot/images/new5.png"
    ]:
        if find_and_click(new_img, 
                         retry=0,
                         confidence=CONFIDENCE_BUILDER,
                         region=SEARCH_REGION):
            log(f"✅ Найдено 'Новое': {new_img}")
            new_found = True
            break

    # Если не нашли - пробуем проскроллить
    if not new_found:
        log("📜 Не найдено 'Новое' в видимой области, пролистываем...")
        pyautogui.moveTo(950, 200)  # Позиция для скролла
        time.sleep(0.3)
        pyautogui.scroll(-350)  # Скролл вниз
        time.sleep(0.5)
        
        # Повторяем поиск после скролла
        log(f"🔍 Ищем 'Новое' в регионе: {SEARCH_REGION}")
        debug_screenshot(region=SEARCH_REGION)
        for new_img in [
            "C:/farmbot/images/new1.png",
            "C:/farmbot/images/new2.png",
            "C:/farmbot/images/new3.png",
            "C:/farmbot/images/new4.png",
            "C:/farmbot/images/new5.png"
        ]:
            if find_and_click(new_img, retry=0, region=SEARCH_REGION):
                log(f"✅ Найдено 'Новое' после скролла: {new_img}")
                new_found = True
                break
    
    # Если после скролла не нашли - выходим
    if not new_found:
        log("❌ Ни одно новое здание не найдено.")
        return False

    # 3. Проверка на хижину строителя (особый случай)
    time.sleep(1)
    if find_on_screen("C:/farmbot/images/builder_hut_label.png"):
        log("🚫 Обнаружена Хижина строителя — отменяем выбор.")
        find_and_click("C:/farmbot/images/red_cross.png")  # Клик по крестику
        return False

    # 4. Поиск стрелки, указывающей на доступное место для постройки
    log("🎯 Ищем стрелку...")
    arrow = None
    for arrow_img in [
        "C:/farmbot/images/arrow1.png",
        "C:/farmbot/images/arrow2.png",
        "C:/farmbot/images/arrow3.png",
        "C:/farmbot/images/arrow4.png",
        "C:/farmbot/images/arrow5.png",
        "C:/farmbot/images/arrow6.png"
    ]:
        arrow = find_on_screen(arrow_img)
        if arrow:
            log(f"✅ Найдена стрелка: {arrow_img}")
            break

    if not arrow:
        log("❌ Стрелка не найдена.")
        return False

    # 5. Загрузка данных о доступных зданиях из JSON
    path = os.path.join(os.path.dirname(__file__), "new_buildings.json")
    with open(path, "r", encoding="utf-8") as f:
        building_data = json.load(f)

    # 6. Поиск подходящего здания
    match_found = False
    for b in building_data:
        # Поддержка как строки, так и списка изображений для здания
        image_paths = [b["name"]] if isinstance(b["name"], str) else b["name"]
        
        if find_any_on_screen(image_paths):
            building_name = os.path.basename(image_paths[0]) if isinstance(image_paths, list) else os.path.basename(image_paths)
            log(f"🔎 Определено здание: {building_name}")
            
            # Проверка достаточности ресурсов
            if gold >= b.get("gold", 0) and elixir >= b.get("elixir", 0):
                match_found = True
                break
            else:
                log("❌ Недостаточно ресурсов для постройки. Отменяем...")
                find_and_click("C:/farmbot/images/red_cross.png")
                return False

    if not match_found:
        log("❌ Не удалось определить здание по шаблонам. Прерываем.")
        find_and_click("C:/farmbot/images/red_cross.png")
        return False

    # 7. Размещение здания на карте
    x, y, w, h = arrow
    target_x = x + w // 2  # Центр стрелки по X
    target_y = y + h + 40   # Ниже стрелки на 40px
    pyautogui.moveTo(target_x, target_y)
    pyautogui.click()
    log(f"📦 Клик по зданию под стрелкой: ({target_x}, {target_y})")

    # 8. Подтверждение строительства
    time.sleep(2)  # Ожидание появления окна подтверждения

    log("✅ Подтверждаем размещение здания...")
    
    # Пробуем несколько вариантов кнопки подтверждения
    check_found = False
    for check_img in [
        "C:/farmbot/images/green_check.png",
        "C:/farmbot/images/green_check_v2.png",
        "C:/farmbot/images/green_check_small.png"
    ]:
        if find_and_click(check_img, 
                         confidence=0.9,  # Высокий уровень уверенности
                         retry=3,         # 3 попытки
                         pause=0.5):      # Пауза между попытками
            log(f"✅ Галочка найдена: {check_img}")
            check_found = True
            break
        time.sleep(0.3)

    if not check_found:
        debug_path = debug_screenshot()
        log("❌ Ни одна из галочек не найдена")
        log(f"Скриншот сохранен: {debug_path}")
        return False

    # Финализация процесса
    time.sleep(1)  # Ожидание завершения анимации
    log("✅ Здание успешно размещено.")
    return True
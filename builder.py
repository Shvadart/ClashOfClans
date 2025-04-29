# builder.py (финальная версия)
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

#@with_resource_collection
def build_new_structure():
    gold, elixir, _ = get_resources()
    log("Открываем меню строителя...")
    if not find_and_click(
            "C:/farmbot/images/builder_icon.png",
            confidence=0.8,
            retry=5,
            silent_errors=True
        ):
            log("❌ Меню строителя не найдено после 5 попыток")
            return False

    time.sleep(0.5)
    new_found = False
    for new_img in [
        "C:/farmbot/images/new1.png",
        "C:/farmbot/images/new2.png",
        "C:/farmbot/images/new3.png",
        "C:/farmbot/images/new4.png",
        "C:/farmbot/images/new5.png"
    ]:
        if find_and_click(new_img, retry=0, region=SEARCH_REGION):  # Добавляем region
            log(f"✅ Найдено 'Новое': {new_img}")
            new_found = True
            break

    if not new_found:
        log("📜 Не найдено 'Новое' в видимой области, пролистываем...")
        pyautogui.moveTo(500, 500)
        pyautogui.dragRel(0, -100, duration=0.3)
        time.sleep(0.5)
        # Повторяем поиск после скролла
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
    if not new_found:
        log("❌ Ни одно новое здание не найдено.")
        return False

    time.sleep(1)
    if find_on_screen("C:/farmbot/images/builder_hut_label.png"):
        log("🚫 Обнаружена Хижина строителя — отменяем выбор.")
        find_and_click("C:/farmbot/images/red_cross.png")
        return False

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

    path = os.path.join(os.path.dirname(__file__), "new_buildings.json")
    with open(path, "r", encoding="utf-8") as f:
        building_data = json.load(f)

    match_found = False
    for b in building_data:
        # Поддержка как строки, так и списка изображений
        image_paths = [b["name"]] if isinstance(b["name"], str) else b["name"]
        
        if find_any_on_screen(image_paths):
            building_name = os.path.basename(image_paths[0]) if isinstance(image_paths, list) else os.path.basename(image_paths)
            log(f"🔎 Определено здание: {building_name}")
            
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

    x, y, w, h = arrow
    target_x = x + w // 2
    target_y = y + h + 40
    pyautogui.moveTo(target_x, target_y)
    pyautogui.click()
    log(f"📦 Клик по зданию под стрелкой: ({target_x}, {target_y})")

    # Увеличиваем задержку и добавляем проверку анимации
    time.sleep(2)  # Даем время для появления окна подтверждения

    log("✅ Подтверждаем размещение здания...")
    
    # Пробуем несколько вариантов галочки с разными параметрами
    check_found = False
    for check_img in [
        "C:/farmbot/images/green_check.png",
        "C:/farmbot/images/green_check_v2.png",
        "C:/farmbot/images/green_check_small.png"
    ]:
        if find_and_click(check_img, confidence=0.9, retry=3, pause=0.5):
            log(f"✅ Галочка найдена: {check_img}")
            check_found = True
            break
        time.sleep(0.3)  # Небольшая пауза между попытками

    if not check_found:
        debug_path = debug_screenshot()
        log("❌ Ни одна из галочек не найдена")
        log(f"Скриншот сохранен: {debug_path}")
        return False

    # Дополнительная пауза после клика
    time.sleep(1)
    log("✅ Здание успешно размещено.")
    return True
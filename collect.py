# collect.py
from utils import find_any_and_click, find_any_on_screen, debug_screenshot
from logger import log
from config import IMAGE_DIR, CONFIDENCE, PAUSE_SHORT
import time
import os
import pyautogui

def collect_resources_if_visible():
    """Сбор ресурсов с использованием ваших текущих функций"""
    resource_groups = {
        'gold': [
            os.path.join(IMAGE_DIR, "collect_gold_sv.png"),
            os.path.join(IMAGE_DIR, "collect_gold_v.png")
        ],
        'elixir': [
            os.path.join(IMAGE_DIR, "collect_elixir_svs.png"),
            os.path.join(IMAGE_DIR, "collect_elixir_szfv.png")
        ]
    }

    collected = False
    max_attempts = 3  # Максимальное количество попыток
    
    for attempt in range(1, max_attempts + 1):
        log(f"Попытка сбора {attempt}/{max_attempts}...")
        
        for res_type, images in resource_groups.items():
            # Проверяем наличие хотя бы одного изображения
            if not any(os.path.exists(img) for img in images):
                log(f"⚠️ Нет изображений для {res_type}", silent=True)
                continue
                
            # Используем find_any_and_click для автоматического клика
            if find_any_and_click(images, pause=PAUSE_SHORT):
                log(f"💰 Собраны ресурсы ({res_type})")
                collected = True
                time.sleep(0.5)  # Пауза между сборами

        if collected:
            break  # Если что-то собрали, выходим
            
        time.sleep(1)  # Пауза между попытками
        
        # Если не нашли в первые две попытки, пробуем прокрутить
        if attempt == 2:
            try_scroll()

    if not collected:
        log("⚠️ Ресурсы не найдены. Диагностика...")
        run_diagnostics(resource_groups)
    
    return collected

def try_scroll():
    """Пробуем прокрутить экран"""
    log("Пробуем прокрутить экран...")
    try:
        pyautogui.moveTo(500, 300)
        pyautogui.dragRel(0, -200, duration=0.5)
        time.sleep(1)
    except Exception as e:
        log(f"⚠️ Ошибка прокрутки: {str(e)}", silent=True)

def run_diagnostics(resource_groups):
    """Диагностика причин неудачи"""
    debug_screenshot()
    
    # Проверяем какие изображения вообще видны на экране
    for res_type, images in resource_groups.items():
        visible = []
        for img in images:
            if os.path.exists(img) and find_any_on_screen(img, CONFIDENCE-0.1):
                visible.append(os.path.basename(img))
        
        if visible:
            log(f"🔍 Видимые изображения для {res_type}: {', '.join(visible)}")
        else:
            log(f"🔍 Для {res_type} ничего не найдено")

if __name__ == "__main__":
    collect_resources_if_visible()
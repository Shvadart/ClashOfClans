# collect.py
from utils import find_and_click, debug_screenshot
from logger import log
import time
import os

def collect_resources_if_visible():
    collected = False
    resource_images = [
        os.path.join("collect_gold.png"),
        os.path.join("collect_elixir.png"),
        os.path.join("collect_gold_d.png"),  # альтернативные варианты
        os.path.join("collect_elixir_s.png"),
        os.path.join("collect_gold_sv.png"),
        os.path.join("collect_elixir_svs.png")

    ]
    
    # Пробуем с разными уровнями confidence
    conf_levels = [0.7, 0.6, 0.5] if not collected else []
    
    for conf in conf_levels:
        for img in resource_images:
            if find_and_click(img, confidence=conf):
                log(f"💰 Ресурсы собраны (confidence={conf}): {img}")
                time.sleep(0.5)
                collected = True
                break
        if collected:
            break
            
    if not collected:
        debug_path = debug_screenshot()
        log(f"⚠️ Ресурсы не найдены. Скриншот сохранен: {debug_path}")
    
    return collected
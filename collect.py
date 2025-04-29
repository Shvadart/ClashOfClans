# collect.py
from utils import find_and_click, debug_screenshot
from logger import log
from config import IMAGE_DIR
import time
import os

def collect_resources_if_visible():
    """Сбор ресурсов с улучшенной логикой и обработкой ошибок"""
    resource_groups = {
        'gold': [
            "collect_gold.png",
            "collect_gold_d.png",
            "collect_gold_sv.png"
        ],
        'elixir': [
            "collect_elixir.png",
            "collect_elixir_s.png",
            "collect_elixir_svs.png"
        ]
    }

    collected = False
    max_attempts = 2
    
    for attempt in range(max_attempts):
        for res_type, images in resource_groups.items():
            for img in images:
                full_path = os.path.join(IMAGE_DIR, img)
                if not os.path.exists(full_path):
                    continue
                    
                try:
                    if find_and_click(full_path, confidence=0.8, retry=1, silent_errors=True):
                        log(f"💰 Собраны ресурсы ({res_type}): {img}")
                        collected = True
                        time.sleep(0.3)
                except Exception as e:
                    log(f"[WARN] Ошибка при сборе {res_type}: {str(e)}", silent=True)

    if not collected:
        log("⚠️ Ресурсы не найдены", silent=True)
        debug_screenshot()
    
    return collected
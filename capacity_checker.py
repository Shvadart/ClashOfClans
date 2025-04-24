# capacity_checker.py
import json
import os
import cv2
import numpy as np
from utils import find_on_screen
from make_screenshot import make_screenshot
from logger import log
from resources import get_townhall_level

def get_total_capacity(resource_type):
    IMAGE_DIR = "C:/farmbot/images/"
    storage_file = os.path.join(os.path.dirname(__file__), "storage_levels.json")
    screenshot_path = "C:/farmbot/images/village_snapshot.png"

    with open(storage_file, "r", encoding="utf-8") as f:
        capacities = json.load(f)

    cached_townhall_level = [None]

    def calculate_from_screenshot():
        make_screenshot(region=None, filename=screenshot_path)
        screenshot = cv2.imread(screenshot_path)
        if screenshot is None:
            log("[ERROR] Скриншот не загружен.")
            return 0

        total = 0
        filtered_global = []
        min_distance = 20

        for file in os.listdir(IMAGE_DIR):
            if not file.endswith(".png"):
                continue

            for level_key in capacities.get(f"{resource_type}_storage", {}).keys():
                if file.startswith(f"{resource_type}_storage_lvl{level_key}_"):
                    level = level_key
                    amount = capacities[f"{resource_type}_storage"][level]
                    image_path = os.path.join(IMAGE_DIR, file)
                    template = cv2.imread(image_path)
                    if template is None:
                        log(f"[ERROR] Шаблон не загружен: {image_path}")
                        continue

                    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.89
                    locations = np.where(result >= threshold)
                    matches = list(zip(*locations[::-1]))

                    count = 0
                    for pt in matches:
                        if all(np.linalg.norm(np.array(pt) - np.array(f)) > min_distance for f in filtered_global):
                            filtered_global.append(pt)
                            count += 1
                            log(f"[INFO] Найдено хранилище уровня {level} для {resource_type} по шаблону {file}")

                    total += int(amount) * count

        if cached_townhall_level[0] is None:
            cached_townhall_level[0] = get_townhall_level()

        townhall_level = cached_townhall_level[0]
        if townhall_level:
            townhall_key = f"townhall_{resource_type}_storage"
            fallback_key = "townhall_storage"
            th_storage = capacities.get(townhall_key, {}).get(str(townhall_level)) or capacities.get(fallback_key, {}).get(str(townhall_level))
            if th_storage:
                total += int(th_storage)
                log(f"[INFO] Вместимость ратуши ({resource_type}): {th_storage}")

        return total

    cap1 = calculate_from_screenshot()
    cap2 = calculate_from_screenshot()
    return max(cap1, cap2)

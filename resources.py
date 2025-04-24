#resources.py
from numbers_from_screenshotes import get_all_resources
from make_screenshot import make_screenshot
from config import GOLD_REGION, ELIXIR_REGION, GEMS_REGION
from logger import log
from utils import find_on_screen
import time
import os

def get_resources():
    make_screenshot(GOLD_REGION, 'gold_region.png')
    make_screenshot(ELIXIR_REGION, 'elixir_region.png')
    make_screenshot(GEMS_REGION, 'gems_region.png')

    gold, elixir, gems = get_all_resources()
    log(f"Ресурсы: золото = {gold}, эликсир = {elixir}, гемы = {gems}")
    return gold, elixir, gems

def get_townhall_level():
    import time
    import cv2
    import os
    from make_screenshot import make_screenshot
    from logger import log

    IMAGE_DIR = "C:/farmbot/images/"
    screenshot_path = os.path.join(IMAGE_DIR, "townhall_snapshot.png")
    attempts = 3
    delay_between = 2  # секунды

    for attempt in range(attempts):
        make_screenshot(region=None, filename=screenshot_path)
        screenshot = cv2.imread(screenshot_path)
        if screenshot is None:
            log("[ERROR] Скриншот деревни не загружен.")
            return None

        for level in range(2, 11):  # от 2 до 10 уровня
            for file in os.listdir(IMAGE_DIR):
                if file.startswith(f"townhall_{level}_") and file.endswith(".png"):
                    path = os.path.join(IMAGE_DIR, file)
                    template = cv2.imread(path)
                    if template is None:
                        log(f"[ERROR] Не удалось загрузить шаблон: {path}")
                        continue

                    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)
                    threshold = 0.87
                    if max_val >= threshold:
                        log(f"✅ Найдена ратуша уровня {level} по шаблону {file}")
                        return level

        if attempt < attempts - 1:
            log("🔁 Ратуша не найдена, повторная попытка...")
            time.sleep(delay_between)

    log("❌ Ратуша не найдена ни в одной из попыток.")
    return None



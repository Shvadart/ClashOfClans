# capacity_checker.py
import os
import json
import cv2
import numpy as np
from logger import log
from cache import load_cache, save_cache, get_cached_storage  # type: ignore
from make_screenshot import make_screenshot
from resources import get_townhall_level

def set_storage_levels(resource_type, level_counts: dict):
    """
    Перезаписывает уровни хранилищ в cache.json.
    """
    cache = load_cache()
    if "storage_levels" not in cache:
        cache["storage_levels"] = {}
    cache["storage_levels"][resource_type] = {str(k): int(v) for k, v in level_counts.items()}
    save_cache(cache)

def initialize_storage_cache():
    """
    Сканирует деревню, обновляет cache.json и позволяет вручную
    добавить недостающие шаблоны хранилищ, не выходя из программы.
    """
    IMAGE_DIR = "C:/farmbot/images/"
    while True:  # Главный цикл "скан → проверка → докинул → скан"
        screenshot_path = os.path.join(IMAGE_DIR, "village_snapshot.png")
        make_screenshot(region=None, filename=screenshot_path)
        screenshot = cv2.imread(screenshot_path)

        if screenshot is None:
            log("[ERROR] Скриншот деревни не загружен.")
            return

        detected = {"gold": {}, "elixir": {}}  # {level: count}

        min_distance = 20
        threshold = 0.89

        for file in os.listdir(IMAGE_DIR):
            if not file.endswith(".png"):  # Только png
                continue
            if "gold_storage_lvl" in file or "elixir_storage_lvl" in file:
                path = os.path.join(IMAGE_DIR, file)
                template = cv2.imread(path)
                if template is None:
                    continue

                res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                locs = np.where(res >= threshold)
                pts = list(zip(*locs[::-1]))
                if not pts:
                    continue

                level = int(file.split("lvl")[1].split("_")[0])
                rtype = "gold" if "gold" in file else "elixir"

                uniq = []
                for pt in pts:
                    if all(np.linalg.norm(np.array(pt) - np.array(p)) > min_distance for p in uniq):
                        uniq.append(pt)

                if uniq:
                    detected[rtype][level] = len(uniq)

        # ────────── Выводим результат скана
        for r in ("gold", "elixir"):
            if detected[r]:
                found = ", ".join(f"lvl{lvl}×{cnt}" for lvl, cnt in sorted(detected[r].items()))
                log(f"✅ Найдено {r}: {found}")
            else:
                log(f"❌ Не найдено ни одного {r}-хранилища")

        # ────────── Обновляем кэш хранилищ
        for r in ("gold", "elixir"):
            set_storage_levels(r, detected[r])

        # ────────── Проверяем пропуски
        missing = []
        for r in ("gold", "elixir"):
            available_lvls = {int(f.split("lvl")[1].split("_")[0])
                              for f in os.listdir(IMAGE_DIR)
                              if f.startswith(f"{r}_storage_lvl")}
            not_found = sorted(available_lvls - detected[r].keys())
            if not_found:
                missing.append((r, not_found))

        if not missing:
            log("🎉 Все уровни хранилищ, имеющиеся в images/, найдены. Продолжаем работу.")
            return

        for r, lvls in missing:
            lvls_txt = ", ".join(map(str, lvls))
            log(f"⚠️  Не найдены шаблоны/склады: {r} lvl {lvls_txt}")

        inp = input("\n➕ Добавьте недостающие шаблоны в папку images и нажмите Enter "
                    "для повторного сканирования (или введите 'skip' чтобы продолжить без них): ")
        if inp.strip().lower() == "skip":
            log("⏭ Пропускаем недостающие уровни и продолжаем работу.")
            return

def get_total_capacity(resource_type):
    storage_file = os.path.join(os.path.dirname(__file__), "storage_levels.json")

    with open(storage_file, "r", encoding="utf-8") as f:
        capacities = json.load(f)

    storage_data = get_cached_storage(resource_type)
    total = 0
    for level_str, count in storage_data.items():
        amount = capacities.get(f"{resource_type}_storage", {}).get(level_str, 0)
        total += int(amount) * int(count)
        log(f"[INFO] {count}x хранилище уровня {level_str} для {resource_type}: вместимость {amount}")

    townhall_level = get_townhall_level()
    if townhall_level:
        townhall_key = f"townhall_{resource_type}_storage"
        fallback_key = "townhall_storage"
        th_storage = capacities.get(townhall_key, {}).get(str(townhall_level)) or capacities.get(fallback_key, {}).get(str(townhall_level))
        if th_storage:
            total += int(th_storage)
            log(f"[INFO] Вместимость ратуши ({resource_type}): {th_storage}")

    return total

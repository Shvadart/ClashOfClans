# capacity_checker.py
"""
Модуль для работы с хранилищами ресурсов в игре. Функционал:
- Инициализация и обновление кеша хранилищ
- Сканирование деревни для обнаружения хранилищ
- Подсчет общей вместимости ресурсов
"""

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
    Полностью перезаписывает данные о хранилищах в кеш.
    
    Args:
        resource_type (str): Тип ресурса ('gold' или 'elixir')
        level_counts (dict): Словарь с количеством хранилищ по уровням
                            Пример: {11: 3, 12: 1} - 3 хранилища 11 уровня, 1 - 12 уровня
    """
    cache = load_cache()
    # Инициализируем структуру данных, если ее нет
    if "storage_levels" not in cache:
        cache["storage_levels"] = {}
    # Преобразуем ключи в строки и значения в int для JSON-совместимости
    cache["storage_levels"][resource_type] = {str(k): int(v) for k, v in level_counts.items()}
    save_cache(cache)

def initialize_storage_cache():
    """
    Основная функция инициализации кеша хранилищ.
    Выполняет последовательность:
    1. Делает скриншот деревни
    2. Ищет на нем хранилища по шаблонам
    3. Обновляет кеш
    4. Проверяет пропущенные уровни
    5. Позволяет добавить недостающие шаблоны
    """
    IMAGE_DIR = "C:/farmbot/images/"
    
    # Главный цикл сканирования
    while True:
        # 1. Создание скриншота деревни
        screenshot_path = os.path.join(IMAGE_DIR, "village_snapshot.png")
        make_screenshot(region=None, filename=screenshot_path)
        screenshot = cv2.imread(screenshot_path)

        if screenshot is None:
            log("[ERROR] Скриншот деревни не загружен.")
            return

        # 2. Поиск хранилищ на скриншоте
        detected = {"gold": {}, "elixir": {}}  # {level: count}
        
        # Параметры для matchTemplate
        min_distance = 20  # Минимальное расстояние между совпадениями (чтобы избежать дубликатов)
        threshold = 0.89   # Порог уверенности распознавания (0-1)

        # Перебираем все файлы шаблонов в директории
        for file in os.listdir(IMAGE_DIR):
            if not file.endswith(".png"):
                continue
                
            # Ищем только файлы шаблонов хранилищ
            if "gold_storage_lvl" in file or "elixir_storage_lvl" in file:
                path = os.path.join(IMAGE_DIR, file)
                template = cv2.imread(path)
                if template is None:
                    continue

                # Поиск совпадений шаблона на скриншоте
                res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                locs = np.where(res >= threshold)
                
                # Преобразование координат совпадений
                pts = list(zip(*locs[::-1]))
                if not pts:
                    continue

                # Извлекаем уровень и тип хранилища из имени файла
                level = int(file.split("lvl")[1].split("_")[0])
                rtype = "gold" if "gold" in file else "elixir"

                # Фильтрация дубликатов (близких совпадений)
                uniq = []
                for pt in pts:
                    if all(np.linalg.norm(np.array(pt) - np.array(p)) > min_distance for p in uniq):
                        uniq.append(pt)

                # Сохраняем количество уникальных совпадений
                if uniq:
                    detected[rtype][level] = len(uniq)

        # 3. Логирование результатов сканирования
        for r in ("gold", "elixir"):
            if detected[r]:
                found = ", ".join(f"lvl{lvl}×{cnt}" for lvl, cnt in sorted(detected[r].items()))
                log(f"✅ Найдено {r}: {found}")
            else:
                log(f"❌ Не найдено ни одного {r}-хранилища")

        # 4. Обновление кеша
        for r in ("gold", "elixir"):
            set_storage_levels(r, detected[r])

        # 5. Проверка пропущенных уровней
        missing = []
        for r in ("gold", "elixir"):
            # Получаем все доступные уровни из имен файлов
            available_lvls = {int(f.split("lvl")[1].split("_")[0])
                              for f in os.listdir(IMAGE_DIR)
                              if f.startswith(f"{r}_storage_lvl")}
            # Находим уровни, которые есть в шаблонах, но не найдены на скриншоте
            not_found = sorted(available_lvls - detected[r].keys())
            if not_found:
                missing.append((r, not_found))

        # Если все найдено - выходим
        if not missing:
            log("🎉 Все уровни хранилищ, имеющиеся в images/, найдены. Продолжаем работу.")
            return

        # Логируем пропущенные уровни
        for r, lvls in missing:
            lvls_txt = ", ".join(map(str, lvls))
            log(f"⚠️  Не найдены шаблоны/склады: {r} lvl {lvls_txt}")

        # 6. Запрос на добавление недостающих шаблонов
        inp = input("\n➕ Добавьте недостающие шаблоны в папку images и нажмите Enter "
                   "для повторного сканирования (или введите 'skip' чтобы продолжить без них): ")
        if inp.strip().lower() == "skip":
            log("⏭ Пропускаем недостающие уровни и продолжаем работу.")
            return

def get_total_capacity(resource_type):
    """
    Вычисляет общую вместимость хранилищ указанного типа ресурсов.
    Учитывает:
    - Хранилища разных уровней
    - Вместимость ратуши
    
    Args:
        resource_type (str): Тип ресурса ('gold' или 'elixir')
    
    Returns:
        int: Общая вместимость всех хранилищ данного типа ресурсов
    """
    # Загрузка данных о вместимости хранилищ
    storage_file = os.path.join(os.path.dirname(__file__), "storage_levels.json")
    with open(storage_file, "r", encoding="utf-8") as f:
        capacities = json.load(f)

    # Получаем данные о хранилищах из кеша
    storage_data = get_cached_storage(resource_type)
    total = 0
    
    # Суммируем вместимость всех хранилищ
    for level_str, count in storage_data.items():
        amount = capacities.get(f"{resource_type}_storage", {}).get(level_str, 0)
        total += int(amount) * int(count)
        log(f"[INFO] {count}x хранилище уровня {level_str} для {resource_type}: вместимость {amount}")

    # Добавляем вместимость ратуши
    townhall_level = get_townhall_level()
    if townhall_level:
        # Пробуем разные ключи для поиска данных
        townhall_key = f"townhall_{resource_type}_storage"
        fallback_key = "townhall_storage"
        th_storage = (capacities.get(townhall_key, {}).get(str(townhall_level)) or 
                     capacities.get(fallback_key, {}).get(str(townhall_level)))
        
        if th_storage:
            total += int(th_storage)
            log(f"[INFO] Вместимость ратуши ({resource_type}): {th_storage}")

    return total
"""
Модуль управления улучшениями зданий. Функционал:
- Приоритетное улучшение зданий
- Добавление новых зданий для улучшения
- Проверка доступности улучшений
- Взаимодействие с JSON-хранилищами данных
"""

import json
import os

# Константы путей к файлам данных
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILDINGS_PATH = os.path.join(BASE_DIR, "buildings.json")  # Основной файл с данными зданий
NEW_BUILDINGS_PATH = os.path.join(BASE_DIR, "new_buildings.json")  # Файл для новых зданий

from utils import find_and_click
from resources import get_resources
from logger import log
from decorators import with_resource_collection
from cache import update_storage_level

@with_resource_collection
def try_upgrade_prioritized():
    """
    Пытается улучшить здания в порядке приоритета.
    
    Returns:
        bool: True если улучшение выполнено, False если улучшать нечего
        
    Алгоритм:
    1. Проверяет наличие незавершенных улучшений
    2. Если все улучшено - предлагает добавить новое здание
    3. Перебирает здания в порядке приоритета
    4. Пытается улучшить первое доступное
    """
    with open(BUILDINGS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Проверяем, все ли улучшения завершены
    all_done = True
    for item in data:
        if not item.get("done", False):
            all_done = False
            break

    if all_done:
        log("🎉 Все улучшения завершены! Пора добавить новое улучшение.")
        # Запрашиваем данные для нового здания
        new_building = prompt_for_new_building()
        if new_building:
            add_new_building_to_json(new_building)
        return False

    # Перебираем здания для улучшения
    for item in data:
        # Поддержка нескольких изображений для одного здания
        image_paths = item.get("names", [item["name"]])  
        for image_path in image_paths:
            if upgrade_building(image_path):
                return True
    return False

def prompt_for_new_building():
    """
    Запрашивает у пользователя данные для нового здания.
    
    Returns:
        dict: Словарь с данными нового здания или None если ввод отменен
        
    Данные включают:
    - Название изображения
    - Стоимость в ресурсах
    - Время улучшения
    - Тип здания
    - Статус выполнения
    """
    print("\nДобавление нового здания для улучшения:")
    name = input("Введите название скриншота здания (например, 'elixir_collector_lvl1.png'): ")
    gold_cost = int(input("Введите стоимость в золоте: "))
    elixir_cost = int(input("Введите стоимость в эликсире: "))
    upgrade_time = int(input("Введите время улучшения в секундах: "))
    building_type = input("Введите тип здания (storage/defense/troop/resource): ")
    done = input("Здание уже улучшено? (да/нет): ").strip().lower() == 'да'

    return {
        "name": name,
        "gold": gold_cost,
        "elixir": elixir_cost,
        "upgrade_time": upgrade_time,
        "type": building_type,
        "done": done,
        "level": 1  # Новые здания всегда начинаются с 1 уровня
    }

def add_new_building_to_json(new_building):
    """
    Добавляет новое здание в файл new_buildings.json.
    
    Args:
        new_building (dict): Данные нового здания
        
    Создает файл если он не существует.
    """
    if not os.path.exists(NEW_BUILDINGS_PATH):
        with open(NEW_BUILDINGS_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    with open(NEW_BUILDINGS_PATH, "r", encoding="utf-8") as f:
        new_data = json.load(f)

    new_data.append(new_building)

    with open(NEW_BUILDINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)

    log(f"Добавлено новое здание: {new_building}")

def get_cost_from_data(image_name):
    """
    Получает стоимость улучшения и тип здания по имени изображения.
    
    Args:
        image_name (str): Имя файла изображения здания
        
    Returns:
        tuple: (gold_cost, elixir_cost, building_type, full_image_path)
    """
    with open(NEW_BUILDINGS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        # Проверка на соответствие имени файла
        if any(image_name.endswith(path) for path in item.get("names", [item["name"]])):
            return (
                item.get("gold", 0), 
                item.get("elixir", 0), 
                item.get("type"), 
                item["name"]
            )
    
    log(f"Здание {image_name} не найдено. Добавьте его в new_buildings.json")
    return 0, 0, None, image_name

def can_upgrade(image_name):
    """
    Проверяет, достаточно ли ресурсов для улучшения здания.
    
    Args:
        image_name (str): Путь к изображению здания
        
    Returns:
        bool: True если ресурсов достаточно, иначе False
    """
    gold, elixir = get_resources()
    cost = get_cost_from_data(os.path.basename(image_name))
    return gold >= cost[0] and elixir >= cost[1]

def upgrade_building(image_name):
    """
    Выполняет улучшение указанного здания.
    
    Args:
        image_name (str): Путь к изображению здания
        
    Returns:
        bool: True если улучшение выполнено, иначе False
    """
    gold_cost, elixir_cost, building_type, full_image_path = get_cost_from_data(
        os.path.basename(image_name)
    )
    gold, elixir = get_resources()

    if gold >= gold_cost and elixir >= elixir_cost:
        log(f"Улучшаем: {os.path.basename(image_name)}")
        if find_and_click(image_name):
            log("Улучшение начато")
            # Обновляем кэш для хранилищ
            if building_type == "storage":
                resource_type = "gold" if gold_cost > 0 else "elixir"
                update_storage_level(resource_type, 1)
            return True
        else:
            log("Не удалось кликнуть по зданию")
    else:
        log(f"Не хватает ресурсов для {os.path.basename(image_name)}")
    return False

def get_upgradable_buildings(townhall_level, gold, elixir, gold_cap, elixir_cap, storage_only=False):
    """
    Получает список доступных для улучшения зданий.
    
    Args:
        townhall_level (int): Уровень ратуши
        gold (int): Текущее золото
        elixir (int): Текущий эликсир
        gold_cap (int): Вместимость золота
        elixir_cap (int): Вместимость эликсира
        storage_only (bool): Только хранилища
        
    Returns:
        list: Список доступных для улучшения зданий
    """
    with open(BUILDINGS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    buildings_for_level = data.get(str(townhall_level), [])

    result = []
    for item in buildings_for_level:
        if item.get("done"):
            continue

        if storage_only and item.get("type") != "storage":
            continue

        g = item.get("gold", 0)
        e = item.get("elixir", 0)

        # Добавляем если хватает ресурсов ИЛИ если нужно увеличить хранилища
        if gold >= g and elixir >= e:
            result.append(item)
        elif g > gold_cap or e > elixir_cap:
            result.append(item)

    return result
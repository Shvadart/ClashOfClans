
import json
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILDINGS_PATH = os.path.join(BASE_DIR, "buildings.json")
NEW_BUILDINGS_PATH = os.path.join(BASE_DIR, "new_buildings.json")
from utils import find_and_click
from resources import get_resources
from logger import log
from decorators import with_resource_collection
from cache import update_storage_level


@with_resource_collection
def try_upgrade_prioritized():
    with open(BUILDINGS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_done = True
    for item in data:
        if not item.get("done", False):
            all_done = False
            break  # Есть хотя бы одно не завершённое улучшение, продолжаем

    if all_done:
        log("🎉 Все улучшения завершены! Пора добавить новое улучшение.")
        # Запрашиваем данные для следующего здания
        new_building = prompt_for_new_building()
        if new_building:
            add_new_building_to_json(new_building)
        return False  # Прерываем цикл улучшений, так как все завершены

    for item in data:
        image_paths = item.get("names", [item["name"]])  # Работаем с несколькими шаблонами
        for image_path in image_paths:
            if upgrade_building(image_path):
                return True
    return False


def prompt_for_new_building():
    """
    Запрашивает у пользователя данные для следующего здания и возвращает их как словарь.
    """
    name = input("Введите название скриншота здания (например, 'elixir_collector_lvl1.png'): ")
    gold_cost = int(input("Введите стоимость в золоте: "))
    elixir_cost = int(input("Введите стоимость в эликсире: "))
    upgrade_time = int(input("Введите время улучшения в секундах: "))
    building_type = input("Введите тип здания (например, 'storage', 'defense', 'troop', и т.д.): ")
    done = input("Здание уже улучшено? (да/нет): ").strip().lower() == 'да'

    return {
        "name": name,
        "gold": gold_cost,
        "elixir": elixir_cost,
        "upgrade_time": upgrade_time,
        "type": building_type,
        "done": done,
        "level": 1  # Устанавливаем уровень всегда 1 для новых зданий
    }


def add_new_building_to_json(new_building):
    """
    Добавляет новое здание в new_buildings.json.
    """
    if not os.path.exists("new_buildings.json"):
        with open(NEW_BUILDINGS_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    with open(NEW_BUILDINGS_PATH, "r", encoding="utf-8") as f:
        new_data = json.load(f)

    new_data.append(new_building)

    with open(NEW_BUILDINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)

    log(f"Новый элемент добавлен в new_buildings.json: {new_building}")


def get_cost_from_data(image_name):
    # Теперь проверяем в new_buildings.json для новых зданий
    with open(NEW_BUILDINGS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        if any(image_name.endswith(path) for path in item.get("names", [item["name"]])):  # Проверка на несколько путей
            return item.get("gold", 0), item.get("elixir", 0), item.get("type"), item["name"]
    
    # Если здание не найдено в new_buildings.json, выводим информацию для добавления
    log(f"Здание {image_name} не найдено в new_buildings.json. Пожалуйста, добавьте его.")
    return 0, 0, None, image_name


def can_upgrade(image_name):
    gold, elixir = get_resources()
    cost = get_cost_from_data(os.path.basename(image_name))
    return gold >= cost[0] and elixir >= cost[1]


def upgrade_building(image_name):
    gold_cost, elixir_cost, building_type, full_image_path = get_cost_from_data(os.path.basename(image_name))
    gold, elixir = get_resources()

    if gold >= gold_cost and elixir >= elixir_cost:
        log(f"Улучшаем здание: {image_name}")
        if find_and_click(image_name):
            log("Клик выполнен успешно.")
            # Обновляем кэш хранилищ
            if building_type == "storage":
                resource_type = "gold" if gold_cost > 0 else "elixir"
                update_storage_level(resource_type, 1)  # Теперь всегда первый уровень
            return True
        else:
            log("Клик не сработал.")
    else:
        log(f"Недостаточно ресурсов для улучшения: {image_name}")
    return False


def get_upgradable_buildings(townhall_level, gold, elixir, gold_cap, elixir_cap, storage_only=False):
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

        if gold >= g and elixir >= e:
            result.append(item)
        elif g > gold_cap or e > elixir_cap:
            result.append(item)

    return result



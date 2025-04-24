# upgrade.py
from utils import find_and_click
from resources import get_resources
from logger import log
import json
import os

COSTS = {
    "townhall_lvl1.png": (200, 0),
    "gold_storage_lvl1.png": (1000, 0),
    # Добавьте остальные здания и их стоимости
}

def can_upgrade(image_name):
    gold, elixir = get_resources()
    cost = COSTS.get(image_name, (0, 0))
    return gold >= cost[0] and elixir >= cost[1]

def upgrade_building(image_name):
    if can_upgrade(image_name):
        log(f"Улучшаем здание: {image_name}")
        if find_and_click(image_name):
            log("Клик выполнен успешно.")
            return True
        else:
            log("Клик не сработал.")
    else:
        log(f"Недостаточно ресурсов для улучшения: {image_name}")
    return False
def try_upgrade_prioritized(townhall_level):
    with open("buildings.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    buildings = data.get(str(townhall_level), [])
    for item in buildings:
        image_path = item["name"]
        if upgrade_building(image_path):
            return True

    return False

def get_upgradable_buildings(townhall_level, gold, elixir, gold_cap, elixir_cap, storage_only=False):
    path = os.path.join(os.path.dirname(__file__), "buildings.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    buildings = data.get(str(townhall_level), [])
    result = []
    for item in buildings:
        if item.get("done"):
            continue

        if storage_only and item.get("type") != "storage":
            continue

        g = item.get("gold", 0)
        e = item.get("elixir", 0)

        if gold >= g and elixir >= e:
            result.append(item)
        elif g > gold_cap or e > elixir_cap:
            result.append(item)  # можно улучшить, но хранилища не позволяют

    return result

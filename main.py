from resources import get_resources, get_townhall_level
from capacity_checker import get_total_capacity, initialize_storage_cache
from upgrade import get_upgradable_buildings
from upgrade_controller import upgrade_then_build
from attack import auto_attack
from logger import log
from builder_status import builders_busy
import time

def farm_until_full():
    while True:
        gold, elixir, _ = get_resources()
        gold_cap = get_total_capacity("gold")
        elixir_cap = get_total_capacity("elixir")

        if gold >= gold_cap and elixir >= elixir_cap:
            log("🧺 Хранилища заполнены. Останавливаем фарм.")
            break

        log("⚔️ Хранилища не полные. Запускаем атаку для фарма...")
        success = auto_attack()

        if not success:
            log("⚠️ Атака не удалась. Повтор через 10 сек...")
            time.sleep(10)

def main():
    import os
    print("[DEBUG] Текущая рабочая директория:", os.getcwd())
    log("📊 Анализ ресурсов и построек...")

    # 🔄 Обновляем кэш хранилищ каждый раз при запуске
    log("🔄 Обновляем кэш хранилищ...")
    initialize_storage_cache()

    townhall_level = get_townhall_level()
    gold, elixir, _ = get_resources()
    gold_cap = get_total_capacity("gold")
    elixir_cap = get_total_capacity("elixir")

    upgradable = get_upgradable_buildings(townhall_level, gold, elixir, gold_cap, elixir_cap)

    if upgradable:
        log("🛠 Найдены здания для улучшения.")
        upgrade_then_build()
    else:
        log("❌ Нет доступных улучшений. Проверяем причины...")

        possible_upgrades = get_upgradable_buildings(townhall_level, 9999999, 9999999, gold_cap, elixir_cap)
        if possible_upgrades:
            log("📦 Требуется увеличить хранилища.")
            upgrade_then_build(storage_only=True)
        else:
            if builders_busy():
                log("⛏ Все строители заняты.")
                farm_until_full()
            else:
                log("⚔️ Недостаточно ресурсов — идём в бой.")
                auto_attack()

if __name__ == "__main__":
    main()

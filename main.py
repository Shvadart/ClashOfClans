# main.py
"""
Главный модуль игрового бота. Содержит основную логику работы:
- Управление ресурсами
- Принятие решений о строительстве/апгрейде
- Организацию цикла фарма
- Координацию всех подсистем
"""

from resources import get_resources, get_townhall_level
from capacity_checker import get_total_capacity, initialize_storage_cache
from upgrade import get_upgradable_buildings
from upgrade_controller import upgrade_then_build
from attack import auto_attack
from logger import log
from builder_status import builders_busy
import time

def farm_until_full():
    """
    Цикл фарма ресурсов до заполнения хранилищ.
    Выполняет атаки, пока не будет достигнут максимальный уровень ресурсов.
    """
    while True:
        # Получаем текущее количество ресурсов
        gold, elixir, _ = get_resources()
        
        # Получаем максимальную вместимость хранилищ
        gold_cap = get_total_capacity("gold")
        elixir_cap = get_total_capacity("elixir")

        # Условие выхода из цикла - хранилища заполнены
        if gold >= gold_cap and elixir >= elixir_cap:
            log("🧺 Хранилища заполнены. Останавливаем фарм.")
            break

        log("⚔️ Хранилища не полные. Запускаем атаку для фарма...")
        success = auto_attack()

        # Если атака не удалась - пауза перед повторной попыткой
        if not success:
            log("⚠️ Атака не удалась. Повтор через 10 сек...")
            time.sleep(10)

def main():
    """
    Основная функция бота. Выполняет:
    1. Инициализацию и диагностику
    2. Принятие решений о действиях
    3. Организацию рабочих процессов
    """
    # Диагностика: вывод рабочей директории
    import os
    print("[DEBUG] Текущая рабочая директория:", os.getcwd())
    log("📊 Анализ ресурсов и построек...")

    # 1. Обновление кэша хранилищ (актуальные данные о вместимости)
    log("🔄 Обновляем кэш хранилищ...")
    initialize_storage_cache()

    # 2. Получение текущего состояния
    townhall_level = get_townhall_level()  # Уровень ратуши
    gold, elixir, _ = get_resources()  # Текущие ресурсы
    gold_cap = get_total_capacity("gold")  # Вместимость золота
    elixir_cap = get_total_capacity("elixir")  # Вместимость эликсира

    # 3. Поиск доступных для улучшения зданий
    upgradable = get_upgradable_buildings(townhall_level, gold, elixir, gold_cap, elixir_cap)

    if upgradable:
        # 4. Если есть что улучшать - запускаем процесс улучшения
        log("🛠 Найдены здания для улучшения.")
        upgrade_then_build()
    else:
        # 5. Если улучшать нечего - анализируем причины
        log("❌ Нет доступных улучшений. Проверяем причины...")

        # Проверяем, есть ли вообще доступные улучшения при максимальных ресурсах
        possible_upgrades = get_upgradable_buildings(townhall_level, 9999999, 9999999, gold_cap, elixir_cap)
        
        if possible_upgrades:
            # 6. Если улучшения есть, но не хватает ресурсов - улучшаем хранилища
            log("📦 Требуется увеличить хранилища.")
            upgrade_then_build(storage_only=True)
        else:
            if builders_busy():
                # 7. Если все строители заняты - фармим ресурсы
                log("⛏ Все строители заняты.")
                farm_until_full()
            else:
                # 8. Если строители свободны, но улучшать нечего - идем в бой
                log("⚔️ Недостаточно ресурсов — идём в бой.")
                auto_attack()

if __name__ == "__main__":
    """
    Точка входа при запуске скрипта напрямую.
    """
    main()
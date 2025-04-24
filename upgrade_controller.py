# upgrade_controller.py

import time
from upgrade import try_upgrade_prioritized
from builder import build_new_structure
from builder_status import wait_for_free_builder
from utils import find_and_click
from logger import log
from collect import collect_resources_if_visible

def try_speedup_if_possible():
    if find_and_click("C:/farmbot/images/speedup_gem.png"):
        log("💨 Найдена кнопка ускорения.")
        time.sleep(1)
        if find_and_click("C:/farmbot/images/use_gems.png"):
            log("✅ Ускорение успешно применено.")
            return True
        else:
            log("⚠️ Кнопка 'Использовать' не найдена.")
    else:
        log("⏳ Кнопка ускорения не найдена.")
    return False

def upgrade_then_build():
    # 💰 Попытка собрать ресурсы перед действиями
    collect_resources_if_visible()

    log("🔁 Начинаем приоритетные улучшения...")
    any_upgraded = False

    while True:
        collect_resources_if_visible()  # ещё раз перед каждым поиском

        success = try_upgrade_prioritized()
        if success:
            log("✅ Улучшено здание.")
            any_upgraded = True
            if not try_speedup_if_possible():
                wait_for_free_builder()
            time.sleep(2)
        else:
            log("⏹ Больше нечего улучшать.")
            break

    log("🏗 Переходим к строительству новых зданий...")
    collect_resources_if_visible()

    build_success = build_new_structure()
    if build_success:
        if not try_speedup_if_possible():
            wait_for_free_builder()

    if not build_success and not any_upgraded:
        log("ℹ️ Нет действий для выполнения.")
    else:
        log("✅ Цикл улучшения/строительства завершён.")

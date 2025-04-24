# test_prioritized_upgrade.py

from resources import get_townhall_level
from upgrade import try_upgrade_prioritized
from logger import log

if __name__ == "__main__":
    log("=== Тест приоритетного улучшения по уровню ТХ ===")

    level = get_townhall_level()
    if not level:
        log("❌ Уровень ратуши не найден.")
    else:
        log(f"🏰 Уровень ратуши: TH{level}")
        upgraded = try_upgrade_prioritized(level)
        if upgraded:
            log("✅ Улучшение выполнено.")
        else:
            log("❌ Не удалось выполнить улучшение.")

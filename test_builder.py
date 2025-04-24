# test_builder.py
from builder import build_new_structure
from upgrade_controller import try_speedup_if_possible
from logger import log

if __name__ == "__main__":
    log("=== Тест строительства нового здания ===")
    success = build_new_structure()

    if success:
        log("✅ Здание построено. Пробуем ускорить за гемы...")
        try_speedup_if_possible()
    else:
        log("❌ Тест не пройден: не удалось построить здание.")

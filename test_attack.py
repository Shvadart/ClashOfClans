# test_attack.py
import time
from attack import auto_attack
from logger import log # type: ignore

if __name__ == "__main__":
    log("=== Тест автоатаки ===")
    time.sleep(5)
    success = auto_attack()
    if success:
        log("✅ Атака завершена успешно.")
    else:
        log("❌ Атака не удалась.")

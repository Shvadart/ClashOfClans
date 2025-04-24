import pyautogui
import time

# ================== CONFIGURATION ==================
IMAGE_DIR = "images/"
# Включить использование гемов для ускорения строительства
USE_GEMS = True

TEMPLATES = {
    "collect": "collect.png",
    "clan_castle": "clan_castle.png",
    # Обновление
    "townhall_1": "townhall_lvl1.png",
    "townhall_2": "townhall_lvl2.png",
    "townhall_3": "townhall_lvl3.png",
    "townhall_4": "townhall_lvl4.png",
    "townhall_5": "townhall_lvl5.png",
    "townhall_6": "townhall_lvl6.png",
    # Хранилища
    "gold_storage_1": "gold_storage_lvl1.png",
    "gold_storage_2": "gold_storage_lvl2.png",
    "gold_storage_3": "gold_storage_lvl3.png",
    "elixir_storage_1": "elixir_storage_lvl1.png",
    "elixir_storage_2": "elixir_storage_lvl2.png",
    
    # Атака
    "barracks": "barracks.png",
    "barbarian": "barbarian.png",
    "army_ok": "army_ok.png",
    "attack": "attack.png",
    "next": "next.png",
    "deploy_barbarian": "deploy_barbarian.png",

    # Ускорение
    "speedup": "speedup.png",            # Иконка ускорения по гемам
    "speedup_confirm": "speedup_confirm.png"  # Кнопка подтверждения использования гемов
}

CONFIDENCE = 0.8
PAUSE_SHORT = 2
PAUSE_LONG = 5

# ====================================================

def find_and_click(key, confidence=CONFIDENCE, pause=PAUSE_SHORT, region=None):
    path = IMAGE_DIR + TEMPLATES[key]
    location = pyautogui.locateOnScreen(path, confidence=confidence, region=region)
    if location:
        x, y = pyautogui.center(location)
        pyautogui.moveTo(x, y)
        pyautogui.click()
        print(f"[{time.strftime('%H:%M:%S')}] Clicked '{key}'")
        time.sleep(pause)
        return True
    return False


def use_gems_to_speedup():
    """
    Использует гемы для ускорения текущего улучшения, не покупая ресурсы.
    """
    if not USE_GEMS:
        return
    print(f"[{time.strftime('%H:%M:%S')}] Пробуем ускорить постройку по гемам")
    # Ищем иконку ускорения
    if find_and_click("speedup", pause=PAUSE_SHORT):
        # Подтверждаем использование
        if find_and_click("speedup_confirm", pause=PAUSE_SHORT):
            print(f"[{time.strftime('%H:%M:%S')}] Постройка ускорена по гемам")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Не удалось подтвердить ускорение")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] Нет возможности ускорить")


def try_upgrade_building(templates_prefixes):
    # Пытаемся найти и кликнуть шаблоны по префиксу (уровни)
    for key in templates_prefixes:
        if key in TEMPLATES and find_and_click(key, pause=PAUSE_LONG):
            # После старта улучшения — ускоряем постройку
            use_gems_to_speedup()
            return True
    return False


def auto_attack():
    print(f"[{time.strftime('%H:%M:%S')}] Запуск атаки")
    if not find_and_click("attack", pause=PAUSE_LONG):
        print("Не удалось найти кнопку атаки")
        return
    if find_and_click("barracks"):
        for _ in range(10):
            if not find_and_click("barbarian", pause=0.5): break
        find_and_click("army_ok")
    time.sleep(PAUSE_LONG)
    find_and_click("next")
    for _ in range(10):
        if not find_and_click("deploy_barbarian", confidence=0.6, pause=0.1): break
    time.sleep(60)
    print(f"[{time.strftime('%H:%M:%S')}] Атака завершена")


def main():
    print("Переключитесь на окно эмулятора в течение 5 секунд...")
    time.sleep(5)
    print("Бот запущен")

    # Ключи для обновления
    townhall_keys = [f"townhall_{lvl}" for lvl in range(1, 7)]
    gold_keys = [f"gold_storage_{lvl}" for lvl in range(1, 4)]
    elixir_keys = [f"elixir_storage_{lvl}" for lvl in range(1, 3)]

    while True:
        if find_and_click("collect"): continue
        if find_and_click("clan_castle"): continue
        if try_upgrade_building(townhall_keys): continue
        if try_upgrade_building(gold_keys): continue
        if try_upgrade_building(elixir_keys): continue
        auto_attack()
        print(f"[{time.strftime('%H:%M:%S')}] Перерыв перед следующей итерацией...")
        time.sleep(10)

if __name__ == "__main__":
    main()

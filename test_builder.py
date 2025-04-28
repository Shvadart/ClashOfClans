# test_builder.py
from builder import build_new_structure
from logger import log
from utils import find_on_screen
from resources import get_townhall_level
import time

def live_test():
    """Интерактивный тест строительства в реальной игре"""
    log("\n=== ТЕСТ СТРОИТЕЛЬСТВА В РЕАЛЬНОЙ ИГРЕ ===")
    log("Перед началом убедитесь, что:")
    log("1. Игра запущена на главном экране деревни")
    log("2. У вас есть свободный строитель")
    log("3. Достаточно ресурсов для постройки")
    
    input("\nНажмите Enter когда будете готовы...")
    
    log("\n1. Тестируем открытие меню строителя")
    input("Убедитесь что курсор не перекрывает иконку строителя. Нажмите Enter...")
    
    log("\n2. Тестируем поиск новых зданий")
    log("Проверьте что в меню есть доступные для постройки здания")
    input("Нажмите Enter чтобы начать поиск 'Нового'...")
    
    log("\n3. Тестируем определение зданий")
    log("Бот будет пытаться определить здание по шаблонам")
    input("Нажмите Enter чтобы продолжить...")
    
    log("\n4. Тестируем размещение здания")
    log("Бот попытается разместить выбранное здание")
    input("Нажмите Enter для запуска финальной стадии...")
    
    start_time = time.time()
    result = build_new_structure()
    elapsed = time.time() - start_time
    
    log(f"\nРезультат теста: {'УСПЕХ' if result else 'НЕ УДАЛОСЬ'}")
    log(f"Время выполнения: {elapsed:.1f} секунд")
    
    if result:
        log("\nПроверьте в игре - новое здание должно быть размещено")
    else:
        log("\nПроверьте логи чтобы определить на каком этапе произошла ошибка")

def step_by_step_test():
    """Пошаговый тест с ручным подтверждением"""
    log("\n=== ПОШАГОВЫЙ ТЕСТ ===")
    
    steps = [
        ("Открытие меню строителя", "builder_icon.png"),
        ("Поиск новых зданий", ["new1.png", "new2.png", "new3.png"]),
        ("Проверка хижины строителя", "builder_hut_label.png"),
        ("Поиск стрелки", ["arrow1.png", "arrow2.png"]),
        ("Подтверждение строительства", "green_check.png")
    ]
    
    for desc, images in steps:
        log(f"\nШАГ: {desc}")
        if isinstance(images, list):
            log(f"Ищем: {', '.join(images)}")
        else:
            log(f"Ищем: {images}")
        
        input("Нажмите Enter когда будете готовы к проверке...")
        
        # Эмуляция работы builder.py
        if isinstance(images, list):
            found = False
            for img in images:
                if find_on_screen(f"C:/farmbot/images/{img}"):
                    log(f"Найдено: {img}")
                    found = True
                    break
            if not found:
                log("Ни один элемент не найден")
        else:
            if find_on_screen(f"C:/farmbot/images/{images}"):
                log("Элемент найден")
            else:
                log("Элемент не найден")

def resource_check_test():
    """Тест проверки ресурсов"""
    log("\n=== ТЕСТ ПРОВЕРКИ РЕСУРСОВ ===")
    from resources import get_resources
    
    gold, elixir, dark = get_resources()
    log(f"Текущие ресурсы: Золото={gold}, Эликсир={elixir}, Тёмный={dark}")
    
    townhall = get_townhall_level()
    log(f"Уровень ратуши: {townhall}")
    
    # Проверка соответствия зданий
    import json
    with open("new_buildings.json", "r") as f:
        buildings = json.load(f).get(str(townhall), [])
    
    log("\nДоступные для постройки здания:")
    for b in buildings:
        affordable = ""
        if gold >= b.get("gold", 0) and elixir >= b.get("elixir", 0):
            affordable = " (ДОСТУПНО)"
        log(f"- {b['names'][0]}: {b.get('gold', 0)} золота, {b.get('elixir', 0)} эликсира{affordable}")

if __name__ == "__main__":
    print("Выберите тип теста:")
    print("1. Полный тест строительства")
    print("2. Пошаговый тест элементов")
    print("3. Проверка ресурсов")
    
    choice = input("Ваш выбор (1-3): ")
    
    if choice == "1":
        live_test()
    elif choice == "2":
        step_by_step_test()
    elif choice == "3":
        resource_check_test()
    else:
        print("Некорректный выбор")
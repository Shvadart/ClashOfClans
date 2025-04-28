# test_collect.py
from collect import collect_resources_if_visible
from logger import log
import time
import os

def live_collection_test():
    """Тест сбора ресурсов в реальной игре"""
    log("\n=== ТЕСТ СБОРА РЕСУРСОВ ===")
    log("Перед началом убедитесь, что:")
    log("1. Игра Clash of Clans запущена")
    log("2. На экране есть собираемые ресурсы (полные шахты/хранилища)")
    log("3. Окно игры активно и не перекрыто другими окнами")
    
    input("\nНажмите Enter когда будете готовы...")
    
    log("\nСобираем ресурсы (3 попытки с разными параметрами)...")
    for attempt in range(1, 4):
        log(f"\nПопытка {attempt}:")
        start_time = time.time()
        result = collect_resources_if_visible()
        elapsed = time.time() - start_time
        
        if result:
            log(f"✅ Успешно! Время: {elapsed:.2f} сек")
            log("Проверьте в игре - ресурсы должны быть собраны")
        else:
            log(f"❌ Не удалось собрать. Время: {elapsed:.2f} сек")
            log("Проверьте скриншот в папке debug/")
        
        if attempt < 3:
            input("Измените положение ресурсов и нажмите Enter для следующей попытки...")

def image_validator():
    """Проверка шаблонов изображений"""
    log("\n=== ПРОВЕРКА ШАБЛОНОВ ===")
    images = [
        "collect_gold.png",
        "collect_elixir.png",
        "collect_gold_d.png",
        "collect_elixir_s.png",
        "collect_gold_sv.png",
        "collect_elixir_svs.png"
    ]
    
    missing = []
    for img in images:
        path = os.path.join("C:/farmbot/images/", img)
        if os.path.exists(path):
            log(f"✅ {img} - найден")
        else:
            log(f"❌ {img} - отсутствует")
            missing.append(img)
    
    if missing:
        log("\nВНИМАНИЕ: Отсутствуют следующие файлы изображений:")
        for img in missing:
            log(f"- {img}")
        log("\nДобавьте их в папку C:/farmbot/images/ для полной функциональности")

def main_menu():
    while True:
        log("\n=== ТЕСТ МОДУЛЯ COLLECT ===")
        log("1. Тест сбора ресурсов")
        log("2. Проверка шаблонов изображений")
        log("3. Выход")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            live_collection_test()
        elif choice == "2":
            image_validator()
        elif choice == "3":
            break
        else:
            log("Некорректный выбор, попробуйте again")

if __name__ == "__main__":
    log("=== ТЕСТИРОВАНИЕ СБОРА РЕСУРСОВ ===")
    try:
        main_menu()
    except KeyboardInterrupt:
        log("\nТестирование прервано пользователем")
    except Exception as e:
        log(f"Ошибка: {str(e)}")
    
    log("\nТестирование завершено. Проверьте логи для анализа результатов.")
# test_capacity_checker.py
import os
import time
from capacity_checker import *
from logger import log
from cache import CACHE_FILE

def print_storage_status():
    """Выводит текущее состояние хранилищ"""
    log("\nТекущие уровни хранилищ:")
    for res_type in ["gold", "elixir"]:
        levels = get_cached_storage(res_type)
        if levels:
            log(f"{res_type}:")
            for lvl, count in levels.items():
                log(f"  Уровень {lvl}: {count} шт")
        else:
            log(f"{res_type}: данные отсутствуют")

def test_initial_scan():
    """Тестирование первоначального сканирования"""
    log("\n=== ТЕСТ СКАНИРОВАНИЯ ХРАНИЛИЩ ===")
    log("Перед началом убедитесь, что:")
    log("1. Игра открыта на главном экране деревни")
    log("2. Все хранилища видны на экране")
    log("3. В папке images/ есть шаблоны gold_storage_lvlX.png и elixir_storage_lvlX.png")
    
    input("\nНажмите Enter чтобы начать сканирование...")
    
    start_time = time.time()
    initialize_storage_cache()
    elapsed = time.time() - start_time
    
    log(f"\nСканирование завершено за {elapsed:.1f} сек")
    print_storage_status()

def test_manual_update():
    """Тестирование ручного обновления уровней"""
    log("\n=== ТЕСТ РУЧНОГО ОБНОВЛЕНИЯ ===")
    
    print_storage_status()
    
    while True:
        res_type = input("\nВведите тип ресурса (gold/elixir): ").strip().lower()
        if res_type not in ["gold", "elixir"]:
            log("❌ Неверный тип ресурса")
            continue
            
        level = input("Введите уровень хранилища: ")
        count = input("Введите количество: ")
        
        try:
            levels = {level: count}
            set_storage_levels(res_type, levels)
            log(f"✅ Обновлено: {res_type} уровень {level} = {count} шт")
        except Exception as e:
            log(f"❌ Ошибка: {str(e)}")
        
        print_storage_status()
        
        if input("\nПродолжить (y/n)? ").strip().lower() != 'y':
            break

def test_capacity_calculation():
    """Тестирование расчета вместимости"""
    log("\n=== ТЕСТ РАСЧЕТА ВМЕСТИМОСТИ ===")
    
    print_storage_status()
    
    for res_type in ["gold", "elixir"]:
        log(f"\nРасчет для {res_type}:")
        capacity = get_total_capacity(res_type)
        log(f"Общая вместимость: {capacity}")

def main_menu():
    while True:
        log("\n=== ТЕСТ МОДУЛЯ CAPACITY_CHECKER ===")
        log("1. Тест сканирования хранилищ")
        log("2. Тест ручного обновления")
        log("3. Тест расчета вместимости")
        log("4. Просмотр текущих данных")
        log("5. Выход")
        
        choice = input("Выберите тест: ").strip()
        
        if choice == "1":
            test_initial_scan()
        elif choice == "2":
            test_manual_update()
        elif choice == "3":
            test_capacity_calculation()
        elif choice == "4":
            print_storage_status()
        elif choice == "5":
            break
        else:
            log("❌ Неверный выбор")

if __name__ == "__main__":
    log("=== ТЕСТИРОВАНИЕ МОДУЛЯ CAPACITY_CHECKER ===")
    log(f"Файл кэша: {os.path.abspath(CACHE_FILE)}")
    
    try:
        main_menu()
    except KeyboardInterrupt:
        log("\nТестирование прервано")
    except Exception as e:
        log(f"❌ Ошибка: {str(e)}")
    
    log("\nТестирование завершено. Проверьте файлы:")
    log(f"→ Кэш: {os.path.abspath(CACHE_FILE)}")
    log(f"→ Шаблоны хранилищ: C:/farmbot/images/gold_storage_lvl*.png")
    log(f"→ Шаблоны хранилищ: C:/farmbot/images/elixir_storage_lvl*.png")
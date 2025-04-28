# test_cache.py
import os
import time
from cache import *
from logger import log

def print_cache():
    """Выводит текущее содержимое кэша"""
    log("\nТекущее содержимое кэша:")
    cache = load_cache()
    for key, value in cache.items():
        if key == "storage_levels":
            log("\nУровни хранилищ:")
            for res_type, levels in value.items():
                log(f"  {res_type}:")
                for lvl, count in levels.items():
                    log(f"    Уровень {lvl}: {count} шт")
        else:
            log(f"{key}: {value}")

def test_townhall_cache():
    """Тестирование кэширования уровня ратуши"""
    log("\n=== ТЕСТ КЭША РАТУШИ ===")
    
    current = get_cached_townhall()
    log(f"Текущий уровень в кэше: {current}")
    
    if current is not None:
        log("\n1. Тестируем обновление уровня")
        new_level = input(f"Введите новый уровень ратуши (текущий {current}): ")
        set_townhall(int(new_level))
    else:
        log("\n1. Тестируем первое сохранение")
        new_level = input("Введите уровень ратуши: ")
        set_townhall(int(new_level))
    
    log("\nПроверяем обновление...")
    updated = get_cached_townhall()
    log(f"Новый уровень в кэше: {updated}")
    print_cache()

def test_storage_cache():
    """Тестирование кэширования хранилищ"""
    log("\n=== ТЕСТ КЭША ХРАНИЛИЩ ===")
    
    resource_types = ["gold", "elixir", "dark_elixir"]
    log("Доступные типы ресурсов: gold, elixir, dark_elixir")
    
    while True:
        print_cache()
        log("\n1. Добавить уровень хранилища")
        log("2. Выйти в меню")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            res_type = input("Тип ресурса (gold/elixir/dark_elixir): ")
            if res_type not in resource_types:
                log("❌ Неверный тип ресурса")
                continue
            
            level = input("Уровень хранилища: ")
            try:
                update_storage_level(res_type, int(level))
                log(f"✅ Добавлено {res_type} уровень {level}")
            except ValueError:
                log("❌ Уровень должен быть числом")
        elif choice == "2":
            break

def stress_test():
    """Тест производительности и надежности"""
    log("\n=== ТЕСТ НАГРУЗКИ ===")
    
    iterations = 10
    log(f"Выполняем {iterations} циклов записи...")
    
    start_time = time.time()
    for i in range(1, iterations+1):
        set_townhall(i % 15 + 1)  # уровни 1-15
        update_storage_level("gold", i % 10 + 1)
        update_storage_level("elixir", i % 10 + 1)
        if i % 3 == 0:
            update_storage_level("dark_elixir", i % 5 + 1)
    
    elapsed = time.time() - start_time
    log(f"Готово! Время выполнения: {elapsed:.2f} сек")
    log(f"Среднее время операции: {(elapsed/iterations)*1000:.2f} мс")
    print_cache()

def cleanup_test():
    """Тест очистки кэша"""
    log("\n=== ТЕСТ ОЧИСТКИ ===")
    
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        log("Файл кэша удален")
    else:
        log("Файл кэша не существует")
    
    log("Проверяем загрузку пустого кэша...")
    empty_cache = load_cache()
    log(f"Результат: {empty_cache}")

def main_menu():
    while True:
        log("\n=== ТЕСТ КЭШИРОВАНИЯ ===")
        log("1. Тест кэша ратуши")
        log("2. Тест кэша хранилищ")
        log("3. Нагрузочный тест")
        log("4. Тест очистки")
        log("5. Просмотр кэша")
        log("6. Выход")
        
        choice = input("Выберите тест: ")
        
        if choice == "1":
            test_townhall_cache()
        elif choice == "2":
            test_storage_cache()
        elif choice == "3":
            stress_test()
        elif choice == "4":
            cleanup_test()
        elif choice == "5":
            print_cache()
        elif choice == "6":
            break
        else:
            log("❌ Неверный выбор")

if __name__ == "__main__":
    log("=== ТЕСТИРОВАНИЕ МОДУЛЯ CACHE ===")
    log(f"Файл кэша: {CACHE_FILE}")
    
    try:
        main_menu()
    except KeyboardInterrupt:
        log("\nТестирование прервано")
    except Exception as e:
        log(f"❌ Ошибка: {str(e)}")
    
    log("\nТестирование завершено. Проверьте файл кэша:")
    log(f"→ {os.path.abspath(CACHE_FILE)}")
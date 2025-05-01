# cache.py
"""
Модуль для работы с кешированием данных игры.
Реализует сохранение и загрузку данных в JSON-файл.
Хранит информацию о:
- Уровне ратуши
- Уровнях хранилищ ресурсов
- Времени последнего обновления
"""

import json
import os
from datetime import datetime

# Константы модуля
CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache.json")  # Путь к файлу кеша

def load_cache():
    """
    Загружает данные из кеш-файла.
    
    Returns:
        dict: Словарь с данными кеша. Пустой словарь, если файл не существует.
    """
    # Проверяем существование файла перед загрузкой
    if not os.path.exists(CACHE_FILE):
        return {}  # Возвращаем пустой словарь, если файла нет
    
    # Открываем файл для чтения с указанием кодировки UTF-8
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)  # Загружаем и возвращаем данные JSON

def save_cache(data):
    """
    Сохраняет данные в кеш-файл с обновлением метки времени.
    
    Args:
        data (dict): Словарь с данными для сохранения
    """
    # Добавляем/обновляем метку времени последнего обновления
    data["last_update"] = datetime.now().isoformat()
    
    # Сохраняем данные с форматированием
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data, 
            f, 
            ensure_ascii=False,  # Для корректного сохранения Unicode
            indent=2  # Отступы для читаемости файла
        )

def get_cached_townhall():
    """
    Получает сохраненный уровень ратуши из кеша.
    
    Returns:
        int or None: Уровень ратуши или None, если не сохранен
    """
    cache = load_cache()
    return cache.get("townhall_level")  # Используем .get() для безопасного доступа

def set_townhall(level):
    """
    Устанавливает уровень ратуши в кеш.
    
    Args:
        level (int): Уровень ратуши для сохранения
    """
    cache = load_cache()
    cache["townhall_level"] = level  # Устанавливаем значение
    save_cache(cache)  # Сохраняем обновленный кеш

def get_cached_storage(resource_type):
    """
    Получает данные о хранилищах определенного типа ресурсов.
    
    Args:
        resource_type (str): Тип ресурса ('gold', 'elixir' и т.д.)
    
    Returns:
        dict: Словарь с уровнями хранилищ и их количеством. 
              Пример: {'1': 2, '2': 1} - два хранилища 1 уровня, одно 2 уровня
    """
    cache = load_cache()
    # Возвращаем данные по типу ресурса или пустой словарь
    return cache.get("storage_levels", {}).get(resource_type, {})

def update_storage_level(resource_type, level):
    """
    Обновляет информацию о хранилище в кеше.
    Увеличивает счетчик хранилищ указанного уровня.
    
    Args:
        resource_type (str): Тип ресурса ('gold', 'elixir' и т.д.)
        level (int): Уровень хранилища
    """
    cache = load_cache()
    
    # Инициализируем структуру данных, если ее нет
    if "storage_levels" not in cache:
        cache["storage_levels"] = {}
    if resource_type not in cache["storage_levels"]:
        cache["storage_levels"][resource_type] = {}

    # Получаем текущее количество хранилищ этого уровня
    count = cache["storage_levels"][resource_type].get(str(level), 0)
    # Увеличиваем счетчик и сохраняем
    cache["storage_levels"][resource_type][str(level)] = count + 1
    save_cache(cache)
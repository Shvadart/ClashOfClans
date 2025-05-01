# upgrade_controller.py
"""
Модуль управления улучшениями и строительством в игре. Функционал:
1. Приоритетное улучшение существующих зданий
2. Строительство новых сооружений
3. Ускорение процессов за самоцветы
4. Координация действий строителей
"""

import time
from upgrade import try_upgrade_prioritized
from builder import build_new_structure
from builder_status import wait_for_free_builder
from utils import find_and_click
from logger import log
from collect import collect_resources_if_visible

def try_speedup_if_possible():
    """
    Пытается ускорить текущее строительство/улучшение за самоцветы.
    
    Returns:
        bool: True если ускорение успешно применено, иначе False
        
    Процесс:
    1. Ищет кнопку ускорения
    2. Подтверждает использование самоцветов
    3. Логирует результат операции
    """
    # Поиск и нажатие кнопки ускорения
    if find_and_click("C:/farmbot/images/speedup_gem.png"):
        log("💨 Найдена кнопка ускорения.")
        time.sleep(1)  # Пауза для появления диалога подтверждения
        
        # Подтверждение использования самоцветов
        if find_and_click("C:/farmbot/images/use_gems.png"):
            log("✅ Ускорение успешно применено.")
            return True
        else:
            log("⚠️ Кнопка 'Использовать' не найдена.")
    else:
        log("⏳ Кнопка ускорения не найдена.")
    return False

def upgrade_then_build():
    """
    Основной цикл улучшения и строительства. Выполняет:
    1. Сбор доступных ресурсов
    2. Приоритетное улучшение зданий
    3. Строительство новых сооружений
    4. Управление строителями
    
    Логика работы:
    - Сначала улучшает существующие здания (приоритет)
    - Затем строит новые (если есть возможность)
    - Автоматически использует ускорение при доступности
    - Ожидает свободных строителей при необходимости
    """
    # Первоначальный сбор ресурсов
    collect_resources_if_visible()

    log("🔁 Начинаем приоритетные улучшения...")
    any_upgraded = False  # Флаг успешного улучшения

    # Основной цикл улучшений
    while True:
        # Сбор ресурсов перед каждой итерацией
        collect_resources_if_visible()

        # Попытка улучшить приоритетное здание
        success = try_upgrade_prioritized()
        if success:
            log("✅ Улучшено здание.")
            any_upgraded = True
            
            # Пробуем ускорить, иначе ждем свободного строителя
            if not try_speedup_if_possible():
                wait_for_free_builder()
                
            time.sleep(2)  # Пауза между действиями
        else:
            log("⏹ Больше нечего улучшать.")
            break

    # Фаза строительства новых зданий
    log("🏗 Переходим к строительству новых зданий...")
    collect_resources_if_visible()

    # Попытка построить новое здание
    build_success = build_new_structure()
    if build_success:
        # Пробуем ускорить или ждем строителя
        if not try_speedup_if_possible():
            wait_for_free_builder()

    # Логирование итогов
    if not build_success and not any_upgraded:
        log("ℹ️ Нет действий для выполнения.")
    else:
        log("✅ Цикл улучшения/строительства завершён.")
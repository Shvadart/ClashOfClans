# make_screenshot.py
"""
Модуль для создания и сохранения скриншотов экрана.
Функционал:
- Создание скриншотов указанной области экрана
- Автоматическое создание директории для сохранения
- Сохранение с указанным именем файла
"""

import os
import pyautogui

def make_screenshot(region=None, filename='screenshot.png'):
    """
    Создает и сохраняет скриншот указанной области экрана.

    Args:
        region (tuple, optional): Область для скриншота в формате (x, y, width, height).
                                Если None - захватывает весь экран. По умолчанию None.
        filename (str): Имя файла для сохранения. По умолчанию 'screenshot.png'.

    Returns:
        str: Абсолютный путь к сохраненному файлу скриншота

    Raises:
        OSError: Если возникли проблемы с созданием директории или сохранением файла
        pyautogui.ImageNotFoundException: Если не удалось сделать скриншот
    """
    # Получаем абсолютный путь к директории скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Создаем папку screenshots, если ее нет (в той же директории, где находится скрипт)
    save_dir = os.path.join(script_dir, 'screenshots')
    os.makedirs(save_dir, exist_ok=True)  # exist_ok=True предотвращает ошибку если папка уже существует

    # Формируем полный путь для сохранения скриншота
    screenshot_path = os.path.join(save_dir, filename)
    
    try:
        # Делаем скриншот указанной области
        screenshot = pyautogui.screenshot(region=region)
        
        # Сохраняем скриншот в файл
        screenshot.save(screenshot_path)
        
        return screenshot_path
        
    except Exception as e:
        # Перехватываем возможные ошибки и добавляем информативности
        error_msg = f"Ошибка при создании скриншота: {str(e)}"
        raise type(e)(error_msg) from e
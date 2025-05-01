# utils.py
"""
Модуль вспомогательных функций для работы с интерфейсом игры. Функционал:
- Создание скриншотов для отладки
- Поиск и взаимодействие с элементами интерфейса
- Работа с геометрическими областями
- Управление мышью (клики, перемещения)
"""

import pyautogui
import time
import random
import os
from config import IMAGE_DIR, CONFIDENCE, PAUSE_SHORT
from logger import log

def debug_screenshot(region=None):
    """
    Создает и сохраняет скриншот для отладки.
    
    Args:
        region (tuple, optional): Область для скриншота (x, y, width, height). 
                               Если None - скриншот всего экрана.
                               
    Returns:
        str or None: Путь к сохраненному файлу или None при ошибке
    """
    debug_dir = os.path.join(IMAGE_DIR, "debug")
    os.makedirs(debug_dir, exist_ok=True)  # Создаем папку, если не существует
    
    # Генерируем имя файла с временной меткой
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(debug_dir, f"debug_{timestamp}.png")
    
    try:
        # Делаем скриншот указанной области или всего экрана
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return path
    except Exception as e:
        log(f"[ERROR] Не удалось сохранить скриншот: {str(e)}")
        return None

def find_and_click(
    image_name, 
    pause=PAUSE_SHORT, 
    confidence=None, 
    retry=2,
    silent_errors=False,
    silent_all=False,
    region=None
):
    """
    Находит изображение на экране и кликает по нему.
    
    Args:
        image_name (str): Путь к изображению (абсолютный или относительный)
        pause (float): Пауза после клика (секунды)
        confidence (float): Уровень уверенности распознавания (0-1)
        retry (int): Количество попыток поиска
        silent_errors (bool): Не логировать ошибки
        silent_all (bool): Полное отключение логов
        region (tuple): Область поиска (x, y, width, height)
        
    Returns:
        bool: True если клик выполнен успешно
    """
    # Устанавливаем уровень уверенности по умолчанию
    if confidence is None:
        confidence = CONFIDENCE
        
    # Обрабатываем абсолютные и относительные пути
    if os.path.isabs(image_name):
        path = image_name
    else:
        path = os.path.join(IMAGE_DIR, image_name)

    # Проверяем существование файла изображения
    if not os.path.exists(path):
        if not silent_all:
            log(f"[ERROR] Файл изображения не найден: {path}")
        return False

    # Цикл попыток поиска и клика
    for attempt in range(retry + 1):
        try:
            # Поиск изображения в указанной области или на всем экране
            if region:
                screenshot = pyautogui.screenshot(region=region)
                location = pyautogui.locate(path, screenshot, confidence=confidence)
            else:
                location = pyautogui.locateOnScreen(path, confidence=confidence)
            
            if location:
                x, y, w, h = location
                
                # Вычисляем случайную точку внутри найденной области
                if region:
                    # Корректируем координаты с учетом области поиска
                    rand_x = region[0] + random.randint(x + 5, x + w - 5)
                    rand_y = region[1] + random.randint(y + 5, y + h - 5)
                else:
                    rand_x = random.randint(x + 5, x + w - 5)
                    rand_y = random.randint(y + 5, y + h - 5)
                
                # Выполняем клик с небольшой случайной задержкой
                pyautogui.moveTo(rand_x, rand_y)
                pyautogui.click()
                time.sleep(pause + random.uniform(0.1, 0.4))
                return True
            
            # Логирование при последней неудачной попытке
            if attempt == retry and not silent_all:
                debug_path = debug_screenshot()
                if not silent_errors:
                    log(f"[DEBUG] Изображение не найдено: {os.path.basename(path)}")
                    if region:
                        log(f"[DEBUG] Поиск в регионе: {region}")
                log(f"[DEBUG] Скриншот сохранен: {debug_path}")
                
        except Exception as e:
            # Обработка ошибок с учетом настроек логирования
            if not silent_all:
                if not silent_errors:
                    log(f"[ERROR] Ошибка при поиске изображения: {str(e)}")
                if attempt == retry:
                    debug_path = debug_screenshot()
                    log(f"[DEBUG] Скриншот сохранен: {debug_path}")
        
        # Пауза между попытками (кроме последней)
        if attempt < retry:
            time.sleep(1)
    
    return False

def random_point_in_parallelogram(A, B, D):
    """
    Генерирует случайную точку внутри параллелограмма.
    
    Args:
        A (tuple): Координаты первой вершины (x, y)
        B (tuple): Координаты второй вершины (x, y)
        D (tuple): Координаты четвертой вершины (x, y)
        
    Returns:
        tuple: Случайные координаты (x, y) внутри параллелограмма
    """
    # Векторы сторон параллелограмма
    AB = (B[0] - A[0], B[1] - A[1])
    AD = (D[0] - A[0], D[1] - A[1])
    
    # Генерируем случайные коэффициенты
    u = random.random()
    v = random.random()
    
    # Вычисляем координаты точки
    x = int(A[0] + u * AB[0] + v * AD[0])
    y = int(A[1] + u * AB[1] + v * AD[1])
    return x, y

def click_random_in_parallelogram(zone):
    """
    Кликает в случайную точку внутри параллелограмма.
    
    Args:
        zone (tuple): Кортеж из трех точек (A, B, D) определяющих параллелограмм
    """
    A, B, D = zone
    x, y = random_point_in_parallelogram(A, B, D)
    pyautogui.click(x, y)

def hold_mouse_in_parallelogram(zone, hold_time=2.0):
    """
    Удерживает мышь в случайной точке параллелограмма.
    
    Args:
        zone (tuple): Кортеж из трех точек (A, B, D)
        hold_time (float): Время удержания в секундах
    """
    A, B, D = zone
    x, y = random_point_in_parallelogram(A, B, D)
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    time.sleep(hold_time)
    pyautogui.mouseUp()

def find_on_screen(image_path, confidence=CONFIDENCE, multiple=False, is_expected_fail=False):
    """
    Поиск изображения на экране с различными параметрами.
    
    Args:
        image_path (str): Путь к изображению
        confidence (float): Уровень уверенности распознавания
        multiple (bool): Поиск всех совпадений
        is_expected_fail (bool): Ожидается ли неудача (не логировать)
        
    Returns:
        list or tuple or None: Найденные позиции или None
    """
    if not os.path.exists(image_path):
        log(f"[WARN] Файл не найден: {image_path}")
        return None

    try:
        if multiple:
            return list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
        return pyautogui.locateOnScreen(image_path, confidence=confidence)
    except Exception as e:
        if not is_expected_fail:
            log(f"[DEBUG] Ошибка поиска {os.path.basename(image_path)}: {e}")
        return None

def find_any_and_click(image_paths, pause=PAUSE_SHORT):
    """
    Пытается найти и кликнуть по любому из переданных изображений.
    
    Args:
        image_paths (str or list): Одно или несколько изображений
        pause (float): Пауза после клика
        
    Returns:
        bool: True если хотя бы один клик выполнен
    """
    # Нормализуем входные данные к списку
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    for img in image_paths:
        if find_and_click(img, pause=pause):
            return True
    return False

def find_any_on_screen(image_paths, confidence=CONFIDENCE):
    """
    Ищет любое из переданных изображений на экране.
    
    Args:
        image_paths (str or list): Одно или несколько изображений
        confidence (float): Уровень уверенности
        
    Returns:
        str or None: Путь к найденному изображению или None
    """
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    for img in image_paths:
        if find_on_screen(img, confidence=confidence):
            return img  # Возвращаем путь к найденному изображению
    return None
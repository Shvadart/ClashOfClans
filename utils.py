# utils.py
import pyautogui
import time
import random
import os
from config import IMAGE_DIR, CONFIDENCE, PAUSE_SHORT
from logger import log

def debug_screenshot():
    """Сохраняет скриншот для отладки"""
    debug_dir = os.path.join(IMAGE_DIR, "debug")
    os.makedirs(debug_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(debug_dir, f"debug_{timestamp}.png")
    pyautogui.screenshot(path)
    return path

def find_and_click(image_name, pause=PAUSE_SHORT, confidence=None, retry=2):
    if confidence is None:
        confidence = CONFIDENCE
        
    if os.path.isabs(image_name):
        path = image_name
    else:
        path = os.path.join(IMAGE_DIR, image_name)

    if not os.path.exists(path):
        log(f"[ERROR] Файл изображения не найден: {path}")
        return False

    for attempt in range(retry + 1):
        try:
            location = pyautogui.locateOnScreen(path, confidence=confidence)
            if location:
                x, y, w, h = location
                rand_x = random.randint(x + 5, x + w - 5)
                rand_y = random.randint(y + 5, y + h - 5)
                pyautogui.moveTo(rand_x, rand_y)
                pyautogui.click()
                time.sleep(pause + random.uniform(0.1, 0.4))
                return True
            
            if attempt == retry:
                debug_path = debug_screenshot()
                log(f"[DEBUG] Изображение не найдено: {path} (попытка {attempt + 1}/{retry + 1})")
                log(f"[DEBUG] Скриншот сохранен: {debug_path}")
                
        except Exception as e:
            log(f"[ERROR] Ошибка при поиске изображения: {str(e)}")
            if attempt == retry:
                debug_path = debug_screenshot()
                log(f"[DEBUG] Скриншот сохранен: {debug_path}")
        
        time.sleep(1)  # Пауза между попытками
    
    return False


def random_point_in_parallelogram(A, B, D):
    AB = (B[0] - A[0], B[1] - A[1])
    AD = (D[0] - A[0], D[1] - A[1])
    u = random.random()
    v = random.random()
    x = int(A[0] + u * AB[0] + v * AD[0])
    y = int(A[1] + u * AB[1] + v * AD[1])
    return x, y

def click_random_in_parallelogram(zone):
    A, B, D = zone
    x, y = random_point_in_parallelogram(A, B, D)
    pyautogui.click(x, y)

def hold_mouse_in_parallelogram(zone, hold_time=2.0):
    """
    Зажимает мышку в случайной точке зоны на hold_time секунд
    """
    A, B, D = zone
    x, y = random_point_in_parallelogram(A, B, D)
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    time.sleep(hold_time)
    pyautogui.mouseUp()

def find_on_screen(image_path, confidence=CONFIDENCE, multiple=False):
    import pyautogui

    if not os.path.exists(image_path):
        log(f"[WARN] Файл не найден: {image_path}")
        return None

    try:
        if multiple:
            return list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
        return pyautogui.locateOnScreen(image_path, confidence=confidence)
    except Exception as e:
        log(f"[ERROR] Поиск изображения завершился с ошибкой: {e}")
        return None

def find_any_and_click(image_paths, pause=PAUSE_SHORT):
    """
    Принимает либо строку, либо list[str].
    Возвращает True, если хотя бы один шаблон найден и нажат.
    """
    # нормализуем к списку
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    for img in image_paths:
        if find_and_click(img, pause=pause):
            return True
    return False

def find_any_on_screen(image_paths, confidence=CONFIDENCE):
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    for img in image_paths:
        if find_on_screen(img, confidence=confidence):
            return img   # вернём путь, который сработал
    return None
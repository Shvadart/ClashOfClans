# utils.py
import pyautogui
import time
import random
import os
from config import IMAGE_DIR, CONFIDENCE, PAUSE_SHORT
from logger import log

def debug_screenshot(region=None):
    """Скриншот всей области или указанного региона"""
    debug_dir = os.path.join(IMAGE_DIR, "debug")
    os.makedirs(debug_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(debug_dir, f"debug_{timestamp}.png")
    
    try:
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
    """Версия с корректной обработкой region"""
    if confidence is None:
        confidence = CONFIDENCE
        
    if os.path.isabs(image_name):
        path = image_name
    else:
        path = os.path.join(IMAGE_DIR, image_name)

    if not os.path.exists(path):
        if not silent_all:
            log(f"[ERROR] Файл изображения не найден: {path}")
        return False

    for attempt in range(retry + 1):
        try:
            # Делаем скриншот области, если указан region
            if region:
                screenshot = pyautogui.screenshot(region=region)
                location = pyautogui.locate(path, screenshot, confidence=confidence)
            else:
                location = pyautogui.locateOnScreen(path, confidence=confidence)
            
            if location:
                x, y, w, h = location
                
                # Корректируем координаты для клика
                if region:
                    rand_x = region[0] + random.randint(x + 5, x + w - 5)
                    rand_y = region[1] + random.randint(y + 5, y + h - 5)
                else:
                    rand_x = random.randint(x + 5, x + w - 5)
                    rand_y = random.randint(y + 5, y + h - 5)
                
                pyautogui.moveTo(rand_x, rand_y)
                pyautogui.click()
                time.sleep(pause + random.uniform(0.1, 0.4))
                return True
            
            if attempt == retry and not silent_all:
                debug_path = debug_screenshot()
                if not silent_errors:
                    log(f"[DEBUG] Изображение не найдено: {os.path.basename(path)}")
                    if region:
                        log(f"[DEBUG] Поиск в регионе: {region}")
                log(f"[DEBUG] Скриншот сохранен: {debug_path}")
                
        except Exception as e:
            if not silent_all:
                if not silent_errors:
                    log(f"[ERROR] Ошибка при поиске изображения: {str(e)}")
                if attempt == retry:
                    debug_path = debug_screenshot()
                    log(f"[DEBUG] Скриншот сохранен: {debug_path}")
        
        if attempt < retry:
            time.sleep(1)
    
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

def find_on_screen(image_path, confidence=CONFIDENCE, multiple=False, is_expected_fail=False):
    """Поиск изображения на экране с управлением логированием ошибок"""
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
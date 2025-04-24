#utils.py
import pyautogui
import time
import random
import os
from config import IMAGE_DIR, CONFIDENCE, PAUSE_SHORT
from logger import log

def find_and_click(image_name, pause=PAUSE_SHORT):
    import random
    if os.path.isabs(image_name):
        path = image_name
    else:
        path = os.path.join(IMAGE_DIR, image_name)

    if not os.path.exists(path):
        print(f"[WARN] Файл не найден: {path}")
        return False

    location = pyautogui.locateOnScreen(path, confidence=CONFIDENCE)
    if location:
        x, y, w, h = location
        # Рандомный клик внутри найденного прямоугольника
        rand_x = random.randint(x + 5, x + w - 5)
        rand_y = random.randint(y + 5, y + h - 5)
        pyautogui.moveTo(rand_x, rand_y)
        pyautogui.click()
        time.sleep(pause + random.uniform(0.1, 0.4))  # дополнительная случайная задержка
        return True
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

    
# decorators.py
from functools import wraps
from collect import collect_resources_if_visible
from logger import log
from utils import debug_screenshot
import time

def with_resource_collection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            collect_resources_if_visible()
            time.sleep(0.5)  # Добавляем небольшую паузу после сбора
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            log("⏹ Сбор ресурсов прерван пользователем")
            raise
        except Exception as e:
            log(f"❌ Ошибка при сборе ресурсов: {str(e)}")
            debug_screenshot()
            raise
    return wrapper
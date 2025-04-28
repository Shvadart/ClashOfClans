# builder_status.py
import time
from utils import find_on_screen
from logger import log
from config import CONFIDENCE_BUILDER

IMAGE_DIR = "C:/farmbot/images/"

def get_builder_status():
    for status_img in ["0_2.png", "1_2.png", "2_2.png"]:
        found = find_on_screen(IMAGE_DIR + status_img, confidence=CONFIDENCE_BUILDER)
        if found:
            return status_img.replace(".png", "")
    return "unknown"

def wait_for_free_builder(timeout=300):
    """Ожидает, пока хотя бы один строитель освободится."""
    log("⏳ Ожидаем свободного строителя...")
    start = time.time()
    while time.time() - start < timeout:
        status = get_builder_status()
        if status in ["2_2", "1_2"]:  # Исправлено условие
            log(f"✅ Найден свободный строитель ({status})")
            return True
        time.sleep(5)
    log("❌ Строители не освободились в течение времени ожидания.")
    return False

def builders_busy():
    """Возвращает True, если все строители заняты, иначе False."""
    status = get_builder_status()
    return status == "0_2"  # Упрощенное и правильное условие
# builder_status.py
import time
from utils import find_on_screen
from logger import log

IMAGE_DIR = "C:/farmbot/images/"

def get_builder_status():
    """Возвращает '0_2', '1_2', '2_2' или 'unknown'."""
    for status_img in ["0_2.png", "1_2.png", "2_2.png"]:
        full_path = IMAGE_DIR + status_img
        if find_on_screen(full_path):
            return status_img.replace(".png", "")
    return "unknown"

def wait_for_free_builder(timeout=300):
    """Ожидает, пока хотя бы один строитель освободится."""
    log("⏳ Ожидаем свободного строителя...")
    start = time.time()
    while time.time() - start < timeout:
        status = get_builder_status()
        if status in ["0_2", "1_2"]:
            log(f"✅ Найден свободный строитель ({status})")
            return True
        time.sleep(5)
    log("❌ Строители не освободились в течение времени ожидания.")
    return False

def builders_busy():
    """Возвращает True, если все строители заняты, иначе False."""
    status = get_builder_status()
    return status not in ["1_2", "2_2"]  # т.е. ни один строитель не свободен


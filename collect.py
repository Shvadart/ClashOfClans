# collect.py
from utils import find_and_click
from logger import log
import time

def collect_resources_if_visible():
    collected = False
    for img in [
        "C:/farmbot/images/collect_gold.png",
        "C:/farmbot/images/collect_elixir.png"
    ]:
        if find_and_click(img):
            log(f"💰 Собраны ресурсы: {img}")
            time.sleep(0.5)
            collected = True
    return collected

# make_screenshot.py
import os
import pyautogui

def make_screenshot(region, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(script_dir, 'screenshots')
    os.makedirs(save_dir, exist_ok=True)

    screenshot_path = os.path.join(save_dir, filename)
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(screenshot_path)

    return screenshot_path

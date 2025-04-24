import os
import pyautogui

# Получите путь к директории, где находится скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))

# Определите путь к папке 'screenshots' внутри директории скрипта
save_dir = os.path.join(script_dir, 'screenshots')
os.makedirs(save_dir, exist_ok=True)

# Полный путь к файлу
#screenshot_path = os.path.join(save_dir, 'gold_region.png')
screenshot_path = os.path.join(save_dir, 'elixir_region.png')
# Сделать скриншот и сохранить его
#screenshot = pyautogui.screenshot(region=(1472, 70, 1712-1472, 112-70))
screenshot = pyautogui.screenshot(region=(1471, 166, 1714-1471, 199-166))
screenshot.save(screenshot_path)
print(f"Скриншот сохранён по пути: {screenshot_path}")
screenshot_path = os.path.join(save_dir, 'gold_region.png')
screenshot = pyautogui.screenshot(region=(1472, 70, 1712-1472, 112-70))
screenshot.save(screenshot_path)

print(f"Скриншот сохранён по пути: {screenshot_path}")

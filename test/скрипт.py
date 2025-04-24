import pyautogui
import time

print("Нажмите Ctrl+C для выхода.")
try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x} Y: {y}      ", end='\r')  # Добавлены пробелы
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nПрограмма завершена.")

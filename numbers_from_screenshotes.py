# numbers_from_screenshots.py
"""
Модуль для распознавания числовых значений с игровых скриншотов.
Использует OpenCV для обработки изображений и Tesseract OCR для распознавания текста.
Функционал:
- Извлечение чисел из изображений ресурсов (золото, эликсир, самоцветы)
- Предварительная обработка изображений для улучшения распознавания
- Отладка и валидация результатов
"""

import os
import cv2
import pytesseract
import numpy as np

# Конфигурация пути к Tesseract OCR (необходимо установить отдельно)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_number_from_image(filename, crop_right_half=False, debug_name="debug.png"):
    """
    Извлекает числовое значение с изображения ресурсов из игры.
    
    Args:
        filename (str): Имя файла изображения в папке screenshots
        crop_right_half (bool): Обрезать правую половину изображения перед обработкой
        debug_name (str): Имя файла для сохранения отладочного изображения
    
    Returns:
        int or None: Распознанное число или None при ошибке
    
    Обработка изображения включает:
    1. Загрузку и масштабирование изображения
    2. Обрезку (при необходимости)
    3. Фильтрацию по цвету (белые цифры)
    4. Бинаризацию и морфологические операции
    5. Поиск контуров цифр
    6. Распознавание с помощью Tesseract OCR
    """
    # Формирование полного пути к файлу изображения
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, 'screenshots', filename)

    # Проверка существования файла
    if not os.path.exists(image_path):
        print(f"Файл не найден: {image_path}")
        return None

    # 1. Загрузка и масштабирование изображения
    image = cv2.imread(image_path)
    image = cv2.resize(image, None, fx=2, fy=3, interpolation=cv2.INTER_CUBIC)

    # 2. Обрезка правой половины при необходимости
    if crop_right_half:
        height, width = image.shape[:2]
        image = image[:, width // 2:]

    # 3. Фильтрация по цвету (выделение белых цифр)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])  # Нижняя граница белого цвета в HSV
    upper_white = np.array([180, 60, 255])  # Верхняя граница белого цвета
    mask = cv2.inRange(hsv, lower_white, upper_white)
    result = cv2.bitwise_and(image, image, mask=mask)

    # 4. Подготовка к распознаванию
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh = cv2.bitwise_not(thresh)  # Инверсия цветов

    # Морфологическая операция для улучшения качества
    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # 5. Поиск контуров цифр
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    digit_regions = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # Фильтрация слишком маленьких областей
        if h > 10 and w > 5:
            digit_regions.append((x, y, w, h))

    if not digit_regions:
        print("Цифры не найдены.")
        return None

    # Объединение всех цифр в одну область
    digit_regions = sorted(digit_regions, key=lambda box: box[0])
    x_min = digit_regions[0][0]
    x_max = digit_regions[-1][0] + digit_regions[-1][2]
    y_min = min(box[1] for box in digit_regions)
    y_max = max(box[1] + box[3] for box in digit_regions)

    # Выделение области с цифрами
    roi = thresh[y_min:y_max, x_min:x_max]
    roi = cv2.copyMakeBorder(roi, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)

    # 6. Сохранение отладочного изображения
    cv2.imwrite(debug_name, roi)

    # Настройки Tesseract для распознавания цифр
    config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(roi, config=config)
    print(f"OCR результат ({debug_name}):", repr(text))

    # Преобразование распознанного текста в число
    try:
        return int(text.strip().replace(' ', '').replace(',', ''))
    except ValueError:
        print(f"Не удалось распознать число ({debug_name}): '{text.strip()}'")
        return 0

def get_all_resources():
    """
    Получает количество всех ресурсов из соответствующих скриншотов.
    
    Returns:
        tuple: (gold, elixir, gems) - количество каждого ресурса или None при ошибке
    
    Для каждого ресурса используется свой метод обработки:
    - Золото: полное изображение
    - Эликсир: правая половина изображения
    - Самоцветы: полное изображение
    """
    gold = extract_number_from_image('gold_region.png', crop_right_half=False, debug_name='debug_gold.png')
    elixir = extract_number_from_image('elixir_region.png', crop_right_half=True, debug_name='debug_elixir.png')
    gems = extract_number_from_image('gems_region.png', crop_right_half=False, debug_name='debug_gems.png')
    return gold, elixir, gems
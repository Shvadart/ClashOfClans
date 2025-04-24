import os
import cv2
import pytesseract
import numpy as np

# Укажи путь к tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_number_from_image(filename, crop_right_half=False, debug_name="debug.png"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, 'screenshots', filename)

    if not os.path.exists(image_path):
        print(f"Файл не найден: {image_path}")
        return None

    image = cv2.imread(image_path)
    image = cv2.resize(image, None, fx=2, fy=3, interpolation=cv2.INTER_CUBIC)

    if crop_right_half:
        height, width = image.shape[:2]
        image = image[:, width // 2:]  # оставляем правую половину

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 60, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    result = cv2.bitwise_and(image, image, mask=mask)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh = cv2.bitwise_not(thresh)

    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Поиск контуров и определение ROI
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    digit_regions = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > 10 and w > 5:  # фильтр от шума
            digit_regions.append((x, y, w, h))

    if not digit_regions:
        print("Цифры не найдены.")
        return None

    digit_regions = sorted(digit_regions, key=lambda box: box[0])
    x_min = digit_regions[0][0]
    x_max = digit_regions[-1][0] + digit_regions[-1][2]
    y_min = min(box[1] for box in digit_regions)
    y_max = max(box[1] + box[3] for box in digit_regions)

    roi = thresh[y_min:y_max, x_min:x_max]
    roi = cv2.copyMakeBorder(roi, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)

    # Отладка
    cv2.imshow("ROI", roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(debug_name, roi)

    config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(roi, config=config)
    print(f"OCR результат ({debug_name}):", repr(text))

    try:
        return int(text.strip().replace(' ', '').replace(',', ''))
    except ValueError:
        print(f"Не удалось распознать число ({debug_name}): '{text.strip()}'")
        return None


# Использование:
gold = extract_number_from_image('gold_region.png', crop_right_half=False, debug_name='debug_gold.png')
elixir = extract_number_from_image('elixir_region.png', crop_right_half=True, debug_name='debug_elixir.png')

print(f"Золото: {gold}")
print(f"Эликсир: {elixir}")

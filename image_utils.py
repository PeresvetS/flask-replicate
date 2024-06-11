from PIL import Image, ImageDraw, ImageFont
from flask import current_app as app
import os
import re

def add_footer_with_text_and_squares(image_path, colors_and_text):
    # Найти все цветовые кортежи
    colors = re.findall(r'\(\d{1,3}, \d{1,3}, \d{1,3}\)', colors_and_text)

    # Преобразовать строки с цветами в кортежи
    colors = [eval(color) for color in colors]

    # Найти текстовую часть
    text_match = re.search(r'[a-zA-Z]+.', colors_and_text)
    app.logger.error("{text_match}")
    test = text_match.group(1)
    app.logger.error("{test}")
    text = test.group(1).strip() if text_match else ""
    app.logger.error("{text}")
    
    # Получить базовый путь из переменной окружения
    base_path = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", "/app/data")

    # Полный путь к файлу
    full_image_path = os.path.join(base_path, image_path)

    # Проверка существования файла
    if not os.path.isfile(full_image_path):
        raise FileNotFoundError(f"No such file: '{full_image_path}'")

    # Открыть исходное изображение
    image = Image.open(full_image_path)
    width, height = image.size

    # Создать новое изображение с дополнительными 200 пикселями снизу
    new_height = height + 200
    new_image = Image.new('RGB', (width, new_height), (255, 255, 255))
    new_image.paste(image, (0, 0))

    # Создать объект для рисования
    draw = ImageDraw.Draw(new_image)

    # Задать параметры квадратов
    square_size = 100
    padding_right = 20
    positions = [(width - (3 * square_size + 2 * padding_right), height + 20),
                 (width - (2 * square_size + padding_right), height + 20),
                 (width - square_size, height + 20)]

    # Нарисовать квадраты
    for position, color in zip(positions, colors):
        draw.rectangle([position, (position[0] + square_size, position[1] + square_size)], fill=color)

    # Добавить текст
    font = ImageFont.load_default(size=45)
    text_position = (20, height + 40)  # Поднято вверх
    draw.text(text_position, text, fill=(0, 0, 0), font=font)

    # Сохранить новое изображение во временный файл
    temp_path = os.path.join(base_path, "temp_image.jpg")
    new_image.save(temp_path)

    # Переместить временный файл на место исходного
    os.replace(temp_path, full_image_path)
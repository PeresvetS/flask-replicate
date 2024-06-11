import os
from PIL import Image, ImageDraw, ImageFont

def add_footer_with_text_and_squares(image_path):
    # Открыть исходное изображение
    image = Image.open(image_path)
    width, height = image.size

    # Создать новое изображение с дополнительными 300 пикселями снизу
    new_height = height + 300
    new_image = Image.new('RGB', (width, new_height), (255, 255, 255))
    new_image.paste(image, (0, 0))

    # Создать объект для рисования
    draw = ImageDraw.Draw(new_image)

    # Задать параметры квадратов
    square_size = 50
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    positions = [(width - 160, height + 20), (width - 100, height + 20), (width - 40, height + 20)]

    # Нарисовать квадраты
    for position, color in zip(positions, colors):
        draw.rectangle([position, (position[0] + square_size, position[1] + square_size)], fill=color)

    # Добавить текст
    text = "Your Text Here"
    font = ImageFont.load_default()
    text_position = (20, height + 120)
    draw.text(text_position, text, fill=(0, 0, 0), font=font)

    # Сохранить новое изображение во временный файл
    temp_path = "temp_image.jpg"
    new_image.save(temp_path)

    # Переместить временный файл на место исходного
    os.replace(temp_path, image_path)

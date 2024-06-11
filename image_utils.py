from PIL import Image, ImageDraw, ImageFont
import os

def add_footer_with_text_and_squares(image_path):
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

    # Создать новое изображение с дополнительными 300 пикселями снизу
    new_height = height + 300
    new_image = Image.new('RGB', (width, new_height), (255, 255, 255))
    new_image.paste(image, (0, 0))

    # Создать объект для рисования
    draw = ImageDraw.Draw(new_image)

    # Задать параметры квадратов
    square_size = 100  # Увеличено в 2 раза
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    positions = [(20, height + 20), (140, height + 20), (260, height + 20)]  # Сдвинуто влево

    # Нарисовать квадраты
    for position, color in zip(positions, colors):
        draw.rectangle([position, (position[0] + square_size, position[1] + square_size)], fill=color)

    # Добавить текст
    text = "Your Text Here"
    font = ImageFont.truetype("arial.ttf", 72)  # Увеличено в 3 раза
    text_position = (20, height + 140)
    draw.text(text_position, text, fill=(0, 0, 0), font=font)

    # Сохранить новое изображение во временный файл
    temp_path = os.path.join(base_path, "temp_image.jpg")
    new_image.save(temp_path)

    # Переместить временный файл на место исходного
    os.replace(temp_path, full_image_path)

import os
import time
import random
import requests
from image_utils import add_footer_with_text_and_squares
from flask import Blueprint, request, jsonify, send_from_directory, current_app as app

make_archetype_img_blueprint = Blueprint('make_archetype_img', __name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SEGMIND_API_KEY = os.getenv("SEGMIND_API_KEY")
segmind_url = "https://api.segmind.com/v1/sdxl1.0-juggernaut-lightning"
save_path = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", "/app/data")

def get_openai_prompt(gender, archetype):

    openai_payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": f"Представь себя профессиональным ai-художников и промпт-инженером в Stable diffusion. Вот информация для определения архетипа (архетипов, не более 2). Варианты ответов: (1) Стремление к простоте и искренности (2) Поиск новых впечатлений и знаний (3) Стремление к мудрости и пониманию (4) Желание преодолевать препятствия и защищать других (5) Бунтарский дух и желание изменить мир (6) Стремление к трансформации и магии (7) Желание дружбы и поддержки других (8) Стремление к любви и романтике (9) Любовь к юмору и веселью (10) Желание служить и помогать другим (11) Творческое самовыражение (12) Стремление к лидерству и контролю // Мне важно: {archetype}  Сейчас определи мои главные 1 или 2 архетипа. // А это запросы для создания картинки в stable diffusion по 12 архетипам женщин и мужчин, разделённые нумерацией. Сначала я пишу название архетипа, а после тире пишу сам промпт. Для женщин: 1. Ruler — by Alphonse Mucha, (painting, drawing, line art: 2), modern beautiful girl ruler, owner, leader, power and strength, sitting on the throne, close-up, black dress, power, leadership and control, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, spectral texture, dreamy mood, 4k, hd, award winning art / 2. Magic — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful girl magician, magic, feminine, transformation, mystery, halo around the head, areola around the head, light comes from the eyes, purple, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 3. Hero —  by Alphonse Mucha, (painting, drawing, line art: 2), beautiful girl hero, close-up, warrior, feminine, adventures, bow and arrows, determination, red and blue color, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 4. Innocent — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful girl innocent, close-up, soft and nice, hope, gentle, chamomile behind the ear, feminine, light blue color, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 5. Creator — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful girl creator, close-up, face in paint, steampunk glasses, paint brush, steampunk clock, creative, glowing light bulbs, feminine, orange and yellow color, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 6. Caregiver — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful girl caregiver, close-up, kind, symbols of care, ambulance cross, protection and sympathy, soft blanket, first aid kit, feminine, pink and light blue color, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 7. Explorer —  by Alphonse Mucha, (painting, drawing, line art: 2), beautiful girl explorer, close-up, adventurer, feminine, green and brown color, compass, backpack, nature and freedom, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 8. Outlaw — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful girl outlaw, close-up, rebel, feminine, black and red color, motorcycle, leather jacket, independence and challenge, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 9. Lover by Alphonse Mucha, (painting, drawing, line art: 2), beautiful girl lover, close-up, passionate, feminine, red and pink color, rose, heart, romance and sensuality, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 10. Jester by Alphonse Mucha, (painting, drawing, line art: 2), beautiful girl jester, close-up, playful, feminine, yellow and orange color, jester's cap, comedic mask, humor and joy, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 11. Everyman — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful girl everyman, close-up, relatable, feminine, brown and green color, working gloves, mug, simplicity and honesty, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 12. Sage — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful girl sage, close-up, wise, feminine, blue and purple color, book, pince-nez, knowledge and wisdom, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art // для мужчин: 1. Ruler — by Alphonse Mucha, (painting, drawing, line art: 2), modern beautiful man ruler, owner, leader, power and strength, with crown on the head, close-up, black dress, power, leadership and control, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, spectral texture, dreamy mood, 4k, hd, award winning art / 2. Magician — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful man magician, magic, courageous and brutal, transformation, mystery, halo around the head, areola around the head, light comes from the eyes, purple, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 3. Hero — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful man hero, close-up, warrior, courageous and brutal, adventures, sword and shield, determination, red and blue color, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 4. Innocent — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful man innocent, close-up, soft and nice, hope, gentle, chamomile behind the ear, courageous and brutal, light blue color, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 5. Creator — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful man creator, close-up, face in paint, steampunk glasses, paint brush, steampunk clock, creative, glowing light bulbs, courageous and brutal, orange and yellow color, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 6. Caregiver — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful man caregiver, close-up, kind, symbols of care, ambulance cross, protection and sympathy, soft blanket, first aid kit, courageous and brutal, pink and light blue color, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 7. Explorer — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful man explorer, close-up, adventurer, courageous and brutal, green and brown color, compass, backpack, nature and freedom, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 8. Outlaw — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful man outlaw, close-up, rebel, courageous and brutal, black and red color, motorcycle, leather jacket, independence and challenge, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 9. Lover — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful man lover, close-up, passionate, sexy, courageous and brutal, red and pink color, rose in pocket, heart, romance and sensuality, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 10. Jester — by Alphonse Mucha, (painting, drawing, line art: 2), beautiful man jester, close-up, playful, courageous and brutal, yellow and orange color, jester's cap, comedic mask, humor and joy, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 11. Everyman -- by Alphonse Mucha, (painting, drawing, line art: 2), beautiful man everyman, close-up, relatable, courageous and brutal, brown and green color, working gloves, mug, simplicity and honesty, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art / 12. Sage -- by Alphonse Mucha, (painting, drawing, line art: 2), beautiful man sage, close-up, wise, courageous and brutal, blue and purple color, book, glasses, knowledge and wisdom, futuristic, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), elegant, highly detailed, spectral texture, dreamy mood, 4k, hd, award winning art // на основе примеров, чётко придерживаясь структуре, создай запрос для {gender} пола архетипа(ов), который(ые) ты опредил. Если я указал 2 архетипа, создай мне запрос более длинный, в который будут включены 2-3 цвета, 3-5 качества и 2-3 атрибуты обоих архетипов. Пиши только сам запрос без заголовка и без дополнительных слов. Я буду благодарен за отличный результат, это важно для меня. Я дам $1000000 чаевых за хороший результат." }
        ]
    }

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", json=openai_payload, headers=headers)
        response.raise_for_status()
        openai_response = response.json()
        prompt = openai_response['choices'][0]['message']['content']
        return prompt
    except requests.RequestException as e:
        app.logger.error(f"Request to OpenAI failed: {e}")
        return None

def generate_image(prompt):
    segmind_payload = {
        "prompt": prompt,
        "negative_prompt": "(deformed, distorted, disfigured:1.3), (ugly mutated hands and fingers:2), extra finger, wrong hands anatomy, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, NSFW, low contrast, text, BadDream, 3d, fake, anime, open mouth, big forehead, long neck",
        "samples": 1,
        "scheduler": "Euler",
        "num_inference_steps": 7,
        "guidance_scale": 2,
        "seed": random.randint(1, 9999999999),
        "img_width": 1024,
        "img_height": 1024,
        "base64": False
    }

    headers = {
        'x-api-key': SEGMIND_API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(segmind_url, json=segmind_payload, headers=headers)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        app.logger.error(f"Request to Segmind failed: {e}")
        return None

def save_image(image):
    file_name = f"generated_archetype_image_{int(time.time())}.jpg"
    file_path = os.path.join(save_path, file_name)

    try:
        with open(file_path, "wb") as f:
            f.write(image)
        return file_name
    except IOError as e:
        app.logger.error(f"Failed to save image: {e}")
        return None

@make_archetype_img_blueprint.route('/make_archetype_img', methods=['POST'])
def make_archetype_img():
    data = request.json
    gender = data.get("gender")
    archetype = data.get("archetype")

    if not gender or not archetype:
        app.logger.error("Invalid input data")
        return jsonify({"error": "Invalid input data"}), 400

    if 'X-Auth-Code' not in request.headers or request.headers['X-Auth-Code'] != os.getenv('API_SECRET_CODE'):
        return jsonify({"error": "Unauthorized"}), 401

    prompt = get_openai_prompt(gender, archetype)
    if not prompt:
        return jsonify({"error": "Failed to generate prompt"}), 500

    image = generate_image(prompt)
    if not image:
        return jsonify({"error": "Failed to generate image"}), 500

    file_name = save_image(image)
    if not file_name:
        return jsonify({"error": "Failed to save image"}), 500
    
    add_footer_with_text_and_squares(file_name)

    return jsonify({"image_url": f"/data/{file_name}"})

@make_archetype_img_blueprint.route('/data/<path:filename>')
def serve_file(filename):
    return send_from_directory(save_path, filename)

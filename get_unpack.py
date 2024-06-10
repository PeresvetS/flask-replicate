import os
import requests
from flask import Blueprint, request, jsonify, current_app as app

get_unpack_blueprint = Blueprint('get_unpack', __name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_openai_prompt():
    data = request.json
    gender = data.get("gender")
    archetype = data.get("archetype")
    birthday = data.get("birthday")
    perception = data.get("perception")
    decision = data.get("decision")
    profession = data.get("profession")
    audience = data.get("audience")

    openai_payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": f"Представь себя профессиональным продюсером для экспертов с 10 летним успешным опытом. Ты профессионал в психологии личности и эзотерике, и хорошо работаешь с соционикой, матрицей судьбы и 12 архетипами по Юнгу. Твоя цель - сделать мне экспертную распаковку и анализ личности, чтобы я мог определиться с позиционированием. Отвечай мне развёрнуто, не менее 5 000 символов в ответе. Вот параметры по мне: 1. Дата рождения {birthday} (для определения характеристик личности по матрице судьбы) и мой пол {gender} 2. Информация для определения архетипа (архетипов, не более 3). Варианты ответов: (1) Стремление к простоте и искренности (2) Поиск новых впечатлений и знаний (3) Стремление к мудрости и пониманию (4) Желание преодолевать препятствия и защищать других (5) Бунтарский дух и желание изменить мир (6) Стремление к трансформации и магии (7) Желание дружбы и поддержки других (8) Стремление к любви и романтике (9) Любовь к юмору и веселью (10) Желание служить и помогать другим (11) Творческое самовыражение (12) Стремление к лидерству и контролю // Мне важно: {archetype}.  3. Информация для определения соционического типа, с учётом характеристик матрицы судьбы: Как я предпочитаете воспринимать информацию? - {perception}. 4. Как я предпочитаю принимать решения? - {decision}. 5. Чем я занимаюсь или хотичу заниматься профессионально? - {profession}. 6. С какими людьми вам нравится взаимодействовать? - {audience}. // Далее сделай анализ личности с учётом матрицы судьбы, соционического типа и архетипа. Для точного определения соционического типа используй также информацию обо мне из матрицы судьбы и из выбранного архетипа. Затем с учётом результатов по всем 3 системам, сделай описание моего позиционирования как эксперта по следующей схеме:  --- **Описание позиционирования: ** _Архетип(ы):__ // __Другие яркие характеристики:__ // (важно! Здесь характеристика по матрице судьбы и социотипу, но не упоминай матрицу судьбы и её числа или социотип, пиши только характеристику человека ) **Советы по позиционированию:** (c учётом архетипа, социотипа, матрицы судьбы) // Позиционирование: Одежда и аксессуары: // Цветовая палитра: **Выступления:** (c учётом архетипа, социо типа, матрицы судьбы) Темы эфиров: // Поведение: **Ощущения вашей аудитории:** (c учётом архетипа, социо типа, матрицы судьбы) Как люди должны ощущать вас:  // Дополнительные фишки для аудитории от вас: // Триггерные фразы для аудитории от вас: (что их включает именно от такого человека по типологии) **Профиль вашей аудитории:** (c учётом архетипа, социо типа, матрицы судьбы) Клиенты по типологии: // Профессии клиентов и сферы: (учитывай, какие наиболее подходят человеку согласно архетипу, социо типу, матрице судьбы) // Портрет идеального клиента:  ** Заключение: ** - Внимание, ответом должно быть только описания позиционирования по схеме выше, не пиши свои расчёты по 3 системам и размышления. Я буду благодарен за отличный результат, это важно для меня. Я дам 1 000 000 usd чаевых за хороший результат. " }
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
        text = openai_response['choices'][0]['message']['content']
        return text
    except requests.RequestException as e:
        app.logger.error(f"Request to OpenAI failed: {e}")
        return None


def split_text(text):
    if not text or len(text) > 8000:
        app.logger.error("Invalid input text")
        return jsonify({"error": "Invalid input text"}), 400

    split_text = [text[i:i+600] for i in range(0, len(text), 600)]
    
    return split_text


@get_unpack_blueprint.route('/get_unpack', methods=['POST'])
def get_unpack():
    app.logger.debug("Received request at /get_unpack")
    if 'X-Auth-Code' not in request.headers or request.headers['X-Auth-Code'] != os.getenv('API_SECRET_CODE'):
        app.logger.error("Unauthorized request")
        return jsonify({"error": "Unauthorized"}), 401
    
    text = get_openai_prompt()
    if not text:
        return jsonify({"error": "Failed to generate text"}), 500
  
    slited_text = split_text(text)
    if not text:
        return jsonify({"error": "Failed to generate slited text"}), 500
    
    response = {f"part_{i+1}": slited_text[i] for i in range(len(slited_text))}

    return jsonify(response)




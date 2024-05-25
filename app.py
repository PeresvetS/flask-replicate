from flask import Flask, request, jsonify
import replicate

app = Flask(__name__)

# Аутентификация с помощью API-ключа
client = replicate.Client(api_token="REPLICATE_API_TOKEN")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    version_id = data.get("version")
    input_data = data.get("input")

    if not version_id or not input_data:
        return jsonify({"error": "Invalid input data"}), 400

    # Создание предсказания с указанием более мощного GPU
    prediction = client.predictions.create(
        version=version_id,
        input=input_data,
        hardware="gpu-a100"
    )

    # Получение ID предсказания
    prediction_id = prediction.id

    # Возвращение ID предсказания
    return jsonify({"id": prediction_id})

if __name__ == '__main__':
    app.run(debug=True)

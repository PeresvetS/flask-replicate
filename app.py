from flask import Flask, request, jsonify
import replicate

app = Flask(__name__)

# Аутентификация с помощью API-ключа
client = replicate.Client(api_token="r8_NI7XcG0HukUN4Z8oS6vpK4yCXw3toP52Rk3Yv")

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

    # Ожидание завершения предсказания
    prediction.wait()

    # Проверка статуса предсказания
    if prediction.status == "succeeded":
        return jsonify({"output": prediction.output})
    elif prediction.status == "failed":
        return jsonify({"error": prediction.error}), 500
    else:
        return jsonify({"status": prediction.status}), 202

if __name__ == '__main__':
    app.run(debug=True)

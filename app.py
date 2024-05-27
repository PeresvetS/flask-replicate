import os
import time
import random
import requests
import logging
from flask import Flask, request, jsonify, send_from_directory
from base64 import b64encode

def create_app():
    app = Flask(__name__)

    app.logger.setLevel(logging.DEBUG) 

    random_integer = random.randint(1, 999999999)

    api_key = os.getenv("SEGMIND_API_KEY")
    if not api_key:
        raise ValueError("No SEGMIND_API_KEY set for Flask application")
    segmind_url = "https://api.segmind.com/v1/instantid"

    # Путь для сохранения изображений
    save_path = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", "/app/data")

    def to_b64(img_url):
        return b64encode(requests.get(img_url).content).decode('utf-8')

    @app.route('/generate', methods=['POST'])
    def generate():
        data = request.json
        prompt = data.get("prompt")
        face_image_url = data.get("face_image")
        negative_prompt = data.get("negative_prompt")
        style = data.get("style")
        samples = data.get("samples")
        num_inference_steps = data.get("num_inference_steps")
        guidance_scale = data.get("guidance_scale")
        identity_strength = data.get("identity_strength")
        adapter_strength = data.get("adapter_strength")


        if not prompt or not face_image_url:
            app.logger.error("Invalid input data")
            return jsonify({"error": "Invalid input data"}), 400

        payload = { 
            "prompt": prompt,
            "face_image": to_b64(face_image_url),
            "negative_prompt": negative_prompt,
            "style": style,
            "samples": samples,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "seed": random_integer,
            "identity_strength": identity_strength,
            "adapter_strength": adapter_strength,
            "enhance_face_region": True,
            "base64": False
        }

        headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        }

        app.logger.debug(f"Payload: {payload}")

        try:
            response = requests.post(url=segmind_url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
           app.logger.error(f"Request to Segmind failed: {e}")
           app.logger.error(f"Response content: {response.content}")
           app.logger.error(f"Response status code: {response.status_code}")
           app.logger.error(f"Request payload: {payload}")
           return jsonify({"error": "Failed to generate image"}), 500

        image = response.content
        file_name = f"generated_image_{int(time.time())}.jpg"
        file_path = os.path.join(save_path, file_name)

        try:
            with open(file_path, "wb") as f:
                f.write(image)
        except IOError as e:
            app.logger.error(f"Failed to save image: {e}")
            return jsonify({"error": "Failed to save image"}), 500

        return jsonify({"image_url": f"/data/{file_name}"})

    @app.route('/data/<path:filename>')
    def serve_file(filename):
        return send_from_directory(save_path, filename)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

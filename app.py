import os
import time
import requests
from flask import Flask, request, jsonify
from base64 import b64encode

def create_app():
    app = Flask(__name__)

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
        # style = data.get("style")
        samples = data.get("samples")
        num_inference_steps = data.get("num_inference_steps")
        guidance_scale = data.get("guidance_scale")
        seed = data.get("seed")
        identity_strength = data.get("identity_strength")
        adapter_strength = data.get("adapter_strength")
        enhance_face_region = data.get("enhance_face_region")
        base64_required = data.get("base64")

        if not prompt or not face_image_url:
            return jsonify({"error": "Invalid input data"}), 400

        payload = {
            "prompt": prompt,
            "face_image": to_b64(face_image_url),
            "negative_prompt": negative_prompt,
            # "style": style,
            "samples": samples,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "seed": seed,
            "identity_strength": identity_strength,
            "adapter_strength": adapter_strength,
            "enhance_face_region": enhance_face_region,
            "base64": base64_required
        }

        headers = {'x-api-key': api_key}

        try:
            response = requests.post(segmind_url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            app.logger.error(f"Request to Segmind failed: {e}")
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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

import os
import time
import random
import requests
from flask import Blueprint, request, jsonify, send_from_directory, current_app as app

generate_blueprint = Blueprint('generate', __name__)

api_key = os.getenv("SEGMIND_API_KEY")
if not api_key:
    raise ValueError("No SEGMIND_API_KEY set for Flask application")
segmind_url = "https://api.segmind.com/v1/instantid"
save_path = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", "/app/data")

@generate_blueprint.route('/generate', methods=['POST'])
def generate():
    if 'X-Auth-Code' not in request.headers or request.headers['X-Auth-Code'] != 'YOUR_SECRET_CODE':
        return jsonify({"error": "Unauthorized"}), 401
    
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
        "face_image": face_image_url,
        "negative_prompt": negative_prompt,
        "style": style,
        "samples": samples,
        "num_inference_steps": num_inference_steps,
        "guidance_scale": guidance_scale,
        "seed": random.randint(1, 999999999),
        "identity_strength": identity_strength,
        "adapter_strength": adapter_strength,
        "enhance_face_region": True,
        "base64": False
    }

    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

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

@generate_blueprint.route('/data/<path:filename>')
def serve_file(filename):
    return send_from_directory(save_path, filename)

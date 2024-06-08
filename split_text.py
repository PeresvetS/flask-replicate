from flask import Blueprint, request, jsonify, current_app as app

split_text_blueprint = Blueprint('split_text', __name__)

@split_text_blueprint.route('/split_text', methods=['POST'])
def split_text():
    data = request.json
    text = data.get("text")

    if not text or len(text) > 11000:
        app.logger.error("Invalid input text")
        return jsonify({"error": "Invalid input text"}), 400

    split_text = [text[i:i+600] for i in range(0, len(text), 600)]
    response = {f"part_{i+1}": split_text[i] for i in range(len(split_text))}
    
    return jsonify(response)
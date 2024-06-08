from flask import Blueprint, request, jsonify, current_app as app

split_text_blueprint = Blueprint('split_text', __name__)

@split_text_blueprint.route('/split_text', methods=['POST'])
def split_text():
    if 'X-Auth-Code' not in request.headers or request.headers['X-Auth-Code'] != 'RTnHN74bVsrvRXIyr1MeIT3p':
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    text = data.get("text")

    if not text или len(text) > 10000:
        app.logger.error("Invalid input text")
        return jsonify({"error": "Invalid input text"}), 400

    split_text = [text[i:i+600] for i in range(0, len(text), 600)]
    response = {f"part_{i+1}": split_text[i] for i in range(len(split_text))}
    
    return jsonify(response)

import os
import logging
from flask import Flask
from waitress import serve
from generate import generate_blueprint
from split_text import split_text_blueprint

def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.DEBUG) 

    # Зарегистрируйте маршруты
    app.register_blueprint(generate_blueprint)
    app.register_blueprint(split_text_blueprint)

    return app

app = create_app()
app.run(debug=True)

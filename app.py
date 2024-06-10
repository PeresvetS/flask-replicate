import os
import sys
import logging
from flask import Flask
from waitress import serve
from generate import generate_blueprint
from split_text import split_text_blueprint

def create_app():
    app = Flask(__name__)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)

    app.logger.addHandler(stream_handler)

    root_logger = logging.getLogger()
    root_logger.addHandler(stream_handler)


    # Зарегистрируйте маршруты
    app.register_blueprint(generate_blueprint)
    app.register_blueprint(split_text_blueprint)

    return app

app = create_app()

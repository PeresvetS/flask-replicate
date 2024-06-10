import os
import sys
import logging
from flask import Flask
from generate import generate_blueprint
from get_unpack import get_unpack_blueprint
from make_archetype_img import make_archetype_img_blueprint

def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.DEBUG) 

    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # stream_handler = logging.StreamHandler(sys.stdout)
    # stream_handler.setFormatter(formatter)
    # stream_handler.setLevel(logging.DEBUG)

    # app.logger.addHandler(stream_handler)

    # root_logger = logging.getLogger()
    # root_logger.addHandler(stream_handler)

    @app.route('/')
    def index():
        app.logger.debug("Index route accessed")
        return "Hello, World!"

    app.register_blueprint(generate_blueprint)
    app.register_blueprint(get_unpack_blueprint)
    app.register_blueprint(make_archetype_img_blueprint)


    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
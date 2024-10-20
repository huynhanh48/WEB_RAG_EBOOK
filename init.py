from flask import Flask
import Pages as p
def create_app():
    app = Flask(__name__)
    app.register_blueprint(p.bp)
    return app
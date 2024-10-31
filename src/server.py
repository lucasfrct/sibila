# flake8: noqa: E501

from flask import Flask
from src.routes.routes import app as Routes


app = Flask(__name__)
app.register_blueprint(Routes)


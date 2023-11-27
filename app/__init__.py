from flask import Flask

app = Flask(__name__)

DATA = {"users": [], "contests": []}

from app import views
from app import models

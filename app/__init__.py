#author: Rui Maximo

from flask import Flask

app = Flask(__name__)

# this import is placed here to circumvent the circular imports problem.
from app import routes



from flask import Blueprint

bp = Blueprint('passphrase', __name__)

from app.passphrase import routes
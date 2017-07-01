from flask import Blueprint

main = Blueprint('main', __name__)

# import in the last, avoiding dep loop
from . import files, errors


from flask import Blueprint

main = Blueprint('main', __name__)

# 在最后导入，避免循环依赖
from . import files, errors


"""
all api about files manipulation
"""
import os
from flask import render_template
from flask import redirect, request
from flask import send_from_directory
from config import BaseConfig
from . import main
from .lib import jsonify_wrapper
from ..model import Files
from .. import db

UPLOAD_FOLDER = BaseConfig.UPLOAD_FOLDER

@main.route("/")
def index():
    """
    home page index.html
    """
    return render_template('index.html', files = listFiles())


@main.route("/api/uploadFile", methods=['POST'])
def upload_file():
    """
    upload a file to server by post
    """
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    addFile(filename)
    return redirect('/')

@main.route("/api/delFile/<file_id>", methods=['GET'])
def del_file(file_id):
    """
    remove file in server
    """
    delFile(file_id)
    return redirect('/')

@main.route("/file/<filename>", methods=['GET'])
def serve_file(filename):
    """
    access file content, you can download or something
    """
    folder = UPLOAD_FOLDER
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        filename = 'not-exist'
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


def addFile(filename):
    """
    add a record in db
    """
    files = listFiles()
    for f in files:
        if filename == f.filename:
            return

    db.session.add(Files(filename=filename))
    db.session.commit()

def delFile(id):
    """
    remove the record in db
    """
    fileToDelete = Files.query.filter_by(id=id).one()
    db.session.delete(fileToDelete)
    db.session.commit()

def listFiles():
    """
    query all records
    """
    return Files.query.all()


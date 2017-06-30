from flask import url_for, request
from flask import json
import io
from app.model import Files


# test model
def test_files_db(client):
    assert hasattr(Files, 'id')
    assert hasattr(Files, 'filename')

# test route
def test_404(client):
    assert client.get('/url-not-exist').status_code == 404

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert "/static/main.css".encode() in rv.data

def test_files_operation(client):
    # upload a file
    client.post(url_for('main.upload_file'), data=dict(
        file=(io.BytesIO(b'hi everybody'), 'name.test')
    ))
    # check if it's uploaded
    rv = client.get('/')
    assert "/file/name.test".encode() in rv.data
    # delete file
    file_id = Files.query.filter_by(filename='name.test').one().id
    client.get(url_for('main.del_file', file_id=file_id))
    # check if it's gone
    rv = client.get('/')
    assert "/file/name.test".encode() not in rv.data


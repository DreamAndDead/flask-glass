"""
关于静态文件相关的接口定义，包括sql文件的下载及图片的上传与下载
"""

import base64
import hashlib
import os

from flask import redirect, request
from flask import url_for, send_from_directory

from config import BaseConfig
from . import main
from .base import jsonify_wrapper

UPLOAD_FOLDER = BaseConfig.UPLOAD_FOLDER


@main.route("/")
def index():
    return redirect('/static/index.html')


@main.route("/api/uploadFile", methods=['POST'])
@jsonify_wrapper
def upload_file():
    """
    上传文件接口

    这里并没有限定文件的类型，但是这里只是提供给上传icon图片文件用的

    在设置item的时候，需要设置一个icon_uri的字段，标识图片服务器中icon的地址，这个地址uri是可以
    由文件本身进行计算的，也是我们要设置给item的icon_uri属性的，这样就避免了与远程线上服务器进行
    交互的麻烦，也取得了正确的值

    注意，实际的图片资源并没有部署到alpha/beta/online环境的图片服务器，需要批处理上传同样的图片！

    兼容前端的Upload组件，相应的file key要设置为'file'

    input:

    .. code-block:: javascript

       { "file": ... }

    output:

    uri设置作为icon_uri属性，url用于在前端显示图片

    .. code-block:: javascript

       {
         "url": "http://ip:host/file/aW1hZ2UvTVRveE1HUm1aV1l5WWpsa09URTNNV0kxTWpFNFlURmxOMk00TTJJNE5qZ3dPUQ",
         "uri": "cs://1/image/aW1hZ2UvTVRveE1HUm1aV1l5WWpsa09URTNNV0kxTWpFNFlURmxOMk00TTJJNE5qZ3dPUQ"
       }
    """
    file = request.files['file']
    filename = hash_file(file.stream)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return {'url': url_for('main.serve_file', filename=filename),
            'uri': 'cs://1/image/%s' % filename}


def hash_file(file):
    """
    生成uri的算法

    正常上传图片的时候，会返回uri
    cs://1/image/aW1hZ2UvTVRveE1HUm1aV1l5WWpsa09URTNNV0kxTWpFNFlURmxOMk00TTJJNE5qZ3dPUQ

    这个链接的生成过程：
    md5 = md5sum( 文件流 )
    s1 = base64( 1:${md5} )
    s2 = base64( image/${s1} )
    res = cs://1/image/${s2}

    注意：base64的所有结果都删除结尾的==
    """
    tmp = hashlib.md5(file.read()).hexdigest()
    tmp = base64.b64encode(('1:%s' % tmp).encode()).decode().strip('=')
    tmp = base64.b64encode(('image/%s' % tmp).encode()).decode().strip('=')
    # reset pointer
    file.seek(0)
    return tmp


@main.route("/file/<filename>", methods=['GET'])
def serve_file(filename):
    """
    提供静态资源的访问，如下载sql，下载图片

    如果相应filename在服务器端未存储，返回文件 not-exist
    """
    folder = UPLOAD_FOLDER
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        filename = 'not-exist'
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

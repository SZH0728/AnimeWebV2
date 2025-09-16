# -*- coding:utf-8 -*-
# AUTHOR: Sun

from flask import Blueprint, abort
from flask import send_from_directory, send_file

from constant import ENABLE_INNER_PICTURE, PICTURE_PATH

# 创建错误处理蓝图
file_bp = Blueprint('file', __name__)


@file_bp.route('/picture/<int:pid>')
def picture(pid: int):
    if not ENABLE_INNER_PICTURE:
        abort(404)

    return send_from_directory(PICTURE_PATH, str(pid) + '.jpg')

@file_bp.route('/robots.txt')
def robot():
    return send_file('static/robots.txt')

if __name__ == '__main__':
    pass

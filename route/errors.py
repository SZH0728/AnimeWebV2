# -*- coding:utf-8 -*-
# AUTHOR: Sun

from flask import Blueprint, render_template

# 创建错误处理蓝图
errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(400)
def handle_400(error):
    return render_template('error.html', code=400, message=error.description), 400


@errors_bp.app_errorhandler(401)
def handle_401(error):
    return render_template('error.html', code=401, message=error.description), 401


@errors_bp.app_errorhandler(403)
def handle_403(error):
    return render_template('error.html', code=403, message=error.description), 403


@errors_bp.app_errorhandler(404)
def handle_404(error):
    return render_template('error.html', code=404, message=error.description), 404


@errors_bp.app_errorhandler(408)
def handle_408(error):
    return render_template('error.html', code=408, message=error.description), 408


@errors_bp.app_errorhandler(429)
def handle_429(error):
    return render_template('error.html', code=429, message=error.description), 429


@errors_bp.app_errorhandler(500)
def handle_500(error):
    return render_template('error.html', code=500, message=error.description), 500


@errors_bp.app_errorhandler(502)
def handle_502(error):
    return render_template('error.html', code=502, message=error.description), 502


@errors_bp.app_errorhandler(503)
def handle_503(error):
    return render_template('error.html', code=503, message=error.description), 503


@errors_bp.app_errorhandler(504)
def handle_504(error):
    return render_template('error.html', code=504, message=error.description), 504

if __name__ == '__main__':
    pass

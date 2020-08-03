from flask import Blueprint, render_template, send_from_directory
from application import app

route_index = Blueprint('index_page', __name__)


# 按顺序拦截 带文件名的
@route_index.route('/<path:filename>')
def root_file(filename):
    print(filename)
    return send_from_directory(app.root_path + "/web/templates", filename)


@route_index.route('/')
def index():
    return render_template("index.html")

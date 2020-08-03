# -*- coding: utf-8 -*-
import re

from flask import request, jsonify, make_response

from common.libs.user.UserService import UserService
from application import app

from common.models.IpStaff import (IpStaff)


@app.before_request
def before_request():

    path = request.path

    if '/api' not in path:
        return

    api_ignore_urls = app.config['API_IGNORE_URLS']
    pattern = re.compile('%s' % "|".join(api_ignore_urls))
    if pattern.match(path):
        return
    if check_member_login():
        return
        
    return make_response(jsonify({"data": {"isLogin": False},"errorCode":'401',"errorMessage":"请先登录","success":True}))  # 设置响应体


'''
判断用户是否已经登录
'''


def check_member_login():
    auth_cookie = request.cookies.get(app.config['AUTH_COOKIE_NAME'])

    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split("#")

    if len(auth_info) != 2:
        return False

    try:
        user_info = IpStaff.query.filter_by(id=auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    if user_info.status != 1:
        return False

    return True

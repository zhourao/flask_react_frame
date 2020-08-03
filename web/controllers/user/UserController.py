from flask import Blueprint, jsonify, request, make_response
from application import app

from common.libs.user.UserService import UserService
from common.models.IpStaff import (IpStaff)

route_user = Blueprint('user_page', __name__)


@route_user.route("/account", methods=["POST"])
def account():
    req = request.json

    resp = {
        "status": 'error',
        "type": "account",
        "currentAuthority": 'user',
    }

    if req['userName'] is None or len(req['userName']) < 1:
        resp['message'] = "请输入正确的登录用户名~~"
        return jsonify(resp)

    if req['password'] is None or len(req['password']) < 1:
        resp['message'] = "请输入正确的邮箱密码~~"
        return jsonify(resp)

    user_info = IpStaff.query.filter_by(login_name=req['userName']).first()

    if user_info is None:
        resp['message'] = "请输入正确的登录用户名和密码-1~~"
        return jsonify(resp)

    if user_info.status != 1:
        resp['message'] = "账号已被禁用，请联系管理员处理~~"
        return jsonify(resp)

    print(user_info.login_pwd)
    print(UserService.genePwd(req['password'], user_info.login_salt))
    if user_info.login_pwd != UserService.genePwd(req['password'], user_info.login_salt):
        resp['message'] = "请输入正确的登录用户名和密码-2~~"
        return jsonify(resp)

    resp['status'] = 'ok'
    response = make_response(jsonify(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (
        UserService.geneAuthCode(user_info), user_info.id), 60 * 60 * 24 * 30)  # 保存120天
    return response


@route_user.route("/outLogin", methods=["GET", "POST"])
def outLogin():
    resp = {
        "data": {},
        "success": True,
    }
    response = make_response(jsonify(resp))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response

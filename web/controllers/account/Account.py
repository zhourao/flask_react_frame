# -*- coding: utf-8 -*-
from flask import Blueprint, request, make_response, jsonify

from application import app, db
from common.libs.Helper import getCurrentDate
from common.libs.user.UserService import UserService
from common.models.User import User

route_account = Blueprint('account_page', __name__)


def model_to_dict(result):
    from collections import Iterable
    # 转换完成后，删除  '_sa_instance_state' 特殊属性
    try:
        if isinstance(result, Iterable):
            tmp = [dict(zip(res.__dict__.keys(), res.__dict__.values())) for res in result]
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp = dict(zip(result.__dict__.keys(), result.__dict__.values()))
            tmp.pop('_sa_instance_state')
        return tmp
    except BaseException as e:
        print(e.args)
        raise TypeError('Type error of parameter')


@route_account.route("/list")
def list():
    resp_data = {"code": 0, "message": ""}
    req = request.values
    page = int(req['page']) if ('page' in req and req['page']) else 1

    query = User.query
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))

    page_size = app.config['PAGE_SIZE']

    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by(User.uid.desc()).all()[offset:limit]

    item_list = []
    for l in list:
        item_list.append(l.to_dict())

    resp_data['result'] = {
        "item_list": item_list,
        "page": page,
        "page_size": page_size,
        "total_count": query.count()
    }
    response = make_response(jsonify(resp_data))
    return response


@route_account.route("/edit", methods=["GET", "POST"])
def edit():
    default_pwd = "******"

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    print(req)

    id = req['uid'] if 'uid' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    email = req['email'] if 'email' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    status = req['status'] if 'status' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~"
        return jsonify(resp)

    if mobile is None or len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的手机号码~~"
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱~~"
        return jsonify(resp)

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录用户名~~"
        return jsonify(resp)

    if login_pwd is None or len(email) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录密码~~"
        return jsonify(resp)

    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该登录名已存在，请换一个试试~~"
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()
    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.geneSalt()

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    model_user.status = status
    if login_pwd != default_pwd:
        if user_info and user_info.uid == 1:
            resp['code'] = -1
            resp['msg'] = "该用户是演示账号，不准修改密码和登录用户名~~"
            return jsonify(resp)

        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)

    user_info.update_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)

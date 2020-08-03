from flask import Blueprint, jsonify, request

from application import app, db
from common.libs.Helper import iPagination, getCurrentDate
from common.libs.rsp_utils import to_success, to_error
from common.models.IpStaff import (IpStaff)
import datetime

from common.libs.user.UserService import UserService

ip_staff_route = Blueprint('ip_staff_page', __name__)


@ip_staff_route.route("/query", methods=["GET"])
def get_list():
    body = request.args
    print(body)
    current_page = int(body['current']) if body['current'] else 1
    page_size = int(
        body['pageSize']) if body['pageSize'] else app.config['PAGE_SIZE']

    query = IpStaff.query

    if 'nickname' in body:
        query = query.filter(IpStaff.nickname.ilike(
            "%{0}%".format(body['nickname'])))

    if 'is_male' in body and int(body['is_male']) > -1:
        query = query.filter(IpStaff.is_male == int(body['is_male']))

    if 'status' in body and int(body['status']) > -1:
        query = query.filter(IpStaff.status == int(body['status']))

    count = query.count()

    offset = (current_page - 1) * page_size
    limit = page_size * current_page

    list = query.order_by(IpStaff.id.desc()).all()[offset:limit]

    data_list = []
    for l in list:
        data_list.append(l.to_dict())

    result = {
        'current': current_page,
        'pageSize': page_size,
        'total': int(count / page_size) + 0 if count % page_size == 0 else 1,
        'data': data_list
    }
    print(result)

    return jsonify(to_success(result))


@ip_staff_route.route("/add", methods=["POST"])
def save():
    body = request.json

    model_staff = IpStaff()
    model_staff.created_time = getCurrentDate()
    model_staff.login_salt = UserService.geneSalt()

    model_staff.nickname = body['nickname']
    model_staff.mobile = body['mobile']

    if 'email' in body:
        model_staff.email = body['email']
    model_staff.login_name = body['login_name']
    model_staff.is_male = body['is_male']
    # model_staff.birthday = body['birthday'][0:10]
    model_staff.status = 1

    model_staff.login_pwd = UserService.genePwd(
        body['login_pwd'], model_staff.login_salt)

    model_staff.updated_time = getCurrentDate()

    db.session.add(model_staff)
    db.session.commit()
    return to_success({"message": "操作成功"})

# -*- coding: utf-8 -*-
from web.controllers.index import route_index
from application import app
from web.controllers.api import api_route
from web.controllers.user.UserController import route_user
from web.controllers.ip.StaffController import ip_staff_route
from web.interceptors.ApiAuthInterceptor import *

'''
统一拦截处理和统一错误处理
'''

app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(api_route, url_prefix="/api/")
app.register_blueprint(route_user, url_prefix="/api/login")
app.register_blueprint(ip_staff_route, url_prefix="/api/staff")

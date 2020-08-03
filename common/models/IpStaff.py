# coding: utf-8
from application import db
from datetime import datetime


class IpStaff(db.Model):
    __tablename__ = 'ip_staff'

    id = db.Column(db.BigInteger, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    email = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    is_male = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    birthday = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    address = db.Column(db.String(255), nullable=False, unique=True, server_default=db.FetchedValue())
    avatar = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    login_name = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue())
    login_pwd = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    login_salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    def serialize(self):
        from sqlalchemy.orm import class_mapper
        columns = [c.key for c in class_mapper(self.__class__).columns]
        return dict((c, getattr(self, c)) for c in columns)

    # 单个对象方法
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        for (k, v) in model_dict.items():
            if isinstance(v, datetime):
                model_dict[k] = v.strftime('%Y-%m-%d %H:%M:%S')
        model_dict['login_pwd'] = '******'
        return model_dict

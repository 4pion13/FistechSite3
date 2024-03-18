from flask_sqlalchemy import SQLAlchemy
from flask_login import (UserMixin)
from sweater import db

class UserInfo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    directory = db.Column(db.String(1000))
    status = db.Column(db.String(10))
    def __repr__(self):
        return f"<id={self.id}, directory={self.directory}, email={self.email}>"


class AdminsData(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Processors(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CPU = db.Column(db.String(100))
    def __repr__(self):
        return f"{self.CPU}"


class SendDataProducts(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vers = db.Column(db.String(100))
    developer = db.Column(db.String(100))
    lang = db.Column(db.String(100))
    os_sys = db.Column(db.String(100))
    arch = db.Column(db.String(100))
    processor = db.Column(db.String(100))
    ozu = db.Column(db.String(100))
    videoadapter = db.Column(db.String(100))
    disk = db.Column(db.String(100))
    status = db.Column(db.String(100))
    one_slide = db.Column(db.String(100))
    two_slide = db.Column(db.String(100))
    three_slide = db.Column(db.String(100))
    file = db.Column(db.String(100))
    project_name = db.Column(db.String(100))
    user_email = db.Column(db.String(100))
    def __repr__(self):
        return f"{self.id}, {self.project_name}, {self.vers}, {self.developer}, {self.lang}, {self.os_sys}, {self.arch}, {self.processor}, {self.ozu}, {self.one_slide}, {self.two_slide}, {self.three_slide}, {self.file}, {self.status}, {self.user_email}"


class Videocards(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    def __repr__(self):
        return f"{self.name}"


db.create_all()






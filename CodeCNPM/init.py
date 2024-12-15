from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from urllib.parse import quote
import os

app = Flask(__name__)

app.secret_key = 'HGHJAHA^&^&*AJAVAHJ*^&^&*%&*^GAFGFAG'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:%s@localhost/studentmanagement?charset=utf8mb4" % quote("Admin@123")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

login = LoginManager(app)

db = SQLAlchemy(app)
from init import app,db
from flask_admin import Admin
from models import MonHoc
from flask_admin.contrib.sqla import ModelView

admin = Admin(app=app, name="Trang quản trị", template_mode='bootstrap4')

class MonHocModelView(ModelView):
    column_list = ('id', 'ten_mon_hoc')
admin.add_view(MonHocModelView(MonHoc, db.session))




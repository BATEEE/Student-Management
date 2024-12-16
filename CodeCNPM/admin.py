from init import app,db
from flask_admin import Admin,AdminIndexView
from models import MonHoc,TaiKhoan
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect
from models import UserRole
import dao

class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/index.html')

admin = Admin(app=app, name="Trang quản trị", template_mode='bootstrap4',index_view=MyAdminIndexView())
#Hien thi mon hoc
class MonHocModelView(ModelView):
    column_list = ('id', 'ten_mon_hoc')
    column_searchable_list = ['id', 'ten_mon_hoc']
    column_filters = ['id', 'ten_mon_hoc']
    can_view_details = True
    column_labels = {
        'id': 'Mã môn học',
        'ten_mon_hoc': 'Tên môn học'
    }

#Quản lí user
class AuthenticatedView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.QT)

class MyView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

#Logout
class LogoutView(MyView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


#Thống kê
class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

admin.add_view(MonHocModelView(MonHoc, db.session))
admin.add_view(AuthenticatedView(TaiKhoan, db.session))
admin.add_view(StatsView('Thống kê - Báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))





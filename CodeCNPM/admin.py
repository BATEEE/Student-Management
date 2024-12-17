from init import app,db
from flask_admin import Admin,AdminIndexView
from models import MonHoc,TaiKhoan
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect,abort,url_for,session
from models import UserRole
from functools import wraps
import dao


def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] not in allowed_roles:
                abort(403)  # Trả về lỗi 403 Forbidden
            return func(*args, **kwargs)
        return wrapper
    return decorator

class MyAdminIndexView(AdminIndexView):
    @expose("/")
    @role_required(['qt'])
    def index(self):
        return self.render('admin/index.html')
    def is_accessible(self):
         return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.QT)
    def inaccessible_callback(self, name, **kwargs):
        return abort(403)

admin = Admin(app=app, name="Trang quản trị", template_mode='bootstrap4',index_view=MyAdminIndexView())

#Chặn quyền
class AuthenticatedView(ModelView):
    def is_accessible(self):
         return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.QT)

#Hien thi mon hoc
class MonHocModelView(AuthenticatedView):
    column_display_pk = True
    column_list = ('id', 'ten_mon_hoc')
    column_searchable_list = ['id', 'ten_mon_hoc']
    column_filters = ['id', 'ten_mon_hoc']
    can_view_details = True
    form_columns = ['ten_mon_hoc']
    column_labels = {
        'id': 'Mã môn học',
        'ten_mon_hoc': 'Tên môn học'
    }

class UserModelView(AuthenticatedView):
    can_create = True
    column_list = ('ten_tai_khoan', 'mat_khau','ngay_tao','email','user_role')
    column_searchable_list = ['ten_tai_khoan', 'mat_khau','ngay_tao','email','user_role']
    column_filters = ['ten_tai_khoan', 'mat_khau','ngay_tao','email','user_role']
    can_view_details = True
    column_labels = {
        'ten_tai_khoan': 'Tên tài khoản',
        'mat_khau': 'Mật khẩu',
        'ngay_tao': 'Ngày tạo',
        'email': 'Email',
        'user_role': 'Loại người dùng'
    }

class MyView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

#Logout
class LogoutView(MyView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/login') #/admin

#Thống kê
class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

admin.add_view(MonHocModelView(MonHoc, db.session))
admin.add_view(UserModelView(TaiKhoan, db.session))
admin.add_view(StatsView('Thống kê - Báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))





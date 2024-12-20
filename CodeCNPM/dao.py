from fileinput import hook_compressed

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query_expression

from models import TaiKhoan, UserRole, GiaoVien, QuanTri, MonHoc, HocSinh, HocSinhThuocLop, Lop, LoaiDiem, Diem, \
    HocSinhHocMon, ThongTinNamHoc, NamHocHienTai
from init import db
from sqlalchemy import func, asc
from datetime import datetime
import hashlib

def auth_login(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return TaiKhoan.query.filter(TaiKhoan.tai_khoan.__eq__(username.strip()),
                                 TaiKhoan.mat_khau.__eq__(password)).first()

def add_user(username, password, role):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    n = TaiKhoan.query.count() # so luong user trong Tai Khoan




# thêm môn học
def add_subject(id, ten_mon_hoc):
    mon_hoc = MonHoc(id=id, ten_mon_hoc=ten_mon_hoc)
    db.session.add(mon_hoc)
    db.session.commit()

# thêm học sinh
def add_student(id, ho, ten, gioi_tinh, dia_chi, email, ngay_sinh, so_dien_thoai):
    hoc_sinh = HocSinh(id=id, ho=ho, ten=ten, gioi_tinh=int(gioi_tinh), dia_chi=dia_chi, email=email,
                       ngay_sinh=ngay_sinh, so_dien_thoai=so_dien_thoai)
    db.session.add(hoc_sinh)
    db.session.commit()

def get_user_by_id(id):
    return TaiKhoan.query.get(id)

def find_student_class(id):
    student_class = HocSinhThuocLop.query \
        .filter(HocSinhThuocLop.hoc_sinh_id == id) \
        .join(HocSinhThuocLop.thong_tin_nam_hoc) \
        .order_by(ThongTinNamHoc.nam_hoc.desc(), ThongTinNamHoc.hoc_ki.desc()) \
        .first()
    return student_class

def find_student(id):
    if not id:
        return []
    student = HocSinh.query.filter(HocSinh.id.__eq__(id)).first()
    student_class = find_student_class(student.id)
    if student_class:
        return {
            "id": student_class.hoc_sinh.id,
            "ho": student_class.hoc_sinh.ho,
            "ten": student_class.hoc_sinh.ten,
            "dia_chi": student_class.hoc_sinh.dia_chi,
            "ngay_sinh": student_class.hoc_sinh.ngay_sinh,
            "gioi_tinh": student_class.hoc_sinh.gioi_tinh,
            "ten_lop": student_class.lop.ten_lop,
            "so_dien_thoai": student_class.hoc_sinh.so_dien_thoai,
            "email": student_class.hoc_sinh.email,
        }
    return {
            "id": student.id,
            "ho": student.ho,
            "ten": student.ten,
            "dia_chi": student.dia_chi,
            "ngay_sinh": student.ngay_sinh,
            "gioi_tinh": student.gioi_tinh,
            "ten_lop": "Không có lớp",
            "so_dien_thoai": student.so_dien_thoai,
            "email": student.email,
        }

# Lay danh sach lop hoc
def get_all_class(khoi_lop=[10, 11, 12]):
    return Lop.query.filter(Lop.khoi_lop.in_(khoi_lop)).all()

# Them hoc sinh vao lop
def add_student_into_class(list_student, class_id):
    thong_tin_nam_hoc = ThongTinNamHoc.query.filter(ThongTinNamHoc. nam_hoc.__eq__(NamHocHienTai.NAM_HOC), ThongTinNamHoc.hoc_ki.__eq__(NamHocHienTai.HOC_KY)).first()
    for k in list_student:
        hoc_sinh_thuoc_lop = HocSinhThuocLop(hoc_sinh_id=k['id'], lop_id=class_id, thong_tin_nam_hoc_id=thong_tin_nam_hoc.id)
        db.session.add(hoc_sinh_thuoc_lop)
        db.session.commit()

# Tao danh sach lop
def create_class(number_of_class, class_id):
    student_of_class = HocSinhThuocLop.query.all() # Lấy danh sách học sinh đã có lớp
    new_students = [x.hoc_sinh_id for x in student_of_class] # Lọc học sinh đã có lớp và học sinh chưa có
    # random từ danh sách học sinh bỏ đi danh sách học sinh của new student vì chỉ cần lấy danh sách học sinh chưa có lớp
    random_student = (HocSinh.query.filter(HocSinh.id.notin_(new_students)).order_by(func.random()).order_by(HocSinh.ten.asc()).limit(number_of_class).all())
    return random_student

# sửa thông tin học sinh
def update_studentinfo(id, ho, ten, gioi_tinh, dia_chi, email, ngay_sinh, so_dien_thoai):
    student = HocSinh.query.filter(HocSinh.id.__eq__(id)).first()
    if student:
        student.ho = ho
        student.ten = ten
        student.gioi_tinh = gioi_tinh
        student.dia_chi = dia_chi
        student.email = email
        student.ngay_sinh = ngay_sinh
        student.so_dien_thoai = so_dien_thoai
        db.session.commit()

#Lay du lieu mon hoc
def get_monhoc():
    return db.session.query(MonHoc.ten_mon_hoc)

#Lay du lieu hoc ki
def get_hocki():
    return db.session.query(ThongTinNamHoc.hoc_ki).distinct()

#lay du lieu nam hoc
def get_namhoc():
    return db.session.query(ThongTinNamHoc.nam_hoc).distinct()

# Thống kê
def thongke_DatMon(mon=None,nam=None,hocki=None):
    query= ((((db.session.query(
        Lop.ten_lop.label('ten_lop'),
        HocSinh.id.label('id_hoc_sinh')
        ,(func.sum(Diem.so_diem * LoaiDiem.he_so) / func.sum(LoaiDiem.he_so)).label('diem_trung_binh'))
            .join(HocSinhThuocLop, HocSinhThuocLop.lop_id == Lop.id)
            .join(HocSinh, HocSinhThuocLop.hoc_sinh_id == HocSinh.id)
            .join(HocSinhHocMon, HocSinhHocMon.hoc_sinh_id == HocSinh.id)
            .join(Diem, Diem.hoc_sinh_hoc_mon_id == HocSinhHocMon.id)
            .join(LoaiDiem, Diem.loai_diem_id == LoaiDiem.id)
            .join(MonHoc, HocSinhHocMon.mon_hoc_id == MonHoc.id)
            .join(ThongTinNamHoc, HocSinhHocMon.thong_tin_nam_hoc_id == ThongTinNamHoc.id))
            .filter(MonHoc.ten_mon_hoc.__eq__(mon)))
            .filter(ThongTinNamHoc.nam_hoc.__eq__(nam)))
            .filter(ThongTinNamHoc.hoc_ki.__eq__(hocki)))
    query=query.group_by(Lop.ten_lop,HocSinh.id)
    return query.all()

#Lay cac lop da co hoc sinh
def get_hocsinh_lop():
      return (db.session.query(Lop.id,Lop.ten_lop,func.count(HocSinhThuocLop.hoc_sinh_id).label('siso'))
            .join(HocSinhThuocLop,Lop.id==HocSinhThuocLop.lop_id)
            .join(HocSinh,HocSinhThuocLop.hoc_sinh_id==HocSinh.id).group_by(Lop.id,Lop.ten_lop).distinct().all())
#Lay danh hoc sinh theo lop
def get_listHocSinh_lop(idlop):
      return (db.session.query(HocSinh.id,HocSinh.ho,HocSinh.ten,HocSinh.gioi_tinh,HocSinh.ngay_sinh,HocSinh.dia_chi).join(HocSinhThuocLop,HocSinhThuocLop.hoc_sinh_id==HocSinh.id)
              .join(Lop,HocSinhThuocLop.lop_id.__eq__(Lop.id))).filter(Lop.id.__eq__(idlop)).all()




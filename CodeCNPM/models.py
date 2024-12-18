from init import db, app
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, Date, Integer, DateTime, ForeignKey, Double, Enum
from flask_login import UserMixin
from sqlalchemy.sql import func,cast
from enum import Enum as EnumRole
from flask import redirect
import hashlib
import datetime


class UserRole(EnumRole):
    GV = "GiaoVien",
    NV = "NhanVien",
    QT = "QuanTri"


# 'giao_vien.Id', 'quan_tri.Id', 'nhan_vien.Id'

class TaiKhoan(db.Model, UserMixin):
    __tablename__ = 'tai_khoan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_tai_khoan = Column(String(45), unique=True, nullable=False)
    tai_khoan = Column(String(45), nullable=False, unique=True)
    mat_khau = Column(String(45), nullable=False)
    ngay_tao = Column(DateTime(timezone=True), default=func.now)
    email = Column(String(45), unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.GV)

    # __mapper_args__ = {
    #     'polymorphic_identity': 'tai_khoan',
    #     'polymorphic_on': Id,
    #     'with_polymorphic': "*"
    # }
    giao_vien = relationship('GiaoVien', backref="tai_khoan", lazy=True)
    nhan_vien = relationship('NhanVien', backref="tai_khoan", lazy=True)
    quan_tri = relationship('QuanTri', backref="tai_khoan", lazy=True)


class HocSinh(db.Model):
    id = Column(String(10), primary_key=True)
    ho = Column(String(45), nullable=False)
    ten = Column(String(45), nullable=False)
    gioi_tinh = Column(Boolean)
    dia_chi = Column(String(100))
    email = Column(String(45))
    ngay_sinh = Column(Date)
    so_dien_thoai = Column(String(10))
    avatar = Column(String(50))
    hoc_sinh_hoc_mon = relationship('HocSinhHocMon', backref="hoc_sinh", lazy=True)
    hoc_sinh_thuoc_lop = relationship('HocSinhThuocLop', backref="hoc_sinh", lazy=True)


class GiaoVien(db.Model):
    __tablename__ = 'giao_vien'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ho = Column(String(45), nullable=False)
    ten = Column(String(45), nullable=False)
    gioi_tinh = Column(Boolean)
    dia_chi = Column(String(100))
    email = Column(String(45))
    ngay_sinh = Column(Date)
    so_dien_thoai = Column(String(10))
    day = relationship('Day', backref="giao_vien", lazy=True)
    tai_khoan_id = Column(Integer, ForeignKey('tai_khoan.id'), unique=True)

    # def __init__(self, id, ho, ten, gioi_tinh, dia_chi, email, ngay_sinh, so_dien_thoai):
    #     self.id = id
    #     self.ho = ho
    #     self.ten = ten
    #     self.gioi_tinh = gioi_tinh
    #     self.dia_chi = dia_chi
    #     self.email = email
    #     self.ngay_sinh = ngay_sinh
    #     self.so_dien_thoai = so_dien_thoai

    # __mapper_args__ = {
    #     'polymorphic_identity': 'giao_vien',
    # }


class QuanTri(db.Model):
    __tablename__ = 'quan_tri'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ho = Column(String(45), nullable=False)
    ten = Column(String(45), nullable=False)
    gioi_tinh = Column(Boolean)
    dia_chi = Column(String(100))
    email = Column(String(45))
    ngay_sinh = Column(Date)
    so_dien_thoai = Column(String(10))
    tai_khoan_id = Column(Integer, ForeignKey('tai_khoan.id'), unique=True)

    # __mapper_args__ = {
    #     'polymorphic_identity': 'quan_tri',
    # }


class NhanVien(db.Model):
    __tablename__ = 'nhan_vien'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ho = Column(String(45), nullable=False)
    ten = Column(String(45), nullable=False)
    gioi_tinh = Column(Boolean)
    dia_chi = Column(String(100))
    email = Column(String(45))
    ngay_sinh = Column(Date)
    so_dien_thoai = Column(String(10))
    tai_khoan_id = Column(Integer, ForeignKey('tai_khoan.id'), unique=True)

    def __str__(self):
        return self.ten


class Lop(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_lop = Column(String(50), nullable=False)
    khoi_lop = Column(Integer, nullable=False)
    day = relationship('Day', backref="lop", lazy=True)
    hoc_sinh_thuoc_lop = relationship('HocSinhThuocLop', backref="lop", lazy=True)


class LoaiDiem(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    loai_diem = Column(String(45), nullable=False)
    he_so = Column(Integer, nullable=False)


class MonHoc(db.Model):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ten_mon_hoc = Column(String(50), nullable=False)
    hoc_sinh_hoc_mon = relationship('HocSinhHocMon', backref="mon_hoc", lazy=True)
    giao_vien_day_mon = relationship('GiaoVienDayMon', backref="mon_hoc", lazy=True)

    def __str__(self):
        return self.ten_mon_hoc


class ThongTinNamHoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nam_hoc = Column(String(20), nullable=False)
    hoc_ki = Column(Integer, nullable=False)
    day = relationship('Day', lazy=True)
    hoc_sinh_hoc_mon = relationship('HocSinhHocMon', backref="thong_tin_nam_hoc", lazy=True)
    hoc_sinh_thuoc_lop = relationship('HocSinhThuocLop', backref="thong_tin_nam_hoc", lazy=True)


class PhongHoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_phong = Column(String(45), nullable=False)
    phong = relationship('Day', backref="phong_hoc", lazy=True)


class Day(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    chu_nhiem = Column(Boolean, nullable=False)
    giao_vien_id = Column(Integer, ForeignKey('giao_vien.id'))
    lop_id = Column(Integer, ForeignKey('lop.id'))
    thong_tin_nam_hoc_id = Column(Integer, ForeignKey('thong_tin_nam_hoc.id'))
    phong_id = Column(Integer, ForeignKey('phong_hoc.id'))


class Diem(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    so_diem = Column(Double, nullable=False)
    loai_diem_id = Column(Integer, ForeignKey('loai_diem.id'), nullable=False)
    hoc_sinh_hoc_mon_id = Column(Integer, ForeignKey('hoc_sinh_hoc_mon.id'), nullable=False)


class HocSinhHocMon(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    mon_hoc_id = Column(Integer, ForeignKey('mon_hoc.id'), nullable=False)
    hoc_sinh_id = Column(String(10), ForeignKey('hoc_sinh.id'), nullable=False)
    thong_tin_nam_hoc_id = Column(Integer, ForeignKey('thong_tin_nam_hoc.id'), nullable=False)
    diem = relationship('Diem', backref="hoc_sinh_hoc_mon", lazy=True)


class HocSinhThuocLop(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoc_sinh_id = Column(String(10), ForeignKey('hoc_sinh.id'), nullable=False)
    lop_id = Column(Integer, ForeignKey('lop.id'), nullable=False)
    thong_tin_nam_hoc_id = Column(Integer, ForeignKey('thong_tin_nam_hoc.id'), nullable=False)


class GiaoVienDayMon(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    mon_hoc_id = Column(Integer, ForeignKey('mon_hoc.id'), nullable=False)
    giao_vien_id = Column(Integer, ForeignKey('giao_vien.id'), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        taikhoan1 = TaiKhoan(ten_tai_khoan="Trần Tuấn Thắng", tai_khoan="admin1", mat_khau=str(hashlib.md5("123456".strip().encode('utf-8')).hexdigest()),
                            ngay_tao="2004-2-12", email="thangancut@gmail.com", user_role=UserRole.QT)
        taikhoan2 = TaiKhoan(ten_tai_khoan="Nguyễn Hoàng Phúc", tai_khoan="nhanvien1", mat_khau=str(hashlib.md5("123456".strip().encode('utf-8')).hexdigest()),
                             ngay_tao="2004-12-15", email="phuc@gmail.com", user_role=UserRole.NV)
        quantri = QuanTri(ho="Trần Tuấn", ten='Thắng', gioi_tinh=0, dia_chi="189/34/28A Bach Dang Phuong 3 Go Vap",
                          email="thangdaubuoi@gmail.com", ngay_sinh="2004-3-20", so_dien_thoai="01242542", tai_khoan_id=taikhoan1.id)
        mon_hoc = MonHoc(ten_mon_hoc="Lập trình Python")
        db.session.add_all([taikhoan1, quantri])
        db.session.add(mon_hoc)
        nv = NhanVien(ho='Nguyễn Hoàng', ten='Phúc', gioi_tinh=0, dia_chi='189/34/28A Bach Dang Phuong 3 Go Vap',
                      email="phuc@gmail.com", ngay_sinh="2004-12-31", so_dien_thoai="01242542", tai_khoan_id=taikhoan2.id)
        db.session.add_all([taikhoan2, nv])
         # db.session.add(taikhoan)
        db.session.commit()

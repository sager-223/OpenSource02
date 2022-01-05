from . import db


class BaseModel(object):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    count = db.Column(db.Integer)

# 计算不同品牌的数量的前十名
class CarBrandTop10(BaseModel,db.Model):
    __tablename__ = 'db_car_brand_top10'
    brand = db.Column(db.String(32))

# 计算车二手车的使用时间
class CarUseYear(BaseModel,db.Model):
    __tablename__ = 'db_car_use_year'
    year_area = db.Column(db.String(32))

# 计算不同地区的二手车数量
class CarArea(BaseModel,db.Model):
    __tablename__='db_car_area'
    area = db.Column(db.String(32))

# 计算每个月的二手车数量
class CarMonth(BaseModel,db.Model):
    __tablename__='db_car_month'
    month = db.Column(db.Integer)
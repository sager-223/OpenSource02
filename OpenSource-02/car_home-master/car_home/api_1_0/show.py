from . import api
from car_home.models import CarArea,CarUseYear,CarBrandTop10,CarMonth
from flask import render_template
# 计算不同品牌的数量的前十名
@api.route('/showBrandBar')
def showBrandBar():
    car_brand_top10 = CarBrandTop10.query.all()
    brand = [i.brand for i in car_brand_top10]
    count = [i.count for i  in car_brand_top10]
    print(brand)
    print(count)
    return render_template('showBrandBar.html', **locals())


# 计算二手车的使用时间
@api.route('/showPie')
def showPie():
    car_use_year = CarUseYear.query.all()
    data = [{'name':i.year_area,'value':i.count} for i in car_use_year]
    return render_template('showPie.html',**locals())


# 计算不同地区的二手车数量
@api.route('/showAreaBar')
def showAreaBar():
    car_area = CarArea.query.all()
    area = [i.area for i in car_area]
    count = [i.count for i in car_area]
    return render_template('showAreaBar.html',**locals())

# 计算每个月的二手车数量
@api.route('/showLine')
def showLine():
    car_month = CarMonth.query.all()
    month = [i.month for i in car_month]
    count = [i.count for i in car_month]
    return render_template('showLine.html',**locals())


import re
from pymongo import MongoClient
import requests
from lxml import html

class CarHomeSpider(object):
    def __init__(self):
        self.start_url = 'http://www.che168.com/jiangsu/list/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }
        self.url_temp = 'http://www.che168.com/jiangsu/{}/a0_0msdgscncgpi1ltocsp{}exx0/?pvareaid=102179#currengpostion'
        self.client = MongoClient()
        self.collection = self.client['test']['car_home']

    def get_url_list(self,sign,total_count):
        url_list = [self.url_temp.format(sign,i) for i in range(1,int(total_count)+1)]
        return url_list

    def parse(self,url):
        resp = requests.get(url,headers=self.headers)
        return resp.text

    def get_content_list(self,raw_html):
        resp_html = html.etree.HTML(raw_html)
        car_list = resp_html.xpath('//ul[@class="viewlist_ul"]/li')
        for car in car_list:
            item = {}
            # 获取汽车的标题信息
            card_name = car.xpath('.//h4[@class="card-name"]/text()')
            card_name = card_name[0] if len(card_name)>0 else ''
            car_series = re.findall(r'(.*?) \d{4}款',card_name)
            item['car_series'] = car_series[0].replace(' ','') if len(car_series)>0 else ''
            car_time_style = re.findall(r'.*? (\d{4})款',card_name)
            item['car_time_style'] = car_time_style[0] if len(car_time_style)>0 else ''
            car_detail = re.findall(r'\d{4}款 (.*)',card_name)
            item['car_detail'] = car_detail[0].replace(' ','') if len(car_detail)>0 else ''

            # 获取汽车的详细信息
            card_unit = car.xpath('.//p[@class="cards-unit"]/text()')
            card_unit = card_unit[0].split('／') if len(card_unit)>0 else ''
            item['car_run'] = card_unit[0]
            item['car_push'] = card_unit[1]
            item['car_place'] = card_unit[2]
            item['car_rank'] = card_unit[3]

            # 获取汽车的价格
            car_price = car.xpath('./@price')
            item['car_price'] = car_price[0] if len(car_price)>0 else ''
            print(item)
            self.save(item)

    def save(self,item):
        self.collection.insert(item)

    def run(self):
        # 首先请求首页获取页面分类数据
        rest = self.parse(self.start_url)
        rest_html = html.etree.HTML(rest)
        # 这里取的是按照价格的分类 形如：3万以下 3-5万 5-8万 8-10万 10-15万 15-20万 20-30万 30-50万 50万以上
        price_area_list = rest_html.xpath('//div[contains(@class,"condition-price")]//div[contains(@class,"screening-base")]/a')
        if price_area_list:
            for price_area in price_area_list:
                price_area_text = price_area.xpath('./text()')[0]
                price_area_link = 'http://www.che168.com'+price_area.xpath('./@href')[0]
                # 获取每个分类的url并进行请求 获取每个分类下的总页数
                rest_ = self.parse(price_area_link)
                rest_html_ = html.etree.HTML(rest_)
                total_count = rest_html_.xpath('//div[@id="listpagination"]/a[last()-1]/text()')[0]
                # 获取每个分类url的唯一标识
                sign = re.findall(r'jiangsu/(.*?)/#pvareaid',price_area_link)[0]
                # 生成每个分类下的所有页面的url地址
                url_list = self.get_url_list(sign,total_count)
                for url in url_list:
                    raw_html = self.parse(url)
                    self.get_content_list(raw_html)

if __name__ == '__main__':
    car_home = CarHomeSpider()
    car_home.run()
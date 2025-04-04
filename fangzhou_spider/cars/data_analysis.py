import base64
import multiprocessing
import os
import subprocess
import time
from io import BytesIO
import pandas as pd
from matplotlib import pyplot as plt
from wordcloud import WordCloud


# DataAnalysis 数据分析
class DataAnalysis(object):
    def __init__(self):

        self.queue = multiprocessing.Queue()

    def analysis(self, sorted_data, sorted_data_dict):
        cars_data = {
            "doc_exist": 1,
            "head_info":{
                "counts":int(len(sorted_data_dict)),
                "doc_id":str(time.time())[:10],
                "msg":"success"
            },
            "center_data": self.center_data(sorted_data),
            "center_left1": self.center_left1(sorted_data),
            "center_left2": self.center_left2(sorted_data),
            "center_right1": self.center_right1(sorted_data),
            "center_right2": self.center_right2(sorted_data),
            "bottom_left": self.bottom_left(sorted_data_dict),
            "bottom_right": self.bottom_right()
        }
        return dict(cars_data)

    def center_data(self, sorted_data):
        # 车辆总数据
        cars_total = int(sorted_data.shape[0])
        # 销量最多汽车
        max_sale_car_name = str(sorted_data.iloc[0]["carName"])
        # 车辆最高销售额
        max_sale_volumn = int(sorted_data.nlargest(1, 'saleVolume')['saleVolume'].iloc[0])
        # 销售最多车型
        max_sale_car = str(sorted_data.nlargest(1, 'saleVolume')['carModel'].iloc[0])
        # 车型最多品牌
        max_car_model = str(sorted_data['brand'].value_counts().idxmax())
        # 车辆平均价格
        # 原理：获取DataFrame中price列的所有值，该列的每个值都是一个字典（包含min和max）。apply(lambda x: x['max'])对每个字典应用一个匿名函数，从中提取出max
        # 值，形成一个新的Series，max_prices，其中存储了所有车辆的最大价格。
        cars_average_price = int(sorted_data['price'].apply(lambda x: x['min']).mean())
        # 汽车品牌销售排行榜
        cars_brand_sale_rank = sorted_data['brand'].value_counts().sort_values(ascending=False).to_dict()
        # 油电占比
        type_counts = sorted_data['energyType'].value_counts()
        type_ratios = (type_counts / type_counts.sum() * 100).round(2).to_dict()

        center_data = {
            "cars_total": cars_total,
            "max_sale_car_name": max_sale_car_name,
            "max_sale_car": max_sale_car,
            "max_sale_volumn": max_sale_volumn,
            "max_car_model": max_car_model,
            "cars_average_price": cars_average_price,
            "cars_brand_sale_rank": cars_brand_sale_rank,
            "type_ratios": type_ratios
        }
        return center_data

    def center_left1(self, sorted_data):
        # 新能源汽车销量排行榜
        new_energy_cars = sorted_data[sorted_data['energyType'].isin(['纯电动', '插电式混合动力', '增程式'])]
        sorted_new_energy_cars = new_energy_cars.sort_values(by='saleVolume', ascending=False)
        result = sorted_new_energy_cars[['carName', 'saleVolume', 'energyType']]
        new_energy_cars = result.to_dict(orient='records')

        return new_energy_cars

    def center_left2(self, sorted_data, save_path='output/wordcloud.png'):
        # 生成词云文本
        result = sorted_data.apply(lambda row: f"{row['brand']} {row['carName']}", axis=1)
        cars_string = ' '.join(result)

        # 创建词云对象
        wordcloud = WordCloud(
            font_path="static/江城律动宋.ttf",
            width=800,
            height=400,
            mode='RGBA',
            prefer_horizontal=0.9
        ).generate(cars_string)

        # 生成图像
        buffer = BytesIO()
        plt.figure(facecolor='none')  # 透明画布
        plt.imshow(wordcloud)
        plt.axis("off")

        # 保存到缓冲区
        plt.savefig(
            buffer,
            format='png',
            transparent=True,
            bbox_inches='tight',
            pad_inches=0
        )

        # 保存到本地文件
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 自动创建目录
        with open(save_path, 'wb') as f:
            f.write(buffer.getvalue())  # 直接从缓冲区写入文件

        # 生成base64
        buffer.seek(0)
        base64_str = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()
        #subprocess.run("clip", shell=True, text=True, input=base64_str)
        return base64_str

    def center_right1(self, sorted_data):
        # 汽车品牌销售量饼图
        sales_summary = sorted_data.groupby('brand')['saleVolume'].sum().reset_index()
        sales_summary = sales_summary.to_dict(orient='records')
        result = [{"value": item["saleVolume"], "name": item["brand"]} for item in sales_summary]
        return result

    def center_right2(self,sorted_data):
        # 汽车销售价格占比
        sorted_data['averagePrice'] = sorted_data['price'].apply(lambda x: (x['min'] + x['max']) / 2)
        # 定义价格区间
        bins = [0, 5, 10, 20, 30, float('inf')]
        labels = ['0-5万', '5-10万', '10-20万', '20-30万', '30万以上']
        # 将价格分组
        sorted_data['priceGroup'] = pd.cut(sorted_data['averagePrice'], bins=bins, labels=labels, right=False)
        # 统计每个价格区间的数量
        price_distribution = sorted_data['priceGroup'].value_counts().sort_index()
        price_distribution = price_distribution.to_dict()
        result = [{"value": value, "name": key} for key, value in price_distribution.items()]
        return result

    def bottom_left(self, sorted_data_dict):
        return sorted_data_dict

    def bottom_right(self):
        return "/static/choose-me.jpg"



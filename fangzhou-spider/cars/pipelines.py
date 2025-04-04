# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
# from data_analysis import DataAnalysis

import pandas as pd
import pymongo

from .data_analysis import DataAnalysis


class CarsPipeline:

    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient('mongodb://mongo:27017/')  # MongoDB 连接字符串
        except Exception as e:
            spider.logger.error(f"MongoDB连接失败，{e}")

        self.db = self.client['fangzhou_db']  # 数据库名称
        self.collection = self.db['fangzhou']  # 集合名称
        self.car_data_list = []

    def close_spider(self, spider):
        # 将列表转换为 DataFrame 以进行数据处理
        print()
        spider.logger.info(f"爬取条数：{len(self.car_data_list)}")
        df = pd.DataFrame(self.car_data_list)
        # 数据清洗：去除缺失值
        df.dropna(inplace=True)  # 去掉含有缺失值的行
        # 按 'rank' 列进行排序
        sorted_data = df.sort_values(by='rank')
        sorted_data_dict=sorted_data.to_dict('records')

        # 在这里调用data_analysis
        big_screen_data=DataAnalysis().analysis(sorted_data=sorted_data,sorted_data_dict=sorted_data_dict)

        spider.logger.info(f"-----数据爬取和分析完成！------")


        # 使用 replace_one 方法来替换整个文档
        self.collection.replace_one(
            {'doc_exist': 1},  # 查找条件
            big_screen_data,  # 替换内容
            upsert=True  # 如果不存在则插入新文档
        )
        spider.logger.info(f"-----CarsData已保存至MongoDB-----")


    def process_item(self, item, spider):
        self.car_data_list.append(item)  # 将每个 item 添加到列表中
        return item  





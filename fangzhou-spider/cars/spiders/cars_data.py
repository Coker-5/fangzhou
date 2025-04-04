from urllib.parse import urlencode

import scrapy


class CarsDataSpider(scrapy.Spider):
    name = "cars-data"
    allowed_domains = ["dongchedi.com"]
    start_urls = [
        "https://www.dongchedi.com/motor/pc/car/rank_data"
    ]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    # 重写start_requests方法，因为我们要携带参数去请求
    # 不用parse，因为我们要进行多页爬取，parse只能处理少量数据
    def start_requests(self):
        for i in range(0, 10):
            params = {
                "aid": "1839",
                "app_name": "auto_web_pc",
                "city_name": "长沙",
                "count": "10",
                "offset": str(i * 10),
                "month": "",
                "new_energy_type": "",
                "rank_data_type": "11",
                "brand_id": "",
                "price": "",
                "manufacturer": "",
                "outter_detail_type": "",
                "nation": "0"
            }

            # 使用 urlencode 构建查询字符串
            query_string = urlencode(params)

            # 生成完整的请求 URL
            request_url = f"{self.start_urls[0]}?{query_string}"
            yield scrapy.Request(url=request_url,method='GET', callback=self.parse_rank,
                                 cb_kwargs={'params': params})

    def parse_rank(self, response,params):
        # 解析 JSON 响应
        page_json = response.json()
        car_list = page_json['data']['list']

        for car in car_list:
            car_id = car["series_id"]
            # 构建汽车数据字典
            car_data = {
                "brand": car["brand_name"],
                "carName": car["series_name"],
                "saleVolume": car["count"],
                "price": {
                    "min": car["min_price"],
                    "max": car["max_price"]
                },
                "manufacturer": car["sub_brand_name"],
                "rank": car["rank"],
                "carId": car_id,
                "carImage": car["image"],
            }
            # 现在我们需要获取每辆车的详细信息
            detail_url = f"https://www.dongchedi.com/auto/params-carIds-x-{car_id}"
            yield scrapy.Request(url=detail_url, callback=self.parse_details, cb_kwargs={'car_data': car_data})

    def parse_details(self, response, car_data):
        # 从汽车详细信息页面提取附加细节
        info_html = response.xpath("//div[@data-row-anchor='jb']/div[2]/div/text()").get(default="").strip()
        energy_type = response.xpath("//div[@data-row-anchor='fuel_form']/div[2]/div/text()").get(default="").strip()
        market_time = response.xpath("//div[@data-row-anchor='market_time']/div[2]/div/text()").get(default="").strip()
        insure = response.xpath("//div[@data-row-anchor='period']/div[2]/div/text()").get(default="").strip()

        # 将附加细节添加到汽车数据中
        car_data["carModel"] = info_html
        car_data["energyType"] = energy_type
        car_data["marketTime"] = market_time
        car_data["insure"] = insure

        # 返回完整的汽车数据
        yield car_data

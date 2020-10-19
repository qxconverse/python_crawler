import requests
import json

url1 = "http://www.weather.com.cn/data/sk/{}.html"
url2 = "http://www.weather.com.cn/data/cityinfo/{}.html"


# 气象局城市编码：https://www.cnblogs.com/youlixishi/articles/3612051.html
def get_info(city_code):
    wb_data1 = requests.get(url1.format(city_code)).content.decode()
    weather_info1 = json.loads(wb_data1)['weatherinfo']

    wb_data2 = requests.get(url2.format(city_code)).content.decode()
    weather_info2 = json.loads(wb_data2)['weatherinfo']

    city = weather_info1['city']
    cur_temp = weather_info1['temp']
    weather = weather_info2['weather']
    sd = weather_info1['SD']
    wd = weather_info1['WD']
    ws = weather_info1['WS']
    njd = weather_info1['njd']
    low_temp = weather_info2['temp1']
    high_temp = weather_info2['temp2']

    print(f'{city}，{weather}，{low_temp}-{high_temp}\n当前温度：{cur_temp}℃\n湿度：{sd}\n风向：{wd}，{ws}\n能见度：{njd}')


if __name__ == '__main__':
    get_info("101010200")

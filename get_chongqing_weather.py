import os
from urllib import request

from bs4 import BeautifulSoup

url = "http://www.weather.com.cn/weather1d/101040100.shtml"
response = request.urlopen(url)
data = response.read()
soup = BeautifulSoup(data, 'html.parser')
tag = soup.find(id='hidden_title')
print(tag['value'])
weatherInfo = tag['value'][:-2].replace('/', '到') + '摄氏度'
os.system('say ' + weatherInfo)

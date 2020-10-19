from bs4 import BeautifulSoup
import requests

constellation_dict = {
    '白羊': 'Aries',
    '金牛': 'Taurus',
    '双子': 'Gemini',
    '巨蟹': 'Cancer',
    '狮子': 'leo',
    '处女': 'Virgo',
    '天秤': 'Libra',
    '天蝎': 'Scorpio',
    '射手': 'Sagittarius',
    '魔羯': 'Capricorn',
    '水瓶': 'Aquarius',
    '双鱼': 'Pisces',
}


def get_info(c):
    wb_data = requests.get("http://astro.sina.com.cn/fate_day_{}/".format(constellation_dict.get(c)))
    # 防止出现乱码
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text, "lxml")
    info = soup.select(".tb tr td")
    info_k = [info[k] for k in range(len(info)) if k % 2 == 0]
    info_v = [info[v] for v in range(len(info)) if v % 2 == 1]
    for i in range(len(info_k)):
        print(f'{info_k[i].text}: {info_v[i].text}')


if __name__ == '__main__':
    get_info("双鱼")

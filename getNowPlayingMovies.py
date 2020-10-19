from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
}


class Movie:
    def __init__(self, title, year, score, region, director, actors, duration):
        self.title = title
        self.year = year
        self.score = score
        self.region = region
        self.director = director
        self.actors = actors
        self.duration = duration

    def desc(self):
        return f"电影名：{self.title}\n年份：{self.year}\n豆瓣评分：{self.score}\n地区：{self.region}\n导演：{self.director}\n主演：{self.actors}\n片长：{self.duration}\n"


def get_movie_info(city_name):
    wb_data = requests.get(f'https://movie.douban.com/cinema/nowplaying/{city_name}', headers=headers)
    soup = BeautifulSoup(wb_data.text, "lxml")
    info = soup.select("#nowplaying .mod-bd .list-item")
    movies = []
    for i in info:
        movies.append(Movie(i.attrs['data-title'], i.attrs['data-release'], i.attrs['data-score'],
                            i.attrs['data-region'], i.attrs['data-director'], i.attrs['data-actors'],
                            i.attrs['data-duration']))
    return movies


if __name__ == '__main__':
    movie_list = get_movie_info("beijing")
    for m in movie_list:
        print(m.desc())

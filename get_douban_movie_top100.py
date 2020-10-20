from bs4 import BeautifulSoup
import requests
import re
import csv

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
}

urls = ["https://movie.douban.com/top250?start={}".format(str(i)) for i in range(0, 50, 25)]

movie_info = []


def get_url_movie(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, "lxml")
    movie_href_list = soup.select(".info .hd a")
    for movie_href in movie_href_list:
        get_movie_info(movie_href['href'])


def get_movie_info(url):
    print("I am getting info from " + url)
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, "lxml")
    names = soup.select("#content h1 span")
    if len(names) == 0:
        data = {
            "name": "Not found",
            "director": "Not found",
            "score": "Not found",
            "country": "Not found"
        }
        print(data)
        movie_info.append(data)
        print("I am done!")
        return
    directors = soup.select("#info span .attrs a")
    if len(directors) == 0:
        return
    country = re.findall('<span class="pl">制片国家/地区:</span>(.*?)<br/>', wb_data.text, re.S)
    if len(country) == 0:
        return
    scores = soup.select(".rating_self strong")
    if len(scores) == 0:
        return
    data = {
        "name": names[0].get_text(),
        "director": directors[0].get_text(),
        "score": scores[0].get_text(),
        "country": country[0].split(" ")[1]
    }
    print(data)
    movie_info.append(data)
    print("I am done!")


def write_to_csv():
    csv_file = open('doubanMovieTop100.csv', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(["Name", "Director", "Country", "Score"])
    for i in range(len(movie_info)):
        writer.writerow(
            [movie_info[i]["name"], movie_info[i]["director"], movie_info[i]["country"], movie_info[i]["score"]])
        csv_file.close()


if __name__ == '__main__':
    for i in urls:
        get_url_movie(i)

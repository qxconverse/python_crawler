import json
import re

import requests
from requests.exceptions import RequestException


def get_problem_set(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_problem_set(problem_set):
    all_titles = []
    for i in range(len(problem_set)):
        all_titles.append(problem_set[i]["stat"]["question__title_slug"])
    return all_titles


def construct_url(problem_title):
    url = "https://leetcode.com/problems/" + problem_title + "/description/"
    get_problem_content(url, problem_title)


def get_problem_content(problem_url, title):
    response = requests.get(problem_url)
    # 要想访问到https://leetcode.com/graphql，首先需要访问problem_url，从它的response里面获取到set-cookie，这个里面就包含了
    # csrftoken，可用它去进行跨站请求。当我们访问graphql时，可以看到它的referer为：
    # https://leetcode.com/problems/binary-tree-maximum-path-sum/。
    set_cookie = response.headers["Set-Cookie"]
    print(set_cookie)
    try:
        pattern = re.compile("csrftoken=(.*?);.*?", re.S)
        csrf_token = re.search(pattern, set_cookie)
        print(csrf_token.group(1))
        url = "https://leetcode.com/graphql"
        # 通过GraphQL的语法来进行查询，它是一种用于api的查询语言
        params = {"operationName": "getLikesAndFavorites",
                  "variables": {"titleSlug": title},
                  "query": "query getLikesAndFavorites($titleSlug: String!) "
                           "{\n  "
                               "question(titleSlug: $titleSlug) "
                               "{\n"
                                   "questionId\n"
                                   "likes\n"
                                   "dislikes\n"
                                   "isLiked\n"
                                   "__typename\n"
                               "}\n "
                           "}\n "
                 }
        headers = {
            'x-csrftoken': csrf_token.group(1),
            'referer': problem_url,
            'content-type': 'application/json',
            'origin': 'https://leetcode.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
        cookies = {'__cfduid': 'd9ce37537c705e759f6bea15fffc9c58b1525271602',
                   '_ga': 'GA1.2.5783653.1525271604',
                   '_gid': 'GA1.2.344320119.1533189808',
                   'csrftoken': csrf_token.group(1),
                   ' _gat': '1'
        }
        dump_json_data = json.dumps(params)
        response = requests.post(url, data=dump_json_data, headers=headers, cookies=cookies)
        info = json.loads(response.text)
        print(info)
        likes = info["data"]["question"]["likes"]
        dislikes = info["data"]["question"]["dislikes"]
        print("Problem: " + title + " has " + str(likes) + " likes and " + str(dislikes) + " dislikes")
    except Exception as e:
        print(e)
        print("error：" + problem_url)


def main():
    url = "https://leetcode.com/api/problems/all/"
    html = json.loads(get_problem_set(url))
    problem_set = html["stat_status_pairs"]
    all_problem_titles = parse_problem_set(problem_set)
    todo = all_problem_titles[:2]
    for i in todo:
        construct_url(i)
    # problem_title = 'two-sum'
    # url = "https://leetcode.com/problems/" + problem_title + "/description/"
    # get_problem_content(url, problem_title)


if __name__ == '__main__':
    main()

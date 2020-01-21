import requests
import json
import time
import sys
import os

# argument check
if len(sys.argv) != 3:
    print("Usage: python crawler.py <article_size> <save_path>")
    sys.exit()

article_size = sys.argv[1]
save_path = sys.argv[2]

# get article list
url = "https://www.bigkinds.or.kr/api/news/search.do"
data = {
    "indexName": "news",
    "searchKey": "",
    "searchKeys": [{}],
    "searchSortType": "date",
    "sortMethod": "date",
    "categoryCodes": ["003000000", "003007000", "003003000",
                      "003006000", "003002000", "003009000",
                      "003001000", "003005000", "003010000",
                      "003008000", "003004000"],
    "incidentCodes": [4, 12, 49, 50, 51, 52, 53, 13, 54, 55,
                      56, 57, 58],
    "startNo": 1,
    "resultNumber": article_size
}

resp = requests.post(url, json.dumps(data))
results = json.loads(resp.text).get("resultList")
links = map(lambda r: r.get("NEWS_ID"), results)

# get article contents and save
url = "https://www.bigkinds.or.kr/news/detailView.do"
for link in links:
    def try_request(link):
        try:
            return requests.get(url, {"docId": link})
        except requests.ConnectionError as e:
            time.sleep(2)
            return try_request(link)

    resp = try_request(link)
    raw_article = json.loads(resp.text)

    print("id: {}, title: {}\n".format(
        link, raw_article.get("detail").get("TITLE")))

    with open(os.path.join(save_path, link + ".story"), "w", encoding="utf-8") as f:
        f.write("@title\n")
        f.write(raw_article.get("detail").get("TITLE") + "\n")
        f.write("@content\n")
        f.write(raw_article.get("detail").get("CONTENT"))

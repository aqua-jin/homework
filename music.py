from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# 아래 빈 칸('')을 채워보세요
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20201015', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

#곡순위 body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
# 곡순위 랭크+랭크변동 까지 나옴! 문자열 슬라이싱
#곡제목 body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#가수 body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis

trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
for tr in trs:
    rank = tr.select_one('td.number').text[0:2].strip()
# 슬라이싱 == 문자열 범위 지정 [부터:까지] ( [0:2] 0~2문자열만 가져옴)
    artist = tr.select_one('td.info > a.artist.ellipsis').text
    title = tr.select_one('td.info > a.title.ellipsis').text.strip()
    # print(rank, title, artist)

    doc = {
        'rank' : rank,
        'title' : title,
        'artist' :artist
    }
    db.music.insert_one(doc)
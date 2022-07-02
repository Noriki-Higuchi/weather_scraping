import requests
import psycopg2
import datetime
import csv
import sys
from bs4 import BeautifulSoup


def connect_db():
    try:
        dsn = "dbname=sample user=postgres password="
        conn = psycopg2.connect(dsn)
        return conn
    except:
        print("データベース接続に失敗しました")
        sys.exit()


def insert_weather(AreaCode):
    try:
        url = "https://weather.yahoo.co.jp/weather/jp/13/" + \
            str(AreaCode) + ".html"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        rs = soup.find(class_='forecastCity')
        rs = [i.strip() for i in rs.text.splitlines()]
        rs = [i for i in rs if i != ""]
    except:
        print("天気情報の取得に失敗しました")
        sys.exit()
    """ print(rs[0] + "の天気は" + rs[1] + "、明日の天気は" + rs[19] + "です。") """

    time_now = datetime.datetime.now()
    time_str = str(time_now)[:-7]
    time_datetime = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

    conn = connect_db()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO weather (today_weather, tomorrow_weather, area, time) VALUES (%s, %s, %s, %s)",
                    (rs[1], rs[19], AreaCode, time_datetime))
        conn.commit()
        cur.close()
        conn.close()
    except:
        print("データベースに情報を追加できませんでした")
        sys.exit()


def select_weather():
    conn = connect_db()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM weather;")
        weather_data = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
    except:
        print("データベースから情報を取得できませんでした")
        sys.exit()

    try:
        f = open('weather.csv', 'w', newline='')
        writer = csv.writer(f)
        writer.writerows(weather_data)
        f.close()
    except:
        print("CSV出力に失敗しました")


insert_weather(4410)
select_weather()

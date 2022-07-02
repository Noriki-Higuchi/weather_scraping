import requests
import psycopg2
import datetime
import csv
from bs4 import BeautifulSoup


def connect_db():
    dsn = "dbname=sample user=postgres password="
    conn = psycopg2.connect(dsn)
    return conn


def insert_weather(AreaCode):
    url = "https://weather.yahoo.co.jp/weather/jp/13/" + \
        str(AreaCode) + ".html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    rs = soup.find(class_='forecastCity')
    rs = [i.strip() for i in rs.text.splitlines()]
    rs = [i for i in rs if i != ""]
    """ print(rs[0] + "の天気は" + rs[1] + "、明日の天気は" + rs[19] + "です。") """

    time_now = datetime.datetime.now()
    time_str = str(time_now)[:-7]
    time_datetime = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO weather (today_weather, tomorrow_weather, area, time) VALUES (%s, %s, %s, %s)",
                (rs[1], rs[19], AreaCode, time_datetime))
    conn.commit()
    cur.close()
    conn.close()


def select_weather():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM weather;")
    weather_data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    f = open('weather.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerows(weather_data)
    f.close()


insert_weather(4410)
select_weather()

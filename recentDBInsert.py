import pandas as pd
import mysql.connector
from datetime import datetime
from pytz import timezone
import os

user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
host = os.environ['DB_URL']
port = os.environ['DB_PORT']
database = "toonovel"

seoul_timezone = timezone('Asia/Seoul')
current_date = datetime.now(seoul_timezone).date()
date = current_date.strftime("%Y%m%d").strip()


def connect_to_database():
    return mysql.connector.connect(user=user, password=password, host=host, database=database, port=port)

def close_connection(cnx):
    cnx.close()

def execute_query(cnx, sql, val):
    cursor = cnx.cursor()
    cursor.execute(sql, val)
    cnx.commit()
    novel_id = cursor.lastrowid
    cursor.close()
    return novel_id

def fetch_one(cnx, sql, val):
    cursor = cnx.cursor()
    cursor.execute(sql, val)
    result = cursor.fetchone()
    cursor.close()
    return result

def fetch_all(cnx, sql, val):
    cursor = cnx.cursor()
    cursor.execute(sql, val)
    result = cursor.fetchall()
    cursor.close()
    return result

def insert_novel(cnx, title, author, description, genre, image, user_id):
    sql = "INSERT INTO novel (title, author, description, genre, image, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (title, author, description, genre, image, user_id)
    return execute_query(cnx, sql, val)

def insert_novel_platform(cnx, novel_id, platform_id, url):
    sql = "INSERT INTO novel_platform (novel_id, platform_id, url) VALUES (%s, %s, %s)"
    val = (novel_id, platform_id, url)
    execute_query(cnx, sql, val)

def update_novel_genre(cnx, novel_id, genre):
    sql = "UPDATE novel SET genre = %s WHERE novel_id = %s"
    val = (genre, novel_id)
    execute_query(cnx, sql, val)

def import_csv(cnx, csv, platform_id):
    df = pd.read_csv(csv, encoding='utf-8')

    titles = df['제목'].tolist()
    authors = df['작가'].tolist()
    descriptions = df['소개'].tolist()
    genres = df['장르'].tolist()
    urls = df['링크'].tolist()
    images = df['이미지'].tolist()

    sql = "SELECT user_id, nickname FROM enroll_history WHERE is_approval = 1"
    enroll_history_result = fetch_all(cnx, sql, None)

    enroll_data = {nickname: user_id for user_id, nickname in enroll_history_result}

    for i in range(len(df)):
        title = titles[i]
        author = authors[i]
        description = descriptions[i]
        genre = genres[i]
        url = urls[i]
        image = images[i]
        user_id = enroll_data.get(author)

        sql = "SELECT novel_id FROM novel WHERE title = %s AND author = %s"
        val = (title, author)
        result = fetch_one(cnx, sql, val)

        if result is None:
            novel_id = insert_novel(cnx, title, author, description, genre, image, user_id)
            insert_novel_platform(cnx, novel_id, platform_id, url)
        else:
            novel_id = result[0]
            sql = "SELECT * FROM novel_platform WHERE novel_id = %s AND platform_id = %s"
            val = (novel_id, platform_id)
            result = fetch_all(cnx, sql, val)

            if not result:
                insert_novel_platform(cnx, novel_id, platform_id, url)
            else:
                insert_novel_platform(cnx, novel_id, platform_id, url)
                # 네이버 시리즈 데이터 삽입에만 작동, 시리즈 기준으로 장르 맞추기위함
                if platform_id == 1:
                    update_novel_genre(cnx, novel_id, genre)

try:
    cnx = connect_to_database()

    mycursor = cnx.cursor()
    mycursor.execute("ALTER TABLE novel MODIFY created_date DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6)")
    mycursor.execute("ALTER TABLE novel MODIFY modified_date DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)")
    cnx.commit()
    mycursor.close()

    munpia_csv = date + 'munpia.csv'
    import_csv(cnx, munpia_csv, 3)

    kakao_csv = date + 'page.csv'
    import_csv(cnx, kakao_csv, 2)

    naver_csv = date + 'series.csv'
    import_csv(cnx, naver_csv, 1)

finally:
    close_connection(cnx)

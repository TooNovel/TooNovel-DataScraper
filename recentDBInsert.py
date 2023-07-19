import pandas as pd
import mysql.connector
from datetime import datetime
from pytz import timezone
import os

user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
host = os.environ['DB_URL']
port = os.environ['DB_PORT']

cnx = mysql.connector.connect(user=user, password=password, host=host, database='toonovel', port=port)

seoul_timezone = timezone('Asia/Seoul')
current_date = datetime.now(seoul_timezone).date()
date = current_date.strftime("%Y%m%d").strip()
mycursor = cnx.cursor()

mycursor.execute("ALTER TABLE novel MODIFY created_date DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6)")
mycursor.execute("ALTER TABLE novel MODIFY modified_date DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)")
cnx.commit()

munpia_df = pd.read_csv(date+'munpia.csv', encoding='utf-8')

title = munpia_df['제목'].tolist()
author = munpia_df['작가'].tolist()
description = munpia_df['소개'].tolist()
genre = munpia_df['장르'].tolist()
url = munpia_df['링크'].tolist()
image = munpia_df['이미지'].tolist()

for v in range(len(munpia_df)):
    sql = "SELECT novel_id FROM novel WHERE title = %s AND author = %s"
    val = (title[v], author[v])
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if result is None:
        sql = "INSERT INTO novel (title, author, description, genre, image) VALUES (%s, %s, %s, %s, %s)"
        val = (title[v], author[v], description[v], genre[v], image[v])
        mycursor.execute(sql, val)
        cnx.commit()
        novel_id = mycursor.lastrowid
        sql = "INSERT INTO novel_platform (novel_id, platform_id, url) VALUES (%s, %s, %s)"
        val = (novel_id, 3, url[v])
        mycursor.execute(sql, val)
        cnx.commit()
    else:
        novel_id = result[0]
        sql = "SELECT * FROM novel_platform WHERE novel_id = %s AND platform_id = 3"
        val = (novel_id,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()

        if not result:
            sql = "INSERT INTO novel_platform (novel_id, platform_id, url) VALUES (%s, %s, %s)"
            val = (novel_id, 3, url[v])
            mycursor.execute(sql, val)
            cnx.commit()  

kakao_df = pd.read_csv(date+'page.csv', encoding='utf-8')

title = kakao_df['제목'].tolist()
author = kakao_df['작가'].tolist()
description = kakao_df['소개'].tolist()
genre = kakao_df['장르'].tolist()
url = kakao_df['링크'].tolist()
image = kakao_df['이미지'].tolist()

for v in range(len(kakao_df)):
    sql = "SELECT novel_id FROM novel WHERE title = %s AND author = %s"
    val = (title[v], author[v])
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if result is None:
        sql = "INSERT INTO novel (title, author, description, genre, image) VALUES (%s, %s, %s, %s, %s)"
        val = (title[v], author[v], description[v], genre[v], image[v])
        mycursor.execute(sql, val)
        cnx.commit()
        novel_id = mycursor.lastrowid
        sql = "INSERT INTO novel_platform (novel_id, platform_id, url) VALUES (%s, %s, %s)"
        val = (novel_id, 2, url[v])
        mycursor.execute(sql, val)
        cnx.commit()
    else:
        novel_id = result[0]
        sql = "SELECT * FROM novel_platform WHERE novel_id = %s AND platform_id = 2"
        val = (novel_id,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()

        if not result:
            sql = "INSERT INTO novel_platform (novel_id, platform_id, url) VALUES (%s, %s, %s)"
            val = (novel_id, 2, url[v])
            mycursor.execute(sql, val)
            cnx.commit()

naver_df = pd.read_csv(date+'series.csv', encoding='utf-8')

title = naver_df['제목'].tolist()
author = naver_df['작가'].tolist()
description = naver_df['소개'].tolist()
genre = naver_df['장르'].tolist()
url = naver_df['링크'].tolist()
image = naver_df['이미지'].tolist()

for v in range(len(naver_df)):
    sql = "SELECT novel_id FROM novel WHERE title = %s AND author = %s"
    val = (title[v], author[v])
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if result is None:
        sql = "INSERT INTO novel (title, author, description, genre, image) VALUES (%s, %s, %s, %s, %s)"
        val = (title[v], author[v], description[v], genre[v], image[v])
        mycursor.execute(sql, val)
        cnx.commit()
        novel_id = mycursor.lastrowid
        sql = "INSERT INTO novel_platform (novel_id, platform_id, url) VALUES (%s, %s, %s)"
        val = (novel_id, 1, url[v])
        mycursor.execute(sql, val)
        cnx.commit()
    else:
        novel_id = result[0]
        sql = "SELECT * FROM novel_platform WHERE novel_id = %s AND platform_id = 1"
        val = (novel_id,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()

        if not result:
            sql = "UPDATE novel SET genre = %s WHERE novel_id = %s"
            val = (genre[v], novel_id)
            mycursor.execute(sql, val)
            cnx.commit()
            sql = "INSERT INTO novel_platform (novel_id, platform_id, url) VALUES (%s, %s, %s)"
            val = (novel_id, 1, url[v])
            mycursor.execute(sql, val)
            cnx.commit()

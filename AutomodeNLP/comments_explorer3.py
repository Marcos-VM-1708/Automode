import sys
import requests
import time
import mysql.connector
import json
import re
from api import Api
from emotes import emotes


def video_extractor():
    next_page_token = ''
    videos = []
    while True:
        request = api.videos().list(
            part="id",
            maxResults=50,
            chart="mostPopular",
            regionCode="BR",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            videos.append(item["id"])

        try:
            next_page_token = response["nextPageToken"]
        except KeyError:
            break
    return videos


def verify_dataset(id, cursor):
    # VERIFICAÇÃO SE O VIDEO_ID JA EXISTE NO BANCO DE DADOS
    query = "SELECT COUNT(*) FROM videos WHERE id_video = '%s'" % id
    cursor.execute(query)
    # Obter o resultado
    result = cursor.fetchone()

    return result


def search_videos(video, cursor):
    related_videos_id = []

    request = api.search().list(
        part="snippet",
        maxResults=50,
        order="viewCount",
        regionCode="BR",
        relatedToVideoId=video,
        relevanceLanguage="pt",
        type="video"
    )
    try:
        response = request.execute()
    except Exception as e:
        if str(e) == "Quota Exceeded":
            try:
                print('Trocando de key!')
                api_builder.key = 'AIzaSyAtByI38jNLXEGi2vJmjwV5T-NZz4yhpCw'
            except Exception as e:
                if str(e) == "Quota Exceeded":
                    print('Toda as quotas foram usadas, encerrando programa...')
                    sys.exit()
    else:
        for item in response["items"]:
            # Executar a consulta SQL
            result = verify_dataset(item["id"]["videoId"], cursor)

            # Verificar se o valor existe na coluna
            if result[0] > 0:  # Se já existir ele vai cair no if, se nao existir cai no else.
                print("|SEARCH| O vídeo já está no banco de dados")
                continue
            else:
                related_videos_id.append(item["id"]["videoId"])
                print("|SEARCH| O vídeo não está no banco de dados")

    return related_videos_id


def request_comments(video_id, cont_comments, max_comments, switch):
    response = requests.get(
        f"http://ec2-23-20-119-140.compute-1.amazonaws.com:3000/videoCC/{video_id}")
    comments = []

    if response.status_code == 200:  # código de status HTTP > requisição bem sucedida
        response = response.json()

        for comment in response["analyse"]:
            if cont_comments < max_comments:
                comments.append(clean_comment(comment["comment"]))
                cont_comments += 1
            else:
                switch = False
                break
    else:
        print("NÃO FOI POSSÍVEL EXTRAIR OS COMENTÁRIOS DO VÍDEO")

    return comments, cont_comments, switch


def initialize_search(cursor, cont2):
    query = "SELECT id_video FROM videos"
    cursor.execute(query,)
    rows = cursor.fetchall()
    counter = 0

    for row in rows:
        if counter == cont2:
            id_row = row[0]
            return search_videos(id_row, cursor)

        counter += 1


def clean_comment(comment):
    regex = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]|@[A-Za-z]+|\\[a-zA-Z]|)"
    comment = re.sub(regex, '', comment)

    special_characters = r"!@#$%^&*()_+-=[]{}\\|;':\",./<>?"
    vowels = r"áàãâeéèêiíìîoóòõôuúùûÁÀÃÂEÉÈÊIÍÌÎOÓÒÕÔUÚÙÛ"
    emojis = emotes()
    emoji_codes = [emoji.encode("unicode-escape").decode("utf-8") for emoji in emojis]
    allowed_characters = f"[{special_characters}]+"
    allowed_vowels = f"[{vowels}]+"
    emoji_pattern = "|".join(emoji_codes)
    allowed_pattern = f"(({allowed_characters})|({allowed_vowels})|ç|({emoji_pattern}))"

    comment = re.sub(fr"(?!({allowed_pattern}))([^\x00-\x7f])", " ", comment)
    comment = " ".join(comment.split())
    return comment


def comments_extractor(videos, cursor, cnx):
    cont2 = -1
    cont_comments = 0
    switch = True  # Verificar se o limite de comentários foi atingido

    max_comments = int(input('Quantidade de comentários a serem extraídos: '))

    while cont_comments < max_comments:
        if cont2 > -1:
            videos.clear()
            videos.extend(initialize_search(cursor, cont2))

        # Vídeos momentâneos
        for video_id in videos:
            # VERIFICAÇÃO SE O VIDEO_ID JA EXISTE NO BANCO DE DADOS
            result = verify_dataset(video_id, cursor)
            # Verificar se o valor existe na coluna
            if result[0] > 0:  # Se já existir ele vai cair no if, se nao existir cai no else.
                print("O vídeo já está no banco de dados \n___PULANDO PARA O PROXIMO VIDEO___")
                continue
            else:
                print(f"O vídeo {video_id} NÃO está no banco de dados,\n___EXTRAINDO "
                      f"COMENTARIOS___ ....")
                pass

            comments, cont_comments, switch = request_comments(
                video_id, cont_comments, max_comments, switch)

            print(f"{cont_comments} comentários adicionados...")
            # nesse momento, todos os comentários já foram extraídos

            # inserindo os dados no banco de dados
            if comments:
                query = "INSERT INTO videos (id_video, comentarios) VALUES (%s, %s)"
                cursor.execute(query, (video_id, json.dumps(comments),))
                cnx.commit()

            if not switch:
                break

        cont2 += 1
        print(cont2)

    return cont_comments


def count_comments_sql(cursor):
    # Execute the SELECT query
    cursor.execute("SELECT id_video, LENGTH(comentarios) - LENGTH(REPLACE(comentarios, ',', '')) + 1 AS comment_count FROM videos")

    # Fetch all the rows
    rows = cursor.fetchall()
    total = 0
    # Print the results
    for row in rows:
        print(f"id_video: {row[0]}, comment_count: {row[1]}")
        total += row[1]
    print(total)


def main():
    cnx = mysql.connector.connect(user='usermaster', password='Nrs5JCTnX6H4dOcf5GsY',
                                  host='db-test.cox6pxql4lf9.us-east-1.rds.amazonaws.com',
                                  database='AWS')
    cursor = cnx.cursor()

    start = time.time()

    videos = video_extractor()
    cont_comments = comments_extractor(videos, cursor, cnx)

    count_comments_sql(cursor)

    cursor.close()
    cnx.close()

    print(f"Total de {cont_comments} comentários adicionados!")

    end = time.time()
    exec_time = end - start
    print(f"Tempo de execução: {exec_time:.2f}s ")


if __name__ == "__main__":
    dev_key = 'AIzaSyC-IGrurz9MApvHsM6WQ1BTtmVX7rnV9Co'
    api_builder = Api(dev_key)
    api = api_builder.build()
    main()

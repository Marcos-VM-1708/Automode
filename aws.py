import mysql.connector
import json
import pandas as pd


cnx_silver = mysql.connector.connect(user='Aut0m0D3_m4ster', password='OVcp5j9HOqeAzd1y1t9i',
                                         host=
                                         'automode-db.clkkiaxyfcfw.us-east-1.rds.amazonaws.com',
                                         database='API-silver')

# Cria cursores para executar as queries

cursor_silver = cnx_silver.cursor()

# query = f"SELECT id_video, comentarios FROM video"
# cursor_silver.execute(query)
# # results == comentarios silver
# result = cursor_silver.fetchone()


query = f"SELECT * FROM video"
cursor_silver.execute(query)
rows = cursor_silver.fetchall()

df = pd.DataFrame(rows, columns=["id_video", "comentarios"])
df["comentarios"] = df["comentarios"].apply(lambda x: json.loads(x))

print(df["comentarios"].describe())
print(df.head())


meu_array = json.loads(result[1])

print(len(meu_array))

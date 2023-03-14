import mysql.connector
import json
import pandas as pd
#-----------------------------------------------------------
# importa dados direto da aws

cnx_silver = mysql.connector.connect(user='Aut0m0D3_m4ster', password='OVcp5j9HOqeAzd1y1t9i',
                                         host=
                                         'automode-db.clkkiaxyfcfw.us-east-1.rds.amazonaws.com',
                                         database='API-silver')

cursor_silver = cnx_silver.cursor()

query = f"SELECT * FROM video"
cursor_silver.execute(query)
rows = cursor_silver.fetchall()

df = pd.DataFrame(rows, columns=["id_video", "comentarios"])
df["comentarios"] = df["comentarios"].apply(lambda x: json.loads(x))

df = df["comentarios"]

#-----------------------------------------------------------
# retorna uma lista com todos os dodoa da aws:
def open_data(data):
    df = []
    for i in data:
        for n in i:
          df.append(n)
    return df

data = open_data(df)

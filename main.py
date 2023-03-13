import openai
import time
import pandas as pd
import mysql.connector
import json


#-----------------------------------------------------------
# aws data:

cnx_silver = mysql.connector.connect(user='Aut0m0D3_m4ster', password='OVcp5j9HOqeAzd1y1t9i',
                                         host=
                                         'automode-db.clkkiaxyfcfw.us-east-1.rds.amazonaws.com',
                                         database='API-silver')

# Cria cursores para executar as queries

cursor_silver = cnx_silver.cursor()

query = f"SELECT id_video, comentarios FROM video"
cursor_silver.execute(query)
# results == comentarios silver
result = cursor_silver.fetchone()

result = json.loads(result[1])

#-----------------------------------------------------------
# open data:

df_1 = pd.read_csv("AutomodeNLP/comentarios1.csv")
df_2 = pd.read_csv("AutomodeNLP/comentarios2.csv")

df_1 = df_1[:10000]
df_2 = df_1[:10000]

#-----------------------------------------------------------
# request gpt:

# key_user
openai.api_key = "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"

def request(messages):
    # api log
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= messages,
        max_tokens=1024,
        temperature=0.5
    )
    # request
    return [response.choices[0].message.content, response.usage]

#-----------------------------------------------------------
inicio = time.time()
comentarios = []
gpt_result = []

for i in range(0, len(result)):
    coment = result[i:i+10]

    # contexto:
    mensagens = [{"role": "system",
                  "content": "voce é um interpletador de sentimentos, seu obijetivo é classificar em positivo, negativo ou neutro os textos enseridos, retorne apenas o sentimento do texto, caso vc não consigua identificar o sentimento apenas retorne 0"}]
    comentarios.append(str(coment))
    mensagens.append({"role": "user", "content": str(coment)})
    try:
        temp = request(mensagens)
        gpt_result.append(temp[0])
        print(temp[0])
        print(mensagens)
        print(i)
    except ValueError:
        break

    except:
        print("aguardando limite")
        fim = time.time()
        time.sleep(60 - (fim - inicio))

#---------------------------------------------------

print(comentarios)
print(gpt_result)


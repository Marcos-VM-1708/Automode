# bibliophiles:
import openai
import time
import pandas as pd
import mysql.connector
import json
# ------------------------------------#
# rules:
openai.api_key = "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" #key api_gpt
tam_request = 10
# ------------------------------------#
# open data:
cnx_silver = mysql.connector.connect(user="Aut0m0D3_m4ster",
                                     password="OVcp5j9HOqeAzd1y1t9i",
                                     host="automode-db.clkkiaxyfcfw.us-east-1.rds.amazonaws.com",
                                     database="API-silver")

# cria cursor support p/ query:
query = f"SELECT id_video, comentarios FROM video"
cursor_silver = cnx_silver.cursor()
cursor_silver.execute(query)

# results == comentarios silver
result = cursor_silver.fetchone()
result = json.loads(result[1])

# ------------------------------------#
# gpt request:
def request(messages):
    # api log:
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages= messages,
                                            max_tokens=1024,
                                            temperature=0.5)
    # request:
    return [response.choices[0].message.content, response.usage]

# ------------------------------------#
# process:

comentarios = []
gpt_result = []

inicio = time.time()

for i in range(0, len(result), tam_request):

    coment = result[i:i + tam_request]

    mensagens = [{"role": "system",
                  "content": "preciso que você interplete o sentimento desses textos, retorne apenas positivo, neutro, negativo e 0 caso vc não consigua identificar, escreva o resultado em um formato de lista separado por virgula e sem ponto final "}]

    comentarios.extend(coment)
    mensagens.append({"role": "user", "content": str(coment)})


    try:
        temp = request(mensagens)
        gpt_result.append(temp[0])
        print(temp[0])  # diagnostico
        print(coment)   #comentarios
        print()

    except ValueError:
        fim = time.time()
        print(f"tempo de execução: {fim-inicio}")
        break

    except:
        print("aguardando limite")
        fim = time.time()
        time.sleep(70 - (fim - inicio))

# ------------------------------------#
diagnostico = []
for elemento in gpt_result:
    palavras = elemento.split(',')
    palavras = [palavra.strip('.') for palavra in palavras]
    diagnostico.extend(palavras)

print(f"{diagnostico} tamanho{len(diagnostico)}")
print(f"{comentarios} tamanho{len(comentarios)}")
# ------------------------------------#
# close:
if len(diagnostico) == len(comentarios):
    df = pd.DataFrame((comentarios,diagnostico), columns = ["comentarios", "diagnostico"])

    pd.to_csv(df)
else:
    print("que merda")
# ------------------------------------#
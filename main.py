import aws
import time
import openai
from joblib import parallel, delayed

start_time = time.perf_counter()

df = aws.data
openai.api_key = "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"

def request(messages):
    # api log:
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages= messages,
                                            max_tokens=2024,
                                            temperature=0.5)

    # request:
    return [response.choices[0].message.content, response.usage]

inicio = time.time()
def vai_com(i):

    cont = 10
    coment = df[i:i + 10]
    mensagens = [{"role": "system",
                  "content": "preciso que você interplete o sentimento desses textos, retorne apenas positivo, neutro, negativo e 0 caso vc não consigua identificar, escreva o resultado em um formato de lista separado por virgula e sem ponto final "},
                 {"role": "user", "content": str(coment)}]

    if len("".join(coment)) > 600:
        try:
            temp = request(mensagens)
            cont = cont + 10

        except openai.error.InvalidRequestError:
            return "deu merda aqui poha"


        except ValueError:
            return"deu merda aqui"


        except openai.error.RateLimitError:
            print("esperando request :(")
            fim = time.time()
            print(fim - inicio)
            time.sleep(65)

        return coment, temp[0], cont

resultado = parallel(n_jobs = -1)(delayed(vai_com)(i)for i in range(0, len(df), 10))
print(f"{resultado}\n")

end_time = time.perf_counter()
print(f"Fim do segundo timer. Tempo de execução: {end_time - start_time:+.4f} segundos")

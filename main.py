import aws
import time
import openai

start_time = time.perf_counter()

df = aws.data
openai.api_key = "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"
def request(messages):
    # api log:
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301",
                                            messages= messages,
                                            max_tokens=1024,
                                            temperature=0.5)

    # request:
    return [response.choices[0].message.content, response.usage]

inicio = time.time()
for i in range(0, len(df), 10):
    coment = df[i:i + 10]
    mensagens = [{"role": "system",
                  "content": "preciso que você interplete o sentimento desses textos, retorne apenas positivo, neutro, negativo e 0 caso vc não consigua identificar, escreva o resultado em um formato de lista separado por virgula e sem ponto final "},
                 {"role": "user", "content": str(coment)}]

    if len("".join(coment)) > 600:
        try:
            temp = request(mensagens)
            print(coment)
            print(f"{temp[0]}\n")
            print(i)

        except ValueError:
            print("deu merda aqui")

        except openai.error.RateLimitError:
            print("esperando request :(")
            fim = time.time()
            time.sleep(60 - (fim - inicio))
            continue











end_time = time.perf_counter()
print(f"Fim do segundo timer. Tempo de execução: {end_time - start_time:+.4f} segundos")
import openai
import time
import random
import pandas as pd

#--------------------------------------------------

openai.api_key = "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"

def gerar_resposta(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= messages,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

mensagens = [{"role": "system", "content": "voce é um interpletador de sentimentos, seu obijetivo é classificar em positivo, negativo ou neutro os textos enseridos"}]

while True:
    # Ask a question
    question = input("texto: (\"sair\"): ")


    mensagens.append({"role": "user", "content": str(question)})

    answer = gerar_resposta(mensagens)
    print("enviado:", question)
    print("ChatGPT:", answer[0], "\nCusto:\n", answer[1])


    debugar = False

    if debugar:
        print("Mensagens", mensagens, type(mensagens))


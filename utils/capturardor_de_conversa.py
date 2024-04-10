import utils.convert_json as cj
import json
from datetime import datetime

def __converter_historico(history):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    return history_openai_format


def salvar_historico(history, nome_arquivo = "process_data\\conversas\\conversa-"):
    historico_convertido = __converter_historico(history)
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo_saida = nome_arquivo + formatted_date + ".json"
    cj.salvar_json(historico_convertido,nome_arquivo_saida)
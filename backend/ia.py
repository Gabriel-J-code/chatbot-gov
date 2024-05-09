from openai import OpenAI
import json
from utils.convert_json import converter_aquivo_para_json

class ia:
   
    def __init__(self, openai_key, contexto, model='gpt-3.5-turbo', temperature = 0.75):        
        if (contexto[-4:] == ".txt"):
            contexto = converter_aquivo_para_json(contexto)
        elif (contexto[-5:] == ".json"):
            with open(contexto, 'r', encoding='utf-8') as arquivo_c:
                contexto = json.loads(arquivo_c.read())       
        self.historico = [contexto]            
        self.model = model
        self.temperature = temperature
        self.key = openai_key        
        self.client = OpenAI(api_key= openai_key)
        
    def reset(self):
        if (not self.client.is_closed()):
            self.client.close()
        self.client = OpenAI(api_key=self.key)
       
                
    def responder(self, mensagem):
        
        self.historico.append({"role": "user", "content": mensagem })

        response = self.client.chat.completions.create(
            model= self.model,
            messages= self.historico,
            temperature = self.temperature,
            stream=True
        )

        self.historico.append({"role": "assistant", "content": "" })
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                self.historico[-1]["content"] = self.historico[-1]["content"] + chunk.choices[0].delta.content
                yield self.historico[-1]["content"]
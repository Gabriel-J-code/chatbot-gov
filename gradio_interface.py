import gradio as gr  
from backend.ia import ia
from dotenv import load_dotenv
import os
import json
from utils.convert_json import converter_aquivo_para_json
from frontend.gov_theme import logo, theme, title, descricao

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(os.getcwd(), 'config', '.env'))

# Agora você pode acessar sua chave da OpenAI como uma variável de ambiente
openai_key = os.getenv('OPENAI_API_KEY')
contexto = converter_aquivo_para_json("process_data/processoRenovacaoCNH.txt")
with open('process_data/processoRenovacaoCNH.json', 'r', encoding='utf-8') as arquivo:
    contexto = json.loads(arquivo.read())

ia_model = ia(openai_key,contexto)

def user(user_message, history):
    return "", history + [[user_message, ""]]

'''
def upload_file(files, history):
    file_paths = [file.name for file in files]
    history = history + [[file_paths, "O tratamento de aquivos ainda esta em desenvolvimento"]]
    return history
'''

def respond(history):
    mensagem = history[-1][0] 
    resposta = ia_model.responder(mensagem)       
    for chunk in resposta: 
        history[-1][1] = chunk                  
        yield history   


with gr.Blocks(theme= theme,title= title, css="frontend/gradio.css",fill_height= True)as demo:
    gr.Image(value="frontend/image/gov/barra_cores_gov_pb.png", height= "10px",show_download_button= False, show_label=False, scale= 1)
    gr.Image(value = logo,width="200px",label="logo", show_download_button= False, show_label=False,elem_classes="logo", scale= 5)
    gr.Textbox(value= descricao, elem_classes="subtitle", show_label= False, interactive= False, show_copy_button= False, max_lines= 1)
    with gr.Column(variant="default", scale=45, elem_classes= "painel"):
        with gr.Row(variant="panel", elem_classes= "row-chat"):
            chatbot = gr.Chatbot(label="Chat", height= "350px", elem_classes= "chatbot")
        with gr.Row(variant="compact",elem_classes= "row-user"):
            with gr.Column(scale=19):
                msg = gr.Textbox(placeholder="Digite aqui sua duvida", autofocus= True, show_label=False,  elem_classes="textbox", min_width= 62)
            with gr.Column(scale= 1, min_width=5, elem_classes= "button_column"):
                submit = gr.Button("➥",elem_classes=["button","submit"],variant='primary')
                
                upload_button = gr.UploadButton("🗀", file_types=["file"], file_count="multiple",elem_classes="button", interactive=False)
                
            gr.on(
                triggers=[msg.submit, submit.click],
                fn=user,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot],
            ).then(respond,[chatbot], [chatbot])            
            
            #upload_button.upload(upload_file, [upload_button, chatbot] , [chatbot])
            

#demo.launch(share=False)
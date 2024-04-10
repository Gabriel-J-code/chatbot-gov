import gradio as gr  
from backend.ia import ia
from dotenv import load_dotenv
import os, json
from frontend.gov_theme import logo, theme, title, descricao
from utils.capturardor_de_conversa import salvar_historico

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(os.getcwd(), 'config', '.env'))

# Agora você pode acessar sua chave da OpenAI como uma variável de ambiente
openai_key = os.getenv('OPENAI_API_KEY')

ia_classifiquer = ia(openai_key,"process_data/catalogo de serviços.txt")

def user(user_message, history):
    return "", history + [[user_message, ""]]


def classificar(history):
    for i in range(len(history)):
        bot = history[i][1]
        par = "user: " + history[i][0] + ";\n bot: " + history[i][1]
        clasificacao = ia_classifiquer.responder(par) 
        for chunk in clasificacao:
            history[i][1] = chunk + "\n\n" + bot
            yield history
        
def salvar(history):
    salvar_historico(history) 

def importar(file):
    with open(file, 'r', encoding='utf-8') as arquivo_c:
        conversa_json = json.loads(arquivo_c.read()) 
    conversa = []
    par = []
    for message in conversa_json:
        par.append(message["content"])
        if (len(par)==2): 
            conversa.append(par)
            par = []
    return conversa
        
    


with gr.Blocks(theme= theme,title= title, css="frontend/gradio.css",fill_height= True)as demo:
    gr.Image(value="frontend/image/gov/barra_cores_gov_pb.png", height= "10px",show_download_button= False, show_label=False, scale= 1)
    gr.Image(value = logo,width="200px",label="logo", show_download_button= False, show_label=False,elem_classes="logo", scale= 5)
    gr.Textbox(value= descricao, elem_classes="subtitle", show_label= False, interactive= False, show_copy_button= False, max_lines= 1)
    with gr.Column(variant="default", scale=45, elem_classes= "painel"):
        with gr.Row(variant="panel", elem_classes= "row-chat"):
            chatbot = gr.Chatbot(label="Chat", height= "350px", elem_classes= "chatbot")
        with gr.Row(variant="compact",elem_classes= "row-user"):
            with gr.Column(scale=19):
                file = gr.File(file_types=['.json'])
            with gr.Column(scale= 1, min_width=5, elem_classes= "button_column"):                
                
                classificar_button = gr.Button("classificar",elem_classes="button")
                
            gr.on(
                triggers=[file.change],
                fn=importar,
                inputs=[file],
                outputs=[chatbot],
            )          
            
            classificar_button.click(fn=classificar, inputs=chatbot, outputs=chatbot)
            

demo.launch(share=False)
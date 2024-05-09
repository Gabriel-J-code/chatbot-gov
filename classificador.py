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

ia_classifiquer = ia(openai_key,"process_data/catalogo de serviços.txt",model="gpt-4")

def user(user_message, history):
    return "", history + [[user_message, ""]]

def classificar_unidade(history):    
    
    classificacao = []
    for i in range(len(history)):     
        par = "user: " + history[i][0] + ";\n bot: " + history[i][1]
        responser = ia_classifiquer.responder(par)
        for chunk in responser:
            reposta = chunk
        classificacao.append(reposta)
        bot = history[i][1]
        history[i][1] = classificacao[i] + "\n\n" + bot
        yield history 
        
def classificar_par(history):
    ia_classifiquer.reset()
    par = "user: " + history[0][0] + ";\n bot: " + history[0][1]
    responser = ia_classifiquer.responder(par)  
    for chunk in responser:
        reposta = chunk
    classificacao = [reposta]
    bot = history[0][1]
    history[0][1] = classificacao[0] + "\n\n" + bot
    for i in range(len(history)-1):  
        proximo = i + 1      
        par = "user: " + history[i][0] + ";\n bot: " + history[i][1] + ";\nuser: " + history[proximo][0] + ";\n bot: " + history[i+1][1]
        responser = ia_classifiquer.responder(par)
        for chunk in responser:
            reposta = chunk
        classificacao.append(reposta)
        bot = history[proximo][1]
        history[proximo][1] = classificacao[i] + "\n\n" + bot
        yield history        
        
        
def salvar(history,nome_arquivo):
    loc = str(nome_arquivo).find("conversa")
    nome_arquivo = nome_arquivo[loc:-5]
    print(nome_arquivo)
    salvar_historico(history,str(nome_arquivo)+"-classificado-") 

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
        
    
def info_salvar_sucesso():
    gr.Info("Sucesso em salvar")

with gr.Blocks(theme= theme,title= title, css="frontend/gradio.css",fill_height= True)as demo:
    gr.Image(value="frontend/image/gov/barra_cores_gov_pb.png", height= "10px",show_download_button= False, show_label=False, scale= 1)
    gr.Image(value = logo,width="200px",label="logo", show_download_button= False, show_label=False,elem_classes="logo", scale= 5)
    gr.Textbox(value= descricao, elem_classes="subtitle", show_label= False, interactive= False, show_copy_button= False, max_lines= 1)
    with gr.Column(variant="default", scale=45, elem_classes= "painel"):
        with gr.Row(variant="panel", elem_classes= "row-chat"):
            chatbot = gr.Chatbot(label="Chat", height= "350px", elem_classes= "chatbot")
        with gr.Row(variant="compact",elem_classes= "row-user"):
            with gr.Column(scale=19):
                file = gr.File(file_types=['.json'], elem_classes= "file")
            with gr.Column(scale= 1, min_width=5, elem_classes= "button_column"):                
                
                classificar_button = gr.Button("classificar",elem_classes="button")
                
                salvar_button = gr.Button("salvar",elem_classes="button")
                
            gr.on(
                triggers=[file.change],
                fn=importar,
                inputs=[file],
                outputs=[chatbot],
            )          
            
            classificar_button.click(fn=classificar_unidade, inputs=chatbot, outputs=chatbot)
            
            salvar_button.click(fn=salvar, inputs=[chatbot,file]).then(info_salvar_sucesso)
            

demo.launch(share=False)
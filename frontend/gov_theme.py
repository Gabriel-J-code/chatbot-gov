import gradio as gr
contexto = ""

branco= "#ffffff"
amarelo = "#ffe425"
vermelho = "#f72930"
azul = "#399fe8"
azul_2 = "#3A69E8"
azul_3 = "#3AE8C0"
verde = "#00dc58"
preto = "#0f0a0a"
laranja = "#f7c100"
laranja_claro="#f7c100"
rosa= "#cb297b"
azul_violeta = "#797ba9"
verde_escuro= "#01913c"


cor_principal_fundo = branco
cor_principal_painel = amarelo
cor_botão_principal = azul_2
cor_botao_arquivo = azul_3
cor_barra_texto = amarelo
cor_texto_enviado = branco


theme = gr.themes.Soft(
    primary_hue="sky",
    secondary_hue="blue",
    neutral_hue="neutral",
)

theme.set(
    body_text_color='black',
    body_text_color_subdued='black',
    body_background_fill= cor_principal_fundo,
    body_background_fill_dark= cor_principal_fundo,
    background_fill_secondary = cor_principal_painel,
    background_fill_secondary_dark = cor_principal_painel,
    block_background_fill_dark='white',
    block_info_text_color='black',
    input_placeholder_color='gray',
    input_placeholder_color_dark='gray',
    button_primary_background_fill=cor_botão_principal,
    button_primary_background_fill_dark=cor_botão_principal,
    button_secondary_background_fill=cor_botao_arquivo,
    button_secondary_background_fill_dark=cor_botao_arquivo,
    button_secondary_background_fill_hover='gray',
    button_secondary_background_fill_hover_dark='gray',
    button_secondary_border_color='*body_text_color',
    button_secondary_text_color='white',
)

title = "ChatGov"

logo = "https://paraiba.pb.gov.br/marca-do-governo/GovPBT.png"

descricao = "Serviço de assistencia do Governo da Paraiba"

##  ?__theme=light
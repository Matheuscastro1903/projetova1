
import customtkinter as ctk
from PIL import Image



def login():
    pass
def cadastro():
    pass
def condominio():
    pass


#ctk.set_appearance_mode("light")



# Configuração da janela principal
janela = ctk.CTk()
janela.title("ECODROP SYSTEM")
janela.geometry("800x600+400+150")
janela.resizable(False, False)

# Criasse um frame apenas para parte do cabeçalho do topo 
frame_topo = ctk.CTkFrame(janela, fg_color="#1A73E8", height=80)
frame_topo.pack(fill="x")

titulo = ctk.CTkLabel(frame_topo, text="💧 ECODROP", text_color="#f0f0f0", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

# Divisão em colunas principais (menu lateral e conteúdo)
frame_conteudo = ctk.CTkFrame(janela, fg_color="#f0f0f0")
frame_conteudo.pack(fill="both", expand=True)

# Menu lateral
frame_menu = ctk.CTkFrame(frame_conteudo,fg_color="#f0f0f0",width=200)
frame_menu.pack(side="left", fill="y")

# Botões do menu
botao1 = ctk.CTkButton(frame_menu, text="Login", fg_color="#f0f0f0", text_color="#1A73E8",font=("Arial", 12), anchor="w",command=login)
botao1.pack(fill="x", pady=(20, 10), padx=10)

botao2 = ctk.CTkButton(frame_menu, text="Cadastro usuário", fg_color="#f0f0f0", text_color="#1A73E8",font=("Arial", 12), anchor="w",command=cadastro)
botao2.pack(fill="x", pady=10, padx=10)

botao3 = ctk.CTkButton(frame_menu, text="Cadastro condomínio", fg_color="#f0f0f0", text_color="#1A73E8",font=("Arial", 12), anchor="w",command=cadastro)
botao3.pack(fill="x", pady=10, padx=10)

botao4 = ctk.CTkButton(frame_menu, text="Sobre nós", fg_color="#f0f0f0", text_color="#1A73E8",font=("Arial", 12), anchor="w",command=login)
botao4.pack(fill="x", pady=10, padx=10)



# Área principal de conteúdo
frame_principal = ctk.CTkFrame(frame_conteudo,fg_color="#f0f0f0")
frame_principal.pack(side="left", fill="both", expand=True, padx=30, pady=30)


texto_bem_vindo = ctk.CTkLabel(frame_principal, text="Bem-vindo ao sistema ECODROP",text_color="#202124", font=("Arial", 22, "bold"))
texto_bem_vindo.pack(pady=(0, 20))

texto_instrucao = ctk.CTkLabel(frame_principal, text="Menos consumo, mais consciência, um planeta mais feliz.",text_color="#5f6368",wraplength=500,justify="left",font=("Arial", 18))
texto_instrucao.pack()

imagem = Image.open("fotos/mascoteprincipall.png")
ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(400, 400))

label = ctk.CTkLabel(frame_principal, image=ctk_imagem, text="")
label.pack()


# Frame do rodapé
frame_rodape = ctk.CTkFrame(janela, fg_color="white", height=30)
frame_rodape.pack(fill="x", side="bottom")

texto_rodape = ctk.CTkLabel(frame_rodape, text="Versão 2.0 • Suporte: ecodropsuporte@gmail.com",text_color="#5f6368",font=("Arial", 10))
texto_rodape.pack(pady=5)

janela.mainloop()
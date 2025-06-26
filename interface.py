
import customtkinter as ctk
from PIL import Image


#Função para só permitir digitar números
def validar_numeros(novo_texto):  # Adicione o parâmetro
    return novo_texto.isdigit() or novo_texto == ""

#Função para só permitir digitar letras e espaços
def validar_letras_espacos(novo_texto):  # Adicione o parâmetro
    return all(c.isalpha() or c.isspace() for c in novo_texto) or novo_texto == ""


def voltar_inicial():
    
    pass
    
    pass

def login():
    frame_topo.pack_forget()
    frame_menu.pack_forget()
    frame_conteudo.pack_forget()
    frame_login=ctk.CTkFrame(janela,fg_color="#ffffff")
    label_login=ctk.CTkLabel(frame_login,text="Informe seus dados:",fg_color="#ffffff",text_color="blue",font=("Arial", 20))
    label_login.pack(pady=2)
    label_avisologin=ctk.CTkLabel(frame_login,text=" ",fg_color="#ffffff",text_color="blue",font=("Arial", 20))
    label_avisologin.pack(pady=2)

    #1-entrada email
    label_emaillogin = ctk.CTkLabel(frame_login, text="Digite seu email:",text_color="#000000",anchor="w",width=300)
    label_emaillogin.pack(pady=(2, 0))

    entrada_emaillogin = ctk.CTkEntry(frame_login,width=300)
    entrada_emaillogin.pack(pady=2)

    #2-entrada senha
    label_senhalogin = ctk.CTkLabel(frame_login,text="Digite sua senha:",text_color="#000000",anchor="w",width=300)
    label_senhalogin.pack(pady=(2, 0))

    entrada_senhalogin = ctk.CTkEntry(frame_login,width=300,show="*")
    entrada_senhalogin.pack(pady=2)

    #3-entrada email cond
    label_emailcond = ctk.CTkLabel(frame_login, text="Digite o email do seu condomínio:",text_color="#000000",anchor="w",width=300)
    label_emailcond.pack(pady=(2, 0))
    entrada_emailcond = ctk.CTkEntry(frame_login,width=300)
    entrada_emailcond.pack(pady=2)

    #4senha cond
    label_senhacond = ctk.CTkLabel(frame_login,text="Digite a senha do seu condomínio:",text_color="#000000",anchor="w",width=300)
    label_senhacond.pack(pady=(2, 0))

    entrada_senhacond = ctk.CTkEntry(frame_login,width=300,show="*")
    entrada_senhacond.pack(pady=2)



    #botão logar
    botao_logar = ctk.CTkButton(frame_login, text="Logar",fg_color="blue",text_color="#ffffff",width=300,command=conferir_logar)
    botao_logar.pack(pady=2)
    #botão voltar
    botao_voltarinicial=ctk.CTkButton(frame_login, text="Voltar",fg_color="blue",text_color="#ffffff",width=300,command=lambda:voltar_inicial)
    botao_voltarinicial.pack()

    frame_login.pack(fill="both",expand=True)

    pass

def conferir_logar():
    pass
def cadastro_usuario():
    frame_topo.pack_forget()
    frame_menu.pack_forget()
    frame_conteudo.pack_forget()
    frame_cadastro=ctk.CTkFrame(janela,fg_color="#ffffff")
    label_cadastro=ctk.CTkLabel(frame_cadastro,text="Informe seus dados:",fg_color="#ffffff",text_color="blue",font=("Arial", 20))
    label_cadastro.pack(pady=1)


    label_aviso=ctk.CTkLabel(frame_cadastro,text=" ",fg_color="#ffffff",text_color="blue",font=("Arial", 20))
    label_aviso.pack(pady=1)
    
    # 1-Entrada Nome
    label_email = ctk.CTkLabel(frame_cadastro, text="Digite seu email:", text_color="#000000", anchor="w", width=300)
    label_email.pack(pady=(1, 0))

    entrada_email = ctk.CTkEntry(frame_cadastro, width=300)
    entrada_email.pack(pady=1)

    #2-entrada nome da família
    label_nome = ctk.CTkLabel(frame_cadastro, text="Digite o nome da sua família", text_color="#000000", anchor="w", width=300)
    label_nome.pack(pady=(1, 0))

    entrada_nome = ctk.CTkEntry(frame_cadastro, width=300,validate="key",validatecommand=(janela.register(validar_letras_espacos), "%P"))
    entrada_nome.pack(pady=1)

    
    # 3-Entrada Senha
    label_senha = ctk.CTkLabel(frame_cadastro, text="Senha (mínimo 4 caracteres):", text_color="#000000", anchor="w", width=300)
    label_senha.pack(pady=(1, 0))

    entrada_senha = ctk.CTkEntry(frame_cadastro, width=300, show="*")
    entrada_senha.pack(pady=1)

    # 4. Campo Quantidade de membros
    label_qmembros = ctk.CTkLabel(frame_cadastro, text="Quantidade de membros na família:", text_color="#000000", anchor="w", width=300)
    label_qmembros.pack(pady=(1,0))
    entrada_qmembros = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(janela.register(validar_numeros), "%P"))
    entrada_qmembros.pack(pady=1)

    # 5. Número do apartamento
    label_numeroap = ctk.CTkLabel(frame_cadastro, text="Digite o número do seu apartamento", text_color="#000000", anchor="w", width=300)
    label_numeroap.pack(pady=(1, 0))
    entrada_numeroap = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(janela.register(validar_numeros), "%P"))
    entrada_numeroap.pack(pady=1)

    # 6. Código verificador
    label_verificador = ctk.CTkLabel(frame_cadastro, text="Digite seu código verificador(mínimo 4 caracteres):", text_color="#000000", anchor="w", width=300)
    label_verificador.pack(pady=(1, 0))

    entrada_verificador = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(janela.register(validar_numeros), "%P"))
    entrada_verificador.pack(pady=1)

    #7-entrada email condomínio
    label_emailcond = ctk.CTkLabel(frame_cadastro, text="Digite o email do seu condomínio:", text_color="#000000", anchor="w", width=300)
    label_emailcond.pack(pady=(1, 0))

    entrada_emailcond = ctk.CTkEntry(frame_cadastro, width=300)
    entrada_emailcond.pack(pady=1)

    #8-senha condominio
    label_senhacond = ctk.CTkLabel(frame_cadastro, text="Senha do condomínio:", text_color="#000000", anchor="w", width=300)
    label_senhacond.pack(pady=(1, 0))

    entrada_senhacond = ctk.CTkEntry(frame_cadastro, width=300, show="*")
    entrada_senhacond.pack(pady=1)
    
    botao_cadastrar = ctk.CTkButton(frame_cadastro, text="Cadastrar",fg_color="blue",text_color="#ffffff",width=300,command=cadastrar_conta)
    botao_cadastrar.pack(pady=1)

    #botão de voltar
    botao_voltarinicial=ctk.CTkButton(frame_cadastro, text="Voltar",fg_color="blue",text_color="#ffffff",width=300,command=voltar_inicial)
    botao_voltarinicial.pack()

    frame_cadastro.pack(fill="both",expand=True)


    
    pass


def cadastrar_conta():
    pass

def cadastro_cond():
    frame_topo.pack_forget()
    frame_menu.pack_forget()
    frame_conteudo.pack_forget()

    pass
def sobre_nos():
    pass


def resgatar():
    esconder_todos_frames_secundarios()
    frame_resgatar = ctk.CTkFrame(janela, fg_color="#ffffff")
    label_resgatar = ctk.CTkLabel(frame_resgatar, text="Resgatar Recompensas", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
    label_resgatar.pack(pady=20)

    ctk.CTkLabel(frame_resgatar, text="Troque seus pontos por recompensas incríveis!", text_color="#000000").pack(pady=10)
    ctk.CTkLabel(frame_resgatar, text="Seu Saldo Atual: [X] Pontos", text_color="#000000", font=("Arial", 16, "bold")).pack(pady=5)

    ctk.CTkLabel(frame_resgatar, text="Recompensas Disponíveis:", text_color="#000000").pack(pady=(10, 0))
    ctk.CTkLabel(frame_resgatar, text="1. Voucher de R$50 (500 pontos)", text_color="#000000").pack(pady=2)
    ctk.CTkLabel(frame_resgatar, text="2. Desconto na taxa de condomínio (1000 pontos)", text_color="#000000").pack(pady=2)
    ctk.CTkEntry(frame_resgatar, placeholder_text="Digite o número da recompensa", width=300, validate="key", validatecommand=(janela.register(validar_numeros), "%P")).pack(pady=10)

    ctk.CTkButton(frame_resgatar, text="Resgatar (Placeholder)", fg_color="blue", text_color="#ffffff", width=300, command=lambda: print("Resgatar Recompensa clicado!")).pack(pady=10)
    ctk.CTkButton(frame_resgatar, text="Voltar ao Menu Principal", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial).pack(pady=5)
    frame_resgatar.pack(fill="both", expand=True)

def feedback():
    esconder_todos_frames_secundarios()
    frame_feedback = ctk.CTkFrame(janela, fg_color="#ffffff")
    label_feedback = ctk.CTkLabel(frame_feedback, text="Deixe seu Feedback", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
    label_feedback.pack(pady=20)

    ctk.CTkLabel(frame_feedback, text="Sua opinião é muito importante para nós!", text_color="#000000").pack(pady=10)
    ctk.CTkTextbox(frame_feedback, width=400, height=100, placeholder_text="Escreva seu feedback aqui...").pack(pady=5)
    ctk.CTkEntry(frame_feedback, placeholder_text="Sua Nota (0-10)", width=150, validate="key", validatecommand=(janela.register(validar_numeros), "%P")).pack(pady=5)

    ctk.CTkButton(frame_feedback, text="Enviar Feedback (Placeholder)", fg_color="blue", text_color="#ffffff", width=300, command=lambda: print("Enviar Feedback clicado!")).pack(pady=10)
    ctk.CTkButton(frame_feedback, text="Voltar ao Menu Principal", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial).pack(pady=5)
    frame_feedback.pack(fill="both", expand=True)

def deletar_conta():
    esconder_todos_frames_secundarios()
    frame_deletar = ctk.CTkFrame(janela, fg_color="#ffffff")
    label_deletar = ctk.CTkLabel(frame_deletar, text="Deletar Conta", fg_color="#ffffff", text_color="red", font=("Arial", 20))
    label_deletar.pack(pady=20)

    ctk.CTkLabel(frame_deletar, text="⚠️ Cuidado! Esta ação é irreversível.", text_color="red", font=("Arial", 14, "bold")).pack(pady=10)
    ctk.CTkLabel(frame_deletar, text="Para confirmar, digite seu email e senha:", text_color="#000000").pack(pady=(10, 0))
    ctk.CTkEntry(frame_deletar, placeholder_text="Seu Email", width=300).pack(pady=5)
    ctk.CTkEntry(frame_deletar, placeholder_text="Sua Senha", width=300, show="*").pack(pady=5)

    ctk.CTkButton(frame_deletar, text="Confirmar Deleção (Placeholder)", fg_color="red", text_color="#ffffff", width=300, command=lambda: print("Deletar Conta clicado!")).pack(pady=10)
    ctk.CTkButton(frame_deletar, text="Cancelar e Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial).pack(pady=5)
    frame_deletar.pack(fill="both", expand=True)

def calcular_pontos():
    esconder_todos_frames_secundarios()
    frame_pontos = ctk.CTkFrame(janela, fg_color="#ffffff")
    label_pontos = ctk.CTkLabel(frame_pontos, text="Calcular Pontos de Economia", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
    label_pontos.pack(pady=20)

    ctk.CTkLabel(frame_pontos, text="Veja seus pontos com base no consumo de água do mês!", text_color="#000000").pack(pady=10)
    ctk.CTkLabel(frame_pontos, text="Consumo Mês Anterior: [X] Litros", text_color="#000000", font=("Arial", 14)).pack(pady=5)
    ctk.CTkLabel(frame_pontos, text="Pontos Ganhos: [Y] Pontos", text_color="#000000", font=("Arial", 14, "bold")).pack(pady=5)
    ctk.CTkLabel(frame_pontos, text="Total de Pontos: [Z] Pontos", text_color="green", font=("Arial", 16, "bold")).pack(pady=5)


    ctk.CTkButton(frame_pontos, text="Voltar ao Menu Principal", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial).pack(pady=20)
    frame_pontos.pack(fill="both", expand=True)



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

botao2 = ctk.CTkButton(frame_menu, text="Cadastro usuário", fg_color="#f0f0f0", text_color="#1A73E8",font=("Arial", 12), anchor="w",command=cadastro_usuario)
botao2.pack(fill="x", pady=10, padx=10)

botao3 = ctk.CTkButton(frame_menu, text="Cadastro condomínio", fg_color="#f0f0f0", text_color="#1A73E8",font=("Arial", 12), anchor="w",command=cadastro_cond)
botao3.pack(fill="x", pady=10, padx=10)

botao4 = ctk.CTkButton(frame_menu, text="Sobre nós", fg_color="#f0f0f0", text_color="#1A73E8",font=("Arial", 12), anchor="w",command=sobre_nos)
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

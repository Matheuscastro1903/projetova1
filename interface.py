
import customtkinter as ctk
import tkinter.messagebox as tkmb
from PIL import Image
import os
from ecodrop import *

# --- Variável para controlar o estado de login/cadastro ---
usuario_logado_ou_cadastrado = False

# Funções de validação de entrada
def validar_numeros(novo_texto):
    return novo_texto.isdigit() or novo_texto == ""

def validar_letras_espacos(novo_texto):
    return all(c.isalpha() or c.isspace() for c in novo_texto) or novo_texto == ""

# --- Funções de Navegação e Auxiliares ---

def esconder_todos_frames_secundarios():
    for widget in janela.winfo_children():
        if isinstance(widget, ctk.CTkFrame) and widget not in [frame_topo, frame_conteudo, frame_rodape]:
            widget.pack_forget()

def gerenciar_visibilidade_menu(logado=False):
    global usuario_logado_ou_cadastrado

    usuario_logado_ou_cadastrado = logado

    botoes_pos_login = [
        botao_atualizar_dados,
        botao_ranking,
        botao_resgatar,
        botao_feedback,
        botao_deletar_conta,
        botao_calcular_pontos
    ]
    botoes_pre_login = [
        botao_login,
        botao_cadastro_usuario,
        botao_cadastro_cond
    ]

    if logado:
        for botao in botoes_pre_login:
            botao.pack_forget()
        for botao in botoes_pos_login:
            botao.pack(fill="x", pady=10, padx=10)
        botao_logout.pack(fill="x", pady=10, padx=10)
    else:
        for botao in botoes_pos_login:
            botao.pack_forget()
        for botao in botoes_pre_login:
            if botao == botao_login:
                 botao.pack(fill="x", pady=(20, 10), padx=10)
            else:
                botao.pack(fill="x", pady=10, padx=10)
        botao_logout.pack_forget()

def voltar_inicial():
    frame_topo.pack(fill="x")
    frame_conteudo.pack(fill="both", expand=True)
    frame_menu.pack(side="left", fill="y")
    frame_principal.pack(side="left", fill="both", expand=True, padx=30, pady=30)
    frame_rodape.pack(fill="x", side="bottom")
    gerenciar_visibilidade_menu(logado=False)

# --- Funções para as Telas da Interface (com CTkScrollableFrame) ---

def login():
    esconder_todos_frames_secundarios()
    # MUDANÇA AQUI: de CTkFrame para CTkScrollableFrame
    frame_login = ctk.CTkScrollableFrame(janela, fg_color="#ffffff")
    label_login = ctk.CTkLabel(frame_login,text="Informe seus dados:",fg_color="#ffffff",text_color="blue",font=("Arial", 20))
    label_login.pack(pady=2)
    label_avisologin = ctk.CTkLabel(frame_login,text=" ",fg_color="#ffffff",text_color="red",font=("Arial", 14))
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

    
    def simular_conferir_logar():
        email = entrada_emaillogin.get().strip()
        senha = entrada_senhalogin.get().strip()
        if email == "teste@teste.com" and senha == "1234":
            label_avisologin.configure(text="Login bem-sucedido! Redirecionando...", text_color="green")
            janela.after(1500, lambda: menu_principal_logado())
        else:
            label_avisologin.configure(text="Email ou senha incorretos. Tente novamente.", text_color="red")

    botao_logar = ctk.CTkButton(frame_login, text="Logar",fg_color="blue",text_color="#ffffff",width=300,command=simular_conferir_logar)
    botao_logar.pack(pady=2)
    botao_voltarinicial = ctk.CTkButton(frame_login, text="Voltar",fg_color="blue",text_color="#ffffff",width=300,command=voltar_inicial)
    botao_voltarinicial.pack()

    frame_login.pack(fill="both",expand=True)

def cadastro_usuario():
    esconder_todos_frames_secundarios()
    # MUDANÇA AQUI: de CTkFrame para CTkScrollableFrame
    frame_cadastro = ctk.CTkScrollableFrame(janela,fg_color="#ffffff")
    label_cadastro = ctk.CTkLabel(frame_cadastro,text="Informe seus dados:",fg_color="#ffffff",text_color="blue",font=("Arial", 20))
    label_cadastro.pack(pady=1)

    label_aviso = ctk.CTkLabel(frame_cadastro,text=" ",fg_color="#ffffff",text_color="red",font=("Arial", 14))
    label_aviso.pack(pady=1)

    label_email = ctk.CTkLabel(frame_cadastro, text="Digite seu email:", text_color="#000000", anchor="w", width=300)
    label_email.pack(pady=(1, 0))
    entrada_email = ctk.CTkEntry(frame_cadastro, width=300)
    entrada_email.pack(pady=1)

    label_nome = ctk.CTkLabel(frame_cadastro, text="Digite o nome da sua família", text_color="#000000", anchor="w", width=300)
    label_nome.pack(pady=(1, 0))
    entrada_nome = ctk.CTkEntry(frame_cadastro, width=300,validate="key",validatecommand=(janela.register(validar_letras_espacos), "%P"))
    entrada_nome.pack(pady=1)

    label_senha = ctk.CTkLabel(frame_cadastro, text="Senha (mínimo 4 caracteres):", text_color="#000000", anchor="w", width=300)
    label_senha.pack(pady=(1, 0))
    entrada_senha = ctk.CTkEntry(frame_cadastro, width=300, show="*")
    entrada_senha.pack(pady=1)

    label_qmembros = ctk.CTkLabel(frame_cadastro, text="Quantidade de membros na família:", text_color="#000000", anchor="w", width=300)
    label_qmembros.pack(pady=(1,0))
    entrada_qmembros = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(janela.register(validar_numeros), "%P"))
    entrada_qmembros.pack(pady=1)

    label_numeroap = ctk.CTkLabel(frame_cadastro, text="Digite o número do seu apartamento", text_color="#000000", anchor="w", width=300)
    label_numeroap.pack(pady=(1, 0))
    entrada_numeroap = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(janela.register(validar_numeros), "%P"))
    entrada_numeroap.pack(pady=1)

    label_verificador = ctk.CTkLabel(frame_cadastro, text="Digite seu código verificador(mínimo 4 caracteres):", text_color="#000000", anchor="w", width=300)
    label_verificador.pack(pady=(1, 0))
    entrada_verificador = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(janela.register(validar_numeros), "%P"))
    entrada_verificador.pack(pady=1)

    
    def simular_cadastro_conta():
        email = entrada_email.get().strip()
        if "@" in email and len(entrada_senha.get()) >= 4:
            label_aviso.configure(text="Cadastro realizado com sucesso! Redirecionando...", text_color="green")
            janela.after(1500, lambda: menu_principal_logado())
        else:
            label_aviso.configure(text="Dados inválidos para cadastro (email/senha).", text_color="red")

    botao_cadastrar = ctk.CTkButton(frame_cadastro, text="Cadastrar",fg_color="blue",text_color="#ffffff",width=300,command=simular_cadastro_conta)
    botao_cadastrar.pack(pady=1)

    botao_voltarinicial = ctk.CTkButton(frame_cadastro, text="Voltar",fg_color="blue",text_color="#ffffff",width=300,command=voltar_inicial)
    botao_voltarinicial.pack()

    frame_cadastro.pack(fill="both",expand=True)

def cadastro_cond():
    esconder_todos_frames_secundarios()
    # MUDANÇA AQUI: de CTkFrame para CTkScrollableFrame
    frame_cadastro_cond = ctk.CTkScrollableFrame(janela, fg_color="#ffffff")
    label_cadastro_cond = ctk.CTkLabel(frame_cadastro_cond, text="Cadastro de Condomínio", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
    label_cadastro_cond.pack(pady=20)

    ctk.CTkLabel(frame_cadastro_cond, text="Nome do Condomínio:", text_color="#000000").pack(pady=(5,0))
    ctk.CTkEntry(frame_cadastro_cond, width=300).pack(pady=2)
    ctk.CTkLabel(frame_cadastro_cond, text="Endereço:", text_color="#000000").pack(pady=(5,0))
    ctk.CTkEntry(frame_cadastro_cond, width=300).pack(pady=2)
    ctk.CTkLabel(frame_cadastro_cond, text="Cidade:", text_color="#000000").pack(pady=(5,0))
    ctk.CTkEntry(frame_cadastro_cond, width=300).pack(pady=2)
    ctk.CTkLabel(frame_cadastro_cond, text="CEP:", text_color="#000000").pack(pady=(5,0))
    ctk.CTkEntry(frame_cadastro_cond, width=300).pack(pady=2)
    ctk.CTkLabel(frame_cadastro_cond, text="Telefone:", text_color="#000000").pack(pady=(5,0))
    ctk.CTkEntry(frame_cadastro_cond, width=300, validate="key", validatecommand=(janela.register(validar_numeros), "%P")).pack(pady=2)

    ctk.CTkButton(frame_cadastro_cond, text="Cadastrar Condomínio (Placeholder)", fg_color="blue", text_color="#ffffff", width=300, command=lambda: print("Cadastrar condomínio clicado!")).pack(pady=10)
    ctk.CTkButton(frame_cadastro_cond, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial).pack(pady=5)
    frame_cadastro_cond.pack(fill="both",expand=True)

def sobre_nos():
    esconder_todos_frames_secundarios()
    frame_sobre_nos = ctk.CTkFrame(janela, fg_color="#ffffff")
    label_sobre_nos = ctk.CTkLabel(frame_sobre_nos, text="Sobre Nós", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
    label_sobre_nos.pack(pady=20)

    texto_sobre_nos = """
    Bem-vindo ao Ecodrop System!

    Nosso projeto nasceu da paixão por um futuro mais sustentável e da crença de que
    pequenas ações individuais podem gerar grandes impactos coletivos. O Ecodrop
    é uma plataforma dedicada a ajudar condomínios a monitorar e reduzir o consumo
    de água, incentivando moradores a adotarem hábitos mais conscientes.

    Acreditamos que a conscientização é o primeiro passo para a mudança. Por isso,
    oferecemos ferramentas para calcular seu consumo, acompanhar seu ranking de
    economia e até mesmo ser recompensado por seus esforços.

    Nossa missão é promover o uso responsável da água, um recurso tão vital,
    e construir comunidades mais verdes e engajadas.

    Junte-se a nós nessa jornada por um planeta mais azul e um futuro mais próspero!

    Versão da Interface: 1.0
    Suporte: ecodropsuporte@gmail.com
    """
    ctk.CTkLabel(frame_sobre_nos, text=texto_sobre_nos, text_color="#000000",
                 wraplength=500, justify="left", font=("Arial", 14)).pack(pady=10, padx=20)

    ctk.CTkButton(frame_sobre_nos, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial).pack(pady=20)
    frame_sobre_nos.pack(fill="both", expand=True)

def atualizar_dados():
    esconder_todos_frames_secundarios()
    frame_atualizar = ctk.CTkFrame(janela, fg_color="#ffffff")
    label_atualizar = ctk.CTkLabel(frame_atualizar, text="Atualizar Dados", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
    label_atualizar.pack(pady=20)

    ctk.CTkLabel(frame_atualizar, text="Aqui você pode atualizar suas informações.", text_color="#000000").pack(pady=10)
    ctk.CTkEntry(frame_atualizar, placeholder_text="Novo Email", width=300).pack(pady=5)
    ctk.CTkEntry(frame_atualizar, placeholder_text="Nova Senha", width=300, show="*").pack(pady=5)
    ctk.CTkEntry(frame_atualizar, placeholder_text="Nome da Família", width=300, validate="key", validatecommand=(janela.register(validar_letras_espacos), "%P")).pack(pady=5)
    ctk.CTkEntry(frame_atualizar, placeholder_text="Membros da Família", width=300, validate="key", validatecommand=(janela.register(validar_numeros), "%P")).pack(pady=5)

    ctk.CTkButton(frame_atualizar, text="Salvar Atualizações (Placeholder)", fg_color="blue", text_color="#ffffff", width=300, command=lambda: print("Atualizar Dados clicado!")).pack(pady=10)
    ctk.CTkButton(frame_atualizar, text="Voltar ao Menu Principal", fg_color="blue", text_color="#ffffff", width=300, command=menu_principal_logado).pack(pady=5)
    frame_atualizar.pack(fill="both", expand=True)

def ranking():
    esconder_todos_frames_secundarios()
    frame_ranking = ctk.CTkFrame(janela, fg_color="#ffffff")
    label_ranking = ctk.CTkLabel(frame_ranking, text="Ranking", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
    label_ranking.pack(pady=20)

    ctk.CTkLabel(frame_ranking, text="Confira as famílias com mais pontos de economia!", text_color="#000000").pack(pady=10)
    ctk.CTkLabel(frame_ranking, text="[Tabela de Ranking Placeholder]", text_color="#000000", font=("Arial", 16, "bold")).pack(pady=10)
    ctk.CTkLabel(frame_ranking, text="1º Família ABC - 1500 pontos", text_color="#000000").pack(pady=2)
    ctk.CTkLabel(frame_ranking, text="2º Família XYZ - 1200 pontos", text_color="#000000").pack(pady=2)
    ctk.CTkLabel(frame_ranking, text="3º Família DEF - 1000 pontos", text_color="#000000").pack(pady=2)

    ctk.CTkButton(frame_ranking, text="Voltar ao Menu Principal", fg_color="blue", text_color="#ffffff", width=300, command=menu_principal_logado).pack(pady=20)
    frame_ranking.pack(fill="both", expand=True)

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
    ctk.CTkButton(frame_resgatar, text="Voltar ao Menu Principal", fg_color="blue", text_color="#ffffff", width=300, command=menu_principal_logado).pack(pady=5)
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
    ctk.CTkButton(frame_feedback, text="Voltar ao Menu Principal", fg_color="blue", text_color="#ffffff", width=300, command=menu_principal_logado).pack(pady=5)
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
    ctk.CTkButton(frame_deletar, text="Cancelar e Voltar", fg_color="blue", text_color="#ffffff", width=300, command=menu_principal_logado).pack(pady=5)
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

    ctk.CTkButton(frame_pontos, text="Voltar ao Menu Principal", fg_color="blue", text_color="#ffffff", width=300, command=menu_principal_logado).pack(pady=20)
    frame_pontos.pack(fill="both", expand=True)

def menu_principal_logado():
    esconder_todos_frames_secundarios()
    frame_topo.pack(fill="x")
    frame_conteudo.pack(fill="both", expand=True)
    frame_menu.pack(side="left", fill="y")
    frame_principal.pack(side="left", fill="both", expand=True, padx=30, pady=30)
    frame_rodape.pack(fill="x", side="bottom")
    gerenciar_visibilidade_menu(logado=True)

# --- Configuração da janela principal ---
janela = ctk.CTk()
janela.title("ECODROP SYSTEM")
janela.geometry("800x600+400+150")
janela.resizable(False, False)

# Cabeçalho do topo
frame_topo = ctk.CTkFrame(janela, fg_color="#1A73E8", height=80)
frame_topo.pack(fill="x")

titulo = ctk.CTkLabel(frame_topo, text="💧 ECODROP", text_color="#f0f0f0", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

# Divisão em colunas principais (menu lateral e conteúdo)
frame_conteudo = ctk.CTkFrame(janela, fg_color="#f0f0f0")
frame_conteudo.pack(fill="both", expand=True)

# Menu lateral (IMPORTANTE: CRIAR OS BOTÕES AQUI PARA PODER CONTROLAR A VISIBILIDADE)
frame_menu = ctk.CTkFrame(frame_conteudo,fg_color="#f0f0f0",width=200)
frame_menu.pack(side="left", fill="y")

# Botões do menu que aparecem ANTES do login/cadastro
# Estes botões serão empacotados pela função gerenciar_visibilidade_menu no estado inicial.
botao_login = ctk.CTkButton(frame_menu, text="Login", fg_color="#f0f0f0", text_color="#1A73E8",font=("Arial", 12), anchor="w",command=login)
botao_cadastro_usuario = ctk.CTkButton(frame_menu, text="Cadastro Usuário", fg_color="#f0f0f0", text_color="#1A73E8",font=("Arial", 12), anchor="w",command=cadastro_usuario)
botao_cadastro_cond = ctk.CTkButton(frame_menu, text="Cadastro Condomínio", fg_color="#f0f0f0", text_color="#1A73E8",font=("Arial", 12), anchor="w",command=cadastro_cond)

# Botão "Sobre nós" aparece sempre
botao_sobre_nos = ctk.CTkButton(frame_menu, text="Sobre nós", fg_color="#f0f0f0", text_color="#1A73E8",font=("Arial", 12), anchor="w",command=sobre_nos)
botao_sobre_nos.pack(fill="x", pady=10, padx=10)

# --- NOVOS BOTÕES QUE APARECEM SOMENTE APÓS LOGIN/CADASTRO ---
# É importante criar esses objetos de botão no início para podermos referenciá-los
# na função gerenciar_visibilidade_menu(), mesmo que não os empacotemos inicialmente.
botao_atualizar_dados = ctk.CTkButton(frame_menu, text="Atualizar Dados", fg_color="#f0f0f0", text_color="#1A73E8", font=("Arial", 12), anchor="w", command=atualizar_dados)
botao_ranking = ctk.CTkButton(frame_menu, text="Ranking", fg_color="#f0f0f0", text_color="#1A73E8", font=("Arial", 12), anchor="w", command=ranking)
botao_resgatar = ctk.CTkButton(frame_menu, text="Resgatar Recompensas", fg_color="#f0f0f0", text_color="#1A73E8", font=("Arial", 12), anchor="w", command=resgatar)
botao_feedback = ctk.CTkButton(frame_menu, text="Feedback", fg_color="#f0f0f0", text_color="#1A73E8", font=("Arial", 12), anchor="w", command=feedback)
botao_deletar_conta = ctk.CTkButton(frame_menu, text="Deletar Conta", fg_color="#f0f0f0", text_color="#1A73E8", font=("Arial", 12), anchor="w", command=deletar_conta)
botao_calcular_pontos = ctk.CTkButton(frame_menu, text="Calcular Pontos", fg_color="#f0f0f0", text_color="#1A73E8", font=("Arial", 12), anchor="w", command=calcular_pontos)

# --- NOVO: Botão de Logout ---
botao_logout = ctk.CTkButton(frame_menu, text="Sair / Logout", fg_color="red", text_color="#ffffff", font=("Arial", 12), anchor="w", command=voltar_inicial)


# Área principal de conteúdo (tela inicial)
frame_principal = ctk.CTkFrame(frame_conteudo,fg_color="#f0f0f0")
frame_principal.pack(side="left", fill="both", expand=True, padx=30, pady=30)

texto_bem_vindo = ctk.CTkLabel(frame_principal, text="Bem-vindo ao sistema ECODROP",text_color="#202124", font=("Arial", 22, "bold"))
texto_bem_vindo.pack(pady=(0, 20))

texto_instrucao = ctk.CTkLabel(frame_principal, text="Menos consumo, mais consciência, um planeta mais feliz.",text_color="#5f6368",wraplength=500,justify="left",font=("Arial", 18))
texto_instrucao.pack()

# Carregamento seguro da imagem
try:
    imagem = Image.open("fotos/mascoteprincipall.png")
    ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(400, 400))
    label_imagem = ctk.CTkLabel(frame_principal, image=ctk_imagem, text="")
    label_imagem.pack()
except FileNotFoundError:
    print("Aviso: 'fotos/mascoteprincipall.png' não encontrado. A imagem não será exibida.")
    label_imagem = ctk.CTkLabel(frame_principal, text="[Imagem ECODROP Placeholder]", text_color="#5f6368", font=("Arial", 14))
    label_imagem.pack()


# Frame do rodapé
frame_rodape = ctk.CTkFrame(janela, fg_color="white", height=30)
frame_rodape.pack(fill="x", side="bottom")

texto_rodape = ctk.CTkLabel(frame_rodape, text="Versão 2.0 • Suporte: ecodropsuporte@gmail.com",text_color="#5f6368",font=("Arial", 10))
texto_rodape.pack(pady=5)

# --- Inicializa a visibilidade dos botões ao iniciar a aplicação ---
# Por padrão, o usuário NÃO está logado, então mostra apenas as opções de pré-login.
gerenciar_visibilidade_menu(logado=False)

janela.mainloop()

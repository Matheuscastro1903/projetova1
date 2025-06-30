
import customtkinter as ctk
from PIL import Image
import json
import csv
import time
import re
import random

mensagens_agua = [
    "💧 Cada gota conta. Economize água!",
    "🚿 Banhos curtos, planeta mais saudável.",
    "🌍 Água é vida. Preserve cada gota.",
    "🧼 Feche a torneira ao escovar os dentes.",
    "💦 Pequenas atitudes salvam grandes recursos.",
    "🔧 Torneiras pingando desperdiçam litros por dia!",
    "🌱 Use a água da chuva para regar plantas.",
    "❌ Água não é infinita. Use com consciência.",
    "🪣 Reutilize a água sempre que puder.",
    "🐳 Preserve os rios, lagos e oceanos.",
    "📉 Menos desperdício, mais futuro.",
    "🧽 Economize água ao lavar louça ou roupa.",
    "🏡 Sua casa também pode ser sustentável.",
    "👶 Ensine as crianças a cuidar da água.",
    "💙 Água limpa é direito de todos. Preserve!"
]

with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
    
    # quando usa json.load o arquivo json é transformado em dicionário python
    """
    o objetivo dessa parte do código é abrir o arquivo json e salvar os dicionários em python,facilitando a manipulação
    """
    arquivo_lido = json.load(arquivo)
    dados_conta = arquivo_lido["senha"]
    dados_familia = arquivo_lido["familia"]
    dados_quantidade = arquivo_lido["membros"]
    dados_pontos = arquivo_lido["pontos"]
    dados_apartamento = arquivo_lido["apartamento"]
    dados_codigov = arquivo_lido["verificador"]


# Função para só permitir digitar números
def validar_numeros(novo_texto):  # Adicione o parâmetro
    """Função utilizada para deixar o usuário digitar apenas números,melhorando o tratamento de erros """
    return novo_texto.isdigit() or novo_texto == ""

# Função para só permitir digitar letras e espaços

def validar_letras_espacos(novo_texto):  # Adicione o parâmetro
    """Função utilizada para deixar o usuário digitar apenas letras e espaços,melhorando o tratamento de erros """
    return all(c.isalpha() or c.isspace() for c in novo_texto) or novo_texto == ""

def aviso_sistema():
    """Função utilizada para mostrar o frame_aviso,que só aparecerá se o cadastro for concluído com sucesso"""
    frame_cadastro.pack_forget()
    frame_aviso.pack(fill="both",expand=True)
  

def voltar_inicial():
    """Função utilizada para volta a tela inical,caso tenha entrado na opção errada"""
    # Frames para "esquecer"
    frame_cadastro.pack_forget()
    frame_login.pack_forget()
    frame_adm.pack_forget()
    frame_sobrenos.pack_forget()

    frame_topo.pack(fill="x")
    frame_conteudo.pack(fill="both", expand=True)
    frame_lateral.pack(side="left", fill="y")
    frame_principal.pack(side="right", fill="both",expand=True, padx=30, pady=30)
    frame_rodape.pack(fill="x", side="bottom")

    pass

    pass


def mostrar_login():
    """Função utilizada para expandir o frame login"""
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget()
    frame_aviso.pack_forget()
    frame_login.pack(fill="both", expand=True)

    pass


def conferir_logar(entrada_emaillogin,entrada_senhalogin):
    """Função utilizada para verificar se há espaços em branco ao apertar o botão logar"""
    email = entrada_emaillogin.get().strip()
    senha = entrada_senhalogin.get().strip()
    if email == "" or senha == "":
        label_avisologin.configure(text="Preencha todos os campos.", text_color="red")
        return
    
    login(email,senha,label_avisologin)

def login(email,senha,label_avisologin):
    """Função utilizada para verificar se email e senha estão corretos,para assim ir para o menu"""
    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
        # quando usa json.load o arquivo json é transformado em dicionário python
        arquivo_lido = json.load(arquivo)
        
        dados_conta = arquivo_lido["senha"]
        


        
        if email in dados_conta:
            if dados_conta[email] == senha:
                
                mostrar_menu(email,senha)
                return
            else:
                label_avisologin.configure(text="EMAIL OU SENHA INCORRETO.\nContate o suporte para recuperar usa senha",text_color="red")
                return
                
        else:
            label_avisologin.configure(text="EMAIL NÃO CADASTRADO.\nVá para tela de cadastro")
            return
    pass

def mostrar_cadastro():
    """Função utilizada para expandir o frame cadastro"""
    # frames para esquecer
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget()

    frame_cadastro.pack(fill="both", expand=True)

    pass


def conferir_cadastrar(entrada_email, entrada_nome, entrada_senha,
                       entrada_qmembros, entrada_numeroap, entrada_verificador,label_aviso):
    """
    Essa função será utilizada para verificar se as entradas estão preenchidas
    corretamente e chamará a classe Cadastro para cadastrar a conta.
    """

    email = entrada_email.get().strip()
    nome_familia = entrada_nome.get().strip()
    senha = entrada_senha.get().strip()
    quantidade_pessoas = int(entrada_qmembros.get().strip())
    apartamento = int(entrada_numeroap.get().strip())
    verificador = entrada_verificador.get().strip()

    entradas = [email, nome_familia, senha,quantidade_pessoas,apartamento]

    # Verificação: se algum campo de texto estiver vazio
    if any(campo == "" for campo in entradas):
        label_aviso.configure(text="Todos os campos devem ser preenchidos.", text_color="red")
        return

    # Validação da senha
    if len(senha) < 4 or len(senha) > 20:
        label_aviso.configure(text="A senha deve ter entre 4 e 20 caracteres.", text_color="red")
        return
    
    if len(verificador) < 4 or len(verificador) > 20:
        label_aviso.configure(text="A senha deve ter entre 4 e 20 caracteres.", text_color="red")
        return
    

    
    conta = Cadastro(email,quantidade_pessoas,senha,nome_familia,apartamento,verificador)




    


def modo_adm():
    """Função utilizada para expandir o frame_adm,quando o usuário quiser ir para o modo adm"""
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget() 

    frame_adm.pack(fill="both", expand=True)

    pass

def entrar_modoadm():
    
    pass


def sobre_nos():
    """Função utilizada para mostrar o frame_sobrenos(Contando a história do  projeto ecodrop"""
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget()
    frame_sobrenos.pack(fill="both", expand=True)

    pass

def mostrar_menu(email, senha):
    """Função utilizada para mostrar o frame_menu,onde verá as funções disponíveis do programa"""
    frame_login.pack_forget()

    # Frame principal que envolve o menu e o conteúdo
    frame_menu = ctk.CTkFrame(janela, fg_color="#ffffff")

    # Topo do sistema com título
    frame_topo = ctk.CTkFrame(frame_menu, fg_color="#1A73E8", height=80)
    frame_topo.pack(fill="x")

    titulo = ctk.CTkLabel(frame_topo, text="EcoDrop", fg_color="#1A73E8", text_color="white",
                          font=("Arial", 24, "bold"))
    titulo.pack(pady=20)

    # Menu lateral
    frame_lateral = ctk.CTkFrame(frame_menu, fg_color="white", width=200)
    frame_lateral.pack(side="left", fill="y")

    # Frame de conteúdo
    frame_conteudo = ctk.CTkFrame(frame_menu, fg_color="#f0f2f5")
    

    # ---- Botões reorganizados ----
    botao1 = ctk.CTkButton(frame_lateral, text="🏆 Ranking mensal", fg_color="white", text_color="#1A73E8",
                           font=("Arial", 12), anchor="w",
                           command=lambda: mostrar_ranking(email, senha, frame_principalmenu), cursor="hand2")
    botao1.pack(fill="x", pady=(20, 10), padx=20)

    botao2 = ctk.CTkButton(frame_lateral, text="🎁 Resgatar prêmios", fg_color="white", text_color="#1A73E8",
                           font=("Arial", 12), anchor="w",
                           command=lambda: resgatar_premio(email, senha, frame_principalmenu), cursor="hand2")
    botao2.pack(fill="x", pady=10, padx=20)

    botao3 = ctk.CTkButton(frame_lateral, text="🧮 Cálculo de pontos", fg_color="white", text_color="#1A73E8",
                           font=("Arial", 12), anchor="w",
                           command=lambda: calculo_pontuacao(email, senha, frame_principalmenu), cursor="hand2")
    botao3.pack(fill="x", pady=10, padx=20)

    botao4 = ctk.CTkButton(frame_lateral, text="🧠 Quiz semanal", fg_color="white", text_color="#1A73E8",
                           font=("Arial", 12), anchor="w",
                           command=lambda: mostrar_dados(email, senha, frame_principalmenu), cursor="hand2")
    botao4.pack(fill="x", pady=10, padx=20)

    botao5 = ctk.CTkButton(frame_lateral, text="📘 Área educativa", fg_color="white", text_color="#1A73E8",
                           font=("Arial", 12), anchor="w",
                           command=lambda: area_educativa(email, senha, frame_menu), cursor="hand2")
    botao5.pack(fill="x", pady=10, padx=20)

    botao6 = ctk.CTkButton(frame_lateral, text="📊 Mostrar dados", fg_color="white", text_color="#1A73E8",
                           font=("Arial", 12), anchor="w",
                           command=lambda: mostrar_dados(email, senha, frame_principalmenu), cursor="hand2")
    botao6.pack(fill="x", pady=10, padx=20)

    botao7 = ctk.CTkButton(frame_lateral, text="🔄 Atualizar dados", fg_color="white", text_color="#1A73E8",
                           font=("Arial", 12), anchor="w",
                           command=lambda: atualizar_dados(email, senha, frame_principalmenu), cursor="hand2")
    botao7.pack(fill="x", pady=10, padx=20)

    botao8 = ctk.CTkButton(frame_lateral, text="🗑 Deletar conta", fg_color="white", text_color="#1A73E8",
                           font=("Arial", 12), anchor="w",
                           command=lambda: deletar_conta(email, senha, frame_principalmenu), cursor="hand2")
    botao8.pack(fill="x", pady=10, padx=20)

    botao9 = ctk.CTkButton(frame_lateral, text="✍️ Enviar feedback", fg_color="white", text_color="#1A73E8",
                           font=("Arial", 12), anchor="w",
                           command=lambda: feedback(email, senha, frame_principalmenu), cursor="hand2")
    botao9.pack(fill="x", pady=10, padx=20)

    # Frame principal de conteúdo
    frame_conteudo.pack(fill="both", expand=True)

    frame_principalmenu = ctk.CTkFrame(frame_conteudo, fg_color="#ffffff")
    frame_principalmenu.pack(fill="both", expand=True)

    # Mensagem de boas-vindas
    texto_bem_vindo = ctk.CTkLabel(frame_principalmenu, text="Bem-vindo ao EcoDrop",
                                   fg_color="#ffffff", text_color="#202124", font=("Arial", 18, "bold"))
    texto_bem_vindo.pack(pady=(0, 20))

    texto_instrucao = ctk.CTkLabel(frame_principalmenu,
                                   text=random.choice(mensagens_agua),
                                   fg_color="#ffffff", text_color="#5f6368",
                                   wraplength=500, justify="left", font=("Arial", 12))
    texto_instrucao.pack()

    imagem = Image.open("fotos/mascoteprincipall.png")
    ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(400, 400))

    label = ctk.CTkLabel(frame_principalmenu, image=ctk_imagem, text="")
    label.pack()

    # Exibe o frame principal completo
    frame_menu.pack(fill="both", expand=True)



    pass

def mostrar_dados(email, senha, frame_principalmenu):
    """
    📊 Função: Mostrar Dados
    Mostra os principais dados da conta do usuário (exceto senha e código verificador por segurança).
    Utilizada para que o usuário possa revisar as informações do seu cadastro.
    """
    pass


def atualizar_dados(email, senha, frame_principalmenu):
    """
    🔄 Função: Atualizar Dados,onde será possível o usuário atualizar seus dados"""
    pass


def deletar_conta(email, senha, frame_principalmenu):
    """
    🗑 Função: Deletar Conta
    Permite ao usuário excluir sua conta permanentemente do sistema.
    Após a confirmação, os dados são removidos e ele precisará se cadastrar novamente.
    """
    pass


def feedback(email, senha, frame_principalmenu):
    """
    ✍️ Função: Feedback
    Permite ao usuário enviar uma opinião com até 140 caracteres e uma nota de 0 a 10.
    Serve para avaliar o sistema e coletar sugestões de melhoria.
    """
    pass


def calculo_pontuacao(email, senha, frame_principalmenu):
    """
    🧮 Função: Cálculo de Pontos
    Calcula pontos com base nos litros economizados, número de moradores e consumo médio.
    Os pontos são convertidos em benefícios (ex: vouchers, descontos, milhas).
    """
    pass


def resgatar_premio(email, senha, frame_principalmenu):
    """
    🎁 Função: Resgatar Prêmios
    Permite ao usuário resgatar recompensas usando seus pontos acumulados.
    Verifica se o saldo é suficiente antes de confirmar o resgate.
    """
    pass


def mostrar_ranking(email, senha, frame_principalmenu):
    """
    🏆 Função: Ranking Mensal
    Exibe uma lista com as famílias que mais economizaram água no mês.
    Usa o consumo médio diário como critério de ordenação.
    """
    pass

def quiz_semanal(email, senha, frame_principalmenu):
    pass



def area_educativa(email, senha, frame_menu):
    """Função utilizada para ir para o frame_educativo(usaremos a tela inteira nessa função,por se necessário para ter mais conteúdo.
    Onde terá várias opções de leitura sobre assuntos de sustentabilidade"""
    frame_menu.destroy()

    frame_topoeducativo = ctk.CTkFrame(janela, fg_color="#1A73E8", height=80)
    frame_topoeducativo.pack(fill="x")

    titulo_educativo = ctk.CTkLabel(frame_topoeducativo, text="💧 ÁREA EDUCATIVA",
                                    text_color="#f0f0f0", font=("Arial", 24, "bold"))
    titulo_educativo.pack(pady=20)

    frame_educativo = ctk.CTkFrame(janela, fg_color="#ffffff")
    frame_educativo.pack(fill="both", expand=True, padx=20, pady=10)

    btn1 = ctk.CTkButton(frame_educativo,
                         text="Europa investe €15 bilhões em preservação de recursos hídricos até 2027",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=area_educativa1)
    btn1.pack(fill="x", pady=10)

    btn2 = ctk.CTkButton(frame_educativo,
                         text="Cientistas desenvolvem tecnologia para extrair água potável do ar usando resíduos alimentares",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=area_educativa2)
    btn2.pack(fill="x", pady=10)

    btn3 = ctk.CTkButton(frame_educativo,
                         text="Universidade do Texas inicia construção do maior centro universitário de reúso de água dos EUA",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=area_educativa3)
    btn3.pack(fill="x", pady=10)

    btn4 = ctk.CTkButton(frame_educativo,
                         text="Alunos serão instruídos sobre conservação da água e limpeza do rio Ganges na Índia",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=area_educativa4)
    btn4.pack(fill="x", pady=10)

    btn5 = ctk.CTkButton(frame_educativo,
                         text="Escolas de New Haven, EUA, ampliam programas de sustentabilidade e uso racional da água",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=area_educativa5)
    btn5.pack(fill="x", pady=10)

    btn6 = ctk.CTkButton(frame_educativo,
                         text="10 filmes educativos para crianças sobre sustentabilidade",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=area_educativa6)
    btn6.pack(fill="x", pady=10)

    botao_voltarmenu = ctk.CTkButton(frame_educativo,
                                     text="Voltar ao menu",
                                     fg_color="white",
                                     text_color="#1A73E8",
                                     font=("Arial", 12),
                                     anchor="w",
                                     cursor="hand2",
                                     command=lambda: mostrar_menu(email, senha))
    botao_voltarmenu.pack(fill="x", pady=10)

    frame_educativo.pack(fill="both", expand=True, padx=20, pady=10)


def area_educativa1():
    # Área educativa destinada ao tema: Preservação de recursos hídricos na Europa
    pass

def area_educativa2():
    # Área educativa destinada ao tema: Tecnologia para extrair água potável do ar usando resíduos alimentares
    pass

def area_educativa3():
    # Área educativa destinada ao tema: Construção do maior centro universitário de reúso de água dos EUA
    pass

def area_educativa4():
    # Área educativa destinada ao tema: Conservação da água e limpeza do rio Ganges na Índia
    pass

def area_educativa5():
    # Área educativa destinada ao tema: Programas de sustentabilidade e uso racional da água em escolas de New Haven, EUA
    pass

def area_educativa6():
    # Área educativa destinada ao tema: Filmes educativos para crianças sobre sustentabilidade
    pass


def sair_sistema():
    """Função utilizada para fechar sistema """
    janela.destroy()  # Fecha a janela principal
    # Ou qualquer outra lógica de saída que você preferir

# ctk.set_appearance_mode("light")

######################################################################
# Configuração da janela principal
janela = ctk.CTk()
janela.title("ECODROP SYSTEM")
janela.geometry("1000x800+400+150")
janela.resizable(False, False)

# Criasse um frame apenas para parte do cabeçalho do topo
frame_topo = ctk.CTkFrame(janela, fg_color="#1A73E8", height=80)
frame_topo.pack(fill="x")

titulo = ctk.CTkLabel(frame_topo, text="💧 ECODROP",
                      text_color="#f0f0f0", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

# Divisão em colunas principais (menu lateral e conteúdo)
frame_conteudo = ctk.CTkFrame(janela, fg_color="#f0f0f0")
frame_conteudo.pack(fill="both", expand=True)

# Menu lateral
frame_lateral = ctk.CTkFrame(frame_conteudo, fg_color="#f0f0f0", width=200)
frame_lateral.pack(side="left", fill="y")

# Botões do menu
botao1 = ctk.CTkButton(frame_lateral, text="Login", fg_color="#f0f0f0",
                       text_color="#1A73E8", font=("Arial", 12), anchor="w", command=mostrar_login)
botao1.pack(fill="x", pady=(20, 10), padx=10)

botao2 = ctk.CTkButton(frame_lateral, text="Cadastro usuário", fg_color="#f0f0f0",
                       text_color="#1A73E8", font=("Arial", 12), anchor="w", command=mostrar_cadastro)
botao2.pack(fill="x", pady=10, padx=10)

botao3 = ctk.CTkButton(frame_lateral, text="Modo administrador", fg_color="#f0f0f0",
                       text_color="#1A73E8", font=("Arial", 12), anchor="w", command=modo_adm)
botao3.pack(fill="x", pady=10, padx=10)

botao4 = ctk.CTkButton(frame_lateral, text="Sobre nós", fg_color="#f0f0f0",
                       text_color="#1A73E8", font=("Arial", 12), anchor="w", command=sobre_nos)
botao4.pack(fill="x", pady=10, padx=10)


####################################################
# Área principal de conteúdo
frame_principal = ctk.CTkFrame(frame_conteudo, fg_color="#f0f0f0")
frame_principal.pack(side="left", fill="both", expand=True, padx=30, pady=30)


texto_bem_vindo = ctk.CTkLabel(frame_principal, text="Bem-vindo ao sistema ECODROP",
                               text_color="#202124", font=("Arial", 22, "bold"))
texto_bem_vindo.pack(pady=(0, 20))

texto_instrucao = ctk.CTkLabel(frame_principal, text="Menos consumo, mais consciência, um planeta mais feliz.",
                               text_color="#5f6368", wraplength=500, justify="left", font=("Arial", 18))
texto_instrucao.pack()

imagem = Image.open("fotos/mascoteprincipall.png")
ctk_imagem = ctk.CTkImage(
    light_image=imagem, dark_image=imagem, size=(400, 400))

label = ctk.CTkLabel(frame_principal, image=ctk_imagem, text="")
label.pack()

############################################################
# Frame do rodapé
frame_rodape = ctk.CTkFrame(frame_principal, fg_color="#f0f0f0", height=30)
frame_rodape.pack(fill="x", side="bottom")

texto_rodape = ctk.CTkLabel(
    frame_rodape, text="Versão 2.0 • Suporte: ecodropsuporte@gmail.com", text_color="#5f6368", font=("Arial", 10))
texto_rodape.pack()

###########################################################
"""Parte do frame login"""

frame_login = ctk.CTkFrame(janela, fg_color="#ffffff")
label_login = ctk.CTkLabel(frame_login, text="Informe seus dados:",
                           fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_login.pack(pady=2)
label_avisologin = ctk.CTkLabel(
    frame_login, text=" ", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_avisologin.pack(pady=2)

# 1-entrada email
label_emaillogin = ctk.CTkLabel(
    frame_login, text="Digite seu email:", text_color="#000000", anchor="w", width=300)
label_emaillogin.pack(pady=(2, 0))

entrada_emaillogin = ctk.CTkEntry(frame_login, width=300)
entrada_emaillogin.pack(pady=2)

# 2-entrada senha
label_senhalogin = ctk.CTkLabel(
    frame_login, text="Digite sua senha:", text_color="#000000", anchor="w", width=300)
label_senhalogin.pack(pady=(2, 0))

entrada_senhalogin = ctk.CTkEntry(frame_login, width=300, show="*")
entrada_senhalogin.pack(pady=2)

# 3-entrada email cond


# botão logar
botao_logar = ctk.CTkButton(frame_login, text="Logar", fg_color="blue",
                            text_color="#ffffff", width=300, command=lambda:conferir_logar(entrada_emaillogin,entrada_senhalogin))
botao_logar.pack(pady=2)
# botão voltar
botao_voltarinicial = ctk.CTkButton(
    frame_login, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
botao_voltarinicial.pack()

# frame_login.pack(fill="both",expand=True)


##############################################
"""Parte do frame cadastro"""
frame_cadastro = ctk.CTkFrame(janela, fg_color="#ffffff")
label_cadastro = ctk.CTkLabel(frame_cadastro, text="Informe seus dados:",
                              fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_cadastro.pack(pady=1)


label_aviso = ctk.CTkLabel(frame_cadastro, text=" ",
                           fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_aviso.pack(pady=1)

# 1-Entrada Nome
label_email = ctk.CTkLabel(frame_cadastro, text="Digite seu email:",
                           text_color="#000000", anchor="w", width=300)
label_email.pack(pady=(1, 0))

entrada_email = ctk.CTkEntry(frame_cadastro, width=300)
entrada_email.pack(pady=1)

# 2-entrada nome da família
label_nome = ctk.CTkLabel(frame_cadastro, text="Digite o nome da sua família",
                          text_color="#000000", anchor="w", width=300)
label_nome.pack(pady=(1, 0))

entrada_nome = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(
    janela.register(validar_letras_espacos), "%P"))
entrada_nome.pack(pady=1)

# 3-Entrada Senha
label_senha = ctk.CTkLabel(frame_cadastro, text="Senha (mínimo 4 caracteres):",
                           text_color="#000000", anchor="w", width=300)
label_senha.pack(pady=(1, 0))

entrada_senha = ctk.CTkEntry(frame_cadastro, width=300, show="*")
entrada_senha.pack(pady=1)

# 4. Campo Quantidade de membros
label_qmembros = ctk.CTkLabel(
    frame_cadastro, text="Quantidade de membros na família:", text_color="#000000", anchor="w", width=300)
label_qmembros.pack(pady=(1, 0))
entrada_qmembros = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(
    janela.register(validar_numeros), "%P"))
entrada_qmembros.pack(pady=1)

# 5. Número do apartamento
label_numeroap = ctk.CTkLabel(
    frame_cadastro, text="Digite o número do seu apartamento", text_color="#000000", anchor="w", width=300)
label_numeroap.pack(pady=(1, 0))
entrada_numeroap = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(
    janela.register(validar_numeros), "%P"))
entrada_numeroap.pack(pady=1)

# 6. Código verificador
label_verificador = ctk.CTkLabel(
    frame_cadastro, text="Digite seu código verificador(mínimo 4 caracteres):", text_color="#000000", anchor="w", width=300)
label_verificador.pack(pady=(1, 0))

entrada_verificador = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(
    janela.register(validar_numeros), "%P"))
entrada_verificador.pack(pady=1)


botao_cadastrar = ctk.CTkButton(frame_cadastro, text="Cadastrar", fg_color="blue",
                                text_color="#ffffff", width=300, command=lambda: conferir_cadastrar(entrada_email,entrada_nome,entrada_senha,
                                                                                                    entrada_qmembros,
                                                                                                   entrada_numeroap,entrada_verificador,label_aviso))
botao_cadastrar.pack(pady=1)

# botão de voltar
botao_voltarinicial = ctk.CTkButton(
    frame_cadastro, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
botao_voltarinicial.pack()


#####################################
"""Parte do frame adm(modo administrador"""
frame_adm = ctk.CTkFrame(janela, fg_color="#ffffff")
label_adm = ctk.CTkLabel(frame_adm, text="Informe seus dados:",fg_color="#ffffff", text_color="blue", font=("Arial", 30))
label_adm.pack(pady=1)

label_adm = ctk.CTkLabel(frame_adm, text=" ",fg_color="#ffffff", text_color="blue", font=("Arial", 25))
label_adm.pack(pady=1)

# 1-Entrada Nome
label_codigo = ctk.CTkLabel(frame_adm, text="Digite código de administrador:",
                           text_color="blue", anchor="w", width=300)
label_codigo.pack(pady=(1, 0))

entrada_codigo = ctk.CTkEntry(frame_adm, width=300)
entrada_codigo.pack(pady=1)

botao_modoadm = ctk.CTkButton(frame_adm, text="Entrar modo adm", fg_color="blue",
                                text_color="#ffffff", width=300, command=entrar_modoadm)
botao_modoadm.pack(pady=1)
# botão de voltar
botao_voltarinicial = ctk.CTkButton(frame_adm, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
botao_voltarinicial.pack()


######################################################
"""Parte do frame sobrenos(Conta a história do ecodrop"""
frame_sobrenos = ctk.CTkFrame(janela, fg_color="#ffffff")

# Título principal
titulo_sobrenos = ctk.CTkLabel(frame_sobrenos,text="💧 Projeto ECODROP",font=("Arial", 22, "bold"),text_color="#1A73E8")
titulo_sobrenos.pack(pady=(20, 10))

descricao_projeto = ctk.CTkLabel(
    frame_sobrenos,
    text=(
        "Em um mundo marcado pelo crescimento populacional e pelo consumo excessivo de recursos naturais, "
        "a sustentabilidade se tornou um dos pilares fundamentais para garantir a qualidade de vida das gerações futuras. "
        "É essencial que a sociedade adote práticas conscientes no dia a dia, promovendo o uso equilibrado da água, da energia e demais recursos. "
        "Nesse contexto, a tecnologia tem papel estratégico: aproximar a inovação das soluções ambientais.\n\n"

        "O ECODROP é um sistema desenvolvido com o propósito de promover a sustentabilidade em ambientes residenciais, "
        "especialmente em condomínios. A proposta central é incentivar e premiar os moradores que conseguem manter um "
        "consumo de água abaixo da média nacional, promovendo assim economia, consciência ambiental e um futuro mais responsável.\n\n"

        "Este projeto foi criado por Matheus de Castro e Gabriel Escobar como parte do Projeto Interdisciplinar do curso de "
        "Sistemas de Informação da Universidade Federal Rural de Pernambuco (UFRPE). Para sua construção, foi utilizada a linguagem "
        "de programação Python, aliando tecnologia e responsabilidade ambiental em uma solução acessível e inteligente para o cotidiano dos moradores."
    ),
    font=("Arial", 14),
    text_color="#202124",
    wraplength=650,
    justify="left"
)
descricao_projeto.pack(pady=(0, 30))
imagem = Image.open("fotos/fotosobrenos.jpg")
ctk_imagem = ctk.CTkImage(
    light_image=imagem, dark_image=imagem, size=(500, 300))

label = ctk.CTkLabel(frame_sobrenos, image=ctk_imagem, text="")
label.pack()
botao_voltarinicial = ctk.CTkButton(frame_sobrenos, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
botao_voltarinicial.pack(pady=30)

#######################################
"""Parte do frame aviso(só será usada quando o usuário finalizar corretamente o cadastro,tendo a opção de ir para login ou sair do sistema"""
frame_aviso=ctk.CTkFrame(janela,fg_color="#ffffff")
 # Label de aviso
label = ctk.CTkLabel(frame_aviso, text="Cadastro realizado com sucesso!", font=("Arial", 20), text_color="green")
label.pack(pady=(40, 20))

    # Botão para ir para login
botao_login = ctk.CTkButton(frame_aviso, text="Ir para Login", width=200, command=mostrar_login)
botao_login.pack(pady=(0, 10))

    # Botão para sair do sistema
botao_sair = ctk.CTkButton(frame_aviso, text="Sair do Sistema", width=200, fg_color="red", hover_color="#cc0000", command=sair_sistema)
botao_sair.pack()


###############################################



class Cadastro:
    """
    Essa Classe tem o objetivo de cadastrar os usuários, recebendo os dados básicos como parâmetros.
    Ela realiza o cadastro de uma conta e verifica o código de segurança fornecido.
    """

    def __init__(self, email, quantidade_pessoas, senha, nome_familia, apartamento, verificador):
        # Dados básicos de cadastro
        self.email = email
        self.quantidade = quantidade_pessoas
        self.senha = senha.strip()
        self.nome_familia = nome_familia.strip()
        self.pontos = 0  # Pontos começam zerados
        self.apartamento = apartamento
        self.verificador = verificador.strip()
        print("entrei cadastro")
        self.email_valido()

        # Chamada para verificar o código de segurança
        


    def email_valido(self):
        
        #FUNÇÃO UTILIZADA PARA CONFERIR SE O EMAIL É VÁLIDO OU NÃO
        dominios_validos = [
            'gmail.com', 'outlook.com', 'hotmail.com',
            'yahoo.com', 'icloud.com'
        ]

        tentativas_email = 3
        while tentativas_email != 0:
            # VERIFICA SE O FORMATO DO EMAIL ESTÁ ESCRITO CORRETAMENTE
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
                print("FORMATO DE EMAIL INVÁLIDO, UTILIZE UM DOMÍNIO VÁLIDO")
                self.email = input("Digite novamente seu email: ").strip()
                tentativas_email -= 1
                print(f"Tentativas restantes: {tentativas_email}")

                continue  # volta pro início do while para validar de novo,caso esteja correto,irá passar pelo verificador

            # VERIFICA APENAS O DOMÍNIO,SEPARA TODO O RESTO E PEGA APENAS A PARTE DO DOMÍNIO
            dominio = self.email.split('@')[1].lower()
            if dominio not in dominios_validos:
                print("Domínio não aceito. Use: Gmail, Outlook, Yahoo, iCloud, etc.")
                self.email = input("Digite novamente seu email: ").strip()
                tentativas_email -= 1
                print(f"Tentativas restantes: {tentativas_email}")

                # continuar o loop sem parar
                continue

        # Se chegou aqui, formato e domínio estão corretos
            break

        else:
            print("Limite de tentativas atingido. Encerrando o processo de cadastro.")
            return

        self.conferir_email()

    
    def conferir_email(self):
        
        #FUNÇÃO UTILIZADA PARA CONFERIR SE O EMAIL JÁ ESTÁ CADASTRADO OU NÃO
        
        with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
            arquivo_lido = json.load(arquivo)
            dados_conta = arquivo_lido["senha"]
            dados_familia = arquivo_lido["familia"]
            dados_quantidade = arquivo_lido["membros"]
            dados_pontos = arquivo_lido["pontos"]
            dados_apartamento = arquivo_lido["apartamento"]
            dados_codigov = arquivo_lido["verificador"]

            if self.email in dados_conta:
                print("EMAIL JÁ POSSUI UMA CONTA.")
                tentativas = 3
                while tentativas != 0:
                    resposta1 = input(
                    "Deseja tentar refazer a conta ou ir para tela de login caso já possua conta? (refazer/login) ").strip().lower()
                    if resposta1 in ["login", "tela de login", "logi"]:
                        login()
                        return
                    elif resposta1 in ["refazer", "retentar", "conta", "refazer conta"]:
                        self.email = input("Digite novamente seu email: ").strip()
                        self.conferir_email()
                        return
                    else:
                        print("Resposta inválida")
                        tentativas -= 1
                        print(f"Tentativas restantes {tentativas}")
                else:
                    print(
                    "Limite de tentativas atingido. Encerrando o processo de cadastro.")
                    return
            else:
                self.conferir_ap()  # Continua o processo normalmente

    def conferir_ap(self):
        
       #FUNÇÃO UTILIZADA PARA ANALISAR SE O APARTAMENTO JÁ ESTÁ CADASTRADO OU NÃO
        if self.apartamento in dados_apartamento.values():
            print("APARTAMENTO JÁ CADASTRADO.")
            tentativas = 3
            while tentativas != 0:
                resposta1 = input(
                    "Deseja tentar refazer a conta ou ir para tela de login caso já possua conta ??(refazer/login)").strip().lower()
                if resposta1 in ["login", "tela de login", "logi"]:
                    login()
                    return
                elif resposta1 in ["refazer", "retentar", "conta", "refazer conta"]:
                    Cadastro()
                    return
                else:
                    print("Resposta inválida")
                    tentativas -= 1
                    print(f"Tentativas restantes {tentativas}")
            else:  # ✅ Só imprime quando zerar tentativas
                print(
                    "Limite de tentativas atingido. Encerrando o processo de cadastro.")
        else:
            self.cadastrar_conta()

    def cadastrar_conta(self):
        
        ##FUNÇÃO UTILIZADA PARA CADASTRAR CONTA NO BANCO DE DADOS

        dados_conta[self.email] = self.senha
        dados_familia[self.email] = self.nome_familia
        dados_quantidade[self.email] = self.quantidade
        dados_pontos[self.email] = self.pontos
        dados_apartamento[self.email] = self.apartamento
        dados_codigov[self.email] = self.verificador

        # PARA ARQUIVO TIPO JSON É MELHOR USAR "w" pois qualquer errinho de formatação pode quebrar o sistema
        with open(r"banco_dados.JSON", "w", encoding="utf-8") as arquivo:
            # Aqui, estamos criando um dicionário com duas chaves:
            json.dump({"senha": dados_conta, "familia": dados_familia, "membros": dados_quantidade, "pontos": dados_pontos,
                       "apartamento": dados_apartamento, "verificador": dados_codigov}, arquivo, indent=4, ensure_ascii=False)
            aviso_sistema()
        
        

janela.mainloop()

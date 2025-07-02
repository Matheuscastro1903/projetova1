
import customtkinter as ctk
from PIL import Image
import json
import csv
import time
import re
import random
#interface

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
    verificador = int(entrada_verificador.get().strip())

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

def conferir_adm(entrada_emailadm,entrada_codigoadm):

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
    for widget in janela.winfo_children():
        widget.destroy()

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
                           command=lambda: atualizar_dados(email, senha, frame_principalmenu,frame_menu), cursor="hand2")
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
    
    # Frame do rodapé
    frame_rodape = ctk.CTkFrame(frame_menu, fg_color="#f0f0f0", height=30)
    frame_rodape.pack(fill="x", side="bottom")

    texto_rodape = ctk.CTkLabel(
    frame_rodape, text="Versão 2.0 • Suporte: ecodropsuporte@gmail.com", text_color="#5f6368", font=("Arial", 10))
    texto_rodape.pack()
    
    frame_menu.pack(fill="both", expand=True)



    pass

def mostrar_dados(email, senha, frame_principalmenu):
    """
    📊 Função: Mostrar Dados
    Mostra os principais dados da conta do usuário (exceto senha e código verificador por segurança).
    Utilizada para que o usuário possa revisar as informações do seu cadastro.
    """
    pass


def atualizar_dados(email, senha, frame_principalmenu,frame_menu):
    """
    🔄 Função: Atualizar Dados, onde será possível o usuário atualizar seus dados
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    atualizar_label_titulo = ctk.CTkLabel(frame_principalmenu, text="Informe seus dados:",
                                          fg_color="#ffffff", text_color="blue", font=("Arial", 20))
    atualizar_label_titulo.pack(pady=1)

    atualizar_label_aviso = ctk.CTkLabel(frame_principalmenu, text=" ",
                                         fg_color="#ffffff", text_color="blue", font=("Arial", 20))
    atualizar_label_aviso.pack(pady=1)

    # 1 - Entrada Email
    atualizar_label_email = ctk.CTkLabel(frame_principalmenu, text="Digite seu email:",
                                         text_color="#000000", anchor="w", width=300)
    atualizar_label_email.pack(pady=(1, 0))

    atualizar_entrada_email = ctk.CTkEntry(frame_principalmenu, width=300)
    atualizar_entrada_email.pack(pady=1)

    # 2 - Nome da família
    atualizar_label_nome = ctk.CTkLabel(frame_principalmenu, text="Digite o nome da sua família",
                                        text_color="#000000", anchor="w", width=300)
    atualizar_label_nome.pack(pady=(1, 0))

    atualizar_entrada_nome = ctk.CTkEntry(frame_principalmenu, width=300, validate="key", validatecommand=(
        janela.register(validar_letras_espacos), "%P"))
    atualizar_entrada_nome.pack(pady=1)

    # 3 - Senha
    atualizar_label_senha = ctk.CTkLabel(frame_principalmenu, text="Senha (mínimo 4 caracteres):",
                                         text_color="#000000", anchor="w", width=300)
    atualizar_label_senha.pack(pady=(1, 0))

    atualizar_entrada_senha = ctk.CTkEntry(frame_principalmenu, width=300, show="*")
    atualizar_entrada_senha.pack(pady=1)

    # 4 - Quantidade de membros
    atualizar_label_qmembros = ctk.CTkLabel(frame_principalmenu, text="Quantidade de membros na família:",
                                            text_color="#000000", anchor="w", width=300)
    atualizar_label_qmembros.pack(pady=(1, 0))

    atualizar_entrada_qmembros = ctk.CTkEntry(frame_principalmenu, width=300, validate="key", validatecommand=(
        janela.register(validar_numeros), "%P"))
    atualizar_entrada_qmembros.pack(pady=1)

    # 5 - Número do apartamento
    atualizar_label_numeroap = ctk.CTkLabel(frame_principalmenu, text="Digite o número do seu apartamento",
                                            text_color="#000000", anchor="w", width=300)
    atualizar_label_numeroap.pack(pady=(1, 0))

    atualizar_entrada_numeroap = ctk.CTkEntry(frame_principalmenu, width=300, validate="key", validatecommand=(
        janela.register(validar_numeros), "%P"))
    atualizar_entrada_numeroap.pack(pady=1)

    # 6 - Código verificador
    atualizar_label_verificador = ctk.CTkLabel(frame_principalmenu, text="Digite seu código verificador (mínimo 4 caracteres):",
                                               text_color="#000000", anchor="w", width=300)
    atualizar_label_verificador.pack(pady=(1, 0))

    atualizar_entrada_verificador = ctk.CTkEntry(frame_principalmenu, width=300, validate="key", validatecommand=(
        janela.register(validar_numeros), "%P"))
    atualizar_entrada_verificador.pack(pady=1)

    # Botão de atualizar
    atualizar_botao_confirmar = ctk.CTkButton(frame_principalmenu, text="Atualizar", fg_color="blue",
                                              text_color="#ffffff", width=300,
                                              command=lambda: conferir_atualizar(email,
                                                  atualizar_entrada_email,
                                                  atualizar_entrada_nome,
                                                  atualizar_entrada_senha,
                                                  atualizar_entrada_qmembros,
                                                  atualizar_entrada_numeroap,
                                                  atualizar_entrada_verificador,
                                                  atualizar_label_aviso,frame_menu))
    atualizar_botao_confirmar.pack(pady=5)



def conferir_atualizar(email,atualizar_entrada_email, atualizar_entrada_nome, atualizar_entrada_senha,
                        atualizar_entrada_qmembros, atualizar_entrada_numeroap,
                        atualizar_entrada_verificador, atualizar_label_aviso,frame_menu):
    """
    ✅ Função: Conferir Atualizar - Verifica se os dados inseridos são válidos antes de prosseguir com a atualização.
    """

    # Coletando e limpando os dados
    email_novo = atualizar_entrada_email.get().strip()
    nome_familia = atualizar_entrada_nome.get().strip()
    senha = atualizar_entrada_senha.get().strip()
    verificador = atualizar_entrada_verificador.get().strip()
    quantidade_pessoas=atualizar_entrada_qmembros.get().strip()
    apartamento=atualizar_entrada_numeroap.get().strip()


    # Tenta converter os campos numéricos
    email_antigo=email

    # Lista de campos que devem estar preenchidos
    entradas = [email_novo, nome_familia,quantidade_pessoas, apartamento]

    # Verifica se algum campo está vazio
    if any(str(campo) == "" for campo in entradas):
        atualizar_label_aviso.configure(text="Todos os campos devem ser preenchidos.", text_color="red")
        return

    # Validação do tamanho da senha
    if len(senha) < 4 or len(senha) > 20:
        atualizar_label_aviso.configure(text="A senha deve ter entre 4 e 20 caracteres.", text_color="red")
        return

    # Validação do código verificador
    if len(verificador) < 4 or len(verificador) > 20:
        atualizar_label_aviso.configure(text="O código verificador deve ter entre 4 e 20 caracteres.", text_color="red")
        return

    # Se passou por todas as validações
    atualizar_emailvalido(email_antigo,email_novo,senha,verificador,quantidade_pessoas,apartamento,nome_familia,atualizar_label_aviso,frame_menu)

    # Aqui você pode chamar a função que realmente faz a atualização no sistema/banco
    # exemplo: atualizar_usuario(email, nome_familia, senha, quantidade_pessoas, apartamento, verificador)

def atualizar_emailvalido(email_antigo,email_novo,senha,verificador,quantidade_pessoas,apartamento,nome_familia,atualizar_label_aviso,frame_menu):
    dominios_validos = [
            'gmail.com', 'outlook.com', 'hotmail.com',
            'yahoo.com', 'icloud.com'
        ]

        
            # VERIFICA SE O FORMATO DO EMAIL ESTÁ ESCRITO CORRETAMENTE
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',email_novo):
        #label_aviso é uma variável global,não necessitando importar para edita-la
        atualizar_label_aviso.configure(text="Formato inválido", text_color="red")
        return
            

                  # volta pro início do while para validar de novo,caso esteja correto,irá passar pelo verificador

            # VERIFICA APENAS O DOMÍNIO,SEPARA TODO O RESTO E PEGA APENAS A PARTE DO DOMÍNIO
    dominio = email_novo.split('@')[1].lower()
    if dominio not in dominios_validos:
        atualizar_label_aviso.configure(text="DOMÍNIO INVÁLIDO", text_color="red")
        return
    atualizar_conferiremail(email_antigo,email_novo,senha,verificador,quantidade_pessoas,apartamento,nome_familia,atualizar_label_aviso,frame_menu)

    pass

def atualizar_conferiremail(email_antigo,email_novo,senha,verificador,quantidade_pessoas,apartamento,nome_familia,atualizar_label_aviso,frame_menu):
    if email_novo.strip() in dados_conta:#dessa forma verificará se o email está já cadastrado ou não
        atualizar_label_aviso.configure(text="Email já cadastrado.",text_color="red")
        return     
    else:
        atualizar_conferirap(email_antigo,email_novo,senha,verificador,quantidade_pessoas,apartamento,nome_familia,atualizar_label_aviso,frame_menu)

    pass

def atualizar_conferirap(email_antigo,email_novo,senha,verificador,quantidade_pessoas,apartamento,nome_familia,atualizar_label_aviso,frame_menu):
    if apartamento in dados_apartamento.values():
            atualizar_label_aviso.configure(text="APARTAMENTO JÁ CADASTRADO.TENTE NOVAMENTE")
    else:
        atualizar_conta(email_antigo,email_novo,senha,verificador,quantidade_pessoas,apartamento,nome_familia,atualizar_label_aviso,frame_menu)

    pass

def atualizar_conta(email_antigo,email_novo,senha,verificador,quantidade_pessoas,apartamento,nome_familia,atualizar_label_aviso,frame_menu):
    pontos=dados_pontos[email_antigo]

    dados_conta.pop(email_antigo, None)
    dados_conta[email_novo] = senha

    dados_familia.pop(email_antigo, None)
    dados_familia[email_novo] = nome_familia

    dados_quantidade.pop(email_antigo, None)
    dados_quantidade[email_novo] = quantidade_pessoas

    dados_pontos.pop(email_antigo, None)
    dados_pontos[email_novo] = pontos  # Certifique-se que a variável `pontos` esteja definida

    dados_apartamento.pop(email_antigo, None)
    dados_apartamento[email_novo] = apartamento

    dados_codigov.pop(email_antigo, None)
    dados_codigov[email_novo] = verificador

# Reescreve todo o JSON com os dados atualizados
    with open("banco_dados.JSON", "w", encoding="utf-8") as arquivo:
        json.dump({
        "senha": dados_conta,
        "familia": dados_familia,
        "membros": dados_quantidade,
        "pontos": dados_pontos,
        "apartamento": dados_apartamento,
        "verificador": dados_codigov
        }, arquivo, indent=4, ensure_ascii=False)

        mostrar_frameatualizar(frame_menu)
        pass

def mostrar_frameatualizar(frame_menu):
    
    frame_menu.pack_forget()
    frame_avisoatualizar=ctk.CTkFrame(janela,fg_color="#ffffff")
    # Label de aviso
    label = ctk.CTkLabel(frame_avisoatualizar, text="Atualização  realizada com sucesso!", font=("Arial", 50), text_color="#1A73E8")
    label.pack(pady=(40, 20))
    # Botão para ir para login
    label2=ctk.CTkLabel(frame_avisoatualizar,text="Reiniciando o sistema em 7 segundos", font=("Arial", 50), text_color="#1A73E8")
    label2.pack(pady=(40, 20))
    frame_avisoatualizar.pack(fill="both",expand=True)
    janela.after(7000,sair_sitema)
   

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
    
    for widget in janela.winfo_children():
        widget.destroy()

    frame_topoeducativo = ctk.CTkFrame(janela, fg_color="#1A73E8", height=80)
    frame_topoeducativo.pack(fill="x")

    titulo_educativo = ctk.CTkLabel(frame_topoeducativo, text="💧 ÁREA EDUCATIVA",
                                    text_color="#ffffff", font=("Arial", 24, "bold"))
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
                         command=lambda: area_educativa1(frame_educativo, email, senha, frame_menu))
    btn1.pack(fill="x", pady=10)

    btn2 = ctk.CTkButton(frame_educativo,
                         text="Cientistas desenvolvem tecnologia para extrair água potável do ar usando resíduos alimentares",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=lambda: area_educativa2(frame_educativo, email, senha, frame_menu))
    btn2.pack(fill="x", pady=10)

    btn3 = ctk.CTkButton(frame_educativo,
                         text="Universidade do Texas inicia construção do maior centro universitário de reúso de água dos EUA",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=lambda: area_educativa3(frame_educativo, email, senha, frame_menu))
    btn3.pack(fill="x", pady=10)

    btn4 = ctk.CTkButton(frame_educativo,
                         text="Alunos serão instruídos sobre conservação da água e limpeza do rio Ganges na Índia",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=lambda: area_educativa4(frame_educativo, email, senha, frame_menu))
    btn4.pack(fill="x", pady=10)

    btn5 = ctk.CTkButton(frame_educativo,
                         text="Impacto dos datacenters em áreas com escassez hídrica na América Latina",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=lambda: area_educativa5(frame_educativo, email, senha, frame_menu))
    btn5.pack(fill="x", pady=10)

    btn6 = ctk.CTkButton(frame_educativo,
                         text="8 filmes educativos para crianças sobre sustentabilidade",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=lambda: area_educativa6(frame_educativo, email, senha, frame_menu))
    btn6.pack(fill="x", pady=10)


    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="white",
                                 text_color="#1A73E8",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: mostrar_menu(email, senha))
    botao_voltar.pack(pady=20)

    frame_educativo.pack(fill="both", expand=True, padx=20, pady=10)


def area_educativa1(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🌍 Investimento de €15 bilhões para combater a crise hídrica na Europa",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # Parágrafo da notícia
    corpo_texto = (
        "A Universidade Europeia e o Banco Europeu de Investimento anunciaram, em 7 de junho, "
        "um aporte de €15 bilhões (≈US$17bi) a projetos voltados à redução da poluição, "
        "prevenção do desperdício e fomento à inovação no setor hídrico ao longo dos próximos três anos. "
        "A ação considera a intensificação das secas e pressões agrícolas e urbanas causadas pelas mudanças climáticas. "
        "Como medida de responsabilização, o Reino Unido restringiu bônus a executivos de empresas de água que não investem "
        "o suficiente na qualidade dos corpos de água."
    )

    label_corpo = ctk.CTkLabel(frame_educativo,
                               text=corpo_texto,
                               text_color="#333333",
                               font=("Arial", 14),
                               wraplength=800,
                               justify="left")
    label_corpo.pack(pady=10)

    # Destaque: Por que isso importa?
    label_importancia = ctk.CTkLabel(frame_educativo,
                                     text="💡 Por que isso importa?",
                                     text_color="#1A73E8",
                                     font=("Arial", 20, "bold"),
                                     wraplength=800,
                                     justify="left")
    label_importancia.pack(pady=(20, 5))

    texto_importancia = (
        "Esse investimento maciço pode impulsionar tecnologias verdes, infraestrutura resiliente e processos de governança "
        "que garantam água limpa e gestão sustentável,uma virada estratégica para enfrentar a escassez hídrica em regiões vulneráveis."
    )

    label_texto_importancia = ctk.CTkLabel(frame_educativo,
                                           text=texto_importancia,
                                           text_color="#000000",
                                           font=("Arial", 14),
                                           wraplength=800,
                                           justify="left")
    label_texto_importancia.pack(pady=5)

    # Fontes
    label_fontes = ctk.CTkLabel(frame_educativo,
                                text="🔗 Fontes:",
                                text_color="#1A73E8",
                                font=("Arial", 14, "bold"),
                                wraplength=800,
                                justify="left")
    label_fontes.pack(pady=(20, 5))

 
    
    lbl = ctk.CTkLabel(frame_educativo,
                           text="• reuters.com",
                           text_color="#333333",
                           font=("Arial", 13),
                           anchor="w",
                           justify="left")
    lbl.pack()

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="white",
                                 text_color="#1A73E8",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)

 
def area_educativa2(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🎒 Extração de água potável do ar usando alimentos",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # Parágrafo da notícia
    corpo_texto = (
        "Pesquisadores da Universidade do Texas em Austin publicaram, em abril, um método inovador para captar água do ar "
        "usando hidrogéis feitos com biomassa de resíduos alimentares e conchas. Esses materiais absorvem grandes volumes "
        "de umidade e liberam água pura com aquecimento leve. Em campo, foram obtidos 15L de água por kg de gel por dia—"
        "recuperando 95% do volume captado."
    )

    label_corpo = ctk.CTkLabel(frame_educativo,
                               text=corpo_texto,
                               text_color="#333333",
                               font=("Arial", 14),
                               wraplength=800,
                               justify="left")
    label_corpo.pack(pady=10)

    # Destaque: Impacto prático
    label_importancia = ctk.CTkLabel(frame_educativo,
                                     text="💡 Impacto prático:",
                                     text_color="#1A73E8",
                                     font=("Arial", 20, "bold"),
                                     wraplength=800,
                                     justify="left")
    label_importancia.pack(pady=(20, 5))

    texto_importancia = (
        "Trata-se de uma solução biodegradável, modular e de baixo consumo energético — ideal para comunidades rurais, "
        "irrigação localizada ou situações emergenciais em áreas carentes de infraestrutura hídrica."
    )

    label_texto_importancia = ctk.CTkLabel(frame_educativo,
                                           text=texto_importancia,
                                           text_color="#000000",
                                           font=("Arial", 14),
                                           wraplength=800,
                                           justify="left")
    label_texto_importancia.pack(pady=5)

    # Fontes
    label_fontes = ctk.CTkLabel(frame_educativo,
                                text="🔗 Fontes:",
                                text_color="#1A73E8",
                                font=("Arial", 14, "bold"),
                                wraplength=800,
                                justify="left")
    label_fontes.pack(pady=(20, 5))

    lbl = ctk.CTkLabel(frame_educativo,
                       text="• foodandwine.com",
                       text_color="#333333",
                       font=("Arial", 13),
                       anchor="w",
                       justify="left")
    lbl.pack()

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="white",
                                 text_color="#1A73E8",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)


def area_educativa3(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🏗️ UT Austin constrói o maior centro universitário de reúso de água nos EUA",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # Parágrafo da notícia
    corpo_texto = (
        "Em maio, a UT anunciou a construção do WaterHub, instalação de 900m² que vai tratar até 1 milhão de galões "
        "(≈3,8 mil m³) de esgoto por dia. A previsão de operação é para o segundo semestre de 2027. O local servirá como laboratório "
        "de pesquisa prática para estudantes, integrando ensino e teste de tecnologias de reúso para aliviar sistemas municipais sobrecarregados."
    )

    label_corpo = ctk.CTkLabel(frame_educativo,
                               text=corpo_texto,
                               text_color="#333333",
                               font=("Arial", 14),
                               wraplength=800,
                               justify="left")
    label_corpo.pack(pady=10)

    # Destaque: Impacto prático (pode deixar o título como "💡 Por que isso importa?" para manter padrão, ou "Impacto prático")
    label_importancia = ctk.CTkLabel(frame_educativo,
                                     text="💡 Por que isso importa?",
                                     text_color="#1A73E8",
                                     font=("Arial", 20, "bold"),
                                     wraplength=800,
                                     justify="left")
    label_importancia.pack(pady=(20, 5))

    texto_importancia = (
        "Esse centro universitário vai impulsionar a pesquisa e o desenvolvimento de tecnologias inovadoras de reúso de água, "
        "contribuindo para a sustentabilidade urbana e formação técnica avançada."
    )

    label_texto_importancia = ctk.CTkLabel(frame_educativo,
                                           text=texto_importancia,
                                           text_color="#000000",
                                           font=("Arial", 14),
                                           wraplength=800,
                                           justify="left")
    label_texto_importancia.pack(pady=5)

    # Fontes
    label_fontes = ctk.CTkLabel(frame_educativo,
                                text="🔗 Fontes:",
                                text_color="#1A73E8",
                                font=("Arial", 14, "bold"),
                                wraplength=800,
                                justify="left")
    label_fontes.pack(pady=(20, 5))

    lbl = ctk.CTkLabel(frame_educativo,
                       text="• axios.com",
                       text_color="#333333",
                       font=("Arial", 13),
                       anchor="w",
                       justify="left")
    lbl.pack()

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="white",
                                 text_color="#1A73E8",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)


def area_educativa4(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(frame_educativo,
                          text="📰 Educação Ambiental na Índia: Estudantes de Uttar Pradesh se tornam embaixadores da limpeza",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # Parágrafo da notícia
    corpo_texto = (
        "Em junho de 2024, o governo do estado de Uttar Pradesh, na Índia, lançou uma iniciativa educativa para envolver os alunos "
        "das escolas públicas e privadas na conservação ambiental e limpeza do rio Ganges, um dos maiores e mais sagrados rios da Ásia. "
        "O programa inclui formação de “embaixadores estudantis da limpeza”, práticas de higiene e conservação hídrica, visitas a locais "
        "poluídos, plantio de árvores, redações, campanhas ambientais e integração da comunidade escolar e familiar."
    )

    label_corpo = ctk.CTkLabel(frame_educativo,
                               text=corpo_texto,
                               text_color="#333333",
                               font=("Arial", 14),
                               wraplength=800,
                               justify="left")
    label_corpo.pack(pady=10)

    # Destaque: Por que isso importa?
    label_importancia = ctk.CTkLabel(frame_educativo,
                                     text="💡 Por que isso importa?",
                                     text_color="#1A73E8",
                                     font=("Arial", 20, "bold"),
                                     wraplength=800,
                                     justify="left")
    label_importancia.pack(pady=(20, 5))

    texto_importancia = (
        "A iniciativa ajuda a sensibilizar jovens sobre a conservação hídrica e atitudes sustentáveis desde cedo, "
        "envolvendo também suas famílias e escolas, o que pode gerar impacto real na limpeza do Ganges e na formação de cidadãos conscientes."
    )

    label_texto_importancia = ctk.CTkLabel(frame_educativo,
                                           text=texto_importancia,
                                           text_color="#000000",
                                           font=("Arial", 14),
                                           wraplength=800,
                                           justify="left")
    label_texto_importancia.pack(pady=5)

    # Fontes
    label_fontes = ctk.CTkLabel(frame_educativo,
                                text="🔗 Fontes:",
                                text_color="#1A73E8",
                                font=("Arial", 14, "bold"),
                                wraplength=800,
                                justify="left")
    label_fontes.pack(pady=(20, 5))

    lbl = ctk.CTkLabel(frame_educativo,
                       text="• timesofindia.indiatimes.com",
                       text_color="#333333",
                       font=("Arial", 13),
                       anchor="w",
                       justify="left")
    lbl.pack()

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="white",
                                 text_color="#1A73E8",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)


def area_educativa5(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(frame_educativo,
                          text="📰 Impacto dos datacenters em áreas com escassez hídrica na América Latina",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # Parágrafo da notícia
    corpo_texto = (
        "Um artigo do The Guardian chama atenção para a instalação de grandes datacenters em regiões "
        "com escassez de água no Brasil e outros países da América Latina. Um dos casos citados em Caucaia (CE) "
        "está em regiões afetadas por seca, e esses centros utilizam até 80 % da água retirada para resfriamento, "
        "gerando riscos de esgotamento de recursos hídricos locais. O texto destaca a necessidade de maior transparência, "
        "engajamento comunitário e uso de alternativas como dessalinização e reúso."
    )

    label_corpo = ctk.CTkLabel(frame_educativo,
                               text=corpo_texto,
                               text_color="#333333",
                               font=("Arial", 14),
                               wraplength=800,
                               justify="left")
    label_corpo.pack(pady=10)

    # Destaque: Por que isso importa?
    label_importancia = ctk.CTkLabel(frame_educativo,
                                     text="💡 Por que isso importa?",
                                     text_color="#1A73E8",
                                     font=("Arial", 20, "bold"),
                                     wraplength=800, justify="left")
    label_importancia.pack(pady=(20, 5))

    texto_importancia = (
        "Educação ambiental sobre impactos tecnológicos no ciclo da água.\n\n"
        "Inovação na busca por soluções de resfriamento menos dependentes de água.\n\n"
        "Reflexão sobre políticas de concessão hídrica e planejamento sustentável."
    )

    label_texto_importancia = ctk.CTkLabel(frame_educativo,
                                           text=texto_importancia,
                                           text_color="#000000",
                                           font=("Arial", 14),
                                           wraplength=800,
                                           justify="left")
    label_texto_importancia.pack(pady=5)

    # Fontes
    label_fontes = ctk.CTkLabel(frame_educativo,
                                text="🔗 Fontes:",
                                text_color="#1A73E8",
                                font=("Arial", 14, "bold"),
                                wraplength=800,
                                justify="left")
    label_fontes.pack(pady=(20, 5))

    lbl = ctk.CTkLabel(frame_educativo,
                       text="• theguardian.com",
                       text_color="#333333",
                       font=("Arial", 13),
                       anchor="w",
                       justify="left")
    lbl.pack()

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="white",
                                 text_color="#1A73E8",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)

def area_educativa6(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título principal menor e com menos espaçamento
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🌿 8 Filmes sobre Sustentabilidade para Crianças",
                          text_color="#1A73E8",
                          font=("Arial", 16, "bold"),  # fonte menor
                          wraplength=800,
                          justify="left")
    titulo.pack(pady=(10, 5))  # menos espaçamento

    filmes = [
        ("Wall-E (2008)", "Um clássico da Pixar! Mostra um futuro onde a Terra foi tomada pelo lixo e a humanidade vive no espaço. Wall-E, um robô solitário, nos ensina sobre consumo, lixo e amor pelo planeta."),
        ("Lorax: Em Busca da Trúfula Perdida (2012)", "Baseado na obra do Dr. Seuss, aborda desmatamento e exploração de recursos naturais, com personagens carismáticos e músicas cativantes."),
        ("Happy Feet: O Pinguim (2006)", "Através de um pinguim dançarino, o filme aborda temas como mudança climática, preservação dos oceanos e o impacto da pesca predatória."),
        ("Rio (2011)", "Além da aventura, mostra a importância da biodiversidade brasileira e os perigos do tráfico de animais silvestres."),
        ("Irmão Urso (Brother Bear) (2003)", "Aborda o respeito à natureza, ao ciclo da vida e à conexão espiritual com o meio ambiente, com forte mensagem sobre empatia e equilíbrio natural."),
        ("A Fuga das Galinhas (Chicken Run) (2000)", "Uma metáfora inteligente sobre liberdade animal e os impactos da agroindústria – adaptado ao humor infantil."),
        ("O Rei Leão (1994 / 2019)", "Apesar de não focar diretamente em sustentabilidade, ensina sobre o “ciclo da vida” e o equilíbrio ecológico da savana africana."),
        ("Meu Amigo Totoro (1988)", "Um clássico do Studio Ghibli. Exalta a harmonia entre seres humanos e natureza, com um toque mágico e poético.")
    ]
        

    for titulo_filme, descricao in filmes:
        label_filme_titulo = ctk.CTkLabel(frame_educativo,
                                          text=titulo_filme,
                                          text_color="#1A73E8",
                                          font=("Arial", 14, "bold"),  # fonte menor
                                          wraplength=800,
                                          justify="left")
        label_filme_titulo.pack(padx=20, pady=(8, 2), anchor="w")  # menos espaçamento

        label_filme_desc = ctk.CTkLabel(frame_educativo,
                                        text=descricao,
                                        text_color="#333333",
                                        font=("Arial", 12),  # fonte menor
                                        wraplength=800,
                                        justify="left")
        label_filme_desc.pack(padx=20, pady=(0, 6), anchor="w")  # menos espaçamento

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="white",
                                 text_color="#1A73E8",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=30)



def sair_sitema():
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

entrada_nome = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(janela.register(validar_letras_espacos), "%P"))
entrada_nome.pack(pady=1)

# 3-Entrada Senha
label_senha = ctk.CTkLabel(frame_cadastro, text="Senha (mínimo 4 caracteres):",text_color="#000000", anchor="w", width=300)
label_senha.pack(pady=(1, 0))

entrada_senha = ctk.CTkEntry(frame_cadastro, width=300, show="*")
entrada_senha.pack(pady=1)

# 4. Campo Quantidade de membros
label_qmembros = ctk.CTkLabel(frame_cadastro, text="Quantidade de membros na família:", text_color="#000000", anchor="w", width=300)
label_qmembros.pack(pady=(1, 0))
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


botao_cadastrar = ctk.CTkButton(frame_cadastro, text="Cadastrar", fg_color="blue",
                                text_color="#ffffff", width=300, command=lambda: conferir_cadastrar(entrada_email,entrada_nome,entrada_senha,
                                                                                                    entrada_qmembros,
                                                                                                   entrada_numeroap,entrada_verificador,label_aviso))
botao_cadastrar.pack(pady=10)

# botão de voltar
botao_voltarinicial = ctk.CTkButton(frame_cadastro, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
botao_voltarinicial.pack()


#####################################
"""Parte do frame adm(modo administrador"""
frame_adm = ctk.CTkFrame(janela, fg_color="#ffffff")
label_adm = ctk.CTkLabel(frame_adm, text="Informe seus dados:",fg_color="#ffffff", text_color="blue", font=("Arial", 30))
label_adm.pack(pady=1)

label_adm = ctk.CTkLabel(frame_adm, text=" ",fg_color="#ffffff", text_color="blue", font=("Arial", 25))
label_adm.pack(pady=1)

# 1-Entrada Nome
label_emailadm = ctk.CTkLabel(frame_adm, text="Digite seu email:",
                           text_color="#000000", anchor="w", width=300)
label_emailadm.pack(pady=(1, 0))

entrada_emailadm = ctk.CTkEntry(frame_adm, width=300)
entrada_emailadm.pack(pady=1)

# 1-Entrada Nome
label_codigoadm = ctk.CTkLabel(frame_adm, text="Digite código de administrador:",
                           text_color="blue", anchor="w", width=300)
label_codigoadm.pack(pady=(1, 0))

entrada_codigoadm = ctk.CTkEntry(frame_adm, width=300)
entrada_codigoadm.pack(pady=1)

botao_modoadm = ctk.CTkButton(frame_adm, text="Entrar modo adm", fg_color="blue",
                                text_color="#ffffff", width=300, command=lambda:conferir_adm(entrada_emailadm,entrada_codigoadm))
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
botao_sair = ctk.CTkButton(frame_aviso, text="Sair do Sistema", width=200, fg_color="red", hover_color="#cc0000", command=sair_sitema)
botao_sair.pack()


###############################################
frame_avisoatualizar=ctk.CTkFrame(janela,fg_color="#ffffff")
 # Label de aviso
label = ctk.CTkLabel(frame_avisoatualizar, text="Atualização  realizada com sucesso!", font=("Arial", 50), text_color="green")
label.pack(pady=(40, 20))
    # Botão para ir para login
label2=ctk.CTkLabel(frame_avisoatualizar,text="Reiniciando o sistema em 7 segundos", font=("Arial", 50), text_color="green")
label2.pack(pady=(40, 20))
    # Botão para sair do sistema



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

        
            # VERIFICA SE O FORMATO DO EMAIL ESTÁ ESCRITO CORRETAMENTE
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            #label_aviso é uma variável global,não necessitando importar para edita-la
            label_aviso.configure(text="Formato inválido", text_color="red")
            return
            

                  # volta pro início do while para validar de novo,caso esteja correto,irá passar pelo verificador

            # VERIFICA APENAS O DOMÍNIO,SEPARA TODO O RESTO E PEGA APENAS A PARTE DO DOMÍNIO
        dominio = self.email.split('@')[1].lower()
        if dominio not in dominios_validos:
            label_aviso.configure(text="Domínio não aceito", text_color="red")
            return

                # continuar o loop sem parar
                

        # Se chegou aqui, formato e domínio estão corretos
            

        
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

            if self.email.strip() in dados_conta:#dessa forma verificará se o email está já cadastrado ou não
                label_aviso.configure(text="Email já cadastrado.",text_color="red")
                return
            
            else:
                self.conferir_ap()  # Continua o processo normalmente

    def conferir_ap(self):
        
       #FUNÇÃO UTILIZADA PARA ANALISAR SE O APARTAMENTO JÁ ESTÁ CADASTRADO OU NÃO
        if self.apartamento in dados_apartamento.values():
            label_aviso.configure(text="APARTAMENTO JÁ CADASTRADO.TENTE NOVAMENTE")
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

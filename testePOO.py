import customtkinter as ctk
from customtkinter import CTkImage, CTkLabel

from PIL import Image
import json
import csv
import time
import re
import random
import pandas as pd
import matplotlib as plt
from collections import Counter
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Carregamento dos dados globais
with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
    arquivo_lido = json.load(arquivo)
    dados_conta = arquivo_lido["senha"]
    dados_familia = arquivo_lido["familia"]
    dados_quantidade = arquivo_lido["membros"]
    dados_pontos = arquivo_lido["pontos"]
    dados_apartamento = arquivo_lido["apartamento"]
    dados_codigov = arquivo_lido["verificador"]
    dados_ultimo_quiz = arquivo_lido.get("ultimo_quiz", {})
    dados_questoes_quiz = arquivo_lido.get("questoes_quiz", [])

with open(r"dados_usuarios.json", "r", encoding="utf-8") as arquivo:
    dados_lidos = json.load(arquivo)
    dados_consumo = dados_lidos["consumo"]

# Prêmios disponíveis para resgate
premios_disponiveis = [
    {"nome": "Voucher de R$ 10", "custo": 100},
    {"nome": "Desconto de 5% na conta de água", "custo": 200},
    {"nome": "Kit de produtos sustentáveis", "custo": 300},
    {"nome": "Voucher de R$ 25", "custo": 500},
    {"nome": "Desconto de 10% na conta de água", "custo": 800},
    {"nome": "Voucher de R$ 50", "custo": 1000}
]

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

# Funções de validação
def validar_numeros(novo_texto):
    """Função utilizada para permitir digitar apenas números"""
    return novo_texto.isdigit() or novo_texto == ""

def validar_letras_espacos(novo_texto):
    """Função utilizada para deixar apenas digitar letras e espaços"""
    return all(c.isalpha() or c.isspace() for c in novo_texto) or novo_texto == ""

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ECODROP SYSTEM")
        self.geometry("1000x800+400+150")
        self.resizable(False, False)

        # Inicializa atributos para evitar erro de acesso
        self.tela_inicial = None
        self.tela_login = None
        self.tela_cadastro = None
        self.tela_sobrenos = None
        self.tela_modoadm = None
        self.tela_menu = None
        
        # Lista para ocultar todas as telas
        self.telas = []
        # chamemento da função criar_tela_inicial
        self.criar_tela_inicial()

    def criar_tela_inicial(self):
        self.esquecer_frames()
        if self.tela_inicial is None:
            self.tela_inicial = TelaInicial(self, mostrar_login=self.criar_tela_login, mostrar_cadastro=self.criar_tela_cadastro,
                                            modo_adm=self.criar_tela_modoadm, sobre_nos=self.criar_tela_sobrenos)
            self.telas.append(self.tela_inicial)
        self.tela_inicial.pack(fill="both", expand=True)

    def criar_tela_login(self):
        self.esquecer_frames()
        if self.tela_login is None:
            self.tela_login = TelaLogin(
                self, voltar_inicial=self.criar_tela_inicial, 
                mostrar_menu=self.criar_tela_menu)
            self.telas.append(self.tela_login)

        self.tela_login.pack(fill="both", expand=True)

    def criar_tela_cadastro(self):
        self.esquecer_frames()
        if self.tela_cadastro is None:
            self.tela_cadastro = TelaCadastro(
                self, 
                voltar_inicial=self.criar_tela_inicial, 
                mostrar_login=self.criar_tela_login)
            self.telas.append(self.tela_cadastro)
        self.tela_cadastro.pack(fill="both", expand=True)

    def criar_tela_modoadm(self):
        self.esquecer_frames()

        if self.tela_modoadm is None:
            self.tela_modoadm = TelaModoAdm(self, voltar_inicial=self.criar_tela_inicial)
            
            self.telas.append(self.tela_modoadm)
            
        self.tela_modoadm.pack(fill="both", expand=True)

    def criar_tela_sobrenos(self):

        self.esquecer_frames()
        if self.tela_sobrenos is None:
            self.tela_sobrenos = TelaSobreNos(
                self, voltar_inicial=self.criar_tela_inicial)
            self.telas.append(self.tela_sobrenos)

        self.tela_sobrenos.pack(fill="both", expand=True)

    def criar_tela_menu(self,email,senha):
        
        self.esquecer_frames()
        self.tela_menu = UsuarioLogado(self,email,senha)
        self.telas.append(self.tela_menu)
        self.tela_menu.pack(fill='both', expand=True)

    def esquecer_frames(self):
        for frames in self.telas:
            if frames:
                frames.pack_forget()


class TelaInicial(ctk.CTkFrame):
    def __init__(self, master, mostrar_login, mostrar_cadastro, modo_adm, sobre_nos):
        super().__init__(master)

        # Frame topo
        self.frame_topo = ctk.CTkFrame(self, fg_color="#1A73E8", height=80)
        self.frame_topo.pack(fill="x")
        titulo = ctk.CTkLabel(self.frame_topo, text="💧 ECODROP",
                              text_color="#f0f0f0", font=("Arial", 24, "bold"))
        titulo.pack(pady=20)

        # Divisão principal
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="#f0f0f0")
        self.frame_conteudo.pack(fill="both", expand=True)

        # Menu lateral
        self.frame_lateral = ctk.CTkFrame(
            self.frame_conteudo, fg_color="#f0f0f0", width=200)
        self.frame_lateral.pack(side="left", fill="y")

        # Botões menu lateral com callbacks
        botao1 = ctk.CTkButton(self.frame_lateral, text="Login",
                               fg_color="#f0f0f0", text_color="#1A73E8",
                               font=("Arial", 12), anchor="w",
                               command=mostrar_login)
        botao1.pack(fill="x", pady=(20, 10), padx=10)

        botao2 = ctk.CTkButton(self.frame_lateral, text="Cadastro usuário",
                               fg_color="#f0f0f0", text_color="#1A73E8",
                               font=("Arial", 12), anchor="w",
                               command=mostrar_cadastro)
        botao2.pack(fill="x", pady=10, padx=10)

        botao3 = ctk.CTkButton(self.frame_lateral, text="Modo administrador",
                               fg_color="#f0f0f0", text_color="#1A73E8",
                               font=("Arial", 12), anchor="w",
                               command=modo_adm)
        botao3.pack(fill="x", pady=10, padx=10)

        botao4 = ctk.CTkButton(self.frame_lateral, text="Sobre nós",
                               fg_color="#f0f0f0", text_color="#1A73E8",
                               font=("Arial", 12), anchor="w",
                               command=sobre_nos)
        botao4.pack(fill="x", pady=10, padx=10)

        # Área principal de conteúdo
        self.frame_principal = ctk.CTkFrame(
            self.frame_conteudo, fg_color="#f0f0f0")
        self.frame_principal.pack(
            side="left", fill="both", expand=True, padx=30, pady=30)

        texto_bem_vindo = ctk.CTkLabel(self.frame_principal, text="Bem-vindo ao sistema ECODROP",
                                       text_color="#202124", font=("Arial", 22, "bold"))
        texto_bem_vindo.pack(pady=(0, 20))

        texto_instrucao = ctk.CTkLabel(self.frame_principal,
                                       text="Menos consumo, mais consciência, um planeta mais feliz.",
                                       text_color="#5f6368", wraplength=500, justify="left",
                                       font=("Arial", 18))
        texto_instrucao.pack()

        try:
            imagem = Image.open("fotos/mascoteprincipall.png")
            ctk_imagem = ctk.CTkImage(
                light_image=imagem, dark_image=imagem, size=(400, 400))
            label = ctk.CTkLabel(self.frame_principal, image=ctk_imagem, text="")
            label.pack()
        except:
            placeholder = ctk.CTkLabel(self.frame_principal, 
                                       text="🌊 EcoDrop Mascote 🌊",
                                       font=("Arial", 48))
            placeholder.pack(pady=50)

        # Rodapé
        self.frame_rodape = ctk.CTkFrame(
            self.frame_principal, fg_color="#f0f0f0", height=30)
        self.frame_rodape.pack(fill="x", side="bottom")

        texto_rodape = ctk.CTkLabel(self.frame_rodape, text="Versão 2.0 • Suporte: ecodropsuporte@gmail.com",
                                    text_color="#5f6368", font=("Arial", 10))
        texto_rodape.pack()


class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, voltar_inicial, mostrar_menu):
        super().__init__(master)
        self.voltar_inicial = voltar_inicial
        self.mostrar_menu = mostrar_menu
        self.frame_login = ctk.CTkFrame(self, fg_color="#ffffff")
        label_login = ctk.CTkLabel(self.frame_login, text="Informe seus dados:",
                                   fg_color="#ffffff", text_color="blue", font=("Arial", 20))
        label_login.pack(pady=2)
        self.label_avisologin = ctk.CTkLabel(
            self.frame_login, text=" ", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
        self.label_avisologin.pack(pady=2)

        # 1-entrada email
        label_emaillogin = ctk.CTkLabel(
            self.frame_login, text="Digite seu email:", text_color="#000000", anchor="w", width=300)
        label_emaillogin.pack(pady=(2, 0))

        self.entrada_emaillogin = ctk.CTkEntry(self.frame_login, width=300)
        self.entrada_emaillogin.pack(pady=2)

        # 2-entrada senha
        label_senhalogin = ctk.CTkLabel(
            self.frame_login, text="Digite sua senha:", text_color="#000000", anchor="w", width=300)
        label_senhalogin.pack(pady=(2, 0))

        self.entrada_senhalogin = ctk.CTkEntry(
            self.frame_login, width=300, show="*")
        self.entrada_senhalogin.pack(pady=2)

        # botão logar
        botao_logar = ctk.CTkButton(self.frame_login, text="Logar", fg_color="blue",
                                    text_color="#ffffff", width=300, command=self.conferir_logar)
        botao_logar.pack(pady=2)
        # botão voltar
        botao_voltarinicial = ctk.CTkButton(self.frame_login, text="Voltar", fg_color="blue", text_color="#ffffff", width=300,
                                            command=voltar_inicial)
        botao_voltarinicial.pack()

        self.frame_login.pack(fill="both", expand=True)

    def conferir_logar(self):
        """Função utilizada para verificar se há espaços em branco ao apertar o botão logar"""
        email = self.entrada_emaillogin.get().strip()
        senha = self.entrada_senhalogin.get().strip()
        if email == "" or senha == "":
            self.label_avisologin.configure(
                text="Preencha todos os campos.", text_color="red")
            return
        self.email = email
        self.senha = senha

        self.login()

    def login(self):
        """Função utilizada para verificar se email e senha estão corretos,para assim ir para o menu"""
        with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
            # quando usa json.load o arquivo json é transformado em dicionário python
            arquivo_lido = json.load(arquivo)

            dados_conta = arquivo_lido["senha"]

            if self.email in dados_conta:
                if dados_conta[self.email] == self.senha:
                    self.mostrar_menu(self.email,self.senha)
                    return
                else:
                    self.label_avisologin.configure(
                        text="EMAIL OU SENHA INCORRETO.\nContate o suporte para recuperar usa senha", text_color="red")
                    return

            else:
                self.label_avisologin.configure(
                    text="EMAIL NÃO CADASTRADO.\nVá para tela de cadastro")
                return


class TelaCadastro(ctk.CTkFrame):

    # Atributos de classe,servirão para todos os casos e evitará ter que criar uma lista toda vez que for verificar o email,melhorando

    DOMINIOS_VALIDOS = {"gmail.com", "outlook.com",
                        "hotmail.com", "yahoo.com", "icloud.com"}
    REGEX_EMAIL = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def __init__(self, master, voltar_inicial, mostrar_login):
        super().__init__(master)

        self.mostrar_login = mostrar_login

        self.frame_cadastro = ctk.CTkFrame(self, fg_color="#ffffff")
        self.frame_cadastro.pack(fill="both", expand=True)

        label_cadastro = ctk.CTkLabel(self.frame_cadastro, text="Informe seus dados:",
                                      fg_color="#ffffff", text_color="blue", font=("Arial", 20))
        label_cadastro.pack(pady=1)

        self.label_aviso = ctk.CTkLabel(self.frame_cadastro, text=" ",
                                        fg_color="#ffffff", text_color="blue", font=("Arial", 20))
        self.label_aviso.pack(pady=1)

        # 1 - Entrada email
        label_email = ctk.CTkLabel(self.frame_cadastro, text="Digite seu email:",
                                   text_color="#000000", anchor="w", width=300)
        label_email.pack(pady=(1, 0))

        self.entrada_email = ctk.CTkEntry(self.frame_cadastro, width=300)
        self.entrada_email.pack(pady=1)

        # 2 - Nome da família
        label_nome = ctk.CTkLabel(self.frame_cadastro, text="Digite o nome da sua família",
                                  text_color="#000000", anchor="w", width=300)
        label_nome.pack(pady=(1, 0))

        self.entrada_nome = ctk.CTkEntry(self.frame_cadastro, width=300,
                                         validate="key",
                                         validatecommand=(self.register(validar_letras_espacos), "%P"))
        self.entrada_nome.pack(pady=1)

        # 3 - Senha
        label_senha = ctk.CTkLabel(self.frame_cadastro, text="Senha (mínimo 4 caracteres):",
                                   text_color="#000000", anchor="w", width=300)
        label_senha.pack(pady=(1, 0))

        self.entrada_senha = ctk.CTkEntry(
            self.frame_cadastro, width=300, show="*")
        self.entrada_senha.pack(pady=1)

        # 4 - Quantidade de membros
        label_qmembros = ctk.CTkLabel(self.frame_cadastro, text="Quantidade de membros na família:",
                                      text_color="#000000", anchor="w", width=300)
        label_qmembros.pack(pady=(1, 0))

        self.entrada_qmembros = ctk.CTkEntry(self.frame_cadastro, width=300,
                                             validate="key",
                                             validatecommand=(self.register(validar_numeros), "%P"))
        self.entrada_qmembros.pack(pady=1)

        # 5 - Número do apartamento
        label_numeroap = ctk.CTkLabel(self.frame_cadastro, text="Digite o número do seu apartamento",
                                      text_color="#000000", anchor="w", width=300)
        label_numeroap.pack(pady=(1, 0))

        self.entrada_numeroap = ctk.CTkEntry(self.frame_cadastro, width=300,
                                             validate="key",
                                             validatecommand=(self.register(validar_numeros), "%P"))
        self.entrada_numeroap.pack(pady=1)

        # 6 - Código verificador
        label_verificador = ctk.CTkLabel(self.frame_cadastro, text="Digite seu código verificador\n(MÍNIMO 4 CARACTERES E APENAS NÚMEROS):",
                                         text_color="#000000", anchor="w", width=300)
        label_verificador.pack(pady=(1, 0))

        self.entrada_verificador = ctk.CTkEntry(self.frame_cadastro, width=300,
                                                validate="key", show="*",
                                                validatecommand=(self.register(validar_numeros), "%P"))
        self.entrada_verificador.pack(pady=1)

        # Botão cadastrar
        botao_cadastrar = ctk.CTkButton(self.frame_cadastro, text="Cadastrar",
                                        fg_color="blue", text_color="#ffffff", width=300,
                                        command=self.conferir_cadastrar)

        botao_cadastrar.pack(pady=10)

        # Botão voltar
        botao_voltar = ctk.CTkButton(self.frame_cadastro, text="Voltar",
                                     fg_color="blue", text_color="#ffffff", width=300,
                                     command=voltar_inicial)
        botao_voltar.pack()

    def conferir_cadastrar(self):
        email = self.entrada_email.get().strip()
        nome_familia = self.entrada_nome.get().strip()
        senha = self.entrada_senha.get().strip()
        quantidade_pessoas = self.entrada_qmembros.get().strip()
        apartamento = self.entrada_numeroap.get().strip()
        verificador = self.entrada_verificador.get().strip()

        entradas = [email, nome_familia, senha,
                    quantidade_pessoas, apartamento]
    # Verificação: se algum campo de texto estiver vazio
        if any(campo == "" for campo in entradas):
            self.label_aviso.configure(
                text="Todos os campos devem ser preenchidos.", text_color="red")
            return

    # Validação da senha
        if len(senha) < 4 or len(senha) > 20:
            self.label_aviso.configure(
                text="A senha deve ter entre 4 e 20 caracteres.", text_color="red")
            return

        if len(verificador) < 4 or len(verificador) > 20:
            self.label_aviso.configure(
                text="O código verificador deve ter entre 4 e 20 caracteres.", text_color="red")
            return
        
        #ESSES VERIFICADORES SERVIRÃO PARA DIZER SE O ANDAR E O APARTAMENTO É VÁLIDO OU NÃO
        possiveis_andares=["10","20","30","40","50","60","70","80","90"]
        possiveis_apartamentos=["01","02","03","04","05"]

        andar_valido = False
        apto_valido = False
        numero_valido=False
        
        
        if len(apartamento)==4:
            numero_valido=True

        for andar in possiveis_andares:
            #SÓ VALIDARÁ SE APARTAMENTO INICIAR COM O INTERÁVEL DA LISTA ANDAR
            if apartamento.startswith(andar):
                andar_valido = True
                #BREAK IRÁ QUEBRAR O LOOP FOR,ACABANDO A INTERAÇÃO
                break

        for apto in possiveis_apartamentos:
             #SÓ VALIDARÁ SE APARTAMENTO INICIAR COM O INTERÁVEL DA LISTA APARTAMENTO
            if apartamento.endswith(apto):
                apto_valido = True
                #BREAK IRÁ QUEBRAR O LOOP FOR,ACABANDO COM A INTERAÇÃO
                break

        if not (andar_valido and apto_valido and numero_valido): #VERIFICA SE AMBOS SÃO VÁLIDOS(TRUE)
            self.label_aviso.configure(text="Apartamento inválido", text_color="red")
            #return irá parar a função caso o aviso apareça
            return

        quantidade_pessoas = int(quantidade_pessoas)
        verificador = int(verificador)

        # NECESSÁRIO FAZER DESSA FORMA PARA EVITAR MÚLTIPLAS CHAMADAS DA FUNÇÃO GET,QUE PEGA VALORES DAS ENTRADAS
        self.email = email
        self.senha = senha
        self.nome_familia = nome_familia
        self.quantidade = quantidade_pessoas
        self.pontos = 0
        self.apartamento = int(apartamento)
        self.verificador = int(verificador)

        self.email_valido()

    def email_valido(self):

        # FUNÇÃO UTILIZADA PARA CONFERIR SE O EMAIL É VÁLIDO OU NÃO
        # VERIFICA SE O FORMATO DO EMAIL ESTÁ ESCRITO CORRETAMENTE
        # atributo de classe definido antes do init
        if not self.REGEX_EMAIL.match(self.email):
            self.label_aviso.configure(
                text="Formato inválido", text_color="red")
            return

            # volta pro início do while para validar de novo,caso esteja correto,irá passar pelo verificador

            # VERIFICA APENAS O DOMÍNIO,SEPARA TODO O RESTO E PEGA APENAS A PARTE DO DOMÍNIO
        dominio = self.email.split('@')[1].lower()
        if dominio not in self.DOMINIOS_VALIDOS:  # atributo de classe definido antes do init
            self.label_aviso.configure(
                text="Domínio não aceito", text_color="red")
            return

            # continuar o loop sem parar

        # Se chegou aqui, formato e domínio estão corretos

        self.conferir_email()

    def conferir_email(self):
        # FUNÇÃO UTILIZADA PARA CONFERIR SE O EMAIL JÁ ESTÁ CADASTRADO OU NÃO
        with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
            arquivo_lido = json.load(arquivo)
            dados_conta = arquivo_lido["senha"]

            if self.email.strip() in dados_conta:  # dessa forma verificará se o email está já cadastrado ou não
                self.label_aviso.configure(
                    text="Email já cadastrado.", text_color="red")
                return

            else:
                self.conferir_ap()  # Continua o processo normalmente

    def conferir_ap(self):

       # FUNÇÃO UTILIZADA PARA ANALISAR SE O APARTAMENTO JÁ ESTÁ CADASTRADO OU NÃO
        if self.apartamento in dados_apartamento.values():
            self.label_aviso.configure(
                text="APARTAMENTO JÁ CADASTRADO.TENTE NOVAMENTE", text_color="red")
        else:
            self.cadastrar_conta()

    def cadastrar_conta(self):

        # FUNÇÃO UTILIZADA PARA CADASTRAR CONTA NO BANCO DE DADOS

        try:
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
                self.mostrar_frame_aviso()
        except:
            self.label_aviso.configure(
                text="Banco de dados não está funcionando,tente mais tarde.")

    def mostrar_frame_aviso(self):
        """Parte do frame aviso(só será usada quando o usuário finalizar corretamente o cadastro,tendo a opção de ir para login ou sair do sistema"""
        for widget in self.frame_cadastro.winfo_children():
            widget.destroy()

        # Label de aviso
        label = ctk.CTkLabel(self.frame_cadastro, text="Cadastro realizado com sucesso!", font=(
            "Arial", 20), text_color="green")
        label.pack(pady=(40, 20))

        # Botão para ir para login
        botao_login = ctk.CTkButton(
            self.frame_cadastro, text="Ir para Login", width=200, command=self.mostrar_login)
        botao_login.pack(pady=(0, 10))

    # Botão para sair do sistema
        botao_sair = ctk.CTkButton(self.frame_cadastro, text="Sair do Sistema",
                                   width=200, fg_color="red", hover_color="#cc0000", command=self.sair_sitema)
        botao_sair.pack()

    def sair_sitema(self):
        """Função utilizada para fechar sistema """
        # Fechando dessa forma irá "destruir" a janela que foi definida no master
        self.master.destroy()  # Fecha a janela principal


class TelaSobreNos(ctk.CTkFrame):
    def __init__(self, master, voltar_inicial):
        super().__init__(master)
        self.frame_sobrenos = ctk.CTkFrame(self, fg_color="#ffffff")

        # Título principal
        titulo_sobrenos = ctk.CTkLabel(self.frame_sobrenos, text="💧 Projeto ECODROP", font=(
            "Arial", 22, "bold"), text_color="#1A73E8")
        titulo_sobrenos.pack(pady=(20, 10))

        descricao_projeto = ctk.CTkLabel(self.frame_sobrenos,
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
        
        try:
            imagem = Image.open("fotos/fotosobrenos.jpg")
            ctk_imagem = ctk.CTkImage(
                light_image=imagem, dark_image=imagem, size=(500, 300))
            label = ctk.CTkLabel(self.frame_sobrenos, image=ctk_imagem, text="")
            label.pack()
        except:
            placeholder = ctk.CTkLabel(self.frame_sobrenos, 
                                       text="📷 Imagem não encontrada",
                                       font=("Arial", 16))
            placeholder.pack(pady=30)
            
        botao_voltarinicial = ctk.CTkButton(
            self.frame_sobrenos, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
        botao_voltarinicial.pack(pady=30)

        self.frame_sobrenos.pack(fill="both", expand=True)


class TelaModoAdm(ctk.CTkFrame):
    def __init__(self, master, voltar_inicial):
        super().__init__(master)
        #define self.operaco como None para criar um objeto da classe
        # operações  apenas se o self.operacao não tiver sido criado ainda
        self.operacao=None
        self.tabela=None
        self.grafico_pizza=None
        self.grafico_consumopessoa=None
        self.grafico_consumoap=None
        self.media=None
        
        
        
        self.frame_adm = ctk.CTkFrame(self, fg_color="#ffffff")
        label_adm = ctk.CTkLabel(self.frame_adm, text="Insira o código de acesso \npara entrar no modo administrador:",
                                   fg_color="#ffffff", text_color="blue", font=("Arial", 20))
        label_adm.pack(pady=2)
        self.label_avisoadm = ctk.CTkLabel(self.frame_adm, text=" ", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
        self.label_avisoadm.pack(pady=2)

        # 1-entrada email
        #label_emailadm = ctk.CTkLabel(self.frame_adm, text="Digite seu email:", text_color="#000000", anchor="w", width=300)
        #label_emailadm.pack(pady=(2, 0))

        #self.entrada_emailadm = ctk.CTkEntry(self.frame_adm, width=300)
        #self.entrada_emailadm.pack(pady=2)

        # 2-entrada senha
        label_senhaadm= ctk.CTkLabel(self.frame_adm, text="Digite o código de acesso:", text_color="#000000", anchor="w", width=300)
        label_senhaadm.pack(pady=(2, 0))

        self.entrada_senhaadm = ctk.CTkEntry(self.frame_adm, width=300, show="*")
        self.entrada_senhaadm.pack(pady=2)

        # 3-entrada email cond

        # botão logar
        botao_entrar_adm = ctk.CTkButton(self.frame_adm, text="Entrar", fg_color="blue",
                                    text_color="#ffffff", width=300, command=self.conferir_adm)
        botao_entrar_adm.pack(pady=2)
        # botão voltar
        botao_voltarinicial = ctk.CTkButton(self.frame_adm, text="Voltar", fg_color="blue", text_color="#ffffff", width=300,
                                            command=voltar_inicial)
        botao_voltarinicial.pack()

        self.frame_adm.pack(fill="both", expand=True)

    def conferir_adm(self):
            entrada_senha=self.entrada_senhaadm.get().strip()
            if entrada_senha=="!GaMa#1903!":
                self.tela_inicial_adm()
            else:
                self.label_avisoadm.configure(text="Código inválido",text_color="Red")
            pass
    
    
    
    
    def tela_inicial_adm(self):
            for widget in self.frame_adm.winfo_children():
                widget.destroy()
            #A IDENTAÇÃO TEM QUE FICAR DESSA FORMA OU A CADA INTERAÇÃO,SERÁ CRIADO MAIS FRAMES DESSA TELA DE INÍCIO DO 
            #MODO ADM
            frame_topo = ctk.CTkFrame(self.frame_adm, fg_color="#1A73E8", height=80)
            frame_topo.pack(fill="x")

            titulo = ctk.CTkLabel(frame_topo, text="💧 MODO ADM",text_color="#f0f0f0", font=("Arial", 24, "bold"))
            titulo.pack(pady=10)

            frame_conteudo = ctk.CTkFrame(self.frame_adm, fg_color="#ffffff")

            botao_ver_dados = ctk.CTkButton(frame_conteudo, text="🔍Ver dados", fg_color="blue",
                                                text_color="#ffffff", width=300, command=self.tela_ver_dados)
            botao_ver_dados.pack(pady=10)

            botao_editar_dados = ctk.CTkButton(frame_conteudo, text="✏️Editar dados", fg_color="blue",
                                                text_color="#ffffff", width=300, command=self.tela_editar_dados)
            botao_editar_dados.pack(pady=10)

            botao_analise_dados = ctk.CTkButton(frame_conteudo, text="📊Analisar dados", fg_color="blue",
                                                text_color="#ffffff", width=300, command=self.tela_analise_dados)
            botao_analise_dados.pack(pady=10)

            imagem = Image.open("fotos/mascoteadm.png")
            ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(400, 400))

            label = ctk.CTkLabel(frame_conteudo, image=ctk_imagem, text="")
            label.pack(pady=30)

            frame_conteudo.pack(fill="both", expand=True)

            
            pass
    
    
    
    def tela_ver_dados(self):
            for widget in self.frame_adm.winfo_children():
                widget.destroy()
            
             
            if self.operacao is None:
                self.operacao=OperacoesAdm()
            if self.tabela is None:
                self.tabela=self.operacao.gerar_tabela()

            frame_topo = ctk.CTkFrame(self.frame_adm, fg_color="#1A73E8", height=80)
            frame_topo.pack(fill="x")

            titulo = ctk.CTkLabel(frame_topo, text="💧 MODO ADM",text_color="#ffffff", font=("Arial", 24, "bold"))
            titulo.pack(pady=20)

        

            #criação de um frame com scroll para que seja possível ver todos os dados
            frame_scroll = ctk.CTkScrollableFrame(self.frame_adm,fg_color="#ffffff")
            frame_scroll.pack(fill="both", expand=True, padx=10, pady=10)
            

            #perguntar o porque é melhor usar a fonte courier
            label_tabela = ctk.CTkLabel(frame_scroll, text=self.tabela, font=("Courier", 12), anchor="w", justify="left")
            label_tabela.pack(padx=10, pady=10)

            label_atencao=ctk.CTkLabel(frame_scroll, text="ATENÇÃO!!", font=("Arial", 20,"bold"), anchor="w", justify="left")
            label_atencao.pack(padx=10)

            label_mensagem_atencao=ctk.CTkLabel(frame_scroll, text="Dados com 'N/A' não possuem valores.", font=("Arial", 20,"bold"), anchor="w", justify="left")
            label_mensagem_atencao.pack(padx=10)

            botao_menuadm=ctk.CTkButton(frame_scroll,width=300,text="Voltar",fg_color="white",text_color="#1A73E8",command=self.tela_inicial_adm)
            botao_menuadm.pack(pady=30)
            

            #fazer botão de voltar para o menu
           
            pass
    
    
    
    def tela_editar_dados(self):
            for widget in self.frame_adm.winfo_children():
                widget.destroy()
            frame_topo = ctk.CTkFrame(self.frame_adm, fg_color="#1A73E8", height=80)
            frame_topo.pack(fill="x")

            titulo = ctk.CTkLabel(frame_topo, text="💧 MODO ADM",text_color="#f0f0f0", font=("Arial", 24, "bold"))
            titulo.pack(pady=20)

            self.frame_conteudo = ctk.CTkFrame(self.frame_adm, fg_color="#f0f0f0")
            self.frame_conteudo.pack(fill="both", expand=True)

            self.label_avisoedicao=ctk.CTkLabel(self.frame_conteudo,text="")
            self.label_avisoedicao.pack()

            # Nome
            label_nome = ctk.CTkLabel(self.frame_conteudo, text="Digite o email da conta que você deseja atualiza(Obrigatório):", 
                                      text_color="#000000", font=("Arial", 16, "bold"))
            label_nome.pack(pady=10)
            self.entrada_email=ctk.CTkEntry(self.frame_conteudo, width=300)
            self.entrada_email.pack(pady=10)

            # Família
            label_familia = ctk.CTkLabel(self.frame_conteudo, text="Digite o nome da família associada à conta(Obrigatório):", 
                                         text_color="#000000", font=("Arial", 16, "bold"))
            label_familia.pack(pady=10)
            self.entrada_familia = ctk.CTkEntry(self.frame_conteudo, width=300,
                                         validate="key",
                                         validatecommand=(self.register(self.validar_letras_espacos), "%P"))
            self.entrada_familia.pack(pady=1)

            # Quantidade de Membros
            label_qmembros = ctk.CTkLabel(self.frame_conteudo, text="Digite a quantidade de membros da família(Obrigatório):", 
                                         text_color="#000000", font=("Arial", 16, "bold"))
            label_qmembros.pack(pady=10)
            self.entrada_qmembros = ctk.CTkEntry(self.frame_conteudo, width=300,
                                             validate="key",
                                             validatecommand=(self.register(self.validar_numeros), "%P"))
            self.entrada_qmembros.pack(pady=1)

            # Apartamento
            label_apartamento = ctk.CTkLabel(self.frame_conteudo, text="Digite o número do apartamento:", 
                                             text_color="#000000", font=("Arial", 16, "bold"))
            label_apartamento.pack(pady=10)
            self.entrada_apartamento = ctk.CTkEntry(self.frame_conteudo, width=300,
                                             validate="key",
                                             validatecommand=(self.register(self.validar_numeros), "%P"))
            self.entrada_apartamento.pack(pady=1)

            # Consumo
            label_consumo = ctk.CTkLabel(self.frame_conteudo, text="Digite o consumo registrado (em m³):\n(Obrigatório)", 
                                         text_color="#000000", font=("Arial", 16, "bold"))
            label_consumo.pack(pady=10)
            self.entrada_consumo = ctk.CTkEntry(self.frame_conteudo, width=300,
                                             validate="key",
                                             validatecommand=(self.register(self.validar_numeros), "%P"))
            self.entrada_consumo.pack(pady=1)




            botao_atualizar_conta=ctk.CTkButton(self.frame_conteudo,text="Atualizar dados",text_color="#1A73E8",width=300,fg_color="#f0f0f0",
                                                command=self.conferir_entradas)
            botao_atualizar_conta.pack(pady=(10,5))

            botao_menuadm=ctk.CTkButton(self.frame_conteudo,width=300,text="Voltar",fg_color="#f0f0f0",text_color="#1A73E8",
                                        command=self.tela_inicial_adm)
            botao_menuadm.pack(pady=5)

            #Apartamento
            #Família
            #Pontos
            #Consumo
            #Membros

    @staticmethod  # Permite usar funções que não estão na classe diretamente,sem precisar passar self
    def validar_numeros(novo_texto):
        """Função utilizada para permitir digitar apenas números"""
        return novo_texto.isdigit() or novo_texto == ""

    @staticmethod  # Permite usar funções que não estão na classe diretamente,sem precisar passar self
    def validar_letras_espacos(novo_texto):
        """Função utilizada para deixar apenas digitar letras e espaços"""
        return all(c.isalpha() or c.isspace() for c in novo_texto) or novo_texto == ""
    
    def conferir_entradas(self):
        print(1)
        self.email=self.entrada_email.get().strip()
        self.apartamento=self.entrada_apartamento.get().strip()
        self.quantidade_pessoas=self.entrada_qmembros.get().strip()
        self.consumo=int(self.entrada_consumo.get().strip())
        self.nome_familia=self.entrada_familia.get().strip()

        entradas = [self.email, self.nome_familia,
                    self.quantidade_pessoas,self.consumo] 
    # Verificação: se algum campo de texto estiver vazio
        if any(campo == "" for campo in entradas):
            self.label_avisoedicao.configure(
                text="Preencha os campos obrigatórios.", text_color="red")
            return

        
        
        if self.apartamento!="":
            possiveis_andares=["10","20","30","40","50","60","70","80","90"]
            possiveis_apartamentos=["01","02","03","04","05"]
            #ESSES VERIFICADORES SERVIRÃO PARA DIZER SE O ANDAR E O APARTAMENTO É VÁLIDO OU NÃO
            numero_valido=False
            andar_valido = False
            apto_valido = False
        
            if len(self.apartamento)==4:
                numero_valido=True

            for andar in possiveis_andares:
                #SÓ VALIDARÁ SE APARTAMENTO INICIAR COM O INTERÁVEL DA LISTA ANDAR
                if self.apartamento.startswith(andar):
                    andar_valido = True
                    #BREAK IRÁ QUEBRAR O LOOP FOR,ACABANDO A INTERAÇÃO
                    break

            for apto in possiveis_apartamentos:
                #SÓ VALIDARÁ SE APARTAMENTO INICIAR COM O INTERÁVEL DA LISTA APARTAMENTO
                if self.apartamento.endswith(apto):
                    apto_valido = True
                    #BREAK IRÁ QUEBRAR O LOOP FOR,ACABANDO COM A INTERAÇÃO
                    break

            if not (andar_valido and apto_valido and numero_valido): #VERIFICA SE AMBOS SÃO VÁLIDOS(TRUE)
                print("Apartamento inváldio")
                self.label_avisoedicao.configure(text="Apartamento inválido", text_color="red")
                #return irá parar a função caso o aviso apareça
                return
        
            self.apartamento=int(self.apartamento)
        else:
            self.apartamento=dados_apartamento[self.email]
        
        self.verificar_email_edicao()

    
    
    
    def verificar_email_edicao(self):
        print(2)
        
        
        
        #Verificação se o email já tinha sido cadastrado anteriormente
        if self.email not in dados_conta:
            self.label_avisoedicao.configure(text="Email não cadastrado anteriormente.",text_color="Red")
            return
        self.salvar_edicao_dados()
        pass
    
    def salvar_edicao_dados(self):
        print(3)
        try:
            # Atualiza os dados que o admin pode alterar no
            dados_familia[self.email] = self.nome_familia
            dados_quantidade[self.email] =int(self.quantidade_pessoas)
            dados_apartamento[self.email] = self.apartamento
            dados_consumo[self.email]=self.consumo
            
            

            # Reescreve o banco de dados inteiro, incluindo os dados que não foram alterados
            with open("banco_dados.JSON", "w", encoding="utf-8") as arquivo:
                json.dump({"senha": dados_conta,"familia": dados_familia,"membros": dados_quantidade,"pontos": dados_pontos,
                           "apartamento": dados_apartamento,"verificador": dados_codigov}, arquivo, indent=4, ensure_ascii=False)
        
            self.mostrar_aviso_adm()
        except Exception as e:
            self.label_avisoedicao.configure(text=f"ERRO {e}.\nTente mais tarde!",text_color="red")
            print("Erro salvamento")

    def mostrar_aviso_adm(self):
        for widget in self.frame_adm.winfo_children():
                widget.destroy()

        frame_topo = ctk.CTkFrame(self.frame_adm, fg_color="#1A73E8", height=80)
        frame_topo.pack(fill="x")

        titulo = ctk.CTkLabel(frame_topo, text="💧 MODO ADM",text_color="#f0f0f0", font=("Arial", 24, "bold"))
        titulo.pack(pady=10)

        frame_conteudo = ctk.CTkFrame(self.frame_adm, fg_color="#ffffff")
        label_sucesso=ctk.CTkLabel(frame_conteudo,text="ATUALIZAÇÃO REALIZADA COM SUCESSO!!",text_color="#1A73E8",font=("arial",25))
        label_sucesso.pack()
        label_aviso_sucesso=ctk.CTkLabel(frame_conteudo,text="REINICIALIZAÇÃO NECESSÁRIA EM 7 SEGUNDOS.",text_color="#1A73E8",font=("arial",25))
        label_aviso_sucesso.pack(pady=10)
        
        imagem = Image.open("fotos/mascoteadm.png")
        ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(400, 400))

        label = ctk.CTkLabel(frame_conteudo, image=ctk_imagem, text="")
        label.pack(pady=30)


        frame_conteudo.pack(fill="both",expand=True)

        self.after(7000, self.sair_sistema)
    
        pass
    
    def sair_sistema(self):
        """Função utilizada para fechar sistema """
        # Fechando dessa forma irá "destruir" a janela que foi definida no master
        self.master.destroy()  # Fecha a janela principal
    # Ou qualquer outra lógica de saída que você preferir



    def tela_analise_dados(self):
            for widget in self.frame_adm.winfo_children():
                widget.destroy()
            
            frame_topo = ctk.CTkFrame(self.frame_adm, fg_color="#1A73E8", height=80)
            frame_topo.pack(fill="x")

            titulo = ctk.CTkLabel(frame_topo, text="💧 MODO ADM",text_color="#ffffff", font=("Arial", 24, "bold"))
            titulo.pack(pady=20)

            frame_conteudo = ctk.CTkFrame(self.frame_adm, fg_color="#ffffff")
            frame_conteudo.pack(fill="both", expand=True)

            frame_lado_esquerdo=ctk.CTkFrame(frame_conteudo,fg_color="#ffffff")
            frame_lado_esquerdo.pack(side="left",fill="both",expand=True)

            frame_lado_direito=ctk.CTkFrame(frame_conteudo,fg_color="#ffffff")
            frame_lado_direito.pack(side="right",fill="both",expand=True)
            
            #Gerando gráfico de pizza com a porcentagem de famílias que possuem certa quantidade de membros
            if self.operacao is None:
                self.operacao=OperacoesAdm()
            if self.grafico_pizza is None:
                self.grafico_pizza=self.operacao.gerar_grafico_pizza()
            if self.grafico_consumopessoa is None:
                self.grafico_consumopessoa=self.operacao.gerar_grafico2()
            if self.grafico_consumoap is None:
                self.grafico_consumoap=self.operacao.gerar_grafico3()
            if self.media is None:
                self.media=self.operacao.gerar_valor_media()
            

            img_pizza = CTkImage(dark_image=self.grafico_pizza, size=(400, 400))

            label_pizza = CTkLabel(frame_lado_esquerdo, image=img_pizza, text="")
            label_pizza.pack()

            label_dados=CTkLabel(frame_lado_esquerdo,text="Dados importantes:",font=("Arial",20,"bold"))
            label_dados.pack(pady=10)
            
            label_media_brasileira=CTkLabel(frame_lado_esquerdo,text="-Média brasileira de gasto de água por dia é de 154L por pessoa")
            label_media_brasileira.pack(pady=5)
            
            label_media_condominio=CTkLabel(frame_lado_esquerdo,text=f"-Total de água gasto pelo condomínio {self.media}")
            label_media_condominio.pack(pady=5)

            

            
            
            botao_voltar=ctk.CTkButton(frame_lado_esquerdo,text="Voltar",text_color="#ffffff",fg_color="#1A73E8",command=self.tela_inicial_adm)
            botao_voltar.pack(pady=10)
            

            img_grafico2=CTkImage(dark_image=self.grafico_consumopessoa,size=(300,300))
            label_grafico2=CTkLabel(frame_lado_direito,image=img_grafico2, text="")
            label_grafico2.pack()

            img_grafico3=CTkImage(dark_image=self.grafico_consumoap,size=(300,300))
            label_grafico3=CTkLabel(frame_lado_direito,image=img_grafico3, text="")
            label_grafico3.pack(pady=20)

            
            pass
    
    
    
class OperacoesAdm():
    def __init__(self):
        print("entrei operações adm")
        
        pass
    
    def gerar_tabela(self):
        
        dados_organizados = []
        
        for email in dados_conta:
            if (email in dados_familia and email in dados_quantidade and email in dados_pontos and 
                email in dados_apartamento and 
                email in dados_codigov):
                if email in dados_consumo:        
                    dados_organizados.append({
                        "Email": email,
                        "Família": dados_familia[email],
                        "Membros": dados_quantidade[email],
                        "Pontos": dados_pontos[email],
                        "Apartamento": dados_apartamento[email],
                        "Verificador": dados_codigov[email],
                        "Consumo":dados_consumo[email]

                    })
                else:
                    dados_organizados.append({
                        "Email": email,
                        "Família": dados_familia[email],
                        "Membros": dados_quantidade[email],
                        "Pontos": dados_pontos[email],
                        "Apartamento": dados_apartamento[email],
                        "Verificador": dados_codigov[email],
                        "Consumo":"N/A"

                    })

        df = pd.DataFrame(dados_organizados)
        tabela_formatada = df.to_string(index=False)
        
        return tabela_formatada

        
    
    def gerar_grafico_pizza(self):
        #Método responsável pela geração do gráfico de pizza que será feito em relação a quantidade de membros 

        #esse counter é uma classe nativa do python que contará a repetição de cada valor do dicionário dados_quantidade 
        #e armazenará em um dicionário por exemplo. {2:5,...}-->o número 2 se repete 5 vezes
        contagem = Counter(dados_quantidade.values())


        #Nesse loop for dentro da variável label,será criado mensagens do tipo "2 membros","3 membros" e armazerá em uma lista na variável.
        #O loop irá rolar e irá criar um label para cada tipo de quantidade "2","3" e etc
        labels = [f"{membros} membros" for membros in contagem.keys()]

        #essa variável sizes irá criar uma lista da quantidade de vezes que o valor aparece.Por exemplo,se o valor 3 aparece 5 vezes,ele terá o valor 5
        sizes = list(contagem.values())

        # Criar gráfico de pizza
        # Criar figura e eixo do gráfico

        #fig é a janela geral do gráfico e area_usada é a área específica onde o gráfico será desenhado
        fig, area_usada = plt.subplots(figsize=(8,8)) #fgsize define o tamanho do gráfico em polegadas
        
        #Desenha o gráfico pizza na área a area_usada
        area_usada.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        #size define o tamanho de cada fatia
        #labels+define o texto de cada fatia
        #autopct='%1.1f%%' mostra as porcentagens dentro da fatia
        #startangle=140: gira o gráfico para ficar mais esteticamente agradável.



        area_usada.set_title("Distribuição de famílias por número de membros", fontsize=20, pad=30)#define o título do gráfico e a fonte

        area_usada.axis('equal')#garante que o gráfico seja um círculo perfeito

        # Salvar o gráfico em memória como imagem PNG
        buffer = BytesIO()#cria um buffer de memória que simula um arquivo png,mas que ficará dentro da memória
        fig.savefig(buffer, format='png', bbox_inches='tight') #salva a figura dentro do buffer
        #bbox_inches='tight' remove os espaços em branco entre o gráfico
        plt.close(fig)  #Fecha o gráfico da memória do matplotlib para liberar RAM e evitar vazamentos.
        buffer.seek(0) #Move o cursor do buffer para o início do conteúdo.

        
        imagem = Image.open(buffer)

        print("gráfico pizza gerado")

        return imagem

    def gerar_grafico2(self):
        #Método responsável por gerar o gráfico de consumo por quantidade
        dicionario_grafico={}

        for email in dados_quantidade:
            if email in dados_consumo:
                qtd_membros = dados_quantidade[email]
                consumo = dados_consumo[email]
                valor_quantidade=str(qtd_membros)

                if valor_quantidade in dicionario_grafico:
                    dicionario_grafico[valor_quantidade] += consumo
                else:
                    dicionario_grafico[valor_quantidade] = consumo

                
        #Lista em ordem das chaves.Foi necessário passar temporariamente para inteiro para ser possível ordenar
        #quantidade=Eixo x
        quantidades = sorted(dicionario_grafico.keys(), key=int)
        
        #Aqui usará um loop for para as quantidades já ordenadas,para ser possível colocar o consumo na ordem correta em
        #relação a cada chave
        #Consumo=Eixo y
        consumos=[]    
        for qtd in quantidades:
            consumos.append(dicionario_grafico[qtd])

        

       # Criar figura e área onde o gráfico será desenhado
       #fig="janela" que será utilizada para armazenar a area_utilizada pela figura
        fig, area_utilizada = plt.subplots(figsize=(10, 6))

        # Criar gráfico de barras de consumo(eixoy) x quantidade(eixo x) com a cor skyblue
        area_utilizada.bar(quantidades, consumos, color="skyblue")

        #Título do gráfico
        area_utilizada.set_title("Consumo total por quantidade de moradores", fontsize=16, pad=20)
        #Título relação eixo x
        area_utilizada.set_xlabel("Quantidade de moradores", fontsize=12)
        #Título relação eixo y
        area_utilizada.set_ylabel("Consumo total (litros ou m³)", fontsize=12)
        #cria linhas no eixo y para ajudar a visualizar na análise de dados
        area_utilizada.grid(axis="y", linestyle="--", alpha=0.7)

        # Função enumerate retorna o índice do valor e o valor que está na lista
        for i, valor in enumerate(consumos):
            #+1 serve para posicionar o texto acima da barra.Valor é o valor no eixo y
            #passa o valor para string para ser possível colocar em texto
            #ha=centraliza o texto
            #
            area_utilizada.text(i, valor + 1, str(valor), ha=
                                "center", va="bottom", fontsize=10)

        #AJUSTA AUTOMATICAMENTE O CONTEÚDO DA FIGURA PARA QUE NENHUM TEXTO OU LABEL FIQUE CORTADO   
        plt.tight_layout()

        #aqui cria um buffer na memória(um arquivo temporário na memória)
        buffer = BytesIO()
        #salva a figura no buffer,como se fosse uma imagem sendo "salva em um frame"
        fig.savefig(buffer, format="png", bbox_inches="tight")
        #bbox_inches='tight' corta os espaços em branco 
        #fecha a imagem para liberar RAM e evitar vazamento de memória
        plt.close(fig)

        
        buffer.seek(0)

        #abre o buffer como imagem PIL
        imagem = Image.open(buffer)

        return imagem



    def gerar_grafico3(self):
        dicionario_grafico2={}
       
        dicionario_andares = {
            "10": 0,
                            "20": 0,
                            "30":0,
                            "40": 0,
                            "50": 0,
                            "60": 0,
                            "70":0,
                            "80": 0,
                            "90": 0}

        for email in dados_apartamento:
            if email in dados_consumo:
                apartamento=str(dados_apartamento[email])
                consumo=dados_consumo[email]
                dicionario_grafico2[apartamento]=consumo

        for apartamentos_validos in dicionario_grafico2:
            if apartamentos_validos.startswith("10"):
                dicionario_andares["10"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("20"):
                dicionario_andares["20"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("30"):
                dicionario_andares["30"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("40"):
                dicionario_andares["40"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("50"):
                dicionario_andares["50"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("60"):
                dicionario_andares["60"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("70"):
                dicionario_andares["70"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("80"):
                dicionario_andares["80"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("90"):
                dicionario_andares["90"] += dicionario_grafico2[apartamentos_validos]
        #Lista em ordem das chaves.Foi necessário passar temporariamente para inteiro para ser possível ordenar
        #quantidade=Eixo x
        
        #Lista os valores das chaves do dicionário
        andares=list(dicionario_andares.keys())

        #Lista os valores das chaves
        consumos=list(dicionario_andares.values())
        

       # Criar figura e área onde o gráfico será desenhado
       #fig="janela" que será utilizada para armazenar a area_utilizada pela figura
        fig, area_utilizada = plt.subplots(figsize=(10, 6))

        # Criar gráfico de barras de consumo(eixoy) x quantidade(eixo x) com a cor skyblue
        area_utilizada.bar(andares, consumos, color="skyblue")

        #Título do gráfico
        area_utilizada.set_title("Consumo total por andar", fontsize=16, pad=20)
        #Título relação eixo x
        area_utilizada.set_xlabel("Andar correspondente", fontsize=12)
        #Título relação eixo y
        area_utilizada.set_ylabel("Consumo total (litros ou m³)", fontsize=12)
        #cria linhas no eixo y para ajudar a visualizar na análise de dados
        area_utilizada.grid(axis="y", linestyle="--", alpha=0.7)

        # Função enumerate retorna o índice do valor e o valor que está na lista
        for i, valor in enumerate(consumos):
            #+1 serve para posicionar o texto acima da barra.Valor é o valor no eixo y
            #passa o valor para string para ser possível colocar em texto
            #ha=centraliza o texto
            #
            area_utilizada.text(i, valor + 1, str(valor), ha="center", va="bottom", fontsize=10)

        #AJUSTA AUTOMATICAMENTE O CONTEÚDO DA FIGURA PARA QUE NENHUM TEXTO OU LABEL FIQUE CORTADO   
        plt.tight_layout()

        #aqui cria um buffer na memória(um arquivo temporário na memória)
        buffer = BytesIO()
        #salva a figura no buffer,como se fosse uma imagem sendo "salva em um frame"
        fig.savefig(buffer, format="png", bbox_inches="tight")
        #bbox_inches='tight' corta os espaços em branco 
        #fecha a imagem para liberar RAM e evitar vazamento de memória
        plt.close(fig)

        
        buffer.seek(0)

        #abre o buffer como imagem PIL
        imagem = Image.open(buffer)

        return imagem

        
        

        
            

    def gerar_valor_media(self):
        
        consumo_listado=list(dados_consumo.values())
        media_consumo_condominio=sum(consumo_listado)
        

        return media_consumo_condominio
    pass



class UsuarioLogado(ctk.CTkFrame):
    def __init__(self, master, email, senha):
        super().__init__(master)
        self.email = email
        self.senha = senha
        
        # Inicializar as classes Game e GerenciarUsuario
        self.game = Game()
        self.gerenciar_usuario = GerenciarUsuario()
        
        self.criar_interface()

    def criar_interface(self):
        # Frame topo
        self.frame_topo = ctk.CTkFrame(self, fg_color="#1A73E8", height=80)
        self.frame_topo.pack(fill="x")
        
        titulo = ctk.CTkLabel(self.frame_topo, text="💧 ECODROP",
                              text_color="#f0f0f0", font=("Arial", 24, "bold"))
        titulo.pack(pady=20)

        # Frame principal que contém lateral e conteúdo
        self.frame_principal = ctk.CTkFrame(self, fg_color="#f0f0f0")
        self.frame_principal.pack(fill="both", expand=True)

        # Frame lateral menu
        self.framelateral_menu = ctk.CTkFrame(self.frame_principal, fg_color="#f0f0f0", width=250)
        self.framelateral_menu.pack(side="left", fill="y")
        self.framelateral_menu.pack_propagate(False)  # Mantém a largura fixa

        # Frame principal menu (área de conteúdo)
        self.frameprincipal_menu = ctk.CTkFrame(self.frame_principal, fg_color="#ffffff")
        self.frameprincipal_menu.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Criar o menu lateral organizado
        self.criar_menu_lateral()
        
        # Criar conteúdo inicial do frame principal
        self.criar_conteudo_inicial()

    def criar_menu_lateral(self):
        # Label "Interaja" em azul claro
        label_interaja = ctk.CTkLabel(self.framelateral_menu, text="Interaja", 
                                      text_color="#87CEEB", font=("Arial", 16, "bold"))
        label_interaja.pack(pady=(20, 10), padx=20)

        # Funcionalidades do grupo "Interaja"
        botao_ranking = ctk.CTkButton(self.framelateral_menu, text="🏆 Mostrar Ranking",
                                      fg_color="#f0f0f0", text_color="#1A73E8",
                                      font=("Arial", 12), anchor="w",
                                      command=self.mostrar_ranking)
        botao_ranking.pack(fill="x", pady=5, padx=20)

        botao_premio = ctk.CTkButton(self.framelateral_menu, text="🎁 Resgatar Prêmio",
                                     fg_color="#f0f0f0", text_color="#1A73E8",
                                     font=("Arial", 12), anchor="w",
                                     command=self.resgatar_premio)
        botao_premio.pack(fill="x", pady=5, padx=20)

        botao_pontuacao = ctk.CTkButton(self.framelateral_menu, text="🧮 Cálculo Pontuação",
                                        fg_color="#f0f0f0", text_color="#1A73E8",
                                        font=("Arial", 12), anchor="w",
                                        command=self.calculo_pontuacao)
        botao_pontuacao.pack(fill="x", pady=5, padx=20)

        botao_quiz = ctk.CTkButton(self.framelateral_menu, text="🧠 Quiz Semanal",
                                   fg_color="#f0f0f0", text_color="#1A73E8",
                                   font=("Arial", 12), anchor="w",
                                   command=self.quiz_semanal)
        botao_quiz.pack(fill="x", pady=5, padx=20)

        botao_educativa = ctk.CTkButton(self.framelateral_menu, text="📘 Área Educativa",
                                        fg_color="#f0f0f0", text_color="#1A73E8",
                                        font=("Arial", 12), anchor="w",
                                        command=self.area_educativa)
        botao_educativa.pack(fill="x", pady=5, padx=20)

        # Espaçamento entre os grupos
        ctk.CTkLabel(self.framelateral_menu, text="", height=20).pack()

        # Label "Gerenciar Usuário" em azul claro
        label_gerenciar = ctk.CTkLabel(self.framelateral_menu, text="Gerenciar Usuário", 
                                       text_color="#87CEEB", font=("Arial", 16, "bold"))
        label_gerenciar.pack(pady=(10, 10), padx=20)

        # Funcionalidades do grupo "Gerenciar Usuário"
        botao_mostrar_dados = ctk.CTkButton(self.framelateral_menu, text="📊 Mostrar Dados",
                                            fg_color="#f0f0f0", text_color="#1A73E8",
                                            font=("Arial", 12), anchor="w",
                                            command=self.mostrar_dados)
        botao_mostrar_dados.pack(fill="x", pady=5, padx=20)

        botao_atualizar = ctk.CTkButton(self.framelateral_menu, text="🔄 Atualizar Dados",
                                        fg_color="#f0f0f0", text_color="#1A73E8",
                                        font=("Arial", 12), anchor="w",
                                        command=self.atualizar_dados)
        botao_atualizar.pack(fill="x", pady=5, padx=20)

        botao_deletar = ctk.CTkButton(self.framelateral_menu, text="🗑️ Deletar Conta",
                                      fg_color="#f0f0f0", text_color="#1A73E8",
                                      font=("Arial", 12), anchor="w",
                                      command=self.deletar_conta)
        botao_deletar.pack(fill="x", pady=5, padx=20)

        botao_feedback = ctk.CTkButton(self.framelateral_menu, text="✍️ Feedback",
                                       fg_color="#f0f0f0", text_color="#1A73E8",
                                       font=("Arial", 12), anchor="w",
                                       command=self.feedback)
        botao_feedback.pack(fill="x", pady=5, padx=20)

    def criar_conteudo_inicial(self):
        # Conteúdo inicial do frame principal
        texto_bem_vindo = ctk.CTkLabel(self.frameprincipal_menu, 
                                       text=f"Bem-vindo ao EcoDrop, {self.email}!",
                                       text_color="#202124", font=("Arial", 22, "bold"))
        texto_bem_vindo.pack(pady=(50, 20))

        texto_instrucao = ctk.CTkLabel(self.frameprincipal_menu,
                                       text=random.choice(mensagens_agua),
                                       text_color="#5f6368", wraplength=500, justify="center",
                                       font=("Arial", 16))
        texto_instrucao.pack(pady=20)

        # Imagem do mascote (se existir)
        try:
            imagem = Image.open("fotos/mascoteprincipall.png")
            ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(300, 300))
            label_imagem = ctk.CTkLabel(self.frameprincipal_menu, image=ctk_imagem, text="")
            label_imagem.pack(pady=20)
        except:
            # Se a imagem não existir, mostra um placeholder
            placeholder = ctk.CTkLabel(self.frameprincipal_menu, 
                                       text="🌊 EcoDrop Mascote 🌊",
                                       font=("Arial", 48))
            placeholder.pack(pady=50)

    def limpar_frame_principal(self):
        """Limpa o conteúdo do frame principal"""
        for widget in self.frameprincipal_menu.winfo_children():
            widget.destroy()

    def reset_principal_menu_content(self):
        """Reseta o conteúdo do frame principal para o estado inicial"""
        self.limpar_frame_principal()
        self.criar_conteudo_inicial()

    # Métodos para as funcionalidades do grupo "Interaja"
    def mostrar_ranking(self):
        """🏆 Função: Ranking Mensal - Exibe uma lista com as famílias que mais economizaram água no mês, ordenada por pontos."""
        self.limpar_frame_principal()

        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="🏆 Ranking Mensal",
                                     font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        global dados_pontos, dados_familia

        # Carrega dados atualizados do JSON para garantir consistência
        try:
            with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
                arquivo_lido = json.load(arquivo)
                dados_pontos = arquivo_lido.get("pontos", {})
                dados_familia = arquivo_lido.get("familia", {})
        except Exception as e:
            ctk.CTkLabel(self.frameprincipal_menu, text=f"Erro ao carregar dados do ranking: {e}", text_color="red").pack()
            botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                         fg_color="gray", text_color="white", command=self.reset_principal_menu_content)
            botao_voltar.pack(pady=20)
            return

        # Cria uma lista de dicionários (nome_da_familia, pontos)
        ranking_data = []
        for user_email, pontos in dados_pontos.items():
            nome_familia = dados_familia.get(user_email, "N/A")
            ranking_data.append({"familia": nome_familia, "pontos": pontos})

        # Ordena a lista pelo número de pontos em ordem decrescente
        ranking_data.sort(key=lambda x: x["pontos"], reverse=True)

        if not ranking_data:
            ctk.CTkLabel(self.frameprincipal_menu, text="Nenhum dado de ranking disponível.",
                         font=("Arial", 14), text_color="#5f6368").pack(pady=10)
        else:
            # Cria um cabeçalho para a tabela do ranking
            header_frame = ctk.CTkFrame(self.frameprincipal_menu, fg_color="transparent")
            header_frame.pack(fill="x", padx=50, pady=(10, 5))
            ctk.CTkLabel(header_frame, text="Posição", font=("Arial", 12, "bold"), width=80).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Família", font=("Arial", 12, "bold"), width=200).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Pontos", font=("Arial", 12, "bold"), width=100).pack(side="left", padx=5)

            for i, item in enumerate(ranking_data):
                row_frame = ctk.CTkFrame(self.frameprincipal_menu, fg_color="#f9f9f9" if i % 2 == 0 else "#ffffff")
                row_frame.pack(fill="x", padx=50, pady=2)
                ctk.CTkLabel(row_frame, text=f"{i+1}º", width=80).pack(side="left", padx=5)
                ctk.CTkLabel(row_frame, text=item["familia"], width=200).pack(side="left", padx=5)
                ctk.CTkLabel(row_frame, text=item["pontos"], width=100).pack(side="left", padx=5)

        botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
        botao_voltar.pack(pady=20)

    def resgatar_premio(self):
        """🎁 Função: Resgatar Prêmios - Permite ao usuário resgatar recompensas usando seus pontos acumulados."""
        self.limpar_frame_principal()

        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="🎁 Resgatar Prêmios",
                                     font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        global dados_pontos

        pontos_atuais = dados_pontos.get(self.email, 0)
        label_pontos_saldo = ctk.CTkLabel(self.frameprincipal_menu, text=f"Seus pontos atuais: {pontos_atuais} 🌟",
                                           font=("Arial", 16, "bold"), text_color="#28a745")
        label_pontos_saldo.pack(pady=(0, 20))

        label_instrucao = ctk.CTkLabel(self.frameprincipal_menu, text="Escolha um prêmio para resgatar:",
                                        font=("Arial", 14), text_color="#333333")
        label_instrucao.pack(pady=(0, 10))

        # Frame para os prêmios com scroll
        scroll_frame = ctk.CTkScrollableFrame(self.frameprincipal_menu, width=500, height=300, fg_color="#f8f9fa")
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        for i, premio in enumerate(premios_disponiveis):
            premio_frame = ctk.CTkFrame(scroll_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#e0e0e0")
            premio_frame.pack(fill="x", pady=5, padx=10)

            label_premio_nome = ctk.CTkLabel(premio_frame, text=premio["nome"], font=("Arial", 14, "bold"), anchor="w", text_color="#1A73E8")
            label_premio_nome.pack(side="left", padx=10, pady=5)

            label_premio_custo = ctk.CTkLabel(premio_frame, text=f"Custo: {premio['custo']} pontos", font=("Arial", 12), text_color="#6c757d")
            label_premio_custo.pack(side="left", padx=10, pady=5)

            # Usamos uma função lambda com argumentos padrão para capturar o valor correto de 'premio'
            botao_resgatar = ctk.CTkButton(premio_frame, text="Resgatar", fg_color="#ffc107", text_color="black",
                                           command=lambda p=premio: self.realizar_resgate(p, label_pontos_saldo))
            botao_resgatar.pack(side="right", padx=10, pady=5)

        self.label_mensagem_resgate = ctk.CTkLabel(self.frameprincipal_menu, text="", text_color="red", font=("Arial", 12))
        self.label_mensagem_resgate.pack(pady=(10, 0))

        botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
        botao_voltar.pack(pady=20)

    def realizar_resgate(self, premio_selecionado, label_saldo):
        global dados_pontos

        pontos_disp = dados_pontos.get(self.email, 0)
        custo_premio = premio_selecionado["custo"]

        if pontos_disp >= custo_premio:
            dados_pontos[self.email] -= custo_premio
            # Atualiza o arquivo JSON
            try:
                with open(r"banco_dados.JSON", "r+", encoding="utf-8") as f:
                    data = json.load(f)
                    data["pontos"][self.email] = dados_pontos[self.email]
                    f.seek(0)
                    json.dump(data, f, indent=4, ensure_ascii=False)
                    f.truncate()
                self.label_mensagem_resgate.configure(text=f"Prêmio '{premio_selecionado['nome']}' resgatado com sucesso!", text_color="green")
                label_saldo.configure(text=f"Seus pontos atuais: {dados_pontos[self.email]} 🌟")
            except Exception as e:
                self.label_mensagem_resgate.configure(text=f"Erro ao salvar: {e}", text_color="red")
        else:
            self.label_mensagem_resgate.configure(text="Pontos insuficientes para resgatar este prêmio.", text_color="red")

    def calculo_pontuacao(self):
        """🧮 Função: Cálculo de Pontos - Calcula pontos com base nos litros economizados, número de moradores e consumo médio."""
        self.limpar_frame_principal()

        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="🧮 Cálculo de Pontos",
                                     font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        ctk.CTkLabel(self.frameprincipal_menu, text="Informe seu consumo diário (em litros) para calcular pontos:",
                     font=("Arial", 14), text_color="#333333").pack(pady=(0, 10))

        label_consumo = ctk.CTkLabel(self.frameprincipal_menu, text="Consumo Diário (Litros):",
                                      font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
        label_consumo.pack(fill="x", padx=50, pady=(10, 0))

        self.entrada_consumo = ctk.CTkEntry(self.frameprincipal_menu, width=200, validate="key",
                                       validatecommand=(self.register(validar_numeros), "%P"))
        self.entrada_consumo.pack(padx=50, pady=(0, 10), anchor="w")

        self.label_resultado_pontos = ctk.CTkLabel(self.frameprincipal_menu, text="", font=("Arial", 14, "bold"), text_color="green")
        self.label_resultado_pontos.pack(pady=(10, 0))

        self.label_mensagem_calculo = ctk.CTkLabel(self.frameprincipal_menu, text="", text_color="red", font=("Arial", 12))
        self.label_mensagem_calculo.pack(pady=(0, 10))

        botao_calcular = ctk.CTkButton(self.frameprincipal_menu, text="Calcular Pontos",
                                       fg_color="#1A73E8", text_color="white",
                                       command=self.calcular_pontos_acao)
        botao_calcular.pack(pady=10)

        botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
        botao_voltar.pack(pady=20)

    def calcular_pontos_acao(self):
        consumo_str = self.entrada_consumo.get().strip()
        if not consumo_str:
            self.label_mensagem_calculo.configure(text="Por favor, insira o consumo diário.", text_color="red")
            return

        try:
            consumo_diario = int(consumo_str)
            if consumo_diario < 0:
                self.label_mensagem_calculo.configure(text="O consumo não pode ser negativo.", text_color="red")
                return

            global dados_pontos, dados_quantidade
            membros = dados_quantidade.get(self.email, 1)

            # Lógica de cálculo de pontos simplificada:
            # Consumo ideal per capita (ex: 100 litros/dia)
            consumo_ideal_total = 100 * membros
            pontos_ganhos = 0

            if consumo_diario < consumo_ideal_total:
                litros_economizados = consumo_ideal_total - consumo_diario
                pontos_ganhos = int(litros_economizados / 10)  # 1 ponto a cada 10 litros economizados

            if pontos_ganhos > 0:
                dados_pontos[self.email] = dados_pontos.get(self.email, 0) + pontos_ganhos
                # Atualiza o JSON com os novos pontos
                try:
                    with open(r"banco_dados.JSON", "r+", encoding="utf-8") as f:
                        data = json.load(f)
                        data["pontos"][self.email] = dados_pontos[self.email]
                        f.seek(0)
                        json.dump(data, f, indent=4, ensure_ascii=False)
                        f.truncate()
                    self.label_resultado_pontos.configure(text=f"Parabéns! Você ganhou {pontos_ganhos} pontos. Total: {dados_pontos[self.email]}", text_color="green")
                    self.label_mensagem_calculo.configure(text="")
                except Exception as e:
                    self.label_mensagem_calculo.configure(text=f"Erro ao salvar pontos: {e}", text_color="red")
            else:
                self.label_resultado_pontos.configure(text="Nenhum ponto ganho desta vez. Continue economizando!", text_color="#5f6368")
                self.label_mensagem_calculo.configure(text="Seu consumo foi maior ou igual ao ideal. Tente reduzir mais!", text_color="orange")

        except ValueError:
            self.label_mensagem_calculo.configure(text="Consumo diário deve ser um número válido.", text_color="red")

    def quiz_semanal(self):
        """🧠 Função: Quiz Semanal - Disponibiliza 5 questões toda segunda-feira. Dependendo do desempenho, o usuário recebe pontos."""
        self.limpar_frame_principal()

        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="🧠 Quiz Semanal",
                                     font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        # Implementação simplificada do quiz
        ctk.CTkLabel(self.frameprincipal_menu, text="Quiz semanal não disponível no momento.",
                     font=("Arial", 14), text_color="#5f6368").pack(pady=50)

        ctk.CTkLabel(self.frameprincipal_menu, text="Volte na próxima segunda-feira para participar!",
                     font=("Arial", 12), text_color="orange").pack(pady=10)

        botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
        botao_voltar.pack(pady=20)

    def area_educativa(self):
        """📘 Função: Área Educativa - Exibe conteúdo educativo sobre sustentabilidade e conservação da água."""
        self.limpar_frame_principal()

        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="📘 Área Educativa",
                                     font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        # Scroll frame para o conteúdo educativo
        scroll_frame = ctk.CTkScrollableFrame(self.frameprincipal_menu, width=600, height=400)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Artigos educativos
        artigos = [
            "Europa investe €15 bilhões em preservação de recursos hídricos até 2027",
            "Cientistas desenvolvem tecnologia para extrair água potável do ar usando resíduos alimentares",
            "Universidade do Texas inicia construção do maior centro universitário de reúso de água dos EUA",
            "Alunos serão instruídos sobre conservação da água e limpeza do rio Ganges na Índia",
            "Impacto dos datacenters em áreas com escassez hídrica na América Latina",
            "8 filmes educativos para crianças sobre sustentabilidade"
        ]

        for artigo in artigos:
            btn_artigo = ctk.CTkButton(scroll_frame, text=artigo,
                                       fg_color="white", text_color="#1A73E8",
                                       font=("Arial", 12), anchor="w",
                                       command=lambda a=artigo: self.mostrar_artigo(a))
            btn_artigo.pack(fill="x", pady=5, padx=10)

        botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
        botao_voltar.pack(pady=20)

    def mostrar_artigo(self, titulo_artigo):
        """Exibe o conteúdo de um artigo específico"""
        self.limpar_frame_principal()
        
        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text=titulo_artigo,
                                     font=("Arial", 16, "bold"), text_color="#1A73E8",
                                     wraplength=600)
        label_titulo.pack(pady=(20, 10))

        conteudo = ctk.CTkLabel(self.frameprincipal_menu, 
                                text="Conteúdo do artigo seria exibido aqui com informações detalhadas sobre sustentabilidade e conservação da água.",
                                font=("Arial", 14), wraplength=600, justify="left")
        conteudo.pack(pady=20, padx=20)

        botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar à Área Educativa",
                                     fg_color="gray", text_color="white",
                                     command=self.area_educativa)
        botao_voltar.pack(pady=20)

    # Métodos para as funcionalidades do grupo "Gerenciar Usuário"
    def mostrar_dados(self):
        """📊 Função: Mostrar Dados - Exibe os principais dados da conta do usuário (exceto senha e código verificador por segurança)."""
        self.limpar_frame_principal()

        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="📊 Seus Dados",
                                     font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        global dados_familia, dados_quantidade, dados_pontos, dados_apartamento

        user_family = dados_familia.get(self.email, "N/A")
        user_members = dados_quantidade.get(self.email, "N/A")
        user_points = dados_pontos.get(self.email, "N/A")
        user_apartment = dados_apartamento.get(self.email, "N/A")

        data_text = f"""Email: {self.email}
Nome da Família: {user_family}
Membros da Família: {user_members}
Pontos Acumulados: {user_points}
Número do Apartamento: {user_apartment}"""

        ctk.CTkLabel(self.frameprincipal_menu, text=data_text,
                     font=("Arial", 14), text_color="#333333", justify="left").pack(pady=10)

        botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
        botao_voltar.pack(pady=20)

    def atualizar_dados(self):
        """🔄 Função: Atualizar Dados - Permite ao usuário atualizar o nome da família, quantidade de membros e senha."""
        self.limpar_frame_principal()

        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="🔄 Atualizar Dados",
                                     font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        # Carrega dados atuais
        global dados_familia, dados_quantidade, dados_conta
        nome_atual = dados_familia.get(self.email, "")
        membros_atuais = dados_quantidade.get(self.email, "")

        ctk.CTkLabel(self.frameprincipal_menu, text="Preencha os campos que deseja atualizar:",
                     font=("Arial", 14), text_color="#333333").pack(pady=(0, 10))

        # Campo Nome da Família
        label_nome_familia = ctk.CTkLabel(self.frameprincipal_menu, text="Nome da Família:",
                                           font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
        label_nome_familia.pack(fill="x", padx=50, pady=(10, 0))
        self.entrada_nome_familia = ctk.CTkEntry(self.frameprincipal_menu, width=300)
        self.entrada_nome_familia.insert(0, nome_atual)
        self.entrada_nome_familia.pack(padx=50, pady=(0, 10))

        # Campo Quantidade de Membros
        label_membros = ctk.CTkLabel(self.frameprincipal_menu, text="Quantidade de Membros:",
                                      font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
        label_membros.pack(fill="x", padx=50, pady=(10, 0))
        self.entrada_membros = ctk.CTkEntry(self.frameprincipal_menu, width=300, validate="key",
                                       validatecommand=(self.register(validar_numeros), "%P"))
        self.entrada_membros.insert(0, str(membros_atuais))
        self.entrada_membros.pack(padx=50, pady=(0, 10))

        # Campo Nova Senha (opcional)
        label_nova_senha = ctk.CTkLabel(self.frameprincipal_menu, text="Nova Senha (deixe em branco para não alterar):",
                                         font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
        label_nova_senha.pack(fill="x", padx=50, pady=(10, 0))
        self.entrada_nova_senha = ctk.CTkEntry(self.frameprincipal_menu, width=300, show="*")
        self.entrada_nova_senha.pack(padx=50, pady=(0, 10))

        self.label_mensagem_atualizar = ctk.CTkLabel(self.frameprincipal_menu, text="", text_color="red", font=("Arial", 12))
        self.label_mensagem_atualizar.pack(pady=(0, 10))

        botao_salvar = ctk.CTkButton(self.frameprincipal_menu, text="Salvar Atualizações",
                                     fg_color="#1A73E8", text_color="white",
                                     command=self.salvar_atualizacao_acao)
        botao_salvar.pack(pady=10)

        botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
        botao_voltar.pack(pady=20)

    def salvar_atualizacao_acao(self):
        novo_nome = self.entrada_nome_familia.get().strip()
        nova_qtde_membros_str = self.entrada_membros.get().strip()
        nova_senha = self.entrada_nova_senha.get().strip()

        if not novo_nome or not nova_qtde_membros_str:
            self.label_mensagem_atualizar.configure(text="Nome da família e quantidade de membros são obrigatórios.", text_color="red")
            return

        try:
            nova_qtde_membros = int(nova_qtde_membros_str)
            if nova_qtde_membros <= 0:
                self.label_mensagem_atualizar.configure(text="Quantidade de membros deve ser maior que zero.", text_color="red")
                return
        except ValueError:
            self.label_mensagem_atualizar.configure(text="Quantidade de membros deve ser um número válido.", text_color="red")
            return

        if nova_senha and not (4 <= len(nova_senha) <= 20):
            self.label_mensagem_atualizar.configure(text="A nova senha deve ter entre 4 e 20 caracteres.", text_color="red")
            return

        try:
            with open(r"banco_dados.JSON", "r+", encoding="utf-8") as f:
                data = json.load(f)

                data["familia"][self.email] = novo_nome
                data["membros"][self.email] = nova_qtde_membros
                if nova_senha:
                    data["senha"][self.email] = nova_senha

                # Atualiza as variáveis globais
                dados_familia[self.email] = novo_nome
                dados_quantidade[self.email] = nova_qtde_membros
                if nova_senha:
                    dados_conta[self.email] = nova_senha

                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()
            self.label_mensagem_atualizar.configure(text="Dados atualizados com sucesso!", text_color="green")
            self.entrada_nova_senha.delete(0, ctk.END)
        except Exception as e:
            self.label_mensagem_atualizar.configure(text=f"Erro ao atualizar dados: {e}", text_color="red")

    def deletar_conta(self):
        """🗑️ Função: Deletar Conta - Permite ao usuário excluir sua conta permanentemente do sistema."""
        self.limpar_frame_principal()

        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="🗑️ Deletar Conta",
                                     font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        self.label_confirmacao = ctk.CTkLabel(self.frameprincipal_menu, text="ATENÇÃO: Esta ação é irreversível!\nDeseja realmente deletar sua conta?",
                                          font=("Arial", 14, "bold"), text_color="red")
        self.label_confirmacao.pack(pady=20)

        botao_confirmar_delecao = ctk.CTkButton(self.frameprincipal_menu, text="Confirmar Deleção",
                                               fg_color="red", hover_color="#cc0000",
                                               command=self.confirmar_delecao_action)
        botao_confirmar_delecao.pack(pady=10)

        botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
        botao_voltar.pack(pady=20)

    def confirmar_delecao_action(self):
        global dados_conta, dados_familia, dados_quantidade, dados_pontos, dados_apartamento, dados_codigov, dados_ultimo_quiz
        try:
            with open(r"banco_dados.JSON", "r+", encoding="utf-8") as arquivo:
                data = json.load(arquivo)
                if self.email in data["senha"]:
                    del data["senha"][self.email]
                    del data["familia"][self.email]
                    del data["membros"][self.email]
                    del data["pontos"][self.email]
                    del data["apartamento"][self.email]
                    del data["verificador"][self.email]
                    if self.email in data.get("ultimo_quiz", {}):
                        del data["ultimo_quiz"][self.email]

                    # Atualiza os dicionários globais
                    dados_conta = data.get("senha", {})
                    dados_familia = data.get("familia", {})
                    dados_quantidade = data.get("membros", {})
                    dados_pontos = data.get("pontos", {})
                    dados_apartamento = data.get("apartamento", {})
                    dados_codigov = data.get("verificador", {})
                    dados_ultimo_quiz = data.get("ultimo_quiz", {})

                    arquivo.seek(0)
                    json.dump(data, arquivo, indent=4, ensure_ascii=False)
                    arquivo.truncate()

                    self.label_confirmacao.configure(text="Sua conta foi deletada com sucesso.", text_color="green")
                    # Após a exclusão, volta para a tela inicial
                    self.after(2000, lambda: self.master.criar_tela_inicial())
                else:
                    self.label_confirmacao.configure(text="Erro: Conta não encontrada.", text_color="red")
        except Exception as e:
            self.label_confirmacao.configure(text=f"Erro ao deletar conta: {e}", text_color="red")

    def feedback(self):
        """✍️ Função: Feedback - Permite ao usuário enviar uma opinião com até 140 caracteres e uma nota de 0 a 10."""
        self.limpar_frame_principal()

        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="✍️ Enviar Feedback",
                                     font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        label_instrucao = ctk.CTkLabel(self.frameprincipal_menu, text="Por favor, deixe sua opinião sobre o sistema EcoDrop:",
                                        font=("Arial", 14), text_color="#333333")
        label_instrucao.pack(pady=(0, 10))

        # Campo de Entrada de Texto do Feedback
        label_feedback_texto = ctk.CTkLabel(self.frameprincipal_menu, text="Seu Feedback (até 140 caracteres):",
                                             font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
        label_feedback_texto.pack(fill="x", padx=50, pady=(10, 0))
        self.entrada_feedback = ctk.CTkEntry(self.frameprincipal_menu, width=400, height=80)
        self.entrada_feedback.pack(padx=50, pady=(0, 10))

        # Escala de Avaliação
        label_nota = ctk.CTkLabel(self.frameprincipal_menu, text="Sua nota para o sistema (0 a 10):",
                                  font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
        label_nota.pack(fill="x", padx=50, pady=(10, 0))
        self.entrada_nota = ctk.CTkEntry(self.frameprincipal_menu, width=100, validate="key",
                                    validatecommand=(self.register(lambda text: text.isdigit() and (len(text) <= 2 and (int(text) >= 0 and int(text) <= 10) if text.strip() else True) or text == ""), "%P"))
        self.entrada_nota.pack(padx=50, pady=(0, 20), anchor="w")

        # Label para mensagens de validação
        self.label_mensagem_feedback = ctk.CTkLabel(self.frameprincipal_menu, text="", text_color="red", font=("Arial", 12))
        self.label_mensagem_feedback.pack(pady=(0, 10))

        botao_enviar = ctk.CTkButton(self.frameprincipal_menu, text="Enviar Feedback",
                                     fg_color="#1A73E8", text_color="white",
                                     command=self.enviar_feedback_acao)
        botao_enviar.pack(pady=10)

        botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
        botao_voltar.pack(pady=20)

    def enviar_feedback_acao(self):
        feedback_text = self.entrada_feedback.get().strip()
        nota_text = self.entrada_nota.get().strip()

        if not feedback_text or not nota_text:
            self.label_mensagem_feedback.configure(text="Por favor, preencha todos os campos.", text_color="red")
            return

        try:
            nota = int(nota_text)
            if not (0 <= nota <= 10):
                self.label_mensagem_feedback.configure(text="A nota deve ser entre 0 e 10.", text_color="red")
                return
        except ValueError:
            self.label_mensagem_feedback.configure(text="A nota deve ser um número inteiro.", text_color="red")
            return

        if len(feedback_text) > 140:
            self.label_mensagem_feedback.configure(text="O feedback não pode exceder 140 caracteres.", text_color="red")
            return

        try:
            with open("feedback.csv", "a+", newline="", encoding="utf-8") as f:
                f.seek(0)
                is_empty = f.read() == ''
                if is_empty:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(["Email", "Feedback", "Nota", "Data/Hora"])
                csv_writer = csv.writer(f)
                csv_writer.writerow([self.email, feedback_text, nota, time.strftime("%Y-%m-%d %H:%M:%S")])
            self.label_mensagem_feedback.configure(text="Feedback enviado com sucesso! Agradecemos sua colaboração.", text_color="green")
            self.entrada_feedback.delete(0, ctk.END)
            self.entrada_nota.delete(0, ctk.END)
        except Exception as e:
            self.label_mensagem_feedback.configure(text=f"Erro ao salvar feedback: {e}", text_color="red")


class Game:
    """Classe responsável pelas funcionalidades de gamificação"""
    def __init__(self):
        pass
    
    def mostrar_ranking(self):
        # Implementar lógica do ranking
        pass
    
    def resgatar_premio(self):
        # Implementar lógica de resgate de prêmios
        pass
    
    def calculo_pontuacao(self):
        # Implementar lógica de cálculo de pontuação
        pass
    
    def quiz_semanal(self):
        # Implementar lógica do quiz semanal
        pass
    
    def area_educativa(self):
        # Implementar lógica da área educativa
        pass


class GerenciarUsuario:
    """Classe responsável pelo gerenciamento de dados do usuário"""
    def __init__(self):
        pass
    
    def mostrar_dados(self):
        # Implementar lógica para mostrar dados do usuário
        pass
    
    def atualizar_dados(self):
        # Implementar lógica para atualizar dados do usuário
        pass
    
    def deletar_conta(self):
        # Implementar lógica para deletar conta
        pass
    
    def feedback(self):
        # Implementar lógica para enviar feedback
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()




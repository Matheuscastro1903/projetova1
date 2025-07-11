import customtkinter as ctk
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


with open(r"dados_usuarios.json", "r", encoding="utf-8") as arquivo:
    dados_lidos=json.load(arquivo)
    dados_consumo=dados_lidos["consumo"]

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
        self.esquercer_frames()
        if self.tela_inicial is None:
            self.tela_inicial = TelaInicial(self, mostrar_login=self.criar_tela_login, mostrar_cadastro=self.criar_tela_cadastro,
                                            modo_adm=self.criar_tela_modoadm, sobre_nos=self.criar_tela_sobrenos)
            self.telas.append(self.tela_inicial)
        self.tela_inicial.pack(fill="both", expand=True)

    def criar_tela_login(self):
        self.esquercer_frames()
        if self.tela_login is None:
            self.tela_login = TelaLogin(
                self, voltar_inicial=self.criar_tela_inicial, 
                mostrar_menu=self.criar_tela_menu)
            self.telas.append(self.tela_login)

        self.tela_login.pack(fill="both", expand=True)

    def criar_tela_cadastro(self):
        self.esquercer_frames()
        if self.tela_cadastro is None:
            self.tela_cadastro = TelaCadastro(
                self, 
                voltar_inicial=self.criar_tela_inicial, 
                mostrar_login=self.criar_tela_login)
            self.telas.append(self.tela_cadastro)
        self.tela_cadastro.pack(fill="both", expand=True)

    def criar_tela_modoadm(self):
        self.esquercer_frames()

        if self.tela_modoadm is None:
            self.tela_modoadm = TelaModoAdm(self, voltar_inicial=self.criar_tela_inicial)
            
            self.telas.append(self.tela_modoadm)
            
        self.tela_modoadm.pack(fill="both", expand=True)

    def criar_tela_sobrenos(self):

        self.esquercer_frames()
        if self.tela_sobrenos is None:
            self.tela_sobrenos = TelaSobreNos(
                self, voltar_inicial=self.criar_tela_inicial)
            self.telas.append(self.tela_sobrenos)

        self.tela_sobrenos.pack(fill="both", expand=True)

    def criar_tela_menu(self):
        
        self.esquecer_frames()

        self.tela_menu = Menu(self, email_logado = email_logado, voltar_incial=self.criar_tela_inicial)
        self.telas.append(self.tela_menu)
        self.tela_menu.pack(fill='both', expand=True)



    def criar_tela_educativa(self):
        pass

    def esquercer_frames(self):
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

        imagem = Image.open("fotos/mascoteprincipall.png")
        ctk_imagem = ctk.CTkImage(
            light_image=imagem, dark_image=imagem, size=(400, 400))

        label = ctk.CTkLabel(self.frame_principal, image=ctk_imagem, text="")
        label.pack()

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

        # 3-entrada email cond

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

                    self.mostrar_menu(self.email)
                    return
                else:
                    self.label_avisologin.configure(
                        text="EMAIL OU SENHA INCORRETO.\nContate o suporte para recuperar usa senha", text_color="red")
                    return

            else:
                self.label_avisologin.configure(
                    text="EMAIL NÃO CADASTRADO.\nVá para tela de cadastro")
                return

    def mostrar_menu(self):
        print("Entrei menu")
        pass


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
                                         validatecommand=(self.register(self.validar_letras_espacos), "%P"))
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
                                             validatecommand=(self.register(self.validar_numeros), "%P"))
        self.entrada_qmembros.pack(pady=1)

        # 5 - Número do apartamento
        label_numeroap = ctk.CTkLabel(self.frame_cadastro, text="Digite o número do seu apartamento",
                                      text_color="#000000", anchor="w", width=300)
        label_numeroap.pack(pady=(1, 0))

        self.entrada_numeroap = ctk.CTkEntry(self.frame_cadastro, width=300,
                                             validate="key",
                                             validatecommand=(self.register(self.validar_numeros), "%P"))
        self.entrada_numeroap.pack(pady=1)

        # 6 - Código verificador
        label_verificador = ctk.CTkLabel(self.frame_cadastro, text="Digite seu código verificador\n(MÍNIMO 4 CARACTERES E APENAS NÚMEROS):",
                                         text_color="#000000", anchor="w", width=300)
        label_verificador.pack(pady=(1, 0))

        self.entrada_verificador = ctk.CTkEntry(self.frame_cadastro, width=300,
                                                validate="key", show="*",
                                                validatecommand=(self.register(self.validar_numeros), "%P"))
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

    @staticmethod  # Permite usar funções que não estão na classe diretamente,sem precisar passar self
    def validar_numeros(novo_texto):
        """Função utilizada para permitir digitar apenas números"""
        return novo_texto.isdigit() or novo_texto == ""

    @staticmethod  # Permite usar funções que não estão na classe diretamente,sem precisar passar self
    def validar_letras_espacos(novo_texto):
        """Função utilizada para deixar apenas digitar letras e espaços"""
        return all(c.isalpha() or c.isspace() for c in novo_texto) or novo_texto == ""

    def conferir_cadastrar(self):
        email = self.entrada_email.get().strip()
        nome_familia = self.entrada_nome.get().strip()
        senha = self.entrada_senha.get().strip()
        quantidade_pessoas = self.entrada_qmembros.get().strip()
        apartamento = self.entrada_numeroap.get().strip()
        verificador = self.entrada_verificador.get().strip()

        entradas = [email, nome_familia, senha,
                    quantidade_pessoas, apartamento]
        possiveis_andares=["10","20","30","40","50","60","70","80","90"]
        possiveis_apartamentos=["01","02","03","04","05"]
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
        andar_valido = False
        apto_valido = False

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

        if not (andar_valido and apto_valido): #VERIFICA SE AMBOS SÃO VÁLIDOS(TRUE)
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
    # Ou qualquer outra lógica de saída que você preferir



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
        imagem = Image.open("fotos/fotosobrenos.jpg")
        ctk_imagem = ctk.CTkImage(
            light_image=imagem, dark_image=imagem, size=(500, 300))

        label = ctk.CTkLabel(self.frame_sobrenos, image=ctk_imagem, text="")
        label.pack()
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

            frame_conteudo = ctk.CTkFrame(self.frame_adm, fg_color="#f0f0f0")
            frame_conteudo.pack(fill="both", expand=True)

            self.label_avisoadm=ctk.CTkLabel(frame_conteudo,text="")

            label_atualizar_email=ctk.CTkLabel(frame_conteudo,text="Digite o email da conta que você deseja atualizar",text_color="#1A73E8",font=("Arial", 16, "bold"))
            label_atualizar_email.pack(pady=10)
            entrada_atualizar_email=ctk.CTkEntry(frame_conteudo,width=300)
            entrada_atualizar_email.pack(pady=10)

            botao_atualizar_conta=ctk.CTkButton(frame_conteudo,text="Atualizar dados",text_color="#1A73E8",width=300,command=self.verificar_email_editacao)
            botao_atualizar_conta.pack(pady=20)

            botao_menuadm=ctk.CTkButton(frame_conteudo,width=300,text="Voltar",fg_color="white",text_color="#1A73E8",command=self.tela_inicial_adm)
            botao_menuadm.pack(pady=20)
    
    
    def verificar_email_editacao(self):
        pass

    
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
            label_media_brasileira=CTkLabel(frame_lado_esquerdo,text=f"-Média de gasto do condomínio é {self.media}")
            label_media_brasileira.pack(pady=5)

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
                dados_organizados.append({
                    "Email": email,
                    "Família": dados_familia[email],
                    "Membros": dados_quantidade[email],
                    "Pontos": dados_pontos[email],
                    "Apartamento": dados_apartamento[email],
                    "Verificador": dados_codigov[email]
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
        quantidade_consumo_registrado=len(consumo_listado)
        media_consumo_condominio=sum(consumo_listado)/quantidade_consumo_registrado
        

        return media_consumo_condominio
    pass


app=App()
app.mainloop()

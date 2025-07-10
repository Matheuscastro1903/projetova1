import customtkinter as ctk
import customtkinter as ctk
from PIL import Image
import json
import csv
import time
import re
import random
import pandas as pd
from datetime import datetime, timedelta



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
        self.tela_usuario_logado = None
        
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
                mostrar_usuario_logado=self.criar_tela_usuario_logado)
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

    def criar_tela_usuario_logado(self, email_logado):
        
        self.esquecer_frames()

        self.tela_usuario_logado = UsuarioLogado(self, email_logado = email_logado)
        if self.tela_usuario_logado not in self.telas:
            self.telas.append(self.tela_usuario_logado)
        self.tela_usuario_logado.pack(fill='both', expand=True)


    def criar_tela_educativa(self):
        pass

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
    def __init__(self, master, voltar_inicial, mostrar_usuario_logado):
        super().__init__(master)
        self.voltar_inicial = voltar_inicial
        self.mostrar_usuario_logado= mostrar_usuario_logado
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

                    self.mostrar_usuario_logado(self.email)
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

        quantidade_pessoas = int(quantidade_pessoas)
        verificador = int(verificador)

        # NECESSÁRIO FAZER DESSA FORMA PARA EVITAR MÚLTIPLAS CHAMADAS DA FUNÇÃO GET,QUE PEGA VALORES DAS ENTRADAS
        self.email = email
        self.senha = senha
        self.nome_familia = nome_familia
        self.quantidade = quantidade_pessoas
        self.pontos = 0
        self.apartamento = apartamento
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
        label_senhaadm= ctk.CTkLabel(self.frame_adm, text="Digite código de acesso:", text_color="#000000", anchor="w", width=300)
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
            if entrada_senha=="!GaMa@1903#*!":
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
            titulo.pack(pady=20)

            frame_conteudo = ctk.CTkFrame(self.frame_adm, fg_color="#f0f0f0")

            botao_ver_dados = ctk.CTkButton(frame_conteudo, text="Ver dados", fg_color="blue",
                                                text_color="#ffffff", width=300, command=self.tela_ver_dados)
            botao_ver_dados.pack(pady=10)

            botao_editar_dados = ctk.CTkButton(frame_conteudo, text="Editar dados", fg_color="blue",
                                                text_color="#ffffff", width=300, command=self.tela_editar_dados)
            botao_editar_dados.pack(pady=10)

            botao_analise_dados = ctk.CTkButton(frame_conteudo, text="Analisar dados", fg_color="blue",
                                                text_color="#ffffff", width=300, command=self.tela_analise_dados)
            botao_analise_dados.pack(pady=10)

            frame_conteudo.pack(fill="both", expand=True)

            
            pass
    
    
    
    def tela_ver_dados(self):
            for widget in self.frame_adm.winfo_children():
                widget.destroy()
            tabela=self.gerar_tabela()
            frame_topo = ctk.CTkFrame(self.frame_adm, fg_color="#1A73E8", height=80)
            frame_topo.pack(fill="x")

            titulo = ctk.CTkLabel(frame_topo, text="💧 MODO ADM",text_color="#ffffff", font=("Arial", 24, "bold"))
            titulo.pack(pady=20)

        

            #criação de um frame com scroll para que seja possível ver todos os dados
            frame_scroll = ctk.CTkScrollableFrame(self.frame_adm,fg_color="#ffffff")
            frame_scroll.pack(fill="both", expand=True, padx=10, pady=10)
            

            #perguntar o porque é melhor usar a fonte courier
            label_tabela = ctk.CTkLabel(frame_scroll, text=tabela, font=("Courier", 12), anchor="w", justify="left")
            label_tabela.pack(padx=10, pady=10)

            #fazer botão de voltar para o menu
           
            pass
    
    
    
    def tela_editar_dados(self):
            for widget in self.frame_adm.winfo_children():
                widget.destroy()
            pass
    
    
    
    def tela_analise_dados(self):
            for widget in self.frame_adm.winfo_children():
                widget.destroy()
            pass
    
    def gerar_tabela(self):
        
        #Cria um dataframe(Tabela criada pelo pandas,similar ao de banco de dados)
        df = pd.DataFrame({
            "Email": list(dados_conta.keys()),
            "Família": list(dados_familia.values()),
            "Membros": list(dados_quantidade.values()),
            "Pontos": list(dados_pontos.values()),
            "Apartamento": list(dados_apartamento.values()),
            "Verificador": list(dados_codigov.values()),
        })
        # Transforma o DataFrame para string formatada
        tabela_formatada = df.to_string()
        print(tabela_formatada)
        return tabela_formatada

        pass
    
        






class UsuarioLogado(ctk.CTkFrame):
    def __init__ (self, master, email_logado):
        super().__init__(master)
        
        self.email_logado=email_logado
        
        self.frame_menu = ctk.CTkFrame(self, fg_color="#ffffff")
       
        self.frame_topo_menu = ctk.CTkFrame(self.frame_menu, fg_color= "#1A73E8", height=80)
        self.frame_topo_menu.pack(fill="x")

        label_titulo_menu = ctk.CTkLabel(self.frame_topo_menu, text="EcoDrop", fg_color= "#1A73E8", text_color="white",
                                         font=("Arial", 25, 'bold'))
        label_titulo_menu.pack(pady=20)

        self.frame_lateral_menu = ctk.CTkFrame(self.frame_menu, fg_color='white', width=200)
        self.frame_lateral_menu.pack(side='left', fill='y')

        self.frame_conteudo_menu = ctk.CTkFrame(self.frame_menu, fg_color="#f0f2f5")
        self.frame_conteudo_menu.pack(fill="both", expand=True)

        self.frameprincipalmenu = ctk.CTkFrame(self.frame_conteudo_menu, fg_color="#ffffff")
        self.frameprincipalmenu.pack(fill='both', expand=True, padx=30, pady=30)

        label_interaja = ctk.CTkLabel(
            self.frame_lateral_menu,
            text= 'Interaja',
            font=("Arial", 17, 'bold'),
            text_color = "#1A73E8",
            anchor = 'w'
        )

        label_interaja.pack(fill='x', padx=20, pady=(20, 5))


        #Chamamento da classe game 
        self.game_manager = Game(master=self.frame_lateral_menu,
                                  content_frame=self.frameprincipalmenu, 
                                  email=self.email_logado,
                                  reset_callback=self.reset_principal_menu_content)
        self.game_manager.pack(fill='x', pady=5)

        

        #Separador visual
        separator = ctk.CTkFrame(self.frame_lateral_menu, height=2, fg_color="#792dc0")
        separator.pack(fill='x', padx=20, pady=10)

        #Chamamento da classe GerenciarUser
        label_gerenciar = ctk.CTkLabel(
            self.frame_lateral_menu,
            text="Gerenciar",
            font=("Arial", 14, "bold"),
            text_color="#1A73E8", # Usando a cor do tema para destaque
            anchor="w"
        )
        label_gerenciar.pack(fill='x', padx=20, pady=(0, 5)) # Adiciona espaçamento vertical

        
        self.user_manager = GerenciarUsuario(master=self.frame_lateral_menu, 
                                           content_frame=self.frameprincipalmenu, 
                                           email=self.email_logado,
                                           reset_callback=self.reset_principal_menu_content,
                                           voltar_inicial_callback=self.voltar_inicial_callback)
        self.user_manager.pack(fill='x', pady=5)

        self.reset_principal_menu_content()

    def reset_principal_menu_content(self):
        for widget in self.frameprincipalmenu.winfo_children():
            widget.destroy()

        texto_bem_vindo = ctk.CTkLabel(self.frameprincipalmenu, text="Bem-vindo ao EcoDrop",
                                         fg_color="#ffffff", text_color="#202124", font=("Arial", 18, "bold"))
        texto_bem_vindo.pack(pady=(0, 20))

        texto_instrucao = ctk.CTkLabel(self.frameprincipalmenu,
                                         text=random.choice(mensagens_agua),
                                         fg_color="#ffffff", text_color="#5f6368",
                                         wraplength=500, justify="left", font=("Arial", 12))
        texto_instrucao.pack()

        imagem_menu_principal = Image.open("fotos/mascoteprincipall.png")
        ctk_imagem_menu_principal = ctk.CTkImage(light_image=imagem_menu_principal, dark_image=imagem_menu_principal, size=(400, 400))

        label_menu_principal_image = ctk.CTkLabel(self.frameprincipalmenu, image=ctk_imagem_menu_principal, text="")
        label_menu_principal_image.pack()

    
class Game(ctk.CTkFrame):
    def __init__(self, master, content_frame, reset_callback,  email, **kwargs):
        super(). __init__(master, **kwargs)
        self.content_frame = content_frame
        self.email = email
        self.reset_callback = reset_callback
        self.configure(fg_color='white')

        self.criar_widgets()

    def criar_widgets(self):
        botao1 = ctk.CTkButton(self, text="🏆 Ranking mensal", fg_color='white', text_color="#1A73E8",
                                    font=("Arial", 15), anchor='w', command=self.mostrar_ranking, cursor="hand2")
        botao1.pack(fill='x', pady=(20, 10), padx=20)
        
        botao2 = ctk.CTkButton(self, text="🎁 Resgatar prêmios", fg_color="white", text_color="#1A73E8",
                                    font=("Arial", 15), anchor='w', command=self.resgatar_premio, cursor="hand2")
        botao2.pack(fill='x', pady=10, padx=20)
        
        botao3 = ctk.CTkButton(self, text="🧮 Cálculo de pontos", fg_color="white", text_color="#1A73E8",
                                    font=("Arial", 15), anchor='w', command=self.calculo_pontuacao, cursor='hand2')
        botao3.pack(fill='x',pady=10, padx=20)
        
        botao4 = ctk.CTkButton(self, text="🧠 Quiz semanal", fg_color='white', text_color="#1A73E8",
                                    font=("Arial", 15), anchor='w', command=self.quiz_semanal, cursor="hand2")
        botao4.pack(fill='x', pady=10, padx=20)

    def _carregar_dados(self):
        with open(r"banco_dados.JSON", "r", encoding="utf-8") as f:
            return json.load(f)

    def _salvar_dados(self, dados_completos):
        with open(r"banco_dados.JSON", "w", encoding="utf-8") as f:
            json.dump(dados_completos, f, indent=4, ensure_ascii=False)

    
    def limpar_conteudo(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    

    def mostrar_ranking(self):
        self.limpar_conteudo()
        label_titulo = ctk.CTkLabel(self.content_frame, text="🏆 Ranking Mensal", font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        try:
           dados_lidos=self._carregar_dados()
           dados_pontos_ranking = dados_lidos.get("pontos", {})
           dados_familia_ranking = dados_lidos.get("familia", {})
        except Exception as e:
            ctk.CTkLabel(self.content_frame, text=f"Erro ao carregar dados {e}", text_color='red').pack()
            return
        
        ranking_data = [{'familia': dados_familia_ranking.get(email, "N/A"), 'pontos': pts} 
                        for email, pts in dados_pontos_ranking.items()]
        ranking_data.sort(key=lambda x: x["pontos"], reverse=True)

        if not ranking_data:
            ctk.CTkLabel(self.content_frame, text="Nenhum dado de ranking dispoível", font=("Arial", 15), text_color="#5f6368").pack(pady=10)
        else:
            header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=50, pady=(10, 5))
            ctk.CTkLabel(header_frame, text="Posição", font=("Arial", 12, "bold"), width=80).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Família", font=("Arial", 12, "bold"), width=200).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Pontos", font=("Arial", 12, "bold"), width=100).pack(side="left", padx=5)
            
            for i, item in enumerate(ranking_data):
                row_frame = ctk.CTkFrame(self.content_frame, fg_color="#f0f2f5" if i % 2 == 0 else "white", corner_radius=5)
                row_frame.pack(fill="x", padx=50, pady=2)
                ctk.CTkLabel(row_frame, text=f"{i+1}º", width=80).pack(side="left", padx=5, pady=3)
                ctk.CTkLabel(row_frame, text=item["familia"], width=200, anchor="w").pack(side="left", padx=5, pady=3)
                ctk.CTkLabel(row_frame, text=item["pontos"], width=100).pack(side="left", padx=5, pady=3)

        botao_voltar = ctk.CTkButton(self.content_frame, text="⬅ Voltar ao Menu", fg_color="gray", command=self.reset_callback)
        botao_voltar.pack(pady=20)


    def resgatar_premio(self):
        self.limpar_conteudo()
        dados_atuais=self.carregar_dados()
        pontos_usuario=dados_atuais["pontos"].get(self.email,0)

        label_titulo = ctk.CTkLabel(self.content_frame, text="🎁 Resgatar Prêmios", font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

       
        label_pontos_saldo = ctk.CTkLabel(self.content_frame, text=f"Seus pontos atuais: {pontos_usuario} 🌟",
                                          font=("Arial", 16, "bold"), text_color="#28a745")
        label_pontos_saldo.pack(pady=(0, 20))

        label_mensagem_resgate = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 15))
        label_mensagem_resgate.pack(pady=(0, 10))

        
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, label_text="Prêmios Disponíveis", width=500, height=300)
        scroll_frame.pack(pady=10, padx=20, fill='both', expand=True)

        
        def realizar_resgate(premio_selecionado):
            dados_para_salvar = self._carregar_dados()
            pontos_disponiveis = dados_para_salvar["pontos"].get(self.email, 0)
            
            if pontos_disponiveis >= premio_selecionado["custo"]:
                dados_para_salvar["pontos"][self.email] -= premio_selecionado["custo"]
                self._salvar_dados(dados_para_salvar)
                
                label_pontos_saldo.configure(text=f"Seus pontos atuais: {dados_para_salvar['pontos'][self.email]} 🌟")
                label_mensagem_resgate.configure(text=f"Prêmio '{premio_selecionado['nome']}' resgatado!", text_color="green")
            else:
                label_mensagem_resgate.configure(text='Pontos insuficientes!', text_color='red')

        for premio in premios_disponiveis:
            premio_frame = ctk.CTkFrame(scroll_frame, fg_color='white', corner_radius=10)
            premio_frame.pack(fill='x', pady=5, padx=5)
            info_frame = ctk.CTkFrame(premio_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10)
            ctk.CTkLabel(info_frame, text=premio["nome"], font=("Arial", 14, "bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(info_frame, text=f"Custo: {premio['custo']} pontos", font=("Arial", 12), text_color="#6c757d", anchor="w").pack(fill="x")
            botao_resgatar = ctk.CTkButton(premio_frame, text="Resgatar", fg_color="#ffc107", text_color="black", width=100, command=lambda p=premio: realizar_resgate(p))
            botao_resgatar.pack(side="right", padx=10, pady=10)

        botao_voltar = ctk.CTkButton(self.content_frame, text="⬅ Voltar ao Menu", fg_color="gray", command=self.reset_callback)
        botao_voltar.pack(pady=20)



    def calculo_pontuacao(self):
        self.limpar_conteudo()
        label_titulo = ctk.CTkLabel(self.content_frame, text="🧮 Cálculo de Pontos", font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20,10))

        ctk.CTkLabel(self, text='Informe seu consumo diário (em litros):', font=("Arial", 15)).pack(pady=(0, 10))

        entrada_consumo = ctk.CTkEntry(self.content_frame, width=200, validate="key",
                                       validatecommand=(self.register(self.validar_numeros), "%P"))
        entrada_consumo.pack(padx=50, pady=(0, 10), anchor="w")

        botao_voltar = ctk.CTkButton(self.content_frame, text="⬅ Voltar ao Menu", fg_color="gray",
                                   command=self.reset_callback)
        
        label_resultado=ctk.CTkLabel(self.content_frame, text='', font=("Arial", 15, 'bold'))
        label_resultado.pack(pady=(10, 0))

        botao_voltar.pack(pady=20)

        def calcular_acao():
            consumo_str = entrada_consumo.get()
            if not consumo_str:
                label_resultado.configure(text="Por favor, insira o consumo.", text_color='red')

            try:
                consumo_diario = int(consumo_str)
                dados_atuais=self._carregar_dados()
                pontos_usuario=dados_atuais['pontos'].get(self.email, 0)
                membros =dados_atuais['membros'].get(self.email, 1)

                consumo_ideal_total = 90*membros  #VAMOS ESTABELECER UMA META DE CONSUMO MENOR
                pontos_ganhos = 0

                if consumo_diario < consumo_ideal_total:
                    litros_economizados = consumo_ideal_total - consumo_diario
                    pontos_ganhos = int(litros_economizados/10)

                if pontos_ganhos>0:
                    dados_atuais['pontos'][self.email] = pontos_usuario + pontos_ganhos
                    self._salvar_dados(dados_atuais)
                    label_resultado.configure(text=f'parabéns! Você ganhou {pontos_ganhos} pontos!', text_color='green')
                else:
                    label_resultado.configure(text="Nenhum ponto ganho. Tente reduzir o consumo!", text_color="#E67E22")
            except Exception as e:
                label_resultado.configure(text=f"Erro: {e}", text_color="red")

        botao_calcular=ctk.CTkButton(self.content.frame, text='Voltar ao Menu', fg_color='grey', command=self.reset_callback)
        botao_calcular.pack(pady=10)
        botao_voltar = ctk.CTkButton(self.content_frame, text="⬅ Voltar ao Menu", fg_color="gray", command=self.reset_callback)
        botao_voltar.pack(pady=20)


    def quiz_semanal(self):
        self.limpar_conteudo()
        label_titulo = ctk.CTkLabel(self.content_frane, text = "🧠 Quiz Semanal", font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        try:
            dados_lidos = self._carregar_dados()
            questoes_disponiveis = dados_lidos.get("questoes_quiz", [])
            data_ultimo_quiz_str=dados_lidos.get("ultimo_quiz", {}). get(self.email)

            data_atual = datetime.now().date()
            pode_fazer_quiz = True

            if data_ultimo_quiz_str:
                data_ultimo_quiz = datetime.strptime(data_ultimo_quiz_str, "%Y-%m-%d").date()
                if data_ultimo_quiz > data_atual - timedelta(days=data_atual.weekday() +  7):  #Verifica se o usuário já fez na semana atual
                    pode_fazer_quiz = False
            if not pode_fazer_quiz:
                ctk.CTkLabel(self. content_frame, text='Você já realizou o quiz esta semana', text_color= 'red', font=("Arial", 14)). pack(pady=20)
                ctk.CTkButton(self.content_frame, text='Voltar', fg_color="gray", command=self.reset_callback).pack()
                return
            if len (questoes_disponiveis) < 5:
                ctk.CTklabel(self.content_frame, text= 'Quiz indisponível. Contate o ADM.', font=("Arial", 15)).pack(pady=20)
                ctk.CTkButton(self.content_frame, text='Voltar', fg_color='gray', command= self.reset_callback).pack()
                return
        except Exception as e:
            ctk.CTkLabel(self.content_frame, text=f"Erro ao carregar quiz: {e}", text_color="red").pack()
            return
        
        questoes_para_quiz = random.sample(questoes_disponiveis, 5)
        respostas_usuario = {}
        current_question_index = 0

        question_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 16, "bold"), wraplength=500)
        question_label.pack(pady=(20, 10))
        options_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        options_frame.pack(pady=10)
        radio_var = ctk.StringVar()
        quiz_message_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 12))
        quiz_message_label.pack()

        def mostrar_questao (index):
            for widget in options_frame.winfo_children():
                widget.destroy()

            questao=questoes_para_quiz[index]
            question_label.configure(text=f'Questão {index+1}: {questao['pergunta']}')
            radio_var.set('')

            for option in questao ['opcoes']:
                ctk.CTkRadioButton(options_frame, text=option, variable=radio_var, value=option).pack(anchor='w', pady=4)

            botao_proxima.configure(text='Próxima questão' if index < 4 else "Finalizar quiz")


        def proxima_questao():
            nonlocal current_question_index
            if not radio_var.get():
                quiz_message_label.configure(text="Selecione uma opção!", text_color='red')
                return

            quiz_message_label.configure(text='')
            respostas_usuario[current_question_index] = radio_var.get()

            current_question_index += ''
            if current_question_index < len(questoes_para_quiz):
                mostrar_questao(current_question_index)
            else:
                calculate_score()

        def calculate_score():
            pontuacao = sum(1 for i, q in enumerate(questoes_para_quiz) if respostas_usuario.get(i) == q['resposta_correta'])
            pontos_ganhos = pontuacao * 100
            
            dados_finais = self._carregar_dados()
            dados_finais["pontos"][self.email] = dados_finais["pontos"].get(self.email, 0) + pontos_ganhos
            if "ultimo_quiz" not in dados_finais: dados_finais["ultimo_quiz"] = {}
            dados_finais["ultimo_quiz"][self.email] = datetime.now().date().strftime("%Y-%m-%d")
            self._salvar_dados(dados_finais)

            self.limpar_conteudo()
            ctk.CTkLabel(self.content_frame, text="🎉 Quiz Concluído! 🎉", font=("Arial", 22, "bold"), text_color="#1A73E8").pack(pady=20)
            ctk.CTkLabel(self.content_frame, text=f"Você acertou {pontuacao} de 5 questões.", font=("Arial", 16)).pack(pady=5)
            ctk.CTkLabel(self.content_frame, text=f"Você ganhou {pontos_ganhos} pontos!", font=("Arial", 16, "bold"), text_color="green").pack(pady=5)
            ctk.CTkButton(self.content_frame, text="⬅ Voltar ao Menu", fg_color="gray", command=self.reset_callback).pack(pady=20)

        botao_proxima = ctk.CTkButton(self.content_frame, text="", command=proxima_questao)
        botao_proxima.pack(pady=20)
        mostrar_questao(0)
        





         
class GerenciarUsuario(ctk.CTkFrame):
        
        def __init__ (self, master, content_frame, reset_callback, voltar_inicial_callback, email, **kwargs):
            super().__init__(master, **kwargs)
            self.content_frame=content_frame
            self.email=email
            self.reset_callback=reset_callback
            self.voltar_inicial_callback= voltar_inicial_callback
            self.configure(fg_color="white")

            self.criar_widgets()


        def _carregar_dados(self):
            """Carrega os dados do arquivo JSON."""
            with open(r"banco_dados.JSON", "r", encoding="utf-8") as f:
                return json.load(f)

        def _salvar_dados(self, dados_completos):
            """Salva os dados no arquivo JSON."""
            with open(r"banco_dados.JSON", "w", encoding="utf-8") as f:
                json.dump(dados_completos, f, indent=4, ensure_ascii=False)

        def criar_widgets(self):
            botao5 = ctk.CTkButton (self, text="📘 Área educativa", fg_color="white",text_color="#1A73E8",
                                    font=("Arial", 15), anchor="w", commad=self.area_educativa, cursor="hand2")
            botao5.pack(fill='x', pady=10, padx=20)
            
            botao6= ctk.CTkButton (self, text= "📊 Mostrar dados", fg_color='white', text_color="#1A73E8",
                                   font=("Arial", 15), anchor='w', command=self.mostrar_dados, cursor="hand2")
            botao6.pack(fill='x', pady=10, padx=20)

            botao7 = ctk.CTkButton (self, text ="🔄 Atualizar dados", fg_color='white', text_color= "#1A73E8",
                                    font=("Arial", 15), anchor='w', command=self.atualizar_dados, cursor="hand2")
            botao7.pack(fill='x', pady=10, padx=20)

            botao8 = ctk.CTkButton(self, text="🗑 Deletar conta", fg_color='white', text_color= "#1A73E8",
                                    font=("Arial", 15), anchor='w', command=self.deletar_conta, cursor="hand2")
            botao8.pack(fill='x', pady=10, padx=20)

            botao9 = ctk.CTkButton(self, text="✍️ Enviar feedback", fg_color='white', text_color= "#1A73E8",
                                    font=("Arial", 15), anchor='w', command=self.feedback, cursor="hand2")
            botao9.pack(fill='x', pady=10, padx=20)

        def limpar_conteudo(self):
            for widget in self.content_frame.winfo_children():
                widget.destroy()

        def area_educativa(self):
            self.limpar_conteudo()
            label = ctk.CTkLabel(self.content_frame, text="Funcionalidade: Área Educativa\n(A ser implementada)", font=("Arial", 18))
            label.pack(pady=20)
        # Aqui você pode adicionar o conteúdo da área educativa que já tinha.

        def mostrar_dados(self):
            self.limpar_conteudo()
            label_titulo=ctk.CTkLabel(self.content_frame, text = "📊 Seus Dados",
                                      font=("Arial", 20, 'bold'),
                                      text_color= "#1A73E8")
            label_titulo.pack(pady=(20, 10))

            dados = self._carregar_dados()
            user_family = dados['familia'].get(self.email, "N/A")
            user_membros= dados['membros'].get(self.email, 'N/A')
            user_points= dados['pontos'].get(self.email, 'N/A')
            user_apartment= dados['apartamento']

            data_text = f'''
            Email: {self.email}
            Sobrenome da família: {user_family}
            Membros da família: {user_membros}
            Pontos acumulados: {user_points}
            Número do apartamento: {user_apartment}
            '''

            ctk.CTkLabel(self.content_frame, text=data_text,
                 font=("Arial", 14), text_color="#333333", justify="left").pack(pady=10)

            botao_voltar = ctk.CTkButton(self.content_frame, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=self.reset_callback)
            botao_voltar.pack(pady=20)
                


            

        def atualizar_dados(self):
            self.limpar_conteudo()
            label_titulo = ctk.CTkLabel(self.content_frame, text="🔄 Atualizar Dados", 
                                        font=("Arial", 20,'bold'),
                                        text_color = "#1A73E8")
            label_titulo.pack(pady=(20, 10))

            dados = self._carregar_dados()
            nome_atual = dados_familia.get(self.email, "")
            membros_atuais = dados_quantidade.get(self.email, "")

            # Campo Nome da Família
            label_nome_familia = ctk.CTkLabel(self.content_frame, text="Nome da Família:",
                                       font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
            label_nome_familia.pack(fill="x", padx=50, pady=(10, 0))
            entrada_nome_familia = ctk.CTkEntry(self.content_frame, width=300)
            entrada_nome_familia.insert(0, nome_atual)
            entrada_nome_familia.pack(padx=50, pady=(0, 10))

            # Campo Quantidade de Membros
            label_membros = ctk.CTkLabel(self.content_frame, text="Quantidade de Membros:",
                                  font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
            label_membros.pack(fill="x", padx=50, pady=(10, 0))
            entrada_membros = ctk.CTkEntry(self.content_frame, width=300, validate="key",
                                   validatecommand=(self.register(Game.validar_numeros), "%P"))
            entrada_membros.insert(0, str(membros_atuais))
            entrada_membros.pack(padx=50, pady=(0, 10))

            # Campo Nova Senha (opcional)
            label_nova_senha = ctk.CTkLabel(self.content_frame, text="Nova Senha (deixe em branco para não alterar):",
                                     font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
            label_nova_senha.pack(fill="x", padx=50, pady=(10, 0))
            entrada_nova_senha = ctk.CTkEntry(self.content_frame, width=300, show="*")
            entrada_nova_senha.pack(padx=50, pady=(0, 10))

            label_mensagem_atualizar = ctk.CTkLabel(self.content_frame, text="", text_color="red", font=("Arial", 12))
            label_mensagem_atualizar.pack(pady=(0, 10))

            def salvar_atualizacao_acao():
                novo_nome = entrada_nome_familia.get().strip()
                nova_qtde_membros_str = entrada_membros.get().strip()
                nova_senha = entrada_nova_senha.get().strip()

                if not novo_nome or not nova_qtde_membros_str:
                    label_mensagem_atualizar.configure(text="Nome da família e quantidade de membros são obrigatórios.", text_color="red")
                return

                try:
                    nova_qtde_membros = int(nova_qtde_membros_str)
                    if nova_qtde_membros <= 0:
                        label_mensagem_atualizar.configure(text="Quantidade de membros deve ser maior que zero.", text_color="red")
                        return
                except ValueError:
                    label_mensagem_atualizar.configure(text="Quantidade de membros deve ser um número válido.", text_color="red")
                    return

                if nova_senha and not (4 <= len(nova_senha) <= 20):
                    label_mensagem_atualizar.configure(text="A nova senha deve ter entre 4 e 20 caracteres.", text_color="red")
                    return

                try:
                    data = self._carregar_dados()
                    data['familia'][self.email]=novo_nome
                    data['membros'][self.email]=nova_qtde_membros
                    if nova_senha:
                        data['senha'][self.email]=nova_senha

                    self._salvar_dados(data)
                    label_mensagem_atualizar.configure(text='Dados atualizados com sucesso!', text_color='green')
                    entrada_nova_senha.delete(0, ctk.END)
                except Exception as e:
                           label_mensagem_atualizar.configure(text=f"Erro ao atualizar: {e}", text_color="red")

            botao_salvar = ctk.CTkButton(self.content_frame, text="Salvar Atualizações", fg_color="#1A73E8", text_color="white", command=salvar_atualizacao_acao)
            botao_salvar.pack(pady=10)
            botao_voltar = ctk.CTkButton(self.content_frame, text="⬅ Voltar ao Menu", fg_color="gray", text_color="white", command=self.reset_callback)
            botao_voltar.pack(pady=20)




        def deletar_conta(self):
            self.limpar_conteudo()
            label_titulo = ctk.CTkLabel(self.content_frame, text="🗑 Deletar Conta",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
            label_titulo.pack(pady=(20, 10))

            label_confirmacao = ctk.CTkLabel(self.content_frame, text="ATENÇÃO: Esta ação é irreversível!\nDeseja realmente deletar sua conta?",
                                      font=("Arial", 14, "bold"), text_color="red")
            label_confirmacao.pack(pady=20)

            def confirmar_delecao_action():
                
                try:
                    data=self._carregar_dados()
                    if self.email in data['senha']:
                        del data["senha"][self.mail]
                        del data["familia"][self.email]
                        del data["membros"][self.email]
                        del data["pontos"][self.email]
                        del data["apartamento"][self.email]
                        del data["verificador"][self.email]
                        if self.email in data["ultimo_quiz"]: # Remove o registro do quiz também
                            del data["ultimo_quiz"][self.email]
                    else:
                        label_confirmacao.configure(text="Erro: Conta não encontrada.", text_color="red")
                except Exception as e:
                    label_confirmacao.configure(text=f"Erro ao deletar conta: {e}", text_color="red")

            botao_confirmar_delecao = ctk.CTkButton(self.content_frame, text="Confirmar Deleção", fg_color="red", hover_color="#cc0000", command=confirmar_delecao_action)
            botao_confirmar_delecao.pack(pady=10)
            botao_voltar = ctk.CTkButton(self.content_frame, text="Cancelar", fg_color="gray", text_color="white", command=self.reset_callback)
            botao_voltar.pack(pady=20)


        def feedback(self):
            self.limpar_conteudo()
            label_titulo = ctk.CTkLabel(self.content_frame, text="✍️ Enviar Feedback", font=("Arial", 20, "bold"), text_color="#1A73E8")
            label_titulo.pack(pady=(20, 10))
        
            ctk.CTkLabel(self.content_frame, text="Por favor, deixe sua opinião sobre o sistema EcoDrop:", font=("Arial", 14), text_color="#333333").pack(pady=(0, 10))

            ctk.CTkLabel(self.content_frame, text="Seu Feedback (até 140 caracteres):", font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w").pack(fill="x", padx=50, pady=(10, 0))
            entrada_feedback = ctk.CTkTextbox(self.content_frame, width=400, height=80)
            entrada_feedback.pack(padx=50, pady=(0, 10))

            ctk.CTkLabel(self.content_frame, text="Sua nota para o sistema (0 a 10):", font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w").pack(fill="x", padx=50, pady=(10, 0))
            entrada_nota = ctk.CTkEntry(self.content_frame, width=100, validate="key", validatecommand=(self.register(self._validar_nota), "%P"))
            entrada_nota.pack(padx=50, pady=(0, 20), anchor="w")

            label_mensagem_feedback = ctk.CTkLabel(self.content_frame, text="", text_color="red", font=("Arial", 12))
            label_mensagem_feedback.pack(pady=(0, 10))

            def enviar_feedback_acao():
                feedback_text = entrada_feedback.get("1.0", "end-1c").strip()
                nota_text = entrada_nota.get().strip()

                if not feedback_text or not nota_text:
                    label_mensagem_feedback.configure(text="Por favor, preencha todos os campos.", text_color="red")
                    return
                if len(feedback_text) > 140:
                    label_mensagem_feedback.configure(text="O feedback não pode exceder 140 caracteres.", text_color="red")
                    return

                try:
                    with open("feedback.csv", "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        # Escreve cabeçalho se o arquivo estiver vazio
                        if f.tell() == 0:
                            writer.writerow(["Email", "Feedback", "Nota", "Data/Hora"])
                        writer.writerow([self.email, feedback_text, nota_text, time.strftime("%Y-%m-%d %H:%M:%S")])
                
                    label_mensagem_feedback.configure(text="Feedback enviado com sucesso! Agradecemos.", text_color="green")
                    entrada_feedback.delete("1.0", ctk.END)
                    entrada_nota.delete(0, ctk.END)
                except Exception as e:
                    label_mensagem_feedback.configure(text=f"Erro ao salvar feedback: {e}", text_color="red")

            botao_enviar = ctk.CTkButton(self.content_frame, text="Enviar Feedback", fg_color="#1A73E8", text_color="white", command=enviar_feedback_acao)
            botao_enviar.pack(pady=10)
            botao_voltar = ctk.CTkButton(self.content_frame, text="⬅ Voltar ao Menu", fg_color="gray", text_color="white", command=self.reset_callback)
            botao_voltar.pack(pady=20)

    





      

        







app = App()
app.mainloop()


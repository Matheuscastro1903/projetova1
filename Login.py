import customtkinter as ctk
from customtkinter import CTkImage, CTkLabel

from PIL import Image
import json
import pandas as pd
import matplotlib as plt
from collections import Counter
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from validar import validar_letras_espacos, validar_numeros


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






"""Essa classes será responsável por toda a parte que se refere ao login,seja os tratamentos de erro,seja as operações feitas """


class Login(ctk.CTkFrame):
    def __init__(self, master, voltar_inicial, mostrar_menu):
        """Inicializador chamará a interface,com suas entradas e botões"""
        super().__init__(master)
        #atributo de classe responsável por contar a quantidade de tentativas no login
        self.tentativas=0
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
        """Método utilizado para verificar se há espaços em branco ao apertar o botão logar"""
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
        """Método utilizado para verificar se email e senha estão corretos,para assim ir para o menu.Caso o usuário erre 
        a senha 3x,será direcionado a parte de tentar entrar com o código verificador,caso erre novamente,o sistema fechará
        por segurança """

        with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
            # quando usa json.load o arquivo json é transformado em dicionário python
            arquivo_lido = json.load(arquivo)

            dados_conta = arquivo_lido["senha"]

            if self.email in dados_conta:
                if dados_conta[self.email] == self.senha:
                    self.mostrar_menu(self.email, self.senha)
                    return
                else:
                    self.label_avisologin.configure(
                        text="EMAIL OU SENHA INCORRETO.", text_color="red")
                    self.tentativas+=1
                    if self.tentativas==4:
                        self.tentar_verificador()
                    
                    return

            else:
                self.label_avisologin.configure(
                    text="EMAIL NÃO CADASTRADO.\nVá para tela de cadastro")
                self.tentativas+=1
                if self.tentativas==4:
                    self.aviso_sistema()
                return
    

    def tentar_verificador(self):
        """Método responsvál por mostra o frame onde o usuário tentará entrar com o código verificador"""
        for widget in self.frame_login.winfo_children():
            widget.destroy()

        
        label_adm = ctk.CTkLabel(self.frame_login, text="Insira o código de acesso \nVocê tem apenas uma chance.",
                                   fg_color="#ffffff", text_color="red", font=("Arial", 20))
        label_adm.pack(pady=2)
        
         # 2-entrada senha
        label_emailveri= ctk.CTkLabel(self.frame_login, text="Digite seu email:", text_color="#000000", anchor="w", width=300)
        label_emailveri.pack(pady=(2, 0))

        self.entrada_email_veri = ctk.CTkEntry(self.frame_login, width=300)
        self.entrada_email_veri.pack(pady=2)



        # 2-entrada senha
        label_codigov= ctk.CTkLabel(self.frame_login, text="Digite o código verificador:", text_color="#000000", anchor="w", width=300)
        label_codigov.pack(pady=(2, 0))

        self.entrada_codigo_veri = ctk.CTkEntry(self.frame_login, width=300, show="*")
        self.entrada_codigo_veri.pack(pady=2)

        # 3-entrada email cond

        # botão logar
        botao_entrar_verificador = ctk.CTkButton(self.frame_login, text="Entrar", fg_color="blue",
                                    text_color="#ffffff", width=300, command=self.conferir_verificador)
        botao_entrar_verificador.pack(pady=2)
        # botão voltar
    
        

    def conferir_verificador(self):
        """Método responsável por verificar se o email e código verificador estão batendo.Caso contrário,irá para uma tela
        avisando que o sistema fechará em 7 segundos"""

        try:
            codigo=int(self.entrada_codigo_veri.get().strip())
            email=self.entrada_email_veri.get().strip()

            if dados_codigov[email]==codigo:
                self.mostrar_menu(self.email, self.senha)
            else:
                self.aviso_sistema()

        except:
            self.aviso_sistema()



    def aviso_sistema(self):
        """Método responsável por mostrar aviso que o sistem será encerrado em 7 segundos,por questões de segurança"""
        for widget in self.frame_login.winfo_children():
            widget.destroy()
       
    

        # Mensagem de título
        titulo = ctk.CTkLabel(self.frame_login,
                          text="🚫 Limite de Tentativas Atingido",
                          font=("Arial", 20, "bold"),
                          text_color="red")
        titulo.pack(pady=(30, 10))

        # Mensagem adicional
        msg = ctk.CTkLabel(self.frame_login,
                       text="O sistema será encerrado por segurança.",
                       font=("Arial", 16))
        msg.pack(pady=5)

        # Label de contagem regressiva
        self.label_contador = ctk.CTkLabel(self.frame_login,
                                       text="Fechando em 7 segundos...",
                                       font=("Arial", 16, "italic"))
        self.label_contador.pack(pady=(20, 10))
        self.after(7000, self.sair_sistema)

    def sair_sistema(self):
        """Função utilizada para fechar sistema """
        # Fechando dessa forma irá "destruir" a janela que foi definida no master
        self.master.destroy()  # Fecha a janela principal
    
        pass

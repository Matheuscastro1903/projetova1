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

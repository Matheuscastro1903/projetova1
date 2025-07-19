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

from Telainicial import TelaInicial
from Login import TelaLogin
from Cadastro import TelaCadastro
from ModoAdm import TelaModoAdm,OperacoesAdm
from Sobrenos import TelaSobreNos
from UsuarioLogado import UsuarioLogado,Game,GerenciarUsuario


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








if __name__ == "__main__":
    app = App()
    app.mainloop()
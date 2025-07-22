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
from Login import Login
from Usuario import Usuario
from ModoAdm import ModoAdm,OperacoesAdm
from Sobrenos import SobreNos
from UsuarioLogado import UsuarioLogado




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


"""Class App será a classe Master,que organizará as trocas de tela."""

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        """
        Init serve para inicializar cada função necessária para a criação de uma janela básica.
        """

        self.title("ECODROP SYSTEM")
        self.geometry("1000x800+400+150")
        self.resizable(False, False)

        """
        Cada tela será inicializa por um atributo da classe.Construimos dessa forma,pois conseguimos verificar se o atributo de 
        classe já está puxando a classe,não havendo a necessidade de criar vários objetos,o que provavelmente deixaria o sistema lento
        e pesado
        """
        self.tela_inicial = None
        self.tela_login = None
        self.tela_cadastro = None
        self.tela_sobrenos = None
        self.tela_modoadm = None
        self.tela_menu = None
        
        # Lista para ocultar todas as telas
        """Essa lista será utilizada para ocultar todas as telas que já foram utilizadas alguma vez durante o uso do sistema"""
        self.telas = []
        # chamemento da função criar_tela_inicial
        self.criar_tela_inicial()

    def criar_tela_inicial(self):
        """
        Esse método cria um objeto no self.tela_inicial da classe TelaInicial.Essa classe será responsável pela primeira "página" 
        da interface
        """
        self.esquecer_frames()
        if self.tela_inicial is None:
            self.tela_inicial = TelaInicial(self, mostrar_login=self.criar_tela_login, mostrar_cadastro=self.criar_tela_cadastro,
                                            modo_adm=self.criar_tela_modoadm, sobre_nos=self.criar_tela_sobrenos)
            self.telas.append(self.tela_inicial)
        self.tela_inicial.pack(fill="both", expand=True)

    def criar_tela_login(self):
        """
        Esse método só será utilizado caso na classe TelaInicial,se o usuário aperte o botão para ir para o login.Dessa forma,o atributo
        de calsse self.tela_login criará um objeto da classe Login
        
        """
        self.esquecer_frames()
        if self.tela_login is None:
            self.tela_login = Login(
                self, voltar_inicial=self.criar_tela_inicial, 
                mostrar_menu=self.criar_tela_menu)
            self.telas.append(self.tela_login)

        self.tela_login.pack(fill="both", expand=True)

    def criar_tela_cadastro(self):

        """
        Esse método só será utilizado caso na classe TelaInicial,se o usuário aperte o botão para ir para o cadastro.Dessa forma,o atributo
        de classe self.tela_cadastro criará um objeto da classe Usuario(responsável pelo processo de cadastramento de usuário)
        
        """
        self.esquecer_frames()
        if self.tela_cadastro is None:
            self.tela_cadastro = Usuario(
                self, 
                voltar_inicial=self.criar_tela_inicial, 
                mostrar_login=self.criar_tela_login)
            self.telas.append(self.tela_cadastro)
        self.tela_cadastro.pack(fill="both", expand=True)

    def criar_tela_modoadm(self):
        """
        Esse método só será utilizado caso na classe TelaInicial,se o usuário aperte o botão para ir para o modo administrador.Dessa forma,
        o atributo de classe self.tela_modoadm criará um objeto da classe ModoAdm
        
        """

        self.esquecer_frames()

        if self.tela_modoadm is None:
            self.tela_modoadm = ModoAdm(self, voltar_inicial=self.criar_tela_inicial)
            
            self.telas.append(self.tela_modoadm)
            
        self.tela_modoadm.pack(fill="both", expand=True)

    def criar_tela_sobrenos(self):
        """
        Esse método só será utilizado caso na classe TelaInicial,se o usuário aperte o botão para ir para o Sobre Nós.Dessa forma,
        o atributo de classe self.tela_sobrenos criará um objeto da classe Sobrenos
        
        """

        self.esquecer_frames()
        if self.tela_sobrenos is None:
            self.tela_sobrenos = SobreNos(
                self, voltar_inicial=self.criar_tela_inicial)
            self.telas.append(self.tela_sobrenos)

        self.tela_sobrenos.pack(fill="both", expand=True)

    def criar_tela_menu(self,email,senha):
        """
        Esse método só será utilizado caso o usuário consiga efetuar o login corretamente.Dessa forma,
        o atributo de classe self.tela_menu criará um objeto da classe UsuarioLogado(Que armazena as funções principais do projeto,fazendo o papel 
        de menu principal)
        
        """
        
        self.esquecer_frames()
        self.tela_menu = UsuarioLogado(self,email,senha)
        self.telas.append(self.tela_menu)
        self.tela_menu.pack(fill='both', expand=True)

    def esquecer_frames(self):
        """
        Método responsável por esquecer os frames que foram utilizados(criado objeto) alguma vez.Isso evita que destrua completamente o frame e ajuda 
        no desempenho do sistema
        """
        for frames in self.telas:
            if frames:
                frames.pack_forget()








if __name__ == "__main__":
    app = App()
    app.mainloop()
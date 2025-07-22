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
from validar import validar_letras_espacos,validar_numeros


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



class TelaInicial(ctk.CTkFrame):
    def __init__(self, master, mostrar_login, mostrar_cadastro, modo_adm, sobre_nos):
        super().__init__(master)
        """
        Essa classe é responsável por guardar a parte da interface responsável pela tela inicial.
        O usuário terá 4 opções de botão(Login,cadastro,Modo adm e Sobre Nós),dependendo da escolha,
        será retornado uma respostas para a classe App e inicializará outra parte da interface.
        """

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
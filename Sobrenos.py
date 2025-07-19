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


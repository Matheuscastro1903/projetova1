import customtkinter as ctk
from customtkinter import CTkImage, CTkLabel

from PIL import Image
import json
import csv
import time
import random
from datetime import datetime
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
    dados_calculo=dados_lidos["calculo_realizado"]

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




class UsuarioLogado(ctk.CTkFrame):
    def __init__(self, master, email, senha):
        super().__init__(master)
        self.email = email
        self.senha = senha
        
        
        
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

        # --- INÍCIO DA MODIFICAÇÃO ---

        # Pega a data de hoje
        hoje = datetime.now()

        # Verifica se o dia atual é o dia 28
        if hoje.day != 28:
            # Se não for o dia 28, exibe uma mensagem e impede a execução do resto da função
            ctk.CTkLabel(self.frameprincipal_menu, 
                         text="O cálculo de pontuação só está disponível no dia 28 de cada mês.",
                         font=("Arial", 14), text_color="orange", wraplength=500).pack(pady=20)
            
            botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                         fg_color="gray", text_color="white",
                                         command=self.reset_principal_menu_content)
            botao_voltar.pack(pady=20)
            return # Impede que o resto do código do método seja executado

        # --- FIM DA MODIFICAÇÃO ---

        # O código abaixo só será executado se o dia for 28
        self.label_atencao=ctk.CTkLabel(self.frameprincipal_menu, 
                         text="",
                         font=("Arial", 14), text_color="orange", wraplength=500)
        self.label_atencao.pack(pady=20)

        self.label_aviso=ctk.CTkLabel(self.frameprincipal_menu, 
                         text="Calculo de pontuação disponível.",
                         font=("Arial", 14), text_color="#1A73E8", wraplength=500)
        self.label_aviso.pack(pady=20)


        self.botao_calcular = ctk.CTkButton(self.frameprincipal_menu, text="Calcular Pontos",
                                       fg_color="#1A73E8", text_color="white",
                                       command=self.calcular_pontos_acao)
        self.botao_calcular.pack(pady=10)

        self.botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
        self.botao_voltar.pack(pady=20)

    def calcular_pontos_acao(self):
        self.botao_voltar.destroy()
        self.botao_calcular.destroy()
        if self.email not in dados_consumo:
            self.label_atencao.configure(text="Seu consumo não foi cadastrado ainda,fale com seu síndico.")
            self.botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
            self.botao_voltar.pack(pady=20)
            return
        calculo_realizado=dados_calculo[self.email]
        if calculo_realizado==True:
            consumo=dados_consumo[self.email]
            qpessoas=dados_quantidade[self.email]
            gasto_estimado=qpessoas*30*110
            if consumo>gasto_estimado:
                try:
                    self.label_aviso.configure(text=f"Seu gasto({consumo}L) foi acima do ideal({gasto_estimado}L).Vamos melhorar!!",text_color="Red")
                    imagem = Image.open("fotos/mascotetriste.jpg")
                    ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(200, 200))
                    label = ctk.CTkLabel(self.frameprincipal_menu, image=ctk_imagem, text="")
                    label.pack()
                except:
                    placeholder = ctk.CTkLabel(self.frameprincipal_menu, 
                                       text="📷 Imagem não encontrada",
                                       font=("Arial", 16))
                    placeholder.pack(pady=30)
                self.botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
                self.botao_voltar.pack(pady=20)
                
                return
            
            elif consumo==gasto_estimado:
                try:
                    self.label_aviso.configure(text=f"Seu gasto({consumo}) foi igual ao ideal.Bom desempenho,mas vamos melhorar!!",text_color="#1A73E8")
                    imagem = Image.open("fotos/mascoteprincipall.png")
                    ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(200, 200))
                    label = ctk.CTkLabel(self.frameprincipal_menu, image=ctk_imagem, text="")
                    label.pack()
                except:
                    placeholder = ctk.CTkLabel(self.frameprincipal_menu, 
                                       text="📷 Imagem não encontrada",
                                       font=("Arial", 16))
                    placeholder.pack(pady=30)
                self.botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
                self.botao_voltar.pack(pady=20)
                return
                

            else:
                try:
                    self.label_aviso.configure(text=f"Seu gasto({consumo}) foi abaixo do ideal({gasto_estimado}L).Parabénsss!!!",text_color="green")
                    imagem = Image.open("fotos/mascotefeliz.jpg")
                    ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(200, 200))
                    label = ctk.CTkLabel(self.frameprincipal_menu, image=ctk_imagem, text="")
                    label.pack()
                except:
                    self.label_aviso.configure(text=f"Seu gasto({consumo}) foi abaixo do ideal.Parabénsss!!",text_color="green")
                    placeholder = ctk.CTkLabel(self.frameprincipal_menu, 
                                       text="📷 Imagem não encontrada",
                                       font=("Arial", 16))
                    placeholder.pack(pady=30)
                self.botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
                self.botao_voltar.pack(pady=20)
                    
                
            
        elif calculo_realizado==False:
            consumo=dados_consumo[self.email]
            qpessoas=dados_quantidade[self.email]
            gasto_estimado=qpessoas*30*110
            if consumo>gasto_estimado:
                try:
                    self.label_aviso.configure(text=f"Seu gasto({consumo}L) foi acima do ideal({gasto_estimado}L).Vamos melhorar!!",text_color="Red")
                    imagem = Image.open("fotos/mascotetriste.jpg")
                    ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(200, 200))
                    label = ctk.CTkLabel(self.frameprincipal_menu, image=ctk_imagem, text="")
                    label.pack()
                except:
                    placeholder = ctk.CTkLabel(self.frameprincipal_menu, 
                                       text="📷 Imagem não encontrada",
                                       font=("Arial", 16))
                    placeholder.pack(pady=30)
                self.botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
                self.botao_voltar.pack(pady=20)
                
                return
            
            elif consumo==gasto_estimado:
                try:
                    self.label_aviso.configure(text=f"Seu gasto({consumo}) foi igual ao ideal.Bom desempenho,mas vamos melhorar!!",text_color="#1A73E8")
                    imagem = Image.open("fotos/mascoteprincipall.png")
                    ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(200, 200))
                    label = ctk.CTkLabel(self.frameprincipal_menu, image=ctk_imagem, text="")
                    label.pack()
                except:
                    placeholder = ctk.CTkLabel(self.frameprincipal_menu, 
                                       text="📷 Imagem não encontrada",
                                       font=("Arial", 16))
                    placeholder.pack(pady=30)
                
                self.botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
                self.botao_voltar.pack(pady=20)
                return
                

            else:
                try:
                    self.label_aviso.configure(text=f"Seu gasto({consumo}) foi abaixo do ideal({gasto_estimado}L).Parabénsss!!\nVocê ganhou 100 pontos!!",text_color="green")
                    imagem = Image.open("fotos/mascotefeliz.jpg")
                    ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(200, 200))
                    label = ctk.CTkLabel(self.frameprincipal_menu, image=ctk_imagem, text="")
                    label.pack()
                except:
                    self.label_aviso.configure(text=f"Seu gasto({consumo}) foi abaixo do ideal.Parabénsss!!\nVocê ganhou 100 pontos!!",text_color="green")
                    placeholder = ctk.CTkLabel(self.frameprincipal_menu, 
                                       text="📷 Imagem não encontrada",
                                       font=("Arial", 16))
                    placeholder.pack(pady=30)

                
                    
                dados_pontos[self.email]+=100
                with open(r"banco_dados.JSON", "w", encoding="utf-8") as arquivo:
                # Aqui, estamos criando um dicionário com duas chaves:
                    json.dump({"senha": dados_conta, "familia": dados_familia, "membros": dados_quantidade, "pontos": dados_pontos,
                           "apartamento": dados_apartamento, "verificador": dados_codigov}, arquivo, indent=4, ensure_ascii=False)

                dados_calculo[self.email]=True
                with open(r"dados_usuarios.json", "w", encoding="utf-8") as arquivo:
                # Aqui, estamos criando um dicionário com duas chaves:
                    json.dump({"calculo_realizado":dados_calculo,"consumo":dados_consumo}, arquivo, indent=4, ensure_ascii=False)
                
                self.botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
                self.botao_voltar.pack(pady=20)

                return
            
            



    def quiz_semanal(self):
            """🧠 Função: Quiz Semanal - Disponibiliza 5 questões toda segunda-feira. Dependendo do desempenho, o usuário recebe pontos."""
            self.limpar_frame_principal()
            label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="🧠 Quiz Semanal",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
            label_titulo.pack(pady=(20, 10))

            hoje = datetime.now()
            if hoje.weekday() != 0:  # 0 = Monday
                ctk.CTkLabel(self.frameprincipal_menu, text="O quiz semanal só está disponível às segundas-feiras.",
                     font=("Arial", 14), text_color="#5f6368").pack(pady=50)
                ctk.CTkLabel(self.frameprincipal_menu, text="Volte na próxima segunda-feira para participar!",
                     font=("Arial", 12), text_color="orange").pack(pady=10)
                botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
                botao_voltar.pack(pady=20)
                return

    # Impede refazer o quiz na mesma segunda-feira
            global dados_ultimo_quiz
            ultima_data = dados_ultimo_quiz.get(self.email)
            if ultima_data == hoje.strftime("%Y-%m-%d"):
                ctk.CTkLabel(self.frameprincipal_menu, text="Você já participou do quiz desta semana!",
                     font=("Arial", 14), text_color="orange").pack(pady=50)
                botao_voltar = ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white",
                                     command=self.reset_principal_menu_content)
                botao_voltar.pack(pady=20)
                return

    # Seleciona 5 perguntas aleatórias do banco
            perguntas = random.sample(dados_questoes_quiz, 5)
            self.quiz_perguntas = perguntas
            self.quiz_respostas = []
            self.quiz_indice = 0
            self.quiz_pontos = 0

            def mostrar_pergunta():
                for widget in self.frameprincipal_menu.winfo_children():
                    if widget != label_titulo:
                        widget.destroy()
                pergunta = self.quiz_perguntas[self.quiz_indice]
                ctk.CTkLabel(self.frameprincipal_menu, text=f"Pergunta {self.quiz_indice+1} de 5",
                     font=("Arial", 14, "bold"), text_color="#1A73E8").pack(pady=(10, 5))
                ctk.CTkLabel(self.frameprincipal_menu, text=pergunta["pergunta"],
                     font=("Arial", 14), text_color="#333333", wraplength=500).pack(pady=10)
                var_resposta = ctk.StringVar()
                for alt in pergunta["alternativas"]:
                    ctk.CTkRadioButton(self.frameprincipal_menu, text=alt, variable=var_resposta, value=alt).pack(anchor="w", padx=50)
                def responder():
                    resposta = var_resposta.get()
                    if not resposta:
                        return
                    self.quiz_respostas.append(resposta)
                    if resposta == pergunta["correta"]:
                        self.quiz_pontos += 1
                    self.quiz_indice += 1
                    if self.quiz_indice < 5:
                        mostrar_pergunta()
                    else:
                        mostrar_resultado()
                ctk.CTkButton(self.frameprincipal_menu, text="Responder", fg_color="#1A73E8", text_color="white", command=responder).pack(pady=20)

            def mostrar_resultado(self):
                for widget in self.frameprincipal_menu.winfo_children():
                    if widget != label_titulo:
                        widget.destroy()
                pontos_ganhos = self.quiz_pontos * 20  # Exemplo: 20 pontos por acerto
                global dados_pontos
                dados_pontos[self.email] = dados_pontos.get(self.email, 0) + pontos_ganhos
        # Atualiza banco de dados
                try:
                    with open(r"banco_dados.JSON", "r+", encoding="utf-8") as f:
                        data = json.load(f)
                        data["pontos"][self.email] = dados_pontos[self.email]
                        data.setdefault("ultimo_quiz", {})[self.email] = hoje.strftime("%Y-%m-%d")
                        f.seek(0)
                        json.dump(data, f, indent=4, ensure_ascii=False)
                        f.truncate()
                except Exception as e:
                    ctk.CTkLabel(self.frameprincipal_menu, text=f"Erro ao salvar pontos: {e}", text_color="red").pack()
                ctk.CTkLabel(self.frameprincipal_menu, text=f"Você acertou {self.quiz_pontos} de 5 perguntas!\nPontos ganhos: {pontos_ganhos}",
                     font=("Arial", 16, "bold"), text_color="#28a745").pack(pady=30)
                ctk.CTkButton(self.frameprincipal_menu, text="⬅ Voltar ao Menu",
                      fg_color="gray", text_color="white",
                      command=self.reset_principal_menu_content).pack(pady=20)

            mostrar_pergunta()


    def area_educativa(self):
        """📘 Função: Área Educativa - Exibe conteúdo educativo sobre sustentabilidade e conservação da água."""
        self.limpar_frame_principal()

        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="📘 Área Educativa",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        # Scroll como atributo da classe
        self.scroll_frame = ctk.CTkScrollableFrame(self.frameprincipal_menu, width=600, height=400,fg_color="#ffffff")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Botões locais (sem self)
        botao_areaedu1 = ctk.CTkButton(self.scroll_frame,
            text="Europa investe €15 bilhões em preservação de recursos hídricos até 2027",
            fg_color="white", text_color="#1A73E8", font=("Arial", 12), anchor="w",
            command=self.mostrar_artigo1)
        botao_areaedu1.pack(fill="x", pady=5, padx=10)

        botao_areaedu2 = ctk.CTkButton(self.scroll_frame,
            text="Cientistas desenvolvem tecnologia para extrair água potável do ar usando resíduos alimentares",
            fg_color="white", text_color="#1A73E8", font=("Arial", 12), anchor="w",
            command=self.mostrar_artigo2)
        botao_areaedu2.pack(fill="x", pady=5, padx=10)

        botao_areaedu3 = ctk.CTkButton(self.scroll_frame,
            text="Universidade do Texas inicia construção do maior centro universitário de reúso de água dos EUA",
            fg_color="white", text_color="#1A73E8", font=("Arial", 12), anchor="w",
            command=self.mostrar_artigo3)
        botao_areaedu3.pack(fill="x", pady=5, padx=10)

        botao_areaedu4 = ctk.CTkButton(self.scroll_frame,
            text="Alunos serão instruídos sobre conservação da água e limpeza do rio Ganges na Índia",
            fg_color="white", text_color="#1A73E8", font=("Arial", 12), anchor="w",
            command=self.mostrar_artigo4)
        botao_areaedu4.pack(fill="x", pady=5, padx=10)

        botao_areaedu5 = ctk.CTkButton(self.scroll_frame,
            text="Impacto dos datacenters em áreas com escassez hídrica na América Latina",
            fg_color="white", text_color="#1A73E8", font=("Arial", 12), anchor="w",
            command=self.mostrar_artigo5)
        botao_areaedu5.pack(fill="x", pady=5, padx=10)

        botao_areaedu6 = ctk.CTkButton(self.scroll_frame,
            text="8 filmes educativos para crianças sobre sustentabilidade",
            fg_color="white", text_color="#1A73E8", font=("Arial", 12), anchor="w",
            command=self.mostrar_artigo6)
        botao_areaedu6.pack(fill="x", pady=5, padx=10)

        botao_voltar = ctk.CTkButton(self.scroll_frame, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=self.reset_principal_menu_content)
        botao_voltar.pack(pady=20)

    
    def mostrar_artigo1(self):

        # Limpa o conteúdo anterior do scroll_frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Título da notícia
        titulo = ctk.CTkLabel(
            self.scroll_frame,
            text="🌍 Investimento de €15 bilhões para combater a crise hídrica na Europa",
            text_color="#1A73E8",
            font=("Arial", 20, "bold"),
            wraplength=500,
            justify="left"
        )
        titulo.pack(pady=(20, 10), padx=10)

        # Corpo do texto
        corpo_texto = (
            "A Universidade Europeia e o Banco Europeu de Investimento anunciaram, em 7 de junho, "
            "um aporte de €15 bilhões (≈US$17bi) a projetos voltados à redução da poluição, "
            "prevenção do desperdício e fomento à inovação no setor hídrico ao longo dos próximos três anos. "
            "A ação considera a intensificação das secas e pressões agrícolas e urbanas causadas pelas mudanças climáticas. "
            "Como medida de responsabilização, o Reino Unido restringiu bônus a executivos de empresas de água que não investem "
            "o suficiente na qualidade dos corpos de água."
        )

        label_corpo = ctk.CTkLabel(
            self.scroll_frame,
            text=corpo_texto,
            font=("Arial", 16),
            wraplength=500,
            justify="left"
        )
        label_corpo.pack(padx=10, pady=(0, 20))

        # Botão Voltar
        botao_voltar = ctk.CTkButton(
            self.scroll_frame,
            text="Voltar",
            command=self.area_educativa,
            fg_color="#1A73E8",  
            hover_color="#12496D",
            font=("Arial", 14, "bold")
        )
        botao_voltar.pack(pady=(0, 20))

    def mostrar_artigo2(self):
        # Limpa o conteúdo anterior do scroll_frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Título da notícia
        titulo = ctk.CTkLabel(
            self.scroll_frame,
            text="🎒 Extração de água potável do ar usando alimentos",
            text_color="#1A73E8",
            font=("Arial", 20, "bold"),
            wraplength=500,
            justify="left"
        )
        titulo.pack(pady=(20, 10), padx=10)

        # Corpo do texto
        corpo_texto = (
            "Pesquisadores da Universidade do Texas em Austin publicaram, em abril, um método inovador para captar água do ar "
            "usando hidrogéis feitos com biomassa de resíduos alimentares e conchas. Esses materiais absorvem grandes volumes "
            "de umidade e liberam água pura com aquecimento leve. Em campo, foram obtidos 15L de água por kg de gel por dia—"
            "recuperando 95% do volume captado."
        )

        label_corpo = ctk.CTkLabel(
            self.scroll_frame,
            text=corpo_texto,
            text_color="#333333",
            font=("Arial", 14),
            wraplength=500,
            justify="left"
        )
        label_corpo.pack(padx=10, pady=10)

        # Destaque: Impacto prático
        label_importancia = ctk.CTkLabel(
            self.scroll_frame,
            text="💡 Impacto prático:",
            text_color="#1A73E8",
            font=("Arial", 20, "bold"),
            wraplength=500,
            justify="left"
        )
        label_importancia.pack(pady=(20, 5), padx=10)

        texto_importancia = (
            "Trata-se de uma solução biodegradável, modular e de baixo consumo energético — ideal para comunidades rurais, "
            "irrigação localizada ou situações emergenciais em áreas carentes de infraestrutura hídrica."
        )

        label_importancia_texto = ctk.CTkLabel(
            self.scroll_frame,
            text=texto_importancia,
            font=("Arial", 14),
            wraplength=500,
            justify="left"
        )
        label_importancia_texto.pack(padx=10, pady=(0, 20))

        # Botão Voltar
        botao_voltar = ctk.CTkButton(
            self.scroll_frame,
            text="Voltar",
            command=self.area_educativa,
            fg_color="#1A73E8",  
            hover_color="#12496D",
            font=("Arial", 14, "bold")
        )
        botao_voltar.pack(pady=(0, 20))

    def mostrar_artigo3(self):
        # Limpa o conteúdo anterior do scroll_frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Título da notícia
        titulo = ctk.CTkLabel(
            self.scroll_frame,
            text="🏗️ UT Austin constrói o maior centro universitário de reúso de água nos EUA",
            text_color="#1A73E8",
            font=("Arial", 20, "bold"),
            wraplength=500,
            justify="left"
        )
        titulo.pack(pady=(20, 10), padx=10)

        # Corpo do texto
        corpo_texto = (
            "Em maio, a UT anunciou a construção do WaterHub, instalação de 900m² que vai tratar até 1 milhão de galões "
            "(≈3,8 mil m³) de esgoto por dia. A previsão de operação é para o segundo semestre de 2027. O local servirá como laboratório "
            "de pesquisa prática para estudantes, integrando ensino e teste de tecnologias de reúso para aliviar sistemas municipais sobrecarregados."
        )

        label_corpo = ctk.CTkLabel(
            self.scroll_frame,
            text=corpo_texto,
            text_color="#333333",
            font=("Arial", 14),
            wraplength=500,
            justify="left"
        )
        label_corpo.pack(padx=10, pady=10)

        # Destaque: Por que isso importa?
        label_importancia = ctk.CTkLabel(
            self.scroll_frame,
            text="💡 Por que isso importa?",
            text_color="#1A73E8",
            font=("Arial", 20, "bold"),
            wraplength=500,
            justify="left"
        )
        label_importancia.pack(pady=(20, 5), padx=10)

        texto_importancia = (
            "Esse centro universitário vai impulsionar a pesquisa e o desenvolvimento de tecnologias inovadoras de reúso de água, "
            "contribuindo para a sustentabilidade urbana e formação técnica avançada."
        )

        label_importancia_texto = ctk.CTkLabel(
            self.scroll_frame,
            text=texto_importancia,
            font=("Arial", 14),
            wraplength=500,
            justify="left"
        )
        label_importancia_texto.pack(padx=10, pady=(0, 20))

        # Botão Voltar
        botao_voltar = ctk.CTkButton(
            self.scroll_frame,
            text="Voltar",
            command=self.area_educativa,
            fg_color="#1A73E8",  
            hover_color="#12496D",
            font=("Arial", 14, "bold")
        )
        botao_voltar.pack(pady=(0, 20))

    def mostrar_artigo4(self):
        # Limpa o conteúdo anterior do scroll_frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Título
        titulo = ctk.CTkLabel(
            self.scroll_frame,
            text="📰 Educação Ambiental na Índia: Estudantes de Uttar Pradesh se tornam embaixadores da limpeza",
            text_color="#1A73E8",
            font=("Arial", 20, "bold"),
            wraplength=500,
            justify="left"
        )
        titulo.pack(pady=(20, 10), padx=10)

        # Parágrafo da notícia
        corpo_texto = (
            "Em junho de 2024, o governo do estado de Uttar Pradesh, na Índia, lançou uma iniciativa educativa para envolver os alunos "
            "das escolas públicas e privadas na conservação ambiental e limpeza do rio Ganges, um dos maiores e mais sagrados rios da Ásia. "
            "O programa inclui formação de “embaixadores estudantis da limpeza”, práticas de higiene e conservação hídrica, visitas a locais "
            "poluídos, plantio de árvores, redações, campanhas ambientais e integração da comunidade escolar e familiar."
        )
        label_corpo = ctk.CTkLabel(
            self.scroll_frame,
            text=corpo_texto,
            text_color="#333333",
            font=("Arial", 14),
            wraplength=500,
            justify="left"
        )
        label_corpo.pack(padx=10, pady=10)

        # Destaque: Por que isso importa?
        label_importancia = ctk.CTkLabel(
            self.scroll_frame,
            text="💡 Por que isso importa?",
            text_color="#1A73E8",
            font=("Arial", 20, "bold"),
            wraplength=500,
            justify="left"
        )
        label_importancia.pack(pady=(20, 5), padx=10)

        texto_importancia = (
            "A iniciativa ajuda a sensibilizar jovens sobre a conservação hídrica e atitudes sustentáveis desde cedo, "
            "envolvendo também suas famílias e escolas, o que pode gerar impacto real na limpeza do Ganges e na formação de cidadãos conscientes."
        )

        label_texto_importancia = ctk.CTkLabel(
            self.scroll_frame,
            text=texto_importancia,
            text_color="#000000",
            font=("Arial", 14),
            wraplength=500,
            justify="left"
        )
        label_texto_importancia.pack(padx=10, pady=5)

        # Fontes
        label_fontes = ctk.CTkLabel(
            self.scroll_frame,
            text="🔗 Fontes:",
            text_color="#1A73E8",
            font=("Arial", 14, "bold"),
            wraplength=500,
            justify="left"
        )
        label_fontes.pack(pady=(20, 5), padx=10)

        lbl = ctk.CTkLabel(
            self.scroll_frame,
            text="• timesofindia.indiatimes.com",
            text_color="#333333",
            font=("Arial", 13),
            anchor="w",
            justify="left"
        )
        lbl.pack(padx=10)

        # Botão Voltar
        botao_voltar = ctk.CTkButton(
            self.scroll_frame,
            text="Voltar",
            command=self.area_educativa,
            fg_color="#1A73E8",
            hover_color="#12496D",
            font=("Arial", 14, "bold")
        )
        botao_voltar.pack(pady=(0, 20))

    def mostrar_artigo5(self):
        # Limpa o conteúdo anterior do scroll_frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Título
        titulo = ctk.CTkLabel(
            self.scroll_frame,
            text="📰 Impacto dos datacenters em áreas com escassez hídrica na América Latina",
            text_color="#1A73E8",
            font=("Arial", 20, "bold"),
            wraplength=500,
            justify="left"
        )
        titulo.pack(pady=(20, 10), padx=10)

        # Parágrafo da notícia
        corpo_texto = (
            "Um artigo do The Guardian chama atenção para a instalação de grandes datacenters em regiões "
            "com escassez de água no Brasil e outros países da América Latina. Um dos casos citados em Caucaia (CE) "
            "está em regiões afetadas por seca, e esses centros utilizam até 80 % da água retirada para resfriamento, "
            "gerando riscos de esgotamento de recursos hídricos locais. O texto destaca a necessidade de maior transparência, "
            "engajamento comunitário e uso de alternativas como dessalinização e reúso."
        )

        label_corpo = ctk.CTkLabel(
            self.scroll_frame,
            text=corpo_texto,
            text_color="#333333",
            font=("Arial", 14),
            wraplength=500,
            justify="left"
        )
        label_corpo.pack(padx=10, pady=10)

        # Destaque: Por que isso importa?
        label_importancia = ctk.CTkLabel(
            self.scroll_frame,
            text="💡 Por que isso importa?",
            text_color="#1A73E8",
            font=("Arial", 20, "bold"),
            wraplength=500,
            justify="left"
        )
        label_importancia.pack(pady=(20, 5), padx=10)

        texto_importancia = (
            "Educação ambiental sobre impactos tecnológicos no ciclo da água.\n\n"
            "Inovação na busca por soluções de resfriamento menos dependentes de água.\n\n"
            "Reflexão sobre políticas de concessão hídrica e planejamento sustentável."
        )

        label_texto_importancia = ctk.CTkLabel(
            self.scroll_frame,
            text=texto_importancia,
            text_color="#000000",
            font=("Arial", 14),
            wraplength=500,
            justify="left"
        )
        label_texto_importancia.pack(padx=10, pady=5)

        # Fontes
        label_fontes = ctk.CTkLabel(
            self.scroll_frame,
            text="🔗 Fontes:",
            text_color="#1A73E8",
            font=("Arial", 14, "bold"),
            wraplength=500,
            justify="left"
        )
        label_fontes.pack(pady=(20, 5), padx=10)

        lbl = ctk.CTkLabel(
            self.scroll_frame,
            text="• theguardian.com",
            text_color="#333333",
            font=("Arial", 13),
            anchor="w",
            justify="left"
        )
        lbl.pack(padx=10)

        # Botão Voltar
        botao_voltar = ctk.CTkButton(
            self.scroll_frame,
            text="Voltar",
            command=self.area_educativa,
            fg_color="#1A73E8",
            hover_color="#12496D",
            font=("Arial", 14, "bold")
        )
        botao_voltar.pack(pady=(0, 20))

    def mostrar_artigo6(self):
        # Limpa o conteúdo anterior do scroll_frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Título
        titulo = ctk.CTkLabel(
            self.scroll_frame,
            text="🌿 8 Filmes sobre Sustentabilidade para Crianças",
            text_color="#1A73E8",
            font=("Arial", 16, "bold"),  # fonte menor
            wraplength=500,
            justify="left"
        )
        titulo.pack(pady=(10, 5), padx=10)

        # Lista dos filmes com mini-resumos (sem "A Fuga das Galinhas", com "Avatar" incluído)
        filmes = [
            ("Wall-E (2008)", "Um clássico da Pixar! Mostra um futuro onde a Terra foi tomada pelo lixo e a humanidade vive no espaço. Wall-E, um robô solitário, nos ensina sobre consumo, lixo e amor pelo planeta."),
            ("Lorax: Em Busca da Trúfula Perdida (2012)", "Baseado na obra do Dr. Seuss, aborda desmatamento e exploração de recursos naturais, com personagens carismáticos e músicas cativantes."),
            ("Happy Feet: O Pinguim (2006)", "Através de um pinguim dançarino, o filme aborda temas como mudança climática, preservação dos oceanos e o impacto da pesca predatória."),
            ("Rio (2011)", "Além da aventura, mostra a importância da biodiversidade brasileira e os perigos do tráfico de animais silvestres."),
            ("Irmão Urso (Brother Bear) (2003)", "Aborda o respeito à natureza, ao ciclo da vida e à conexão espiritual com o meio ambiente, com forte mensagem sobre empatia e equilíbrio natural."),
            ("O Rei Leão (1994 / 2019)", "Apesar de não focar diretamente em sustentabilidade, ensina sobre o “ciclo da vida” e o equilíbrio ecológico da savana africana."),
            ("Meu Amigo Totoro (1988)", "Um clássico do Studio Ghibli. Exalta a harmonia entre seres humanos e natureza, com um toque mágico e poético."),
            ("Avatar (2009)", "Conta a história de um ex-fuzileiro que, ao interagir com o povo Na'vi e a natureza de Pandora, aprende a importância do equilíbrio ecológico e respeito ao meio ambiente.")
        ]

        # Exibe os filmes e seus resumos
        #titulo_filme=primeiro elemento da tupla
        #resumo=segundo elemento da tupla
        for titulo_filme, resumo in filmes:
            label_filme = ctk.CTkLabel(
                self.scroll_frame,
                text=f"• {titulo_filme}\n  {resumo}",
                text_color="#333333",
                font=("Arial", 14),
                wraplength=500,
                justify="left"
            )
            label_filme.pack(pady=(5, 10), padx=20)

        # Botão Voltar
        botao_voltar = ctk.CTkButton(
            self.scroll_frame,
            text="Voltar",
            command=self.area_educativa,
            fg_color="#1A73E8",
            hover_color="#12496D",
            font=("Arial", 14, "bold")
        )
        botao_voltar.pack(pady=(10, 20))

    

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
        """🔄 Função: Atualizar Dados - Permite ao usuário atualizar o nome da família, quantidade de membros, email, número do apartamento e senha."""
        self.limpar_frame_principal()

        label_titulo = ctk.CTkLabel(self.frameprincipal_menu, text="🔄 Atualizar Dados",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
        label_titulo.pack(pady=(20, 10))

        global dados_familia, dados_quantidade, dados_conta, dados_apartamento
        nome_atual = dados_familia.get(self.email, "")
        membros_atuais = dados_quantidade.get(self.email, "")
        apartamento_atual = dados_apartamento.get(self.email, "")
        email_atual = self.email

        ctk.CTkLabel(self.frameprincipal_menu, text="Preencha os campos que deseja atualizar:",
                 font=("Arial", 14), text_color="#333333").pack(pady=(0, 10))

    # Campo Email
        label_email = ctk.CTkLabel(self.frameprincipal_menu, text="Novo Email:",
                               font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
        label_email.pack(fill="x", padx=50, pady=(10, 0))
        self.entrada_email = ctk.CTkEntry(self.frameprincipal_menu, width=300)
        self.entrada_email.insert(0, email_atual)
        self.entrada_email.pack(padx=50, pady=(0, 10))

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

    # Campo Número do Apartamento
        label_apartamento = ctk.CTkLabel(self.frameprincipal_menu, text="Número do Apartamento:",
                                     font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
        label_apartamento.pack(fill="x", padx=50, pady=(10, 0))
        self.entrada_apartamento = ctk.CTkEntry(self.frameprincipal_menu, width=300)
        self.entrada_apartamento.insert(0, str(apartamento_atual))
        self.entrada_apartamento.pack(padx=50, pady=(0, 10))

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
        novo_email = self.entrada_email.get().strip()
        novo_nome = self.entrada_nome_familia.get().strip()
        nova_qtde_membros_str = self.entrada_membros.get().strip()
        novo_apartamento = self.entrada_apartamento.get().strip()
        nova_senha = self.entrada_nova_senha.get().strip()

        if not novo_email or not novo_nome or not nova_qtde_membros_str or not novo_apartamento:
            self.label_mensagem_atualizar.configure(text="Todos os campos exceto senha são obrigatórios.", text_color="red")
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

            # Se o email mudou, precisamos transferir todos os dados para o novo email
                if novo_email != self.email:
                # Verifica se o novo email já existe
                    if novo_email in data["senha"]:
                        self.label_mensagem_atualizar.configure(text="Este email já está cadastrado.", text_color="red")
                        return
                # Move todos os dados para o novo email
                    for key in ["senha", "familia", "membros", "pontos", "apartamento", "verificador"]:
                        if self.email in data.get(key, {}):
                            data[key][novo_email] = data[key].pop(self.email)
                # Atualiza campos com os novos valores
                    data["familia"][novo_email] = novo_nome
                    data["membros"][novo_email] = nova_qtde_membros
                    data["apartamento"][novo_email] = novo_apartamento
                    if nova_senha:
                        data["senha"][novo_email] = nova_senha
                # Atualiza variáveis globais
                    self.email = novo_email
                else:
                    data["familia"][self.email] = novo_nome
                    data["membros"][self.email] = nova_qtde_membros
                    data["apartamento"][self.email] = novo_apartamento
                    if nova_senha:
                        data["senha"][self.email] = nova_senha

            # Atualiza variáveis globais
                dados_familia[self.email] = novo_nome
                dados_quantidade[self.email] = nova_qtde_membros
                dados_apartamento[self.email] = novo_apartamento
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
        self.entrada_feedback.pack(padx=50, pady=(0, 10), anchor="w")

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



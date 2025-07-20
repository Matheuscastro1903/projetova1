import customtkinter as ctk
from customtkinter import CTkImage, CTkLabel

from PIL import Image
import json
import csv
import time
import random
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

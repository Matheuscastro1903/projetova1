# main_app.py
import customtkinter as ctk
import json
import time
import re
import random
import os
import sys
import datetime
import csv # Importado para a função de salvar feedback em CSV
from tkinter import messagebox # Import messagebox for GUI alerts
import pyfiglet # Para o banner ASCII

# ==================================================================================================
# --- Configurações Iniciais CustomTkinter e Variáveis Globais ---
# ==================================================================================================
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

# Nomes de arquivos JSON e CSV
NOME_ARQUIVO_BANCO_DADOS = "banco_dados.JSON"
NOME_ARQUIVO_DADOS_USUARIOS = "dados_usuarios.json"
NOME_ARQUIVO_FEEDBACK_CSV = "feedback.csv"
NOME_ARQUIVO_QUESTOES_QUIZ = "questoes_agua.json"

# Mensagens diárias de economia de água (usadas no menu)
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

# ==================================================================================================
# --- Funções Auxiliares Comuns ---
# ==================================================================================================

def limpar_tela():
    """
    Função para simular a limpeza de tela em um ambiente de terminal.
    Em uma GUI, esta função não é diretamente utilizada para limpar o console,
    mas pode ser adaptada para atualizar o conteúdo da interface, se necessário.
    """
    # os.system('cls' if os.name == 'nt' else 'clear') # Descomente se quiser limpar o console real
    pass # Não faz nada na GUI, pois a interface é gerenciada por frames

def barra_progresso():
    """
    Simula uma barra de progresso. Em uma GUI, idealmente seria substituída por
    um widget CTkProgressBar ou feedback visual similar.
    """
    # Em uma GUI real, você animaria um CTkProgressBar aqui.
    # Por simplicidade e para manter a compatibilidade com a ideia original, apenas uma pausa.
    time.sleep(0.5)

def gerar_codigo_resgate():
    """
    Gera um código de resgate alfanumérico e o exibe em uma caixa de mensagem.
    """
    letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    numeros = ''.join(random.choices('0123456789', k=4))
    codigo = f"{letras}-{numeros}"
    messagebox.showinfo("Código de Resgate", f"Seu código para resgatar a recompensa:\n{codigo}")
    return codigo

def carregar_json(filepath):
    """
    Carrega dados de um arquivo JSON. Lida com FileNotFoundError e JSONDecodeError.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Erro de Arquivo", f"Arquivo '{filepath}' não encontrado. Por favor, crie-o ou verifique o caminho.")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("Erro de Leitura", f"Erro ao ler JSON de '{filepath}'. O arquivo pode estar corrompido ou vazio.")
        return {}
    except Exception as e:
        messagebox.showerror("Erro Desconhecido", f"Ocorreu um erro inesperado ao carregar '{filepath}': {e}")
        return {}

def salvar_json(data, filepath):
    """
    Salva dados em um arquivo JSON. Inclui uma barra de progresso simulada.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        barra_progresso() # Pode ser substituída por uma barra de progresso visual
        return True
    except Exception as e:
        messagebox.showerror("Erro de Escrita", f"Não foi possível salvar em '{filepath}': {e}")
        return False

# ==================================================================================================
# --- Classe Principal do Aplicativo (Gerenciamento de Telas) ---
# ==================================================================================================

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ECODROP - Condomínio Village")
        self.geometry("800x700") # Tamanho da janela principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.email_logado = None
        # self.senha_logada = None # Guardar a senha em memória não é ideal por segurança, mas mantido para compatibilidade com funções existentes

        self._carregar_todos_dados() # Carrega todos os dados necessários ao iniciar o app

        self._configurar_tela_inicial() # Configura a tela inicial (login/cadastro)

    def _carregar_todos_dados(self):
        """Carrega todos os dados de arquivos JSON e garante que as estruturas existam."""
        self.banco_dados = carregar_json(NOME_ARQUIVO_BANCO_DADOS)
        self.dados_usuarios = carregar_json(NOME_ARQUIVO_DADOS_USUARIOS)

        # Inicializa seções que podem faltar no banco_dados.JSON
        if "senha" not in self.banco_dados: self.banco_dados["senha"] = {}
        if "familia" not in self.banco_dados: self.banco_dados["familia"] = {}
        if "membros" not in self.banco_dados: self.banco_dados["membros"] = {}
        if "pontos" not in self.banco_dados: self.banco_dados["pontos"] = {}
        if "apartamento" not in self.banco_dados: self.banco_dados["apartamento"] = {}
        if "verificador" not in self.banco_dados: self.banco_dados["verificador"] = {}
        if "feedback" not in self.banco_dados: self.banco_dados["feedback"] = []
        if "usuarios" not in self.banco_dados: self.banco_dados["usuarios"] = {}

        # Inicializa seções que podem faltar no dados_usuarios.json
        if "consumo" not in self.dados_usuarios: self.dados_usuarios["consumo"] = {}
        if "calculo_realizado" not in self.dados_usuarios: self.dados_usuarios["calculo_realizado"] = {}

    def _configurar_tela_inicial(self):
        """Cria e exibe a tela de boas-vindas com opções de Login/Cadastro."""
        self.frame_boas_vindas = ctk.CTkFrame(self)
        self.frame_boas_vindas.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame_boas_vindas.grid_rowconfigure((0,1,2,3), weight=1)
        self.frame_boas_vindas.grid_columnconfigure(0, weight=1)

        ascii_banner = pyfiglet.figlet_format("ECODROP")
        ctk.CTkLabel(self.frame_boas_vindas, text=ascii_banner, font=("Courier New", 24, "bold")).grid(row=0, column=0, pady=(20,0))
        ctk.CTkLabel(self.frame_boas_vindas, text="OLÁ, BEM VINDO AO SISTEMA ECODROP💧 do condomínio Village", font=("Arial", 18)).grid(row=1, column=0, pady=10)

        ctk.CTkButton(self.frame_boas_vindas, text="Login", command=self._mostrar_tela_login, font=("Arial", 16)).grid(row=2, column=0, pady=10)
        ctk.CTkButton(self.frame_boas_vindas, text="Cadastre-se", command=self._mostrar_tela_cadastro, font=("Arial", 16)).grid(row=3, column=0, pady=10)

    def _mostrar_tela_login(self):
        """Simula a tela de login e redireciona para o menu se bem-sucedido."""
        # TODO: Implementar a lógica de login real aqui, com validação de credenciais
        # Por simplicidade, vamos direto para o menu com um usuário de teste fixo.
        email_teste = "teste@email.com"
        # Adicionar um usuário de teste ao banco_dados se não existir
        if email_teste not in self.banco_dados["senha"]:
            self.banco_dados["senha"][email_teste] = "senha123"
            self.banco_dados["familia"][email_teste] = "Família Teste"
            self.banco_dados["membros"][email_teste] = 3
            self.banco_dados["pontos"][email_teste] = 100
            self.banco_dados["apartamento"][email_teste] = 101
            self.banco_dados["verificador"][email_teste] = "VERIF"
            salvar_json(self.banco_dados, NOME_ARQUIVO_BANCO_DADOS)

        if email_teste in self.banco_dados["senha"]:
            self.email_logado = email_teste
            # self.senha_logada = self.banco_dados["senha"].get(email_teste) # Em um app real, não armazenaríamos a senha assim.
            messagebox.showinfo("Login", f"Login bem-sucedido como {self.email_logado} (usuário de teste).")
            self._mostrar_tela_menu()
        else:
            messagebox.showerror("Erro de Login", "Usuário de teste 'teste@email.com' não encontrado no banco de dados. Verifique 'banco_dados.JSON' ou crie uma conta.")
            # Poderia abrir uma tela de login real aqui.

    def _mostrar_tela_cadastro(self):
        """Simula a tela de cadastro e redireciona para o menu após 'cadastro'."""
        # TODO: Implementar a lógica de cadastro real aqui.
        messagebox.showinfo("Cadastro", "Simulando Cadastro. Redirecionando para o menu principal após 'cadastro'.")
        self._mostrar_tela_menu() # Para fins de demonstração

    def _mostrar_tela_menu(self):
        """Exibe o menu principal do aplicativo, escondendo a tela anterior."""
        # Destruir todos os widgets da tela anterior
        for widget in self.winfo_children():
            widget.destroy()

        self.frame_menu = ctk.CTkFrame(self)
        self.frame_menu.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        # Configurar grid para alinhar botões
        self.frame_menu.grid_rowconfigure(list(range(12)), weight=1) # Ajuste o número de linhas conforme necessário
        self.frame_menu.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame_menu, text="BEM VINDO AO MENU PRINCIPAL DO ECODROP💧.", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=(20,10))
        ctk.CTkLabel(self.frame_menu, text=random.choice(mensagens_agua), font=("Arial", 14), wraplength=500).grid(row=1, column=0, pady=10)

        # Botões do Menu (cada um chama um método para exibir sua tela específica)
        ctk.CTkButton(self.frame_menu, text="1. Ver Ranking 🏆", command=self._mostrar_tela_ranking, font=("Arial", 16)).grid(row=2, column=0, pady=5, sticky="ew", padx=50)
        ctk.CTkButton(self.frame_menu, text="2. Calcular Pontos 💧", command=self._mostrar_tela_calculo_pontos, font=("Arial", 16)).grid(row=3, column=0, pady=5, sticky="ew", padx=50)
        ctk.CTkButton(self.frame_menu, text="3. Atualizar Dados 🔄", command=self._mostrar_tela_atualizar_dados, font=("Arial", 16)).grid(row=4, column=0, pady=5, sticky="ew", padx=50)
        ctk.CTkButton(self.frame_menu, text="4. Deletar Conta ❌", command=self._mostrar_tela_deletar_conta, font=("Arial", 16)).grid(row=5, column=0, pady=5, sticky="ew", padx=50)
        ctk.CTkButton(self.frame_menu, text="5. Enviar Feedback ✉️", command=self._mostrar_tela_feedback, font=("Arial", 16)).grid(row=6, column=0, pady=5, sticky="ew", padx=50)
        ctk.CTkButton(self.frame_menu, text="6. Resgatar Recompensas 🎁", command=self._mostrar_tela_resgatar_pontos, font=("Arial", 16)).grid(row=7, column=0, pady=5, sticky="ew", padx=50)
        ctk.CTkButton(self.frame_menu, text="7. Visualizar Dados 📊", command=self._mostrar_tela_visualizar_dados, font=("Arial", 16)).grid(row=8, column=0, pady=5, sticky="ew", padx=50)
        ctk.CTkButton(self.frame_menu, text="8. Jogar Quiz Semanal 💡", command=self._mostrar_tela_quiz, font=("Arial", 16)).grid(row=9, column=0, pady=5, sticky="ew", padx=50)
        ctk.CTkButton(self.frame_menu, text="9. Sair do Sistema 🚪", command=self.encerrar_app, font=("Arial", 16), fg_color="darkred", hover_color="red").grid(row=10, column=0, pady=5, sticky="ew", padx=50)

    # Métodos para exibir as telas modulares (instanciam e empacotam o CTkFrame)
    def _mostrar_tela_ranking(self):
        """Exibe a tela de Ranking."""
        self.frame_menu.destroy()
        TelaRanking(self, self.email_logado).pack(expand=True, fill="both")

    def _mostrar_tela_calculo_pontos(self):
        """Exibe a tela de Cálculo de Pontos."""
        self.frame_menu.destroy()
        TelaCalculoPontos(self, self.email_logado).pack(expand=True, fill="both")

    def _mostrar_tela_atualizar_dados(self):
        """Exibe a tela de Atualizar Dados."""
        self.frame_menu.destroy()
        TelaAtualizarDados(self, self.email_logado).pack(expand=True, fill="both")

    def _mostrar_tela_deletar_conta(self):
        """Exibe a tela de Deleção de Conta."""
        self.frame_menu.destroy()
        TelaDeletarConta(self, self.email_logado).pack(expand=True, fill="both")

    def _mostrar_tela_feedback(self):
        """Exibe a tela de Enviar Feedback."""
        self.frame_menu.destroy()
        TelaFeedback(self, self.email_logado).pack(expand=True, fill="both")

    def _mostrar_tela_resgatar_pontos(self):
        """Exibe a tela de Resgate de Recompensas."""
        self.frame_menu.destroy()
        TelaResgatePontos(self, self.email_logado).pack(expand=True, fill="both")

    def _mostrar_tela_visualizar_dados(self):
        """Exibe a tela de Visualizar Dados."""
        self.frame_menu.destroy()
        TelaVisualizarDados(self, self.email_logado).pack(expand=True, fill="both")

    def _mostrar_tela_quiz(self):
        """Exibe a tela do Quiz Semanal."""
        self.frame_menu.destroy()
        # Não precisa passar senha_logada para o Quiz, apenas o email
        TelaQuiz(self, self.email_logado, NOME_ARQUIVO_QUESTOES_QUIZ).pack(expand=True, fill="both")

    def encerrar_app(self):
        """Pergunta ao usuário se deseja sair e encerra o aplicativo se confirmado."""
        if messagebox.askyesno("Sair", "Tem certeza que deseja sair do sistema?"):
            self.destroy()
            sys.exit()

# ==================================================================================================
# --- Classes Modulares para as Funcionalidades do Menu ---
# ==================================================================================================

# --------------------------------------------------------------------------------------------------
# RANKING (Função 'ranking' original)
# --------------------------------------------------------------------------------------------------
class TelaRanking(ctk.CTkFrame):
    """
    Interface para exibir o ranking de pontos dos usuários.
    """
    def __init__(self, parent, email_login):
        super().__init__(parent)
        self.parent = parent
        self.email_login = email_login

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._mostrar_ranking()

    def _mostrar_ranking(self):
        """Cria e exibe os widgets da tela de ranking."""
        self._limpar_frame() # Limpa widgets existentes

        ctk.CTkLabel(self, text="🏆 RANKING DE PONTOS 🏆", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=20)

        dia_do_mes = datetime.datetime.now().strftime("%d")

        # Ajustado para usar a condição real do dia 28, mas deixado 'True' para testes
        if dia_do_mes == "28": # Altere para 'True' para testar a qualquer dia
            self.parent.banco_dados = carregar_json(NOME_ARQUIVO_BANCO_DADOS) # Recarrega para ter dados mais recentes
            pontos_dict = self.parent.banco_dados.get("pontos", {})
            ranking_ordenado = sorted(pontos_dict.items(), key=lambda item: item[1], reverse=True)

            # Frame rolável para exibir a tabela do ranking
            frame_rolavel = ctk.CTkScrollableFrame(self, width=450, height=300)
            frame_rolavel.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
            frame_rolavel.grid_columnconfigure(0, weight=1)

            # Cabeçalho da tabela
            ctk.CTkLabel(frame_rolavel, text=f"{'#':<3} | {'Email':<25} | {'Pontos':>8}", font=("Arial", 14, "bold")).pack(pady=5, anchor="w", padx=10)
            ctk.CTkLabel(frame_rolavel, text="-"*45, font=("Arial", 10)).pack(anchor="w", padx=10)

            # Linhas da tabela
            for i, (email, pts) in enumerate(ranking_ordenado, start=1):
                email_display = (email[:22] + '...') if len(email) > 25 else email.ljust(25)
                ctk.CTkLabel(frame_rolavel, text=f"{str(i).ljust(3)} | {email_display} | {str(pts).rjust(8)}", font=("Arial", 12)).pack(pady=2, anchor="w", padx=10)

        else:
            ctk.CTkLabel(self, text=f"📅 O Ranking é atualizado e visualizado apenas no dia 28 de cada mês.", font=("Arial", 16)).grid(row=1, column=0, pady=20)
            ctk.CTkLabel(self, text=f"Hoje é {datetime.datetime.now().strftime('%d')}.", font=("Arial", 14)).grid(row=2, column=0, pady=10)

        ctk.CTkButton(self, text="Voltar ao Menu", command=self._voltar_ao_menu).grid(row=3, column=0, pady=20)

    def _voltar_ao_menu(self):
        """Retorna à tela do menu principal."""
        self.destroy()
        self.parent._mostrar_tela_menu()

    def _limpar_frame(self):
        """Destrói todos os widgets filhos deste frame."""
        for widget in self.winfo_children():
            widget.destroy()

# --------------------------------------------------------------------------------------------------
# CÁLCULO DE PONTOS (Função 'calculo' original)
# --------------------------------------------------------------------------------------------------
class TelaCalculoPontos(ctk.CTkFrame):
    """
    Interface para calcular os pontos de economia de água do usuário.
    """
    def __init__(self, parent, email_login):
        super().__init__(parent)
        self.parent = parent
        self.email_login = email_login

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._mostrar_calculo_pontos()

    def _mostrar_calculo_pontos(self):
        """Cria e exibe os widgets da tela de cálculo de pontos."""
        self._limpar_frame()

        ctk.CTkLabel(self, text="💧 CÁLCULO DE ECONOMIA DE ÁGUA", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=20)

        dia_do_mes = datetime.datetime.now().strftime("%d")

        # Ajustado para usar a condição real do dia 27, mas deixado 'True' para testes
        if dia_do_mes == "27": # Altere para 'True' para testar a qualquer dia
            self.parent.dados_usuarios = carregar_json(NOME_ARQUIVO_DADOS_USUARIOS)
            self.parent.banco_dados = carregar_json(NOME_ARQUIVO_BANCO_DADOS)

            gasto_real = self.parent.dados_usuarios["consumo"].get(self.email_login)
            verificar_calculo = self.parent.dados_usuarios["calculo_realizado"].get(self.email_login, False)
            quantidade_membros = self.parent.banco_dados["membros"].get(self.email_login, 0)

            if verificar_calculo:
                ctk.CTkLabel(self, text="Você já realizou o cálculo mensal.", font=("Arial", 16), text_color="blue").grid(row=1, column=0, pady=10)
            elif gasto_real is None:
                ctk.CTkLabel(self, text="❌ Gasto de água não registrado para este e-mail.", font=("Arial", 16), text_color="red").grid(row=1, column=0, pady=10)
                ctk.CTkLabel(self, text="Peça ao seu síndico a atualização do banco de dados.", font=("Arial", 14)).grid(row=2, column=0, pady=5)
            else:
                gasto_estimado = quantidade_membros * 150 * 30 # Gasto médio por pessoa: 150 litros/dia

                ctk.CTkLabel(self, text=f"Membros na residência: {quantidade_membros}", font=("Arial", 14)).grid(row=1, column=0, pady=5, sticky="w", padx=50)
                ctk.CTkLabel(self, text=f"Gasto estimado (litros): {gasto_estimado}", font=("Arial", 14)).grid(row=2, column=0, pady=5, sticky="w", padx=50)
                ctk.CTkLabel(self, text=f"Gasto real (litros): {gasto_real}", font=("Arial", 14)).grid(row=3, column=0, pady=5, sticky="w", padx=50)

                if gasto_real < gasto_estimado:
                    ctk.CTkLabel(self, text="🎉 Parabéns, você economizou água e ganhou pontos!", font=("Arial", 16, "bold"), text_color="green").grid(row=4, column=0, pady=10)
                    pontos_ganhos = 50
                else:
                    ctk.CTkLabel(self, text="🚫 Você não economizou esse mês. Continue tentando!", font=("Arial", 16, "bold"), text_color="red").grid(row=4, column=0, pady=10)
                    pontos_ganhos = 0 # Ajuste se quiser dar 0 pontos para não economia

                # Atualiza pontos no banco_dados.JSON
                self.parent.banco_dados["pontos"][self.email_login] = self.parent.banco_dados["pontos"].get(self.email_login, 0) + pontos_ganhos
                salvar_json(self.parent.banco_dados, NOME_ARQUIVO_BANCO_DADOS)

                # Marca o cálculo como realizado em dados_usuarios.json
                self.parent.dados_usuarios["calculo_realizado"][self.email_login] = True
                salvar_json(self.parent.dados_usuarios, NOME_ARQUIVO_DADOS_USUARIOS)
        else:
            ctk.CTkLabel(self, text=f"📅 Hoje não é dia 27, o cálculo de economia está indisponível.", font=("Arial", 16)).grid(row=1, column=0, pady=20)
            ctk.CTkLabel(self, text=f"O cálculo é liberado no dia 27 de cada mês. Hoje é {datetime.datetime.now().strftime('%d')}.", font=("Arial", 14)).grid(row=2, column=0, pady=10)

        ctk.CTkButton(self, text="Voltar ao Menu", command=self._voltar_ao_menu).grid(row=5, column=0, pady=20)

    def _voltar_ao_menu(self):
        """Retorna à tela do menu principal."""
        self.destroy()
        self.parent._mostrar_tela_menu()

    def _limpar_frame(self):
        """Destrói todos os widgets filhos deste frame."""
        for widget in self.winfo_children():
            widget.destroy()

# --------------------------------------------------------------------------------------------------
# ATUALIZAR DADOS (Função 'atualizar' original e suas sub-funções)
# --------------------------------------------------------------------------------------------------
class TelaAtualizarDados(ctk.CTkFrame):
    """
    Interface para o processo de atualização de dados do usuário (pessoais ou da conta).
    """
    def __init__(self, parent, email_login):
        super().__init__(parent)
        self.parent = parent
        self.email_login = email_login

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._mostrar_opcoes_atualizacao()

    def _mostrar_opcoes_atualizacao(self):
        """Cria e exibe os widgets para as opções de atualização."""
        self._limpar_frame()

        ctk.CTkLabel(self, text="🔄 ATUALIZAÇÃO DE DADOS 🔄", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=20)
        ctk.CTkLabel(self, text="O que você deseja atualizar?", font=("Arial", 16)).grid(row=1, column=0, pady=10)

        ctk.CTkButton(self, text="Dados da Conta (E-mail/Senha)", command=self._mostrar_tela_atualizar_conta, font=("Arial", 16)).grid(row=2, column=0, pady=10, sticky="ew", padx=100)
        ctk.CTkButton(self, text="Dados Pessoais (Membros/Família)", command=self._mostrar_tela_atualizar_pessoais, font=("Arial", 16)).grid(row=3, column=0, pady=10, sticky="ew", padx=100)
        ctk.CTkButton(self, text="Voltar ao Menu", command=self._voltar_ao_menu).grid(row=4, column=0, pady=30)

    def _mostrar_tela_atualizar_pessoais(self):
        """Interface para atualizar membros e nome da família."""
        self._limpar_frame()

        ctk.CTkLabel(self, text="ATUALIZAR DADOS PESSOAIS", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=20)

        ctk.CTkLabel(self, text="Quantidade de membros na família:", font=("Arial", 14)).grid(row=1, column=0, pady=5)
        self.entry_membros = ctk.CTkEntry(self, placeholder_text="Ex: 3", width=200)
        self.entry_membros.grid(row=2, column=0, pady=5)

        ctk.CTkLabel(self, text="Nome da sua família:", font=("Arial", 14)).grid(row=3, column=0, pady=5)
        self.entry_familia = ctk.CTkEntry(self, placeholder_text="Ex: Família Silva", width=200)
        self.entry_familia.grid(row=4, column=0, pady=5)

        ctk.CTkButton(self, text="Confirmar Atualização", command=self._processar_atualizar_pessoais, font=("Arial", 16)).grid(row=5, column=0, pady=20)
        ctk.CTkButton(self, text="Voltar", command=self._mostrar_opcoes_atualizacao).grid(row=6, column=0, pady=10)

    def _processar_atualizar_pessoais(self):
        """Processa a atualização dos dados pessoais."""
        try:
            membros_novos = int(self.entry_membros.get())
            nome_novo = self.entry_familia.get().strip()

            if not (1 <= membros_novos <= 20): # Exemplo de validação
                messagebox.showwarning("Entrada Inválida", "A quantidade de membros deve ser um número entre 1 e 20.")
                return
            if not nome_novo:
                messagebox.showwarning("Entrada Inválida", "O nome da família não pode estar vazio.")
                return

            if messagebox.askyesno("Confirmar Atualização", "Tem certeza que deseja atualizar seus dados pessoais?"):
                self.parent.banco_dados = carregar_json(NOME_ARQUIVO_BANCO_DADOS) # Recarregar para garantir que é o mais recente
                self.parent.banco_dados["membros"][self.email_login] = membros_novos
                self.parent.banco_dados["familia"][self.email_login] = nome_novo

                if salvar_json(self.parent.banco_dados, NOME_ARQUIVO_BANCO_DADOS):
                    messagebox.showinfo("Sucesso", "Dados pessoais atualizados com sucesso!")
                    self._voltar_ao_menu()
                else:
                    messagebox.showerror("Erro", "Não foi possível salvar os dados atualizados.")
        except ValueError:
            messagebox.showerror("Erro de Entrada", "A quantidade de membros deve ser um número inteiro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def _mostrar_tela_atualizar_conta(self):
        """Interface para atualizar e-mail e/ou senha."""
        self._limpar_frame()

        ctk.CTkLabel(self, text="ATUALIZAR DADOS DA CONTA", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=20)

        ctk.CTkLabel(self, text="Novo E-mail (deixe em branco para não alterar):", font=("Arial", 14)).grid(row=1, column=0, pady=5)
        self.entry_novo_email = ctk.CTkEntry(self, placeholder_text="seu.novo.email@exemplo.com", width=300)
        self.entry_novo_email.grid(row=2, column=0, pady=5)

        ctk.CTkLabel(self, text="Nova Senha (deixe em branco para não alterar):", font=("Arial", 14)).grid(row=3, column=0, pady=5)
        self.entry_nova_senha = ctk.CTkEntry(self, placeholder_text="**** (4 a 20 caracteres)", show="*", width=300)
        self.entry_nova_senha.grid(row=4, column=0, pady=5)

        ctk.CTkButton(self, text="Confirmar Atualização", command=self._processar_atualizar_conta, font=("Arial", 16)).grid(row=5, column=0, pady=20)
        ctk.CTkButton(self, text="Voltar", command=self._mostrar_opcoes_atualizacao).grid(row=6, column=0, pady=10)

    def _processar_atualizar_conta(self):
        """Processa a atualização do e-mail e/ou senha."""
        novo_email = self.entry_novo_email.get().strip()
        nova_senha = self.entry_nova_senha.get().strip()

        # Validações baseadas no código de console
        if novo_email and not self._email_valido_formato(novo_email):
            messagebox.showwarning("Erro de E-mail", "Formato de e-mail inválido ou domínio não aceito.")
            return
        if novo_email and self._email_ja_existe(novo_email) and novo_email != self.email_login:
            messagebox.showwarning("Erro de E-mail", "Este e-mail já está cadastrado por outro usuário.")
            return

        if nova_senha and not (4 <= len(nova_senha) <= 20):
            messagebox.showwarning("Erro de Senha", "A senha deve ter entre 4 e 20 caracteres.")
            return

        if not novo_email and not nova_senha:
            messagebox.showinfo("Nenhuma Alteração", "Nenhum dado de conta foi inserido para atualização.")
            return

        if messagebox.askyesno("Confirmar Atualização", "Tem certeza que deseja atualizar os dados da sua conta? Esta ação pode ser irreversível."):
            self.parent.banco_dados = carregar_json(NOME_ARQUIVO_BANCO_DADOS)

            email_antigo = self.email_login
            senha_antiga = self.parent.banco_dados["senha"].get(email_antigo)

            email_para_usar = novo_email if novo_email else email_antigo
            senha_para_usar = nova_senha if nova_senha else senha_antiga

            # Se o email foi alterado, precisamos mover todos os dados para a nova chave de email
            if novo_email and novo_email != email_antigo:
                # Copia os dados do email antigo para o novo email
                self.parent.banco_dados["senha"][email_para_usar] = senha_para_usar
                self.parent.banco_dados["familia"][email_para_usar] = self.parent.banco_dados["familia"].get(email_antigo)
                self.parent.banco_dados["membros"][email_para_usar] = self.parent.banco_dados["membros"].get(email_antigo)
                self.parent.banco_dados["pontos"][email_para_usar] = self.parent.banco_dados["pontos"].get(email_antigo)
                self.parent.banco_dados["apartamento"][email_para_usar] = self.parent.banco_dados["apartamento"].get(email_antigo)
                self.parent.banco_dados["verificador"][email_para_usar] = self.parent.banco_dados["verificador"].get(email_antigo)
                # Adiciona suporte para pontos do quiz (se existirem)
                if email_antigo in self.parent.banco_dados.get("usuarios", {}):
                    self.parent.banco_dados["usuarios"][email_para_usar] = self.parent.banco_dados["usuarios"][email_antigo]

                # Remove os dados do email antigo
                del self.parent.banco_dados["senha"][email_antigo]
                del self.parent.banco_dados["familia"][email_antigo]
                del self.parent.banco_dados["membros"][email_antigo]
                del self.parent.banco_dados["pontos"][email_antigo]
                del self.parent.banco_dados["apartamento"][email_antigo]
                del self.parent.banco_dados["verificador"][email_antigo]
                if email_antigo in self.parent.banco_dados.get("usuarios", {}):
                    del self.parent.banco_dados["usuarios"][email_antigo]

                # Atualiza o email logado na App principal
                self.parent.email_logado = email_para_usar
                messagebox.showinfo("Sucesso", f"E-mail e/ou senha atualizados com sucesso! Seu novo e-mail de login é: {email_para_usar}")

            else: # Apenas a senha ou nenhum dos dois (mas a senha pode ter sido alterada)
                self.parent.banco_dados["senha"][email_para_usar] = senha_para_usar
                messagebox.showinfo("Sucesso", "Senha atualizada com sucesso!" if nova_senha else "Nenhuma alteração feita na conta.")

            if salvar_json(self.parent.banco_dados, NOME_ARQUIVO_BANCO_DADOS):
                self._voltar_ao_menu()
            else:
                messagebox.showerror("Erro", "Não foi possível salvar as alterações da conta.")

    def _email_valido_formato(self, email):
        """Valida o formato e domínio do e-mail."""
        dominios_validos = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com', 'icloud.com']
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False
        dominio = email.split('@')[1].lower()
        if dominio not in dominios_validos:
            return False
        return True

    def _email_ja_existe(self, email):
        """Verifica se o e-mail já existe no banco de dados (excluindo o email_logado atual)."""
        self.parent.banco_dados = carregar_json(NOME_ARQUIVO_BANCO_DADOS)
        return email in self.parent.banco_dados["senha"] and email != self.email_login

    def _voltar_ao_menu(self):
        """Retorna à tela do menu principal."""
        self.destroy()
        self.parent._mostrar_tela_menu()

    def _limpar_frame(self):
        """Destrói todos os widgets filhos deste frame."""
        for widget in self.winfo_children():
            widget.destroy()

# --------------------------------------------------------------------------------------------------
# DELETAR CONTA (Função 'deletar' original)
# --------------------------------------------------------------------------------------------------
class TelaDeletarConta(ctk.CTkFrame):
    """
    Interface para o processo de deleção de conta do usuário.
    """
    def __init__(self, parent, email_login):
        super().__init__(parent)
        self.parent = parent
        self.email_login = email_login

        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._mostrar_confirmacao_delecao()

    def _mostrar_confirmacao_delecao(self):
        """Cria e exibe os widgets para a confirmação de deleção."""
        self._limpar_frame()

        ctk.CTkLabel(self, text="⚠️ ATENÇÃO IMPORTANTE ⚠️", font=("Arial", 24, "bold"), text_color="red").grid(row=0, column=0, pady=20)
        ctk.CTkLabel(self, text="Você está na aba de deleção de conta.", font=("Arial", 16)).grid(row=1, column=0, pady=5)
        ctk.CTkLabel(self, text="Tome cuidado para não realizar uma ação indesejada!", font=("Arial", 16)).grid(row=2, column=0, pady=5)

        ctk.CTkLabel(self, text=f"Deseja deletar sua conta ({self.email_login}) do sistema ECODROP condomínio Village?", font=("Arial", 16)).grid(row=3, column=0, pady=20)

        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.grid(row=4, column=0, pady=10)
        frame_botoes.grid_columnconfigure((0,1), weight=1)

        ctk.CTkButton(frame_botoes, text="Sim, Deletar Conta", command=self._confirmar_e_deletar, fg_color="red", hover_color="darkred", font=("Arial", 16)).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botoes, text="Não, Voltar ao Menu", command=self._voltar_ao_menu, font=("Arial", 16)).grid(row=0, column=1, padx=10)

    def _confirmar_e_deletar(self):
        """Processa a deleção da conta após a confirmação."""
        if messagebox.askyesno("Confirmar Deleção", "Tem certeza ABSOLUTA que deseja deletar sua conta? Esta ação é irreversível!"):
            self.parent.banco_dados = carregar_json(NOME_ARQUIVO_BANCO_DADOS)

            email_para_deletar = self.email_login
            if email_para_deletar in self.parent.banco_dados["senha"]:
                # Remove os dados do usuário de todas as seções
                # Verificando a existência antes de deletar para evitar KeyError se a chave não existir
                if email_para_deletar in self.parent.banco_dados.get("senha", {}): del self.parent.banco_dados["senha"][email_para_deletar]
                if email_para_deletar in self.parent.banco_dados.get("familia", {}): del self.parent.banco_dados["familia"][email_para_deletar]
                if email_para_deletar in self.parent.banco_dados.get("membros", {}): del self.parent.banco_dados["membros"][email_para_deletar]
                if email_para_deletar in self.parent.banco_dados.get("pontos", {}): del self.parent.banco_dados["pontos"][email_para_deletar]
                if email_para_deletar in self.parent.banco_dados.get("apartamento", {}): del self.parent.banco_dados["apartamento"][email_para_deletar]
                if email_para_deletar in self.parent.banco_dados.get("verificador", {}): del self.parent.banco_dados["verificador"][email_para_deletar]
                if email_para_deletar in self.parent.banco_dados.get("usuarios", {}): # Para dados do quiz
                    del self.parent.banco_dados["usuarios"][email_para_deletar]

                # Salva o banco de dados atualizado
                if salvar_json(self.parent.banco_dados, NOME_ARQUIVO_BANCO_DADOS):
                    messagebox.showinfo("Deleção Concluída", "Sua conta foi deletada com sucesso. Tenha um bom dia!")
                    self.parent.destroy() # Fecha o aplicativo inteiro
                    sys.exit()
                else:
                    messagebox.showerror("Erro", "Não foi possível salvar as alterações após a deleção.")
            else:
                messagebox.showwarning("Erro", "Conta não encontrada para deleção.")
        else:
            messagebox.showinfo("Cancelado", "Deleção de conta cancelada.")
            self._voltar_ao_menu()

    def _voltar_ao_menu(self):
        """Retorna à tela do menu principal."""
        self.destroy()
        self.parent._mostrar_tela_menu()

    def _limpar_frame(self):
        """Destrói todos os widgets filhos deste frame."""
        for widget in self.winfo_children():
            widget.destroy()

# --------------------------------------------------------------------------------------------------
# FEEDBACK (Função 'feedback' original)
# --------------------------------------------------------------------------------------------------
class TelaFeedback(ctk.CTkFrame):
    """
    Interface para o sistema de avaliação de serviço (feedback).
    Permite ao usuário deixar um comentário e uma nota.
    """
    def __init__(self, parent, email_login):
        super().__init__(parent)
        self.parent = parent
        self.email_login = email_login

        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._criar_widgets()

    def _criar_widgets(self):
        """Cria e posiciona os elementos da interface de feedback."""
        ctk.CTkLabel(self, text="📝 SISTEMA DE AVALIAÇÃO DE SERVIÇO", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=20)
        ctk.CTkLabel(self, text="Deixe seu comentário (até 140 caracteres):", font=("Arial", 14)).grid(row=1, column=0, pady=5)

        self.caixa_texto_comentario = ctk.CTkTextbox(self, width=400, height=100, font=("Arial", 12))
        self.caixa_texto_comentario.grid(row=2, column=0, pady=10)
        self.caixa_texto_comentario.bind("<KeyRelease>", self._validar_comprimento_comentario)
        self.label_contador_caracteres = ctk.CTkLabel(self, text="0/140 caracteres", font=("Arial", 10), text_color="gray")
        self.label_contador_caracteres.grid(row=3, column=0, sticky="e", padx=50)

        ctk.CTkLabel(self, text="Qual nota você nos dá (0 a 10)?", font=("Arial", 14)).grid(row=4, column=0, pady=(20, 5))

        self.slider_nota = ctk.CTkSlider(self, from_=0, to=10, number_of_steps=20, command=self._atualizar_label_nota)
        self.slider_nota.set(5.0) # Valor inicial do slider
        self.slider_nota.grid(row=5, column=0, pady=10, sticky="ew", padx=50)

        self.label_exibir_nota = ctk.CTkLabel(self, text="Nota: 5.0", font=("Arial", 14, "bold"))
        self.label_exibir_nota.grid(row=6, column=0, pady=5)

        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.grid(row=7, column=0, pady=30)
        frame_botoes.grid_columnconfigure((0,1), weight=1)

        ctk.CTkButton(frame_botoes, text="Enviar Feedback", command=self._enviar_feedback, font=("Arial", 16, "bold")).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botoes, text="Voltar ao Menu", command=self._voltar_ao_menu, font=("Arial", 16)).grid(row=0, column=1, padx=10)
        ctk.CTkButton(self, text="Sair do Sistema", command=self._sair_do_sistema, fg_color="red", hover_color="darkred", font=("Arial", 16)).grid(row=8, column=0, pady=5)

    def _validar_comprimento_comentario(self, event=None):
        """Valida o comprimento do comentário e atualiza o contador de caracteres."""
        comentario = self.caixa_texto_comentario.get("1.0", "end-1c") # Pega todo o texto, exceto a última quebra de linha
        tamanho = len(comentario)
        self.label_contador_caracteres.configure(text=f"{tamanho}/140 caracteres")
        if tamanho > 140:
            self.caixa_texto_comentario.configure(border_color="red", border_width=2)
            self.label_contador_caracteres.configure(text_color="red")
        else:
            self.caixa_texto_comentario.configure(border_color="gray", border_width=1)
            self.label_contador_caracteres.configure(text_color="gray")

    def _atualizar_label_nota(self, valor):
        """Atualiza o label exibindo a nota selecionada pelo slider."""
        self.label_exibir_nota.configure(text=f"Nota: {valor:.1f}")

    def _enviar_feedback(self):
        """Coleta os dados do formulário, valida e salva o feedback."""
        comentario = self.caixa_texto_comentario.get("1.0", "end-1c").strip()
        nota = round(self.slider_nota.get(), 1) # Arredonda a nota para uma casa decimal

        # Validação do comentário
        if not (0 < len(comentario) <= 140):
            messagebox.showwarning("Erro de Comentário", "Por favor, digite um comentário entre 1 e 140 caracteres.")
            self.caixa_texto_comentario.focus_set()
            return

        # Validação da nota (o slider já garante 0-10, mas uma validação extra é segura)
        if not (0 <= nota <= 10):
            messagebox.showwarning("Erro de Nota", "A nota deve estar entre 0 e 10.")
            return

        # Salva o feedback no arquivo CSV
        try:
            with open(NOME_ARQUIVO_FEEDBACK_CSV, mode="a", newline="", encoding="utf-8") as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow([self.email_login, comentario, nota])
            messagebox.showinfo("Sucesso", "Feedback salvo com sucesso! Obrigado pela sua avaliação.")
            self._limpar_campos() # Limpa os campos após o envio
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o feedback: {e}")

    def _limpar_campos(self):
        """Limpa os campos do formulário de feedback."""
        self.caixa_texto_comentario.delete("1.0", "end")
        self.slider_nota.set(5.0)
        self._atualizar_label_nota(5.0)
        self.label_contador_caracteres.configure(text="0/140 caracteres", text_color="gray")
        self.caixa_texto_comentario.configure(border_color="gray", border_width=1)

    def _voltar_ao_menu(self):
        """Retorna à tela do menu principal."""
        self.destroy()
        self.parent._mostrar_tela_menu()

    def _sair_do_sistema(self):
        """Encerra o aplicativo após confirmação."""
        if messagebox.askyesno("Sair", "Tem certeza que deseja sair do sistema?"):
            self.parent.destroy()
            sys.exit()

# --------------------------------------------------------------------------------------------------
# RESGATAR RECOMPENSAS (Função 'resgatar' original)
# --------------------------------------------------------------------------------------------------
class TelaResgatePontos(ctk.CTkFrame):
    """
    Interface para resgate de recompensas utilizando pontos.
    """
    def __init__(self, parent, email_login):
        super().__init__(parent)
        self.parent = parent
        self.email_login = email_login

        self.grid_rowconfigure((0,1,2,3), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.dados_recompensas = {
            "1": {"nome": "Milhas", "custo": 150},
            "2": {"nome": "Desconto no condomínio", "custo": 100},
            "3": {"nome": "Voucher", "custo": 80},
            "4": {"nome": "Cupons", "custo": 60},
            "5": {"nome": "Descontos", "custo": 50},
            "6": {"nome": "Créditos de celular", "custo": 40}
        }
        self._criar_widgets()
        self._atualizar_exibicao_pontos() # Exibe o saldo inicial de pontos

    def _criar_widgets(self):
        """Cria e posiciona os elementos da interface de resgate."""
        ctk.CTkLabel(self, text="🎁 TABELA DE RECOMPENSAS 🎁", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=20)

        self.label_pontos = ctk.CTkLabel(self, text="Seus pontos: --", font=("Arial", 16, "bold"), text_color="blue")
        self.label_pontos.grid(row=1, column=0, pady=10)

        frame_recompensas = ctk.CTkFrame(self)
        frame_recompensas.grid(row=2, column=0, pady=20, padx=20, sticky="ew")
        frame_recompensas.grid_columnconfigure(0, weight=1)

        for i, (num, recompensa) in enumerate(self.dados_recompensas.items()):
            texto_recompensa = f"{recompensa['nome']} ({recompensa['custo']} pts)"
            ctk.CTkButton(
                frame_recompensas,
                text=texto_recompensa,
                command=lambda n=num: self._resgatar_recompensa(n),
                font=("Arial", 14)
            ).grid(row=i, column=0, pady=5, padx=10, sticky="ew")

        ctk.CTkButton(self, text="Voltar ao Menu", command=self._voltar_ao_menu).grid(row=3, column=0, pady=20)
        ctk.CTkButton(self, text="Sair do Sistema", command=self._sair_do_sistema, fg_color="red", hover_color="darkred").grid(row=4, column=0, pady=5)

    def _atualizar_exibicao_pontos(self):
        """Atualiza o texto do saldo de pontos na interface."""
        self.parent.banco_dados = carregar_json(NOME_ARQUIVO_BANCO_DADOS) # Sempre busca a versão mais recente
        pontos = self.parent.banco_dados["pontos"].get(self.email_login, 0)
        self.label_pontos.configure(text=f"Seus pontos: {pontos}")

    def _resgatar_recompensa(self, opcao_escolhida):
        """Processa o resgate de uma recompensa, deduzindo pontos."""
        info_recompensa = self.dados_recompensas.get(opcao_escolhida)
        if not info_recompensa:
            messagebox.showwarning("Opção Inválida", "Por favor, selecione uma recompensa válida.")
            return

        custo = info_recompensa['custo']
        nome = info_recompensa['nome']
        pontos_atuais = self.parent.banco_dados["pontos"].get(self.email_login, 0)

        if pontos_atuais >= custo:
            self.parent.banco_dados["pontos"][self.email_login] = pontos_atuais - custo
            if salvar_json(self.parent.banco_dados, NOME_ARQUIVO_BANCO_DADOS):
                self._atualizar_exibicao_pontos() # Atualiza o display de pontos imediatamente
                messagebox.showinfo("Resgate Realizado", f"🎉 Você resgatou: {nome}\n✅ Seu novo saldo de pontos é: {self.parent.banco_dados['pontos'][self.email_login]}")
                gerar_codigo_resgate() # Exibe o código de resgate em outra caixa de mensagem
            else:
                messagebox.showerror("Erro ao Salvar", "Não foi possível atualizar seu saldo de pontos.")
        else:
            messagebox.showwarning("Saldo Insuficiente", f"⚠️ Você não possui saldo suficiente para resgatar {nome}. Pontos necessários: {custo}")

    def _voltar_ao_menu(self):
        """Retorna à tela do menu principal."""
        self.destroy()
        self.parent._mostrar_tela_menu()

    def _sair_do_sistema(self):
        """Encerra o aplicativo após confirmação."""
        if messagebox.askyesno("Sair", "Tem certeza que deseja sair do sistema?"):
            self.parent.destroy()
            sys.exit()

# --------------------------------------------------------------------------------------------------
# VISUALIZAR DADOS (Função 'mostrar_dados' original)
# --------------------------------------------------------------------------------------------------
class TelaVisualizarDados(ctk.CTkFrame):
    """
    Interface para exibir os dados do usuário.
    """
    def __init__(self, parent, email_login):
        super().__init__(parent)
        self.parent = parent
        self.email_login = email_login

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._mostrar_dados_usuario()

    def _mostrar_dados_usuario(self):
        """Cria e exibe os widgets com os dados do usuário."""
        self._limpar_frame()

        ctk.CTkLabel(self, text="📊 SEUS DADOS DA CONTA 📊", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=20)

        self.parent.banco_dados = carregar_json(NOME_ARQUIVO_BANCO_DADOS) # Recarrega para ter os dados mais recentes

        email = self.email_login
        membros = self.parent.banco_dados["membros"].get(email, "Não disponível")
        pontos = self.parent.banco_dados["pontos"].get(email, "Não disponível")
        apartamento = self.parent.banco_dados["apartamento"].get(email, "Não disponível")
        familia = self.parent.banco_dados["familia"].get(email, "Não disponível")
        pontos_quiz = self.parent.banco_dados.get("usuarios", {}).get(email, {}).get("pontos_quiz", 0)


        ctk.CTkLabel(self, text=f"• E-mail Cadastrado: {email}", font=("Arial", 16)).grid(row=1, column=0, pady=5, sticky="w", padx=50)
        ctk.CTkLabel(self, text=f"• Quantidade de Membros: {membros}", font=("Arial", 16)).grid(row=2, column=0, pady=5, sticky="w", padx=50)
        ctk.CTkLabel(self, text=f"• Pontos Acumulados (Economia): {pontos}", font=("Arial", 16)).grid(row=3, column=0, pady=5, sticky="w", padx=50)
        ctk.CTkLabel(self, text=f"• Pontos Acumulados (Quiz): {pontos_quiz}", font=("Arial", 16)).grid(row=4, column=0, pady=5, sticky="w", padx=50)
        ctk.CTkLabel(self, text=f"• Apartamento: {apartamento}", font=("Arial", 16)).grid(row=5, column=0, pady=5, sticky="w", padx=50)
        ctk.CTkLabel(self, text=f"• Nome da Família: {familia}", font=("Arial", 16)).grid(row=6, column=0, pady=5, sticky="w", padx=50)

        ctk.CTkButton(self, text="Voltar ao Menu", command=self._voltar_ao_menu).grid(row=7, column=0, pady=30)

    def _voltar_ao_menu(self):
        """Retorna à tela do menu principal."""
        self.destroy()
        self.parent._mostrar_tela_menu()

    def _limpar_frame(self):
        """Destrói todos os widgets filhos deste frame."""
        for widget in self.winfo_children():
            widget.destroy()

# --------------------------------------------------------------------------------------------------
# QUIZ SEMANAL (Classe 'Quiz' original, adaptada para CustomTkinter)
# --------------------------------------------------------------------------------------------------
class TelaQuiz(ctk.CTkFrame):
    """
    Interface para o Quiz Semanal sobre o uso da água.
    """
    def __init__(self, parent, email_login, caminho_arquivo_questoes):
        super().__init__(parent)
        self.parent = parent
        self.email_login = email_login
        self.caminho_arquivo = caminho_arquivo_questoes
        self.questoes = [] # Inicializado vazio, carregado em _iniciar_fluxo_quiz
        self.pontuacao_atual = 0
        self.indice_questao_atual = 0
        self.questoes_selecionadas = []
        self.opcoes_embaralhadas = []
        self.num_questoes_desejadas = 5 # Número fixo de questões no quiz

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._iniciar_fluxo_quiz()

    def _carregar_questoes(self):
        """Carrega as questões do arquivo JSON especificado."""
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
                questoes_carregadas = json.load(f)
            # messagebox.showinfo("Quiz", f"✅ Questões carregadas com sucesso! Total: {len(questoes_carregadas)}")
            return questoes_carregadas
        except FileNotFoundError:
            messagebox.showerror("Erro Quiz", f"Arquivo de questões '{self.caminho_arquivo}' não encontrado.")
            return None
        except json.JSONDecodeError:
            messagebox.showerror("Erro Quiz", f"Erro ao ler JSON de '{self.caminho_arquivo}'. O arquivo pode estar corrompido ou vazio.")
            return None
        except Exception as e:
            messagebox.showerror("Erro Quiz", f"Ocorreu um erro inesperado ao carregar '{self.caminho_arquivo}': {e}")
            return None

    def _iniciar_fluxo_quiz(self):
        """Inicia o fluxo do quiz, verificando a data e carregando questões."""
        self._limpar_frame()

        ctk.CTkLabel(self, text="💡 Quiz Semanal - Gasto Consciente", font=("Arial", 24, "bold")).grid(row=0, column=0, pady=20)

        hoje = datetime.datetime.now()
        # Verificar se é segunda-feira (0 = segunda-feira)
        if hoje.weekday() == 0: # 0 é Segunda-feira
            self.questoes = self._carregar_questoes() # Carrega as questões quando o quiz é iniciado

            if not self.questoes:
                ctk.CTkLabel(self, text="⚠️ Nenhuma questão carregada. Verifique o arquivo JSON.", font=("Arial", 16)).grid(row=1, column=0, pady=10)
                ctk.CTkButton(self, text="Voltar ao Menu", command=self._voltar_ao_menu).grid(row=2, column=0, pady=20)
                return

            if len(self.questoes) < self.num_questoes_desejadas:
                messagebox.showwarning("Atenção Quiz", f"Apenas {len(self.questoes)} questão(ões) disponível(is) no arquivo. O quiz terá menos questões.")
                self.num_questoes_desejadas = len(self.questoes) # Ajusta o número de questões se não houver o suficiente

            self.questoes_selecionadas = random.sample(self.questoes, self.num_questoes_desejadas)
            self._exibir_questao() # Inicia a exibição da primeira questão
        else:
            ctk.CTkLabel(self, text=f"🕒 O Quiz Semanal está disponível apenas às **segundas-feiras**.", font=("Arial", 16)).grid(row=1, column=0, pady=10)
            ctk.CTkLabel(self, text=f"Hoje é **{hoje.strftime('%A')}**.", font=("Arial", 14)).grid(row=2, column=0, pady=5)
            ctk.CTkButton(self, text="Voltar ao Menu", command=self._voltar_ao_menu).grid(row=3, column=0, pady=20)

    def _exibir_questao(self):
        """Exibe a questão atual e as opções de resposta."""
        self._limpar_frame()

        if self.indice_questao_atual < len(self.questoes_selecionadas):
            questao = self.questoes_selecionadas[self.indice_questao_atual]

            ctk.CTkLabel(self, text=f"Questão {self.indice_questao_atual + 1}/{self.num_questoes_desejadas}:", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=(20, 5), sticky="w", padx=20)
            ctk.CTkLabel(self, text=questao['pergunta'], font=("Arial", 14), wraplength=700).grid(row=1, column=0, pady=(0, 20), sticky="w", padx=20)

            self.opcoes_embaralhadas = random.sample(questao['opcoes'], len(questao['opcoes']))
            self.variavel_radio = ctk.StringVar(value="") # Variável para armazenar a opção selecionada

            # Cria os botões de rádio para as opções
            for i, opcao in enumerate(self.opcoes_embaralhadas):
                radio_button = ctk.CTkRadioButton(self, text=opcao, variable=self.variavel_radio, value=opcao, font=("Arial", 14))
                radio_button.grid(row=2 + i, column=0, pady=5, sticky="w", padx=40)

            ctk.CTkButton(self, text="Confirmar Resposta", command=self._verificar_resposta, font=("Arial", 16)).grid(row=2 + len(self.opcoes_embaralhadas), column=0, pady=30)
        else:
            self._finalizar_quiz() # Se todas as questões foram respondidas, finaliza o quiz

    def _verificar_resposta(self):
        """Verifica a resposta selecionada e atualiza a pontuação."""
        resposta_selecionada = self.variavel_radio.get()
        if not resposta_selecionada:
            messagebox.showwarning("Atenção", "Por favor, selecione uma opção antes de confirmar.")
            return

        questao = self.questoes_selecionadas[self.indice_questao_atual]

        if resposta_selecionada == questao['resposta_correta']:
            self.pontuacao_atual += 1
            messagebox.showinfo("Resultado", "✅ Correto!")
        else:
            messagebox.showinfo("Resultado", f"❌ Errado. A resposta correta era: {questao['resposta_correta']}")

        self.indice_questao_atual += 1
        # Pequeno atraso antes de exibir a próxima questão ou finalizar
        self.after(500, self._exibir_questao)

    def _finalizar_quiz(self):
        """Exibe a pontuação final do quiz e atualiza os pontos do usuário."""
        self._limpar_frame()
        ctk.CTkLabel(self, text="🎉 FIM DO QUIZ 🎉", font=("Arial", 28, "bold")).grid(row=0, column=0, pady=20)
        ctk.CTkLabel(self, text=f"Sua pontuação final foi: {self.pontuacao_atual} de {self.num_questoes_desejadas}", font=("Arial", 18)).grid(row=1, column=0, pady=10)
        ctk.CTkLabel(self, text="💡 Continue aprendendo e economizando água!", font=("Arial", 14)).grid(row=2, column=0, pady=10)

        # Atualiza a pontuação do usuário no banco de dados principal
        self._atualizar_pontuacao_usuario(self.email_login, self.pontuacao_atual)

        ctk.CTkButton(self, text="Voltar ao Menu", command=self._voltar_ao_menu).grid(row=3, column=0, pady=30)

    def _atualizar_pontuacao_usuario(self, email_usuario, pontos_ganhos):
        """Adiciona os pontos ganhos no quiz à pontuação total do usuário no banco de dados."""
        # Recarrega o banco de dados para garantir que está atualizado
        self.parent.banco_dados = carregar_json(NOME_ARQUIVO_BANCO_DADOS)

        # Garante que as estruturas 'usuarios' e 'pontos_quiz' existam
        if "usuarios" not in self.parent.banco_dados:
            self.parent.banco_dados["usuarios"] = {}
        if email_usuario not in self.parent.banco_dados["usuarios"]:
            self.parent.banco_dados["usuarios"][email_usuario] = {"pontos_quiz": 0}
        if "pontos_quiz" not in self.parent.banco_dados["usuarios"][email_usuario]:
             self.parent.banco_dados["usuarios"][email_usuario]["pontos_quiz"] = 0

        self.parent.banco_dados["usuarios"][email_usuario]["pontos_quiz"] += pontos_ganhos

        if salvar_json(self.parent.banco_dados, NOME_ARQUIVO_BANCO_DADOS):
            messagebox.showinfo("Pontos Atualizados", f"✨ Você ganhou {pontos_ganhos} pontos no quiz!\nTotal de pontos do quiz: {self.parent.banco_dados['usuarios'][email_usuario]['pontos_quiz']}")
        else:
            messagebox.showerror("Erro ao Salvar Pontos", "Não foi possível atualizar sua pontuação no banco de dados.")

    def _voltar_ao_menu(self):
        """Retorna à tela do menu principal."""
        self.destroy()
        self.parent._mostrar_tela_menu()

    def _limpar_frame(self):
        """Destrói todos os widgets filhos deste frame."""
        for widget in self.winfo_children():
            widget.destroy()


# ==================================================================================================
# --- Funções e Classes de Console (Mantidas como Placeholders) ---
# ==================================================================================================
# Estas são as funções e classes originais do seu código que ainda operam via console.
# No contexto da GUI, elas não são chamadas diretamente pelos botões do menu.
# Foram mantidas aqui como placeholders para compatibilidade com partes do seu código que as referenciam.

# Carrega os dados para as funções de console no início do script.
# Em um sistema GUI completo, esses dados seriam gerenciados pela classe principal 'App'.
# Mover este bloco para dentro da classe App ou remover se as funções de console não forem mais usadas.
# Fora da classe App, essas variáveis globais de console não serão as mesmas que as variáveis internas do App.
# Por simplicidade, vou manter o App como a fonte da verdade para os dados.
# As funções de console (login, menu, etc.) que estão abaixo foram movidas para placeholders
# para não conflitar com a lógica da GUI.

# Removi o bloco de leitura inicial do banco_dados.JSON, pois a classe App já faz isso.

def login():
    """Placeholder para a função de login original (console)."""
    messagebox.showinfo("Info", "A função 'login' original do console não é usada diretamente na interface gráfica. Use a tela de Login da GUI.")
    pass

def menu(email_login, senha_login):
    """Placeholder para a função de menu original (console)."""
    messagebox.showinfo("Info", "A função 'menu' original do console não é usada diretamente na interface gráfica. Use a tela de Menu da GUI.")
    pass

def atualizar(email_login, senha_login):
    """Placeholder para a função de atualizar dados (console)."""
    messagebox.showinfo("Info", "A função 'atualizar' original do console não é usada diretamente na interface gráfica.")
    pass

def atualizar_pessoais(email_login, senha_login):
    """Placeholder para a função de atualizar dados pessoais (console)."""
    messagebox.showinfo("Info", "A função 'atualizar_pessoais' original do console não é usada diretamente na interface gráfica.")
    pass

def tipo_atualizacao(email_login, senha_login):
    """Placeholder para a função de tipo de atualização (console)."""
    messagebox.showinfo("Info", "A função 'tipo_atualizacao' original do console não é usada diretamente na interface gráfica.")
    pass

def email_valido(email_login, senha_login):
    """Placeholder para a função de validação de email (console)."""
    messagebox.showinfo("Info", "A função 'email_valido' original do console não é usada diretamente na interface gráfica.")
    pass

def conferir_email(email_novo, email_login, senha_login):
    """Placeholder para a função de conferir email (console)."""
    messagebox.showinfo("Info", "A função 'conferir_email' original do console não é usada diretamente na interface gráfica.")
    pass

def conferir_senha(email_novo, email_login, senha_login):
    """Placeholder para a função de conferir senha (console)."""
    messagebox.showinfo("Info", "A função 'conferir_senha' original do console não é usada diretamente na interface gráfica.")
    pass

def atualizar_conta(email_novo, senha_nova, email_login, senha_login):
    """Placeholder para a função de atualizar conta (console)."""
    messagebox.showinfo("Info", "A função 'atualizar_conta' original do console não é usada diretamente na interface gráfica.")
    pass

def valido_apenas_email(email_login, senha_login):
    """Placeholder para a função de validação de apenas email (console)."""
    messagebox.showinfo("Info", "A função 'valido_apenas_email' original do console não é usada diretamente na interface gráfica.")
    pass

def conferir_apenas_email(email_novo, email_login, senha_login):
    """Placeholder para a função de conferir apenas email (console)."""
    messagebox.showinfo("Info", "A função 'conferir_apenas_email' original do console não é usada diretamente na interface gráfica.")
    pass

def atualizar_apenas_email(email_novo, email_login, senha_login):
    """Placeholder para a função de atualizar apenas email (console)."""
    messagebox.showinfo("Info", "A função 'atualizar_apenas_email' original do console não é usada diretamente na interface gráfica.")
    pass

def valido_apenas_senha(email_login):
    """Placeholder para a função de validação de apenas senha (console)."""
    messagebox.showinfo("Info", "A função 'valido_apenas_senha' original do console não é usada diretamente na interface gráfica.")
    pass

def atualizar_apenas_senha(senha_nova, email_login):
    """Placeholder para a função de atualizar apenas senha (console)."""
    messagebox.showinfo("Info", "A função 'atualizar_apenas_senha' original do console não é usada diretamente na interface gráfica.")
    pass

def mostrar_dados(email_login, senha_login):
    """Placeholder para a função de mostrar dados (console)."""
    messagebox.showinfo("Info", "A função 'mostrar_dados' original do console não é usada diretamente na interface gráfica.")
    pass

class Cadastro:
    """Placeholder para a classe de Cadastro original (console)."""
    def __init__(self):
        messagebox.showinfo("Info", "A classe 'Cadastro' original do console não é usada diretamente na interface gráfica. Use a tela de Cadastro da GUI.")
    # Métodos como conferir_codigo, conferir_senha, email_valido, conferir_email, conferir_ap, cadastrar_conta
    # precisariam ser reescritos ou adaptados para uma versão GUI.
    pass

class Condominio:
    """Placeholder para a classe de Condominio original (console)."""
    def __init__(self):
        messagebox.showinfo("Info", "A classe 'Condominio' original do console não é usada diretamente na interface gráfica.")
    pass

# Estas funções de console (ranking, resgatar, calculo, feedback, deletar) foram substituídas pelas classes da GUI.
# Mantenho as definições para evitar NameErrors se alguma parte do código antigo ainda as referenciar por engano,
# mas elas não serão chamadas pela interface gráfica principal.
def ranking(email_login, senha_login):
    messagebox.showinfo("Info", "A função 'ranking' original do console não é usada diretamente na interface gráfica. Use a tela de Ranking da GUI.")
def resgatar(email_login, senha_login):
    messagebox.showinfo("Info", "A função 'resgatar' original do console não é usada diretamente na interface gráfica. Use a tela de Resgate de Pontos da GUI.")
def calculo(email_login, senha_login):
    messagebox.showinfo("Info", "A função 'calculo' original do console não é usada diretamente na interface gráfica. Use a tela de Cálculo de Pontos da GUI.")
def feedback(email_login, senha_login):
    messagebox.showinfo("Info", "A função 'feedback' original do console não é usada diretamente na interface gráfica. Use a tela de Feedback da GUI.")
import csv # Re-importar para a função salvar_feedback, se ela ainda for usada em algum lugar.
def salvar_feedback(email, senha, comentario, nota):
    messagebox.showinfo("Info", "A função 'salvar_feedback' original do console não é usada diretamente na interface gráfica. O salvamento é feito na classe TelaFeedback.")
def deletar(email_login, senha_login):
    messagebox.showinfo("Info", "A função 'deletar' original do console não é usada diretamente na interface gráfica. Use a tela de Deletar Conta da GUI.")


# ==================================================================================================
# --- Execução Principal do Aplicativo ---
# ==================================================================================================
if __name__ == "__main__":
    # Garante que os arquivos JSON/CSV necessários existam ou são criados com estruturas básicas.
    # Isso evita FileNotFoundError no primeiro uso.
    print("Verificando arquivos de dados...")
    for filename in [NOME_ARQUIVO_BANCO_DADOS, NOME_ARQUIVO_DADOS_USUARIOS, NOME_ARQUIVO_QUESTOES_QUIZ]:
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            print(f"Criando/inicializando arquivo: {filename}")
            with open(filename, 'w', encoding='utf-8') as f:
                if filename == NOME_ARQUIVO_BANCO_DADOS:
                    json.dump({"senha": {}, "familia": {}, "membros": {}, "pontos": {}, "apartamento": {}, "verificador": {}, "feedback": [], "usuarios": {}}, f, indent=4)
                elif filename == NOME_ARQUIVO_DADOS_USUARIOS:
                    json.dump({"consumo": {}, "calculo_realizado": {}}, f, indent=4)
                elif filename == NOME_ARQUIVO_QUESTOES_QUIZ:
                    # Adiciona uma questão de exemplo se o arquivo estiver vazio
                    json.dump([
                        {"pergunta": "Qual a principal fonte de água potável do planeta?", "opcoes": ["Oceanos", "Rios e Lagos", "Glaciares e calotas polares", "Água subterrânea"], "resposta_correta": "Glaciares e calotas polares"},
                        {"pergunta": "Quanto tempo dura um banho ideal para economizar água?", "opcoes": ["15 minutos", "10 minutos", "5 minutos", "Mais de 20 minutos"], "resposta_correta": "5 minutos"},
                        {"pergunta": "O que você deve fazer ao escovar os dentes para economizar água?", "opcoes": ["Deixar a torneira aberta", "Usar um copo de água e fechar a torneira", "Escovar os dentes no chuveiro", "Lavar a boca diretamente na torneira"], "resposta_correta": "Usar um copo de água e fechar a torneira"},
                        {"pergunta": "Qual a melhor forma de lavar a louça para economizar água?", "opcoes": ["Lavar com a torneira sempre aberta", "Enxaguar tudo de uma vez após ensaboar", "Usar máquina de lavar louça para poucas peças", "Lavar cada peça individualmente"], "resposta_correta": "Enxaguar tudo de uma vez após ensaboar"},
                        {"pergunta": "Qual o papel do descarte correto de lixo no combate à poluição da água?", "opcoes": ["Não tem relação", "Ajuda a poluir rios", "Impede que o lixo contamine rios e oceanos", "Apenas contribui para o entupimento de bueiros"], "resposta_correta": "Impede que o lixo contamine rios e oceanos"},
                        {"pergunta": "Quanto de água é desperdiçado por uma torneira pingando por dia?", "opcoes": ["1 litro", "10 litros", "Mais de 40 litros", "Menos de 1 litro"], "resposta_correta": "Mais de 40 litros"}
                    ], f, indent=4)
            print(f"Arquivo '{filename}' criado/inicializado com sucesso.")
        else:
            print(f"Arquivo '{filename}' já existe e não está vazio.")

    # Cria o arquivo CSV para feedback se não existir ou estiver vazio
    if not os.path.exists(NOME_ARQUIVO_FEEDBACK_CSV) or os.path.getsize(NOME_ARQUIVO_FEEDBACK_CSV) == 0:
        print(f"Criando/inicializando arquivo: {NOME_ARQUIVO_FEEDBACK_CSV}")
        with open(NOME_ARQUIVO_FEEDBACK_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['email', 'comentario', 'nota']) # Escreve o cabeçalho
        print(f"Arquivo '{NOME_ARQUIVO_FEEDBACK_CSV}' criado/inicializado com sucesso.")
    else:
        print(f"Arquivo '{NOME_ARQUIVO_FEEDBACK_CSV}' já existe e não está vazio.")

    # Inicia a aplicação CustomTkinter
    app = App()
    app.mainloop()
import customtkinter as ctk
from PIL import Image
import json
import csv
import time
import re
import random
from datetime import datetime, timedelta

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

# Lista de prêmios disponíveis (pode ser carregada de um JSON ou CSV também)
premios_disponiveis = [
    {"nome": "Voucher de R$20 em delivery", "custo": 200},
    {"nome": "Desconto de 10% na conta de água", "custo": 500},
    {"nome": "Kit de sementes para horta caseira", "custo": 150},
    {"nome": "E-book sobre sustentabilidade", "custo": 100},
    {"nome": "Doação de 50L de água para causas sociais", "custo": 250},
    {"nome": "Copo reutilizável EcoDrop", "custo": 300}
]

# Inicializa as estruturas de dados globais
dados_conta = {}
dados_familia = {}
dados_quantidade = {}
dados_pontos = {}
dados_apartamento = {}
dados_codigov = {}
dados_questoes_quiz = []
dados_ultimo_quiz = {}


# Tenta carregar os dados do arquivo JSON
try:
    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
        # Quando json.load é usado, o arquivo JSON é transformado em um dicionário Python
        """
        O objetivo desta parte do código é abrir o arquivo JSON e salvar os dicionários em Python, facilitando a manipulação.
        """
        arquivo_lido = json.load(arquivo)
        dados_conta = arquivo_lido.get("senha", {})
        dados_familia = arquivo_lido.get("familia", {})
        dados_quantidade = arquivo_lido.get("membros", {})
        dados_pontos = arquivo_lido.get("pontos", {})
        dados_apartamento = arquivo_lido.get("apartamento", {})
        dados_codigov = arquivo_lido.get("verificador", {})
        dados_questoes_quiz = arquivo_lido.get("questoes_quiz", [])
        dados_ultimo_quiz = arquivo_lido.get("ultimo_quiz", {})

except FileNotFoundError:
    # Se o arquivo não existir, cria um com a estrutura básica
    print("WARNING: banco_dados.JSON não encontrado. Criando novo arquivo.")
    with open(r"banco_dados.JSON", "w", encoding="utf-8") as arquivo:
        json.dump({"senha": {}, "familia": {}, "membros": {}, "pontos": {}, "apartamento": {}, "verificador": {}, "questoes_quiz": [], "ultimo_quiz": {}}, arquivo, indent=4, ensure_ascii=False)
except json.JSONDecodeError:
    # Se o arquivo JSON estiver vazio ou malformado, inicializa com dados vazios
    print("WARNING: banco_dados.JSON está vazio ou malformado. Inicializando com dados vazios.")
    with open(r"banco_dados.JSON", "w", encoding="utf-8") as arquivo:
        json.dump({"senha": {}, "familia": {}, "membros": {}, "pontos": {}, "apartamento": {}, "verificador": {}, "questoes_quiz": [], "ultimo_quiz": {}}, arquivo, indent=4, ensure_ascii=False)


# Função para permitir apenas a digitação de números
def validar_numeros(novo_texto):
    """Função utilizada para permitir que o usuário digite apenas números, melhorando o tratamento de erros."""
    return novo_texto.isdigit() or novo_texto == ""

# Função para permitir apenas a digitação de letras e espaços
def validar_letras_espacos(novo_texto):
    """Função utilizada para permitir que o usuário digite apenas letras e espaços, melhorando o tratamento de erros."""
    return all(c.isalpha() or c.isspace() for c in novo_texto) or novo_texto == ""

def aviso_sistema():
    """Função utilizada para exibir o frame_aviso, que aparecerá apenas se o cadastro for concluído com sucesso."""
    frame_cadastro.pack_forget()
    frame_aviso.pack(fill="both", expand=True)

def voltar_inicial():
    """Função utilizada para retornar à tela inicial, caso o usuário tenha entrado na opção errada."""
    # Oculta todos os frames de funcionalidade
    frame_cadastro.pack_forget()
    frame_login.pack_forget()
    frame_adm.pack_forget()
    frame_sobrenos.pack_forget()
    frame_aviso.pack_forget()

    # Reexibe os frames iniciais
    frame_topo.pack(fill="x")
    frame_conteudo.pack(fill="both", expand=True)
    frame_lateral.pack(side="left", fill="y")
    frame_principal.pack(side="right", fill="both", expand=True, padx=30, pady=30)
    frame_rodape.pack(fill="x", side="bottom")


def mostrar_login():
    """Função utilizada para exibir o frame de login."""
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget()
    frame_aviso.pack_forget() # Oculta o frame de aviso se estiver visível
    frame_login.pack(fill="both", expand=True)
    label_avisologin.configure(text=" ", text_color="blue") # Limpa mensagens anteriores
    entrada_emaillogin.delete(0, ctk.END) # Limpa o campo de email
    entrada_senhalogin.delete(0, ctk.END) # Limpa o campo de senha


def conferir_logar(entrada_emaillogin, entrada_senhalogin):
    """Função utilizada para verificar se há campos em branco ao clicar no botão de login."""
    email = entrada_emaillogin.get().strip()
    senha = entrada_senhalogin.get().strip()
    if email == "" or senha == "":
        label_avisologin.configure(text="Preencha todos os campos.", text_color="red")
        return

    login(email, senha, label_avisologin)

def login(email, senha, label_avisologin):
    """Função utilizada para verificar se o email e a senha estão corretos, e então navegar para o menu principal."""
    global dados_conta # Garante acesso global aos dados atualizados

    try:
        with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
            arquivo_lido = json.load(arquivo)
            dados_conta = arquivo_lido.get("senha", {})
    except Exception as e:
        label_avisologin.configure(text=f"Erro ao carregar dados: {e}", text_color="red")
        return

    if email in dados_conta:
        if dados_conta[email] == senha:
            mostrar_menu(email, senha)
            return
        else:
            label_avisologin.configure(text="EMAIL OU SENHA INCORRETO.\nContate o suporte para recuperar sua senha", text_color="red")
            return
    else:
        label_avisologin.configure(text="EMAIL NÃO CADASTRADO.\nVá para a tela de cadastro", text_color="red")
        return

def mostrar_cadastro():
    """Função utilizada para exibir o frame de cadastro."""
    # Oculta os frames principais
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget()
    frame_aviso.pack_forget() # Oculta o frame de aviso se estiver visível

    frame_cadastro.pack(fill="both", expand=True)
    label_aviso.configure(text=" ", text_color="blue") # Limpa mensagens anteriores
    # Limpa os campos de entrada
    entrada_email.delete(0, ctk.END)
    entrada_nome.delete(0, ctk.END)
    entrada_senha.delete(0, ctk.END)
    entrada_qmembros.delete(0, ctk.END)
    entrada_numeroap.delete(0, ctk.END)
    entrada_verificador.delete(0, ctk.END)


def conferir_cadastrar(entrada_email_widget, entrada_nome_widget, entrada_senha_widget,
                        entrada_qmembros_widget, entrada_numeroap_widget, entrada_verificador_widget, label_aviso_widget):
    """
    Esta função verifica se os campos de entrada estão preenchidos corretamente
    e chama a classe Cadastro para registrar a conta.
    """
    email = entrada_email_widget.get().strip()
    nome_familia = entrada_nome_widget.get().strip()
    senha = entrada_senha_widget.get().strip()
    quantidade_pessoas_str = entrada_qmembros_widget.get().strip()
    apartamento_str = entrada_numeroap_widget.get().strip()
    verificador = entrada_verificador_widget.get().strip()

    # Verificação inicial para campos vazios
    if not email or not nome_familia or not senha or not quantidade_pessoas_str or not apartamento_str or not verificador:
        label_aviso_widget.configure(text="Todos os campos devem ser preenchidos.", text_color="red")
        return

    try:
        quantidade_pessoas = int(quantidade_pessoas_str)
        apartamento = int(apartamento_str)
    except ValueError:
        label_aviso_widget.configure(text="Quantidade de membros e Apartamento devem ser números.", text_color="red")
        return

    # Validação do comprimento da senha
    if not (4 <= len(senha) <= 20):
        label_aviso_widget.configure(text="A senha deve ter entre 4 e 20 caracteres.", text_color="red")
        return

    # Validação do comprimento do código verificador
    if not (4 <= len(verificador) <= 20):
        label_aviso_widget.configure(text="O código verificador deve ter entre 4 e 20 caracteres.", text_color="red")
        return

    # Cria o objeto Cadastro, que lida com validações adicionais e salvamento
    Cadastro(email, quantidade_pessoas, senha, nome_familia, apartamento, verificador, label_aviso_widget)


def modo_adm():
    """Função utilizada para exibir o frame_adm, quando o usuário desejar entrar no modo administrador."""
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget()
    frame_adm.pack(fill="both", expand=True)


def entrar_modoadm():
    """Lógica para entrar no modo administrador. A ser implementada."""
    print("Entrar modo ADM - Lógica a ser implementada")
    pass


def sobre_nos():
    """Função utilizada para exibir o frame_sobrenos (Contando a história do projeto EcoDrop)."""
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget()
    frame_sobrenos.pack(fill="both", expand=True)


def mostrar_menu(email, senha):
    """Função utilizada para exibir o frame_menu, onde o usuário verá as funcionalidades disponíveis do programa."""
    # Destrói todos os widgets da janela principal para recriar o menu
    for widget in janela.winfo_children():
        widget.destroy()

    # Frame principal que envolve o menu lateral e o conteúdo dinâmico
    frame_menu = ctk.CTkFrame(janela, fg_color="#ffffff")

    # Topo do sistema com título
    frame_topo_menu = ctk.CTkFrame(frame_menu, fg_color="#1A73E8", height=80)
    frame_topo_menu.pack(fill="x")

    titulo = ctk.CTkLabel(frame_topo_menu, text="EcoDrop", fg_color="#1A73E8", text_color="white",
                              font=("Arial", 24, "bold"))
    titulo.pack(pady=20)

    # Menu lateral
    frame_lateral_menu = ctk.CTkFrame(frame_menu, fg_color="white", width=200)
    frame_lateral_menu.pack(side="left", fill="y")

    # Frame de conteúdo principal (onde as funcionalidades serão exibidas)
    frame_conteudo_menu = ctk.CTkFrame(frame_menu, fg_color="#f0f2f5")
    frame_conteudo_menu.pack(fill="both", expand=True)

    # Frame principal para o conteúdo dinâmico do menu
    frame_principalmenu = ctk.CTkFrame(frame_conteudo_menu, fg_color="#ffffff")
    frame_principalmenu.pack(fill="both", expand=True, padx=30, pady=30)

    # Função auxiliar para redefinir o conteúdo do frame principal do menu para a vista padrão de boas-vindas
    def reset_principal_menu_content():
        for widget in frame_principalmenu.winfo_children():
            widget.destroy()

        texto_bem_vindo = ctk.CTkLabel(frame_principalmenu, text="Bem-vindo ao EcoDrop",
                                         fg_color="#ffffff", text_color="#202124", font=("Arial", 18, "bold"))
        texto_bem_vindo.pack(pady=(0, 20))

        texto_instrucao = ctk.CTkLabel(frame_principalmenu,
                                         text=random.choice(mensagens_agua),
                                         fg_color="#ffffff", text_color="#5f6368",
                                         wraplength=500, justify="left", font=("Arial", 12))
        texto_instrucao.pack()

        imagem_menu_principal = Image.open("fotos/mascoteprincipall.png")
        ctk_imagem_menu_principal = ctk.CTkImage(light_image=imagem_menu_principal, dark_image=imagem_menu_principal, size=(400, 400))

        label_menu_principal_image = ctk.CTkLabel(frame_principalmenu, image=ctk_imagem_menu_principal, text="")
        label_menu_principal_image.pack()


    # ---- Botões do Menu Lateral ----
    # Cada botão chama sua respectiva função, passando o frame_principalmenu e a função de reset como callback
    botao1 = ctk.CTkButton(frame_lateral_menu, text="🏆 Ranking mensal", fg_color="white", text_color="#1A73E8",
                            font=("Arial", 12), anchor="w",
                            command=lambda: mostrar_ranking(email, senha, frame_principalmenu, reset_principal_menu_content), cursor="hand2")
    botao1.pack(fill="x", pady=(20, 10), padx=20)

    botao2 = ctk.CTkButton(frame_lateral_menu, text="🎁 Resgatar prêmios", fg_color="white", text_color="#1A73E8",
                            font=("Arial", 12), anchor="w",
                            command=lambda: resgatar_premio(email, senha, frame_principalmenu, reset_principal_menu_content), cursor="hand2")
    botao2.pack(fill="x", pady=10, padx=20)

    botao3 = ctk.CTkButton(frame_lateral_menu, text="🧮 Cálculo de pontos", fg_color="white", text_color="#1A73E8",
                            font=("Arial", 12), anchor="w",
                            command=lambda: calculo_pontuacao(email, senha, frame_principalmenu, reset_principal_menu_content), cursor="hand2")
    botao3.pack(fill="x", pady=10, padx=20)

    botao4 = ctk.CTkButton(frame_lateral_menu, text="🧠 Quiz semanal", fg_color="white", text_color="#1A73E8",
                            font=("Arial", 12), anchor="w",
                            command=lambda: quiz_semanal(email, senha, frame_principalmenu, reset_principal_menu_content), cursor="hand2")
    botao4.pack(fill="x", pady=10, padx=20)

    botao5 = ctk.CTkButton(frame_lateral_menu, text="📘 Área educativa", fg_color="white", text_color="#1A73E8",
                            font=("Arial", 12), anchor="w",
                            command=lambda: area_educativa(email, senha, frame_menu), cursor="hand2")
    botao5.pack(fill="x", pady=10, padx=20)

    botao6 = ctk.CTkButton(frame_lateral_menu, text="📊 Mostrar dados", fg_color="white", text_color="#1A73E8",
                            font=("Arial", 12), anchor="w",
                            command=lambda: mostrar_dados(email, senha, frame_principalmenu, reset_principal_menu_content), cursor="hand2")
    botao6.pack(fill="x", pady=10, padx=20)

    botao7 = ctk.CTkButton(frame_lateral_menu, text="🔄 Atualizar dados", fg_color="white", text_color="#1A73E8",
                            font=("Arial", 12), anchor="w",
                            command=lambda: atualizar_dados(email, senha, frame_principalmenu, reset_principal_menu_content), cursor="hand2")
    botao7.pack(fill="x", pady=10, padx=20)

    botao8 = ctk.CTkButton(frame_lateral_menu, text="🗑 Deletar conta", fg_color="white", text_color="#1A73E8",
                            font=("Arial", 12), anchor="w",
                            command=lambda: deletar_conta(email, senha, frame_principalmenu, reset_principal_menu_content), cursor="hand2")
    botao8.pack(fill="x", pady=10, padx=20)

    botao9 = ctk.CTkButton(frame_lateral_menu, text="✍️ Enviar feedback", fg_color="white", text_color="#1A73E8",
                            font=("Arial", 12), anchor="w",
                            command=lambda: feedback(email, senha, frame_principalmenu, reset_principal_menu_content), cursor="hand2")
    botao9.pack(fill="x", pady=10, padx=20)

    # Conteúdo inicial para o frame_principalmenu
    reset_principal_menu_content()

    # Frame do rodapé
    frame_rodape_menu = ctk.CTkFrame(frame_menu, fg_color="#f0f0f0", height=30)
    frame_rodape_menu.pack(fill="x", side="bottom")

    texto_rodape_menu = ctk.CTkLabel(
    frame_rodape_menu, text="Versão 2.0 • Suporte: ecodropsuporte@gmail.com", text_color="#5f6368", font=("Arial", 10))
    texto_rodape_menu.pack()

    frame_menu.pack(fill="both", expand=True)


def mostrar_dados(email, senha, frame_principalmenu, reset_callback):
    """
    📊 Função: Mostrar Dados
    Exibe os principais dados da conta do usuário (exceto senha e código verificador por segurança).
    Utilizada para que o usuário possa revisar as informações do seu cadastro.
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="📊 Seus Dados",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    global dados_familia, dados_quantidade, dados_pontos, dados_apartamento # Acessa dados globais

    user_family = dados_familia.get(email, "N/A")
    user_members = dados_quantidade.get(email, "N/A")
    user_points = dados_pontos.get(email, "N/A")
    user_apartment = dados_apartamento.get(email, "N/A")

    data_text = f"""
    Email: {email}
    Nome da Família: {user_family}
    Membros da Família: {user_members}
    Pontos Acumulados: {user_points}
    Número do Apartamento: {user_apartment}
    """
    ctk.CTkLabel(frame_principalmenu, text=data_text,
                 font=("Arial", 14), text_color="#333333", justify="left").pack(pady=10)

    botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar.pack(pady=20)


def atualizar_dados(email, senha, frame_principalmenu, reset_callback):
    """
    🔄 Função: Atualizar Dados
    Permite ao usuário atualizar o nome da família, quantidade de membros e senha.
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="🔄 Atualizar Dados",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    # Carrega dados atuais
    global dados_familia, dados_quantidade, dados_conta
    nome_atual = dados_familia.get(email, "")
    membros_atuais = dados_quantidade.get(email, "")

    ctk.CTkLabel(frame_principalmenu, text="Preencha os campos que deseja atualizar:",
                 font=("Arial", 14), text_color="#333333").pack(pady=(0, 10))

    # Campo Nome da Família
    label_nome_familia = ctk.CTkLabel(frame_principalmenu, text="Nome da Família:",
                                       font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
    label_nome_familia.pack(fill="x", padx=50, pady=(10, 0))
    entrada_nome_familia = ctk.CTkEntry(frame_principalmenu, width=300)
    entrada_nome_familia.insert(0, nome_atual)
    entrada_nome_familia.pack(padx=50, pady=(0, 10))

    # Campo Quantidade de Membros
    label_membros = ctk.CTkLabel(frame_principalmenu, text="Quantidade de Membros:",
                                  font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
    label_membros.pack(fill="x", padx=50, pady=(10, 0))
    entrada_membros = ctk.CTkEntry(frame_principalmenu, width=300, validate="key",
                                   validatecommand=(janela.register(validar_numeros), "%P"))
    entrada_membros.insert(0, str(membros_atuais))
    entrada_membros.pack(padx=50, pady=(0, 10))

    # Campo Nova Senha (opcional)
    label_nova_senha = ctk.CTkLabel(frame_principalmenu, text="Nova Senha (deixe em branco para não alterar):",
                                     font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
    label_nova_senha.pack(fill="x", padx=50, pady=(10, 0))
    entrada_nova_senha = ctk.CTkEntry(frame_principalmenu, width=300, show="*")
    entrada_nova_senha.pack(padx=50, pady=(0, 10))

    label_mensagem_atualizar = ctk.CTkLabel(frame_principalmenu, text="", text_color="red", font=("Arial", 12))
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
            with open(r"banco_dados.JSON", "r+", encoding="utf-8") as f:
                data = json.load(f)

                data["familia"][email] = novo_nome
                data["membros"][email] = nova_qtde_membros
                if nova_senha: # Só atualiza a senha se um novo valor for fornecido
                    data["senha"][email] = nova_senha

                # Atualiza as variáveis globais
                dados_familia[email] = novo_nome
                dados_quantidade[email] = nova_qtde_membros
                if nova_senha:
                    dados_conta[email] = nova_senha

                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()
            label_mensagem_atualizar.configure(text="Dados atualizados com sucesso!", text_color="green")
            entrada_nova_senha.delete(0, ctk.END) # Limpa o campo da senha após a atualização
        except Exception as e:
            label_mensagem_atualizar.configure(text=f"Erro ao atualizar dados: {e}", text_color="red")

    botao_salvar = ctk.CTkButton(frame_principalmenu, text="Salvar Atualizações",
                                 fg_color="#1A73E8", text_color="white",
                                 command=salvar_atualizacao_acao)
    botao_salvar.pack(pady=10)

    botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar.pack(pady=20)


def deletar_conta(email, senha, frame_principalmenu, reset_callback):
    """
    🗑 Função: Deletar Conta
    Permite ao usuário excluir sua conta permanentemente do sistema.
    Após a confirmação, os dados são removidos e o usuário precisará se cadastrar novamente.
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="🗑 Deletar Conta",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    label_confirmacao = ctk.CTkLabel(frame_principalmenu, text="ATENÇÃO: Esta ação é irreversível!\nDeseja realmente deletar sua conta?",
                                      font=("Arial", 14, "bold"), text_color="red")
    label_confirmacao.pack(pady=20)

    def confirmar_delecao_action():
        global dados_conta, dados_familia, dados_quantidade, dados_pontos, dados_apartamento, dados_codigov, dados_ultimo_quiz
        try:
            with open(r"banco_dados.JSON", "r+", encoding="utf-8") as arquivo:
                data = json.load(arquivo)
                if email in data["senha"]:
                    del data["senha"][email]
                    del data["familia"][email]
                    del data["membros"][email]
                    del data["pontos"][email]
                    del data["apartamento"][email]
                    del data["verificador"][email]
                    if email in data["ultimo_quiz"]: # Remove o registro do quiz também
                        del data["ultimo_quiz"][email]


                    # Atualiza os dicionários globais para refletir as mudanças imediatamente
                    dados_conta = data.get("senha", {})
                    dados_familia = data.get("familia", {})
                    dados_quantidade = data.get("membros", {})
                    dados_pontos = data.get("pontos", {})
                    dados_apartamento = data.get("apartamento", {})
                    dados_codigov = data.get("verificador", {})
                    dados_ultimo_quiz = data.get("ultimo_quiz", {})


                    arquivo.seek(0)  # Volta para o início do arquivo
                    json.dump(data, arquivo, indent=4, ensure_ascii=False)
                    arquivo.truncate() # Remove o restante do arquivo

                    label_confirmacao.configure(text="Sua conta foi deletada com sucesso.", text_color="green")
                    # Após a exclusão, desloga e vai para a tela inicial
                    janela.after(1000, lambda: voltar_inicial()) # Atraso para a mensagem ser visível
                else:
                    label_confirmacao.configure(text="Erro: Conta não encontrada.", text_color="red")
        except Exception as e:
            label_confirmacao.configure(text=f"Erro ao deletar conta: {e}", text_color="red")


    botao_confirmar_delecao = ctk.CTkButton(frame_principalmenu, text="Confirmar Deleção",
                                           fg_color="red", hover_color="#cc0000",
                                           command=confirmar_delecao_action)
    botao_confirmar_delecao.pack(pady=10)

    botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar.pack(pady=20)


def feedback(email, senha, frame_principalmenu, reset_callback):
    """
    ✍️ Função: Feedback
    Permite ao usuário enviar uma opinião com até 140 caracteres e uma nota de 0 a 10.
    Serve para avaliar o sistema e coletar sugestões de melhoria.
    """
    # Limpa os widgets existentes no frame de conteúdo principal
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="✍️ Enviar Feedback",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    label_instrucao = ctk.CTkLabel(frame_principalmenu, text="Por favor, deixe sua opinião sobre o sistema EcoDrop:",
                                    font=("Arial", 14), text_color="#333333")
    label_instrucao.pack(pady=(0, 10))

    # Campo de Entrada de Texto do Feedback
    label_feedback_texto = ctk.CTkLabel(frame_principalmenu, text="Seu Feedback (até 140 caracteres):",
                                         font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
    label_feedback_texto.pack(fill="x", padx=50, pady=(10, 0))
    entrada_feedback = ctk.CTkEntry(frame_principalmenu, width=400, height=80)
    entrada_feedback.pack(padx=50, pady=(0, 10))

    # Escala de Avaliação
    label_nota = ctk.CTkLabel(frame_principalmenu, text="Sua nota para o sistema (0 a 10):",
                              font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
    label_nota.pack(fill="x", padx=50, pady=(10, 0))
    entrada_nota = ctk.CTkEntry(frame_principalmenu, width=100, validate="key",
                                validatecommand=(janela.register(lambda text: text.isdigit() and (len(text) <= 2 and (int(text) >= 0 and int(text) <= 10) if text.strip() else True) or text == ""), "%P"))
    entrada_nota.pack(padx=50, pady=(0, 20), anchor="w")

    # Label para mensagens de validação
    label_mensagem_feedback = ctk.CTkLabel(frame_principalmenu, text="", text_color="red", font=("Arial", 12))
    label_mensagem_feedback.pack(pady=(0, 10))

    def enviar_feedback_acao():
        feedback_text = entrada_feedback.get().strip()
        nota_text = entrada_nota.get().strip()

        if not feedback_text or not nota_text:
            label_mensagem_feedback.configure(text="Por favor, preencha todos os campos.", text_color="red")
            return

        try:
            nota = int(nota_text)
            if not (0 <= nota <= 10):
                label_mensagem_feedback.configure(text="A nota deve ser entre 0 e 10.", text_color="red")
                return
        except ValueError:
            label_mensagem_feedback.configure(text="A nota deve ser um número inteiro.", text_color="red")
            return

        if len(feedback_text) > 140:
            label_mensagem_feedback.configure(text="O feedback não pode exceder 140 caracteres.", text_color="red")
            return

        try:
            with open("feedback.csv", "a+", newline="", encoding="utf-8") as f: # Usa "a+" para ler e anexar
                f.seek(0) # Move para o início do arquivo para verificar seu tamanho
                is_empty = f.read() == ''
                if is_empty: # Se o arquivo estiver vazio, escreve o cabeçalho
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(["Email", "Feedback", "Nota", "Data/Hora"])
                # Escreve os dados
                csv_writer = csv.writer(f) # Re-cria o writer para a posição atual
                csv_writer.writerow([email, feedback_text, nota, time.strftime("%Y-%m-%d %H:%M:%S")])
            label_mensagem_feedback.configure(text="Feedback enviado com sucesso! Agradecemos sua colaboração.", text_color="green")
            entrada_feedback.delete(0, ctk.END)
            entrada_nota.delete(0, ctk.END)
        except Exception as e:
            label_mensagem_feedback.configure(text=f"Erro ao salvar feedback: {e}", text_color="red")


    botao_enviar = ctk.CTkButton(frame_principalmenu, text="Enviar Feedback",
                                 fg_color="#1A73E8", text_color="white",
                                 command=enviar_feedback_acao)
    botao_enviar.pack(pady=10)

    botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar.pack(pady=20)


def calculo_pontuacao(email, senha, frame_principalmenu, reset_callback):
    """
    🧮 Função: Cálculo de Pontos
    Calcula pontos com base nos litros economizados, número de moradores e consumo médio.
    Os pontos são convertidos em benefícios (ex: vouchers, descontos, milhas).
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="🧮 Cálculo de Pontos",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    ctk.CTkLabel(frame_principalmenu, text="Informe seu consumo diário (em litros) para calcular pontos:",
                 font=("Arial", 14), text_color="#333333").pack(pady=(0, 10))

    label_consumo = ctk.CTkLabel(frame_principalmenu, text="Consumo Diário (Litros):",
                                  font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
    label_consumo.pack(fill="x", padx=50, pady=(10, 0))

    entrada_consumo = ctk.CTkEntry(frame_principalmenu, width=200, validate="key",
                                   validatecommand=(janela.register(validar_numeros), "%P"))
    entrada_consumo.pack(padx=50, pady=(0, 10), anchor="w")

    label_resultado_pontos = ctk.CTkLabel(frame_principalmenu, text="", font=("Arial", 14, "bold"), text_color="green")
    label_resultado_pontos.pack(pady=(10, 0))

    label_mensagem_calculo = ctk.CTkLabel(frame_principalmenu, text="", text_color="red", font=("Arial", 12))
    label_mensagem_calculo.pack(pady=(0, 10))

    def calcular_pontos_acao():
        consumo_str = entrada_consumo.get().strip()
        if not consumo_str:
            label_mensagem_calculo.configure(text="Por favor, insira o consumo diário.", text_color="red")
            return

        try:
            consumo_diario = int(consumo_str)
            if consumo_diario < 0:
                label_mensagem_calculo.configure(text="O consumo não pode ser negativo.", text_color="red")
                return

            global dados_pontos, dados_quantidade # Acessa pontos e quantidade de membros
            membros = dados_quantidade.get(email, 1) # Pega a quantidade de membros, padrão 1 se não encontrar

            # Lógica de cálculo de pontos simplificada:
            # Consumo ideal per capita (ex: 100 litros/dia)
            consumo_ideal_total = 100 * membros
            pontos_ganhos = 0

            if consumo_diario < consumo_ideal_total:
                litros_economizados = consumo_ideal_total - consumo_diario
                pontos_ganhos = int(litros_economizados / 10) # 1 ponto a cada 10 litros economizados

            if pontos_ganhos > 0:
                dados_pontos[email] = dados_pontos.get(email, 0) + pontos_ganhos
                # Atualiza o JSON com os novos pontos
                try:
                    with open(r"banco_dados.JSON", "r+", encoding="utf-8") as f:
                        data = json.load(f)
                        data["pontos"][email] = dados_pontos[email]
                        f.seek(0)
                        json.dump(data, f, indent=4, ensure_ascii=False)
                        f.truncate()
                    label_resultado_pontos.configure(text=f"Parabéns! Você ganhou {pontos_ganhos} pontos. Total: {dados_pontos[email]}", text_color="green")
                    label_mensagem_calculo.configure(text="")
                except Exception as e:
                    label_mensagem_calculo.configure(text=f"Erro ao salvar pontos: {e}", text_color="red")
            else:
                label_resultado_pontos.configure(text="Nenhum ponto ganho desta vez. Continue economizando!", text_color="#5f6368")
                label_mensagem_calculo.configure(text="Seu consumo foi maior ou igual ao ideal. Tente reduzir mais!", text_color="orange")

        except ValueError:
            label_mensagem_calculo.configure(text="Consumo diário deve ser um número válido.", text_color="red")

    botao_calcular = ctk.CTkButton(frame_principalmenu, text="Calcular Pontos",
                                   fg_color="#1A73E8", text_color="white",
                                   command=calcular_pontos_acao)
    botao_calcular.pack(pady=10)

    botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar.pack(pady=20)


def resgatar_premio(email, senha, frame_principalmenu, reset_callback):
    """
    🎁 Função: Resgatar Prêmios
    Permite ao usuário resgatar recompensas usando seus pontos acumulados.
    Verifica se o saldo é suficiente antes de confirmar o resgate.
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="🎁 Resgatar Prêmios",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    global dados_pontos # Acessa os pontos globais para mostrar o saldo atual

    pontos_atuais = dados_pontos.get(email, 0)
    label_pontos_saldo = ctk.CTkLabel(frame_principalmenu, text=f"Seus pontos atuais: {pontos_atuais} 🌟",
                                       font=("Arial", 16, "bold"), text_color="#28a745")
    label_pontos_saldo.pack(pady=(0, 20))

    label_instrucao = ctk.CTkLabel(frame_principalmenu, text="Escolha um prêmio para resgatar:",
                                    font=("Arial", 14), text_color="#333333")
    label_instrucao.pack(pady=(0, 10))

    # Frame para os prêmios com scroll
    scroll_frame = ctk.CTkScrollableFrame(frame_principalmenu, width=500, height=300, fg_color="#f8f9fa")
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
                                       command=lambda p=premio: realizar_resgate(email, p, label_pontos_saldo, frame_principalmenu, reset_callback))
        botao_resgatar.pack(side="right", padx=10, pady=5)

    label_mensagem_resgate = ctk.CTkLabel(frame_principalmenu, text="", text_color="red", font=("Arial", 12))
    label_mensagem_resgate.pack(pady=(10, 0))

    def realizar_resgate(email_usuario, premio_selecionado, label_saldo, main_frame, reset_cb):
        global dados_pontos

        pontos_disp = dados_pontos.get(email_usuario, 0)
        custo_premio = premio_selecionado["custo"]

        if pontos_disp >= custo_premio:
            dados_pontos[email_usuario] -= custo_premio
            # Atualiza o arquivo JSON
            try:
                with open(r"banco_dados.JSON", "r+", encoding="utf-8") as f:
                    data = json.load(f)
                    data["pontos"][email_usuario] = dados_pontos[email_usuario]
                    f.seek(0)
                    json.dump(data, f, indent=4, ensure_ascii=False)
                    f.truncate()
                label_mensagem_resgate.configure(text=f"Prêmio '{premio_selecionado['nome']}' resgatado com sucesso!", text_color="green")
                label_saldo.configure(text=f"Seus pontos atuais: {dados_pontos[email_usuario]} 🌟") # Atualiza o saldo na GUI
            except Exception as e:
                label_mensagem_resgate.configure(text=f"Erro ao salvar: {e}", text_color="red")
        else:
            label_mensagem_resgate.configure(text="Pontos insuficientes para resgatar este prêmio.", text_color="red")
        
        # Pode adicionar um log de resgate de prêmios aqui, se desejar.

    botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar.pack(pady=20)


def mostrar_ranking(email, senha, frame_principalmenu, reset_callback):
    """
    🏆 Função: Ranking Mensal
    Exibe uma lista com as famílias que mais economizaram água no mês, ordenada por pontos.
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="🏆 Ranking Mensal",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    global dados_pontos, dados_familia # Acessa os dados globais

    # Carrega dados atualizados do JSON para garantir consistência
    try:
        with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
            arquivo_lido = json.load(arquivo)
            dados_pontos = arquivo_lido.get("pontos", {})
            dados_familia = arquivo_lido.get("familia", {})
    except Exception as e:
        ctk.CTkLabel(frame_principalmenu, text=f"Erro ao carregar dados do ranking: {e}", text_color="red").pack()
        botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white", command=reset_callback)
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
        ctk.CTkLabel(frame_principalmenu, text="Nenhum dado de ranking disponível.",
                     font=("Arial", 14), text_color="#5f6368").pack(pady=10)
    else:
        # Cria um cabeçalho para a tabela do ranking
        header_frame = ctk.CTkFrame(frame_principalmenu, fg_color="transparent")
        header_frame.pack(fill="x", padx=50, pady=(10, 5))
        ctk.CTkLabel(header_frame, text="Posição", font=("Arial", 12, "bold"), width=80).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Família", font=("Arial", 12, "bold"), width=200).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Pontos", font=("Arial", 12, "bold"), width=100).pack(side="left", padx=5)

        for i, item in enumerate(ranking_data):
            row_frame = ctk.CTkFrame(frame_principalmenu, fg_color="#f9f9f9" if i % 2 == 0 else "#ffffff")
            row_frame.pack(fill="x", padx=50, pady=2)
            ctk.CTkLabel(row_frame, text=f"{i+1}º", width=80).pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=item["familia"], width=200).pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=item["pontos"], width=100).pack(side="left", padx=5)

    botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar.pack(pady=20)


def quiz_semanal(email, senha, frame_principalmenu, reset_callback):
    """
    🧠 Função: Quiz Semanal
    Disponibiliza 5 questões toda segunda-feira. Dependendo do desempenho, o usuário recebe pontos.
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="🧠 Quiz Semanal",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    global dados_pontos, dados_questoes_quiz, dados_ultimo_quiz

    # Carrega questões e último quiz do JSON (garante que os dados estão atualizados)
    try:
        with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
            arquivo_lido = json.load(arquivo)
            questoes_disponiveis = arquivo_lido.get("questoes_quiz", [])
            dados_ultimo_quiz = arquivo_lido.get("ultimo_quiz", {})
            dados_pontos = arquivo_lido.get("pontos", {}) # Garante que os pontos globais estão atualizados
    except Exception as e:
        ctk.CTkLabel(frame_principalmenu, text=f"Erro ao carregar questões do quiz: {e}", text_color="red").pack()
        botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white", command=reset_callback)
        botao_voltar.pack(pady=20)
        return

    data_atual = datetime.now().date() # Data atual sem a hora
    data_ultimo_quiz_str = dados_ultimo_quiz.get(email)
    
    pode_fazer_quiz = True
    if data_ultimo_quiz_str:
        data_ultimo_quiz = datetime.strptime(data_ultimo_quiz_str, "%Y-%m-%d").date()
        
        # Calcula a última segunda-feira
        hoje_wday = data_atual.weekday() # 0 = segunda, 1 = terça, ..., 6 = domingo
        dias_para_ultima_segunda = hoje_wday # Se hoje for segunda (0), 0 dias. Se for terça (1), 1 dia para trás.
        ultima_segunda_feira = data_atual - timedelta(days=dias_para_ultima_segunda)

        # Se o último quiz foi feito após a última segunda-feira
        if data_ultimo_quiz >= ultima_segunda_feira:
            pode_fazer_quiz = False


    if not questoes_disponiveis or len(questoes_disponiveis) < 5:
        ctk.CTkLabel(frame_principalmenu, text="Não há questões suficientes para o quiz. Contate o administrador.",
                     font=("Arial", 14), text_color="red").pack(pady=10)
        botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white", command=reset_callback)
        botao_voltar.pack(pady=20)
        return

    if not pode_fazer_quiz:
        ctk.CTkLabel(frame_principalmenu, text=f"Você já realizou o quiz esta semana. Volte na próxima segunda-feira!",
                     font=("Arial", 14), text_color="orange").pack(pady=10)
        botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                     fg_color="gray", text_color="white", command=reset_callback)
        botao_voltar.pack(pady=20)
        return

    # Selecionar 5 questões aleatórias
    questoes_para_quiz = random.sample(questoes_disponiveis, 5)
    respostas_usuario = {}
    
    current_question_index = 0
    
    question_label = ctk.CTkLabel(frame_principalmenu, text="", font=("Arial", 16, "bold"), wraplength=500, justify="left", text_color="#1A73E8")
    question_label.pack(pady=(10, 10))

    options_frame = ctk.CTkFrame(frame_principalmenu, fg_color="transparent")
    options_frame.pack(pady=(0, 20))

    quiz_message_label = ctk.CTkLabel(frame_principalmenu, text="", font=("Arial", 12), text_color="red")
    quiz_message_label.pack(pady=(0, 10))

    radio_var = ctk.StringVar(value="") # Variável para os radio buttons da questão atual

    def show_question(index):
        nonlocal current_question_index
        current_question_index = index
        
        for widget in options_frame.winfo_children():
            widget.destroy() # Limpa as opções anteriores

        radio_var.set("") # Reseta a seleção do radio button

        if index < len(questoes_para_quiz):
            question = questoes_para_quiz[index]
            question_label.configure(text=f"Questão {index + 1}: {question['pergunta']}")

            for i, option in enumerate(question['opcoes']):
                radio_button = ctk.CTkRadioButton(options_frame, text=option, variable=radio_var, value=option,
                                                  font=("Arial", 14), text_color="#333333")
                radio_button.pack(anchor="w", pady=5)
            
            # Atualiza o texto do botão "Próxima" ou "Finalizar"
            if current_question_index == len(questoes_para_quiz) - 1:
                botao_proxima.configure(text="Finalizar Quiz")
            else:
                botao_proxima.configure(text="Próxima Questão")
        else:
            calculate_score()

    def next_question():
        selected_option = radio_var.get()
        if not selected_option:
            quiz_message_label.configure(text="Por favor, selecione uma opção.", text_color="red")
            return
        
        respostas_usuario[current_question_index] = selected_option
        quiz_message_label.configure(text="")
        
        # Move para a próxima questão ou finaliza
        if current_question_index < len(questoes_para_quiz) - 1:
            show_question(current_question_index + 1)
        else:
            calculate_score()
        
    def calculate_score():
        pontuacao = 0
        for i, question in enumerate(questoes_para_quiz):
            if respostas_usuario.get(i) == question['resposta_correta']:
                pontuacao += 1

        pontos_ganhos = pontuacao * 100 # Exemplo: 100 pontos por resposta correta

        global dados_pontos, dados_ultimo_quiz
        dados_pontos[email] = dados_pontos.get(email, 0) + pontos_ganhos
        dados_ultimo_quiz[email] = data_atual.strftime("%Y-%m-%d") # Registra a data do quiz

        # Atualiza o arquivo JSON com os novos pontos e a data do último quiz
        try:
            with open(r"banco_dados.JSON", "r+", encoding="utf-8") as f:
                data = json.load(f)
                data["pontos"][email] = dados_pontos[email]
                data["ultimo_quiz"][email] = dados_ultimo_quiz[email]
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()

            # Exibe o resultado do quiz
            for widget in frame_principalmenu.winfo_children():
                widget.destroy()
            ctk.CTkLabel(frame_principalmenu, text="🎉 Quiz Concluído! 🎉", font=("Arial", 20, "bold"), text_color="#1A73E8").pack(pady=(20, 10))
            ctk.CTkLabel(frame_principalmenu, text=f"Você acertou {pontuacao} de {len(questoes_para_quiz)} questões.", font=("Arial", 16), text_color="#333333").pack(pady=5)
            ctk.CTkLabel(frame_principalmenu, text=f"Você ganhou {pontos_ganhos} pontos!", font=("Arial", 16, "bold"), text_color="green").pack(pady=5)
            ctk.CTkLabel(frame_principalmenu, text=f"Seu total de pontos agora é: {dados_pontos[email]}", font=("Arial", 14), text_color="#28a745").pack(pady=10)
            
            botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                         fg_color="gray", text_color="white", command=reset_callback)
            botao_voltar.pack(pady=20)

        except Exception as e:
            ctk.CTkLabel(frame_principalmenu, text=f"Erro ao salvar resultado do quiz: {e}", text_color="red").pack()
            botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                         fg_color="gray", text_color="white", command=reset_callback)
            botao_voltar.pack(pady=20)


    botao_proxima = ctk.CTkButton(frame_principalmenu, text="Próxima Questão",
                                   fg_color="#1A73E8", text_color="white",
                                   command=next_question)
    botao_proxima.pack(pady=10)

    # Botão de voltar que estará sempre presente durante o quiz
    botao_voltar_quiz = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar_quiz.pack(pady=20)

    show_question(current_question_index) # Inicia exibindo a primeira questão


def area_educativa(email, senha, frame_menu):
    """Função utilizada para ir para o frame_educativo (usaremos a tela inteira nesta função, por ser necessário para ter mais conteúdo.
    Onde haverá várias opções de leitura sobre assuntos de sustentabilidade)."""

    for widget in janela.winfo_children():
        widget.destroy()

    frame_topoeducativo = ctk.CTkFrame(janela, fg_color="#1A73E8", height=80)
    frame_topoeducativo.pack(fill="x")

    titulo_educativo = ctk.CTkLabel(frame_topoeducativo, text="💧 ÁREA EDUCATIVA",
                                     text_color="#ffffff", font=("Arial", 24, "bold"))
    titulo_educativo.pack(pady=20)

    frame_educativo = ctk.CTkFrame(janela, fg_color="#ffffff")
    frame_educativo.pack(fill="both", expand=True, padx=20, pady=10)

    btn1 = ctk.CTkButton(frame_educativo,
                         text="Europa investe €15 bilhões em preservação de recursos hídricos até 2027",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=lambda: area_educativa1(frame_educativo, email, senha, frame_menu))
    btn1.pack(fill="x", pady=10)

    btn2 = ctk.CTkButton(frame_educativo,
                         text="Cientistas desenvolvem tecnologia para extrair água potável do ar usando resíduos alimentares",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=lambda: area_educativa2(frame_educativo, email, senha, frame_menu))
    btn2.pack(fill="x", pady=10)

    btn3 = ctk.CTkButton(frame_educativo,
                         text="Universidade do Texas inicia construção do maior centro universitário de reúso de água dos EUA",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=lambda: area_educativa3(frame_educativo, email, senha, frame_menu))
    btn3.pack(fill="x", pady=10)

    btn4 = ctk.CTkButton(frame_educativo,
                         text="Alunos serão instruídos sobre conservação da água e limpeza do rio Ganges na Índia",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=lambda: area_educativa4(frame_educativo, email, senha, frame_menu))
    btn4.pack(fill="x", pady=10)

    btn5 = ctk.CTkButton(frame_educativo,
                         text="Impacto dos datacenters em áreas com escassez hídrica na América Latina",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=lambda: area_educativa5(frame_educativo, email, senha, frame_menu))
    btn5.pack(fill="x", pady=10)

    btn6 = ctk.CTkButton(frame_educativo,
                         text="8 filmes educativos para crianças sobre sustentabilidade",
                         fg_color="white",
                         text_color="#1A73E8",
                         font=("Arial", 12),
                         anchor="w",
                         cursor="hand2",
                         command=lambda: area_educativa6(frame_educativo, email, senha, frame_menu))
    btn6.pack(fill="x", pady=10)

    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue", # Cor alterada para consistência
                                 text_color="#ffffff", # Cor alterada para consistência
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: mostrar_menu(email, senha))
    botao_voltar.pack(pady=20)


def area_educativa1(frame_educativo, email, senha, frame_menu):
    """Exibe o conteúdo da notícia 1 na área educativa."""
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🌍 Investimento de €15 bilhões para combater a crise hídrica na Europa",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # Parágrafo da notícia
    corpo_texto = (
        "A Universidade Europeia e o Banco Europeu de Investimento anunciaram, em 7 de junho, "
        "um aporte de €15 bilhões (≈US$17bi) a projetos voltados à redução da poluição, "
        "prevenção do desperdício e fomento à inovação no setor hídrico ao longo dos próximos três anos. "
        "A ação considera a intensificação das secas e pressões agrícolas e urbanas causadas pelas mudanças climáticas. "
        "Como medida de responsabilização, o Reino Unido restringiu bônus a executivos de empresas de água que não investem "
        "o suficiente na qualidade dos corpos de água."
    )

    label_corpo = ctk.CTkLabel(frame_educativo,
                               text=corpo_texto,
                               text_color="#333333",
                               font=("Arial", 14),
                               wraplength=800,
                               justify="left")
    label_corpo.pack(pady=10)

    # Destaque: Por que isso importa?
    label_importancia = ctk.CTkLabel(frame_educativo,
                                      text="💡 Por que isso importa?",
                                      text_color="#1A73E8",
                                      font=("Arial", 20, "bold"),
                                      wraplength=800,
                                      justify="left")
    label_importancia.pack(pady=(20, 5))

    texto_importancia = (
        "Esse investimento maciço pode impulsionar tecnologias verdes, infraestrutura resiliente e processos de governança "
        "que garantam água limpa e gestão sustentável, uma virada estratégica para enfrentar a escassez hídrica em regiões vulneráveis."
    )

    label_texto_importancia = ctk.CTkLabel(frame_educativo,
                                           text=texto_importancia,
                                           text_color="#000000",
                                           font=("Arial", 14),
                                           wraplength=800,
                                           justify="left")
    label_texto_importancia.pack(pady=5)

    # Fontes
    label_fontes = ctk.CTkLabel(frame_educativo,
                                text="🔗 Fontes:",
                                text_color="#1A73E8",
                                font=("Arial", 14, "bold"),
                                wraplength=800,
                                justify="left")
    label_fontes.pack(pady=(20, 5))


    lbl = ctk.CTkLabel(frame_educativo,
                            text="• reuters.com",
                            text_color="#333333",
                            font=("Arial", 13),
                            anchor="w",
                            justify="left")
    lbl.pack()

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)


def area_educativa2(frame_educativo, email, senha, frame_menu):
    """Exibe o conteúdo da notícia 2 na área educativa."""
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🎒 Extração de água potável do ar usando alimentos",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # Parágrafo da notícia
    corpo_texto = (
        "Pesquisadores da Universidade do Texas em Austin publicaram, em abril, um método inovador para captar água do ar "
        "usando hidrogéis feitos com biomassa de resíduos alimentares e conchas. Esses materiais absorvem grandes volumes "
        "de umidade e liberam água pura com aquecimento leve. Em campo, foram obtidos 15L de água por kg de gel por dia—"
        "recuperando 95% do volume captado."
    )

    label_corpo = ctk.CTkLabel(frame_educativo,
                               text=corpo_texto,
                               text_color="#333333",
                               font=("Arial", 14),
                               wraplength=800,
                               justify="left")
    label_corpo.pack(pady=10)

    # Destaque: Impacto prático
    label_importancia = ctk.CTkLabel(frame_educativo,
                                      text="💡 Impacto prático:",
                                      text_color="#1A73E8",
                                      font=("Arial", 20, "bold"),
                                      wraplength=800,
                                      justify="left")
    label_importancia.pack(pady=(20, 5))

    texto_importancia = (
        "Trata-se de uma solução biodegradável, modular e de baixo consumo energético — ideal para comunidades rurais, "
        "irrigação localizada ou situações emergenciais em áreas carentes de infraestrutura hídrica."
    )

    label_texto_importancia = ctk.CTkLabel(frame_educativo,
                                           text=texto_importancia,
                                           text_color="#000000",
                                           font=("Arial", 14),
                                           wraplength=800,
                                           justify="left")
    label_texto_importancia.pack(pady=5)

    # Fontes
    label_fontes = ctk.CTkLabel(frame_educativo,
                                text="🔗 Fontes:",
                                text_color="#1A73E8",
                                font=("Arial", 14, "bold"),
                                wraplength=800,
                                justify="left")
    label_fontes.pack(pady=(20, 5))

    lbl = ctk.CTkLabel(frame_educativo,
                       text="• foodandwine.com",
                       text_color="#333333",
                       font=("Arial", 13),
                       anchor="w",
                       justify="left")
    lbl.pack()

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)


def area_educativa3(frame_educativo, email, senha, frame_menu):
    """Exibe o conteúdo da notícia 3 na área educativa."""
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🏗️ UT Austin constrói o maior centro universitário de reúso de água nos EUA",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # Parágrafo da notícia
    corpo_texto = (
        "Em maio, a UT anunciou a construção do WaterHub, instalação de 900m² que vai tratar até 1 milhão de galões "
        "(≈3,8 mil m³) de esgoto por dia. A previsão de operação é para o segundo semestre de 2027. O local servirá como laboratório "
        "de pesquisa prática para estudantes, integrando ensino e teste de tecnologias de reúso para aliviar sistemas municipais sobrecarregados."
    )

    label_corpo = ctk.CTkLabel(frame_educativo,
                               text=corpo_texto,
                               text_color="#333333",
                               font=("Arial", 14),
                               wraplength=800,
                               justify="left")
    label_corpo.pack(pady=10)

    # Destaque: Por que isso importa?
    label_importancia = ctk.CTkLabel(frame_educativo,
                                      text="💡 Por que isso importa?",
                                      text_color="#1A73E8",
                                      font=("Arial", 20, "bold"),
                                      wraplength=800,
                                      justify="left")
    label_importancia.pack(pady=(20, 5))

    texto_importancia = (
        "Esse centro universitário vai impulsionar a pesquisa e o desenvolvimento de tecnologias inovadoras de reúso de água, "
        "contribuindo para a sustentabilidade urbana e formação técnica avançada."
    )

    label_texto_importancia = ctk.CTkLabel(frame_educativo,
                                           text=texto_importancia,
                                           text_color="#000000",
                                           font=("Arial", 14),
                                           wraplength=800,
                                           justify="left")
    label_texto_importancia.pack(pady=5)

    # Fontes
    label_fontes = ctk.CTkLabel(frame_educativo,
                                text="🔗 Fontes:",
                                text_color="#1A73E8",
                                font=("Arial", 14, "bold"),
                                wraplength=800,
                                justify="left")
    label_fontes.pack(pady=(20, 5))

    lbl = ctk.CTkLabel(frame_educativo,
                       text="• axios.com",
                       text_color="#333333",
                       font=("Arial", 13),
                       anchor="w",
                       justify="left")
    lbl.pack()

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)


def area_educativa4(frame_educativo, email, senha, frame_menu):
    """Exibe o conteúdo da notícia 4 na área educativa."""
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(frame_educativo,
                          text="📰 Educação Ambiental na Índia: Estudantes de Uttar Pradesh se tornam embaixadores da limpeza",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # Parágrafo da notícia
    corpo_texto = (
        "Em junho de 2024, o governo do estado de Uttar Pradesh, na Índia, lançou uma iniciativa educativa para envolver os alunos "
        "das escolas públicas e privadas na conservação ambiental e limpeza do rio Ganges, um dos maiores e mais sagrados rios da Ásia. "
        "O programa inclui formação de “embaixadores estudantis da limpeza”, práticas de higiene e conservação hídrica, visitas a locais "
        "poluídos, plantio de árvores, redações, campanhas ambientais e integração da comunidade escolar e familiar."
    )

    label_corpo = ctk.CTkLabel(frame_educativo,
                               text=corpo_texto,
                               text_color="#333333",
                               font=("Arial", 14),
                               wraplength=800,
                               justify="left")
    label_corpo.pack(pady=10)

    # Destaque: Por que isso importa?
    label_importancia = ctk.CTkLabel(frame_educativo,
                                      text="💡 Por que isso importa?",
                                      text_color="#1A73E8",
                                      font=("Arial", 20, "bold"),
                                      wraplength=800,
                                      justify="left")
    label_importancia.pack(pady=(20, 5))

    texto_importancia = (
        "A iniciativa ajuda a sensibilizar jovens sobre a conservação hídrica e atitudes sustentáveis desde cedo, "
        "envolvendo também suas famílias e escolas, o que pode gerar impacto real na limpeza do Ganges e na formação de cidadãos conscientes."
    )

    label_texto_importancia = ctk.CTkLabel(frame_educativo,
                                           text=texto_importancia,
                                           text_color="#000000",
                                           font=("Arial", 14),
                                           wraplength=800,
                                           justify="left")
    label_texto_importancia.pack(pady=5)

    # Fontes
    label_fontes = ctk.CTkLabel(frame_educativo,
                                text="🔗 Fontes:",
                                text_color="#1A73E8",
                                font=("Arial", 14, "bold"),
                                wraplength=800,
                                justify="left")
    label_fontes.pack(pady=(20, 5))

    lbl = ctk.CTkLabel(frame_educativo,
                       text="• timesofindia.indiatimes.com",
                       text_color="#333333",
                       font=("Arial", 13),
                       anchor="w",
                       justify="left")
    lbl.pack()

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)


def area_educativa5(frame_educativo, email, senha, frame_menu):
    """Exibe o conteúdo da notícia 5 na área educativa."""
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(frame_educativo,
                          text="📰 Impacto dos datacenters em áreas com escassez hídrica na América Latina",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # Parágrafo da notícia
    corpo_texto = (
        "Um artigo do The Guardian chama atenção para a instalação de grandes datacenters em regiões "
        "com escassez de água no Brasil e outros países da América Latina. Um dos casos citados em Caucaia (CE) "
        "está em regiões afetadas por seca, e esses centros utilizam até 80 % da água retirada para resfriamento, "
        "gerando riscos de esgotamento de recursos hídricos locais. O texto destaca a necessidade de maior transparência, "
        "engajamento comunitário e uso de alternativas como dessalinização e reúso."
    )

    label_corpo = ctk.CTkLabel(frame_educativo,
                               text=corpo_texto,
                               text_color="#333333",
                               font=("Arial", 14),
                               wraplength=800,
                               justify="left")
    label_corpo.pack(pady=10)

    # Destaque: Por que isso importa?
    label_importancia = ctk.CTkLabel(frame_educativo,
                                      text="💡 Por que isso importa?",
                                      text_color="#1A73E8",
                                      font=("Arial", 20, "bold"),
                                      wraplength=800, justify="left")
    label_importancia.pack(pady=(20, 5))

    texto_importancia = (
        "Educação ambiental sobre impactos tecnológicos no ciclo da água.\n\n"
        "Inovação na busca por soluções de resfriamento menos dependentes de água.\n\n"
        "Reflexão sobre políticas de concessão hídrica e planejamento sustentável."
    )

    label_texto_importancia = ctk.CTkLabel(frame_educativo,
                                           text=texto_importancia,
                                           text_color="#000000",
                                           font=("Arial", 14),
                                           wraplength=800,
                                           justify="left")
    label_texto_importancia.pack(pady=5)

    # Fontes
    label_fontes = ctk.CTkLabel(frame_educativo,
                                text="🔗 Fontes:",
                                text_color="#1A73E8",
                                font=("Arial", 14, "bold"),
                                wraplength=800,
                                justify="left")
    label_fontes.pack(pady=(20, 5))

    lbl = ctk.CTkLabel(frame_educativo,
                       text="• theguardian.com",
                       text_color="#333333",
                       font=("Arial", 13),
                       anchor="w",
                       justify="left")
    lbl.pack()

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)

def area_educativa6(frame_educativo, email, senha, frame_menu):
    """Exibe o conteúdo da notícia 6 (lista de filmes) na área educativa."""
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Título principal menor e com menos espaçamento
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🌿 8 Filmes sobre Sustentabilidade para Crianças",
                          text_color="#1A73E8",
                          font=("Arial", 16, "bold"),  # fonte menor
                          wraplength=800,
                          justify="left")
    titulo.pack(pady=(10, 5))  # menos espaçamento

    filmes = [
        ("Wall-E (2008)", "Um clássico da Pixar! Mostra um futuro onde a Terra foi tomada pelo lixo e a humanidade vive no espaço. Wall-E, um robô solitário, nos ensina sobre consumo, lixo e amor pelo planeta."),
        ("Lorax: Em Busca da Trúfula Perdida (2012)", "Baseado na obra do Dr. Seuss, aborda desmatamento e exploração de recursos naturais, com personagens carismáticos e músicas cativantes."),
        ("Happy Feet: O Pinguim (2006)", "Através de um pinguim dançarino, o filme aborda temas como mudança climática, preservação dos oceanos e o impacto da pesca predatória."),
        ("Rio (2011)", "Além da aventura, mostra a importância da biodiversidade brasileira e os perigos do tráfico de animais silvestres."),
        ("Irmão Urso (Brother Bear) (2003)", "Aborda o respeito à natureza, ao ciclo da vida e à conexão espiritual com o meio ambiente, com forte mensagem sobre empatia e equilíbrio natural."),
        ("A Fuga das Galinhas (Chicken Run) (2000)", "Uma metáfora inteligente sobre liberdade animal e os impactos da agroindústria – adaptado ao humor infantil."),
        ("O Rei Leão (1994 / 2019)", "Apesar de não focar diretamente em sustentabilidade, ensina sobre o “ciclo da vida” e o equilíbrio ecológico da savana africana."),
        ("Meu Amigo Totoro (1988)", "Um clássico do Studio Ghibli. Exalta a harmonia entre seres humanos e natureza, com um toque mágico e poético.")
    ]

    for titulo_filme, descricao in filmes:
        label_filme_titulo = ctk.CTkLabel(frame_educativo,
                                          text=titulo_filme,
                                          text_color="#1A73E8",
                                          font=("Arial", 14, "bold"),  # fonte menor
                                          wraplength=800,
                                          justify="left")
        label_filme_titulo.pack(padx=20, pady=(8, 2), anchor="w")  # menos espaçamento

        label_filme_desc = ctk.CTkLabel(frame_educativo,
                                        text=descricao,
                                        text_color="#333333",
                                        font=("Arial", 12),  # fonte menor
                                        wraplength=800,
                                        justify="left")
        label_filme_desc.pack(padx=20, pady=(0, 6), anchor="w")  # menos espaçamento

    # Botão de voltar
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=30)


def sair_sitema():
    """Função utilizada para fechar o sistema."""
    janela.destroy()  # Fecha a janela principal


######################################################################
# Configuração da janela principal
janela = ctk.CTk()
janela.title("ECODROP SYSTEM")
janela.geometry("1000x800+400+150")
janela.resizable(False, False)

# Cria um frame apenas para o cabeçalho do topo
frame_topo = ctk.CTkFrame(janela, fg_color="#1A73E8", height=80)
frame_topo.pack(fill="x")

titulo = ctk.CTkLabel(frame_topo, text="💧 ECODROP",
                      text_color="#f0f0f0", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

# Divisão em colunas principais (menu lateral e conteúdo)
frame_conteudo = ctk.CTkFrame(janela, fg_color="#f0f0f0")
frame_conteudo.pack(fill="both", expand=True)

# Menu lateral
frame_lateral = ctk.CTkFrame(frame_conteudo, fg_color="#f0f0f0", width=200)
frame_lateral.pack(side="left", fill="y")

# Botões do menu inicial
botao1 = ctk.CTkButton(frame_lateral, text="Login", fg_color="#f0f0f0",
                       text_color="#1A73E8", font=("Arial", 12), anchor="w", command=mostrar_login)
botao1.pack(fill="x", pady=(20, 10), padx=10)

botao2 = ctk.CTkButton(frame_lateral, text="Cadastro usuário", fg_color="#f0f0f0",
                       text_color="#1A73E8", font=("Arial", 12), anchor="w", command=mostrar_cadastro)
botao2.pack(fill="x", pady=10, padx=10)

botao3 = ctk.CTkButton(frame_lateral, text="Modo administrador", fg_color="#f0f0f0",
                       text_color="#1A73E8", font=("Arial", 12), anchor="w", command=modo_adm)
botao3.pack(fill="x", pady=10, padx=10)

botao4 = ctk.CTkButton(frame_lateral, text="Sobre nós", fg_color="#f0f0f0",
                       text_color="#1A73E8", font=("Arial", 12), anchor="w", command=sobre_nos)
botao4.pack(fill="x", pady=10, padx=10)


####################################################
# Área principal de conteúdo
frame_principal = ctk.CTkFrame(frame_conteudo, fg_color="#f0f0f0")
frame_principal.pack(side="left", fill="both", expand=True, padx=30, pady=30)


texto_bem_vindo = ctk.CTkLabel(frame_principal, text="Bem-vindo ao sistema ECODROP",
                               text_color="#202124", font=("Arial", 22, "bold"))
texto_bem_vindo.pack(pady=(0, 20))

texto_instrucao = ctk.CTkLabel(frame_principal, text="Menos consumo, mais consciência, um planeta mais feliz.",
                               text_color="#5f6368", wraplength=500, justify="left", font=("Arial", 18))
texto_instrucao.pack()

image_initial = Image.open("fotos/mascoteprincipall.png")
ctk_image_initial = ctk.CTkImage(
    light_image=image_initial, dark_image=image_initial, size=(400, 400))

label_initial_image = ctk.CTkLabel(frame_principal, image=ctk_image_initial, text="")
label_initial_image.pack()

############################################################
# Frame do rodapé
frame_rodape = ctk.CTkFrame(frame_principal, fg_color="#f0f0f0", height=30)
frame_rodape.pack(fill="x", side="bottom")

texto_rodape = ctk.CTkLabel(
    frame_rodape, text="Versão 2.0 • Suporte: ecodropsuporte@gmail.com", text_color="#5f6368", font=("Arial", 10))
texto_rodape.pack()

###########################################################
"""Parte do frame de login"""

frame_login = ctk.CTkFrame(janela, fg_color="#ffffff")
label_login = ctk.CTkLabel(frame_login, text="Informe seus dados:",
                           fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_login.pack(pady=2)
label_avisologin = ctk.CTkLabel(
    frame_login, text=" ", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_avisologin.pack(pady=2)

# 1-entrada email
label_emaillogin = ctk.CTkLabel(
    frame_login, text="Digite seu email:", text_color="#000000", anchor="w", width=300)
label_emaillogin.pack(pady=(2, 0))

entrada_emaillogin = ctk.CTkEntry(frame_login, width=300)
entrada_emaillogin.pack(pady=2)

# 2-entrada senha
label_senhalogin = ctk.CTkLabel(
    frame_login, text="Digite sua senha:", text_color="#000000", anchor="w", width=300)
label_senhalogin.pack(pady=(2, 0))

entrada_senhalogin = ctk.CTkEntry(frame_login, width=300, show="*")
entrada_senhalogin.pack(pady=2)

# botão logar
botao_logar = ctk.CTkButton(frame_login, text="Logar", fg_color="blue",
                            text_color="#ffffff", width=300, command=lambda: conferir_logar(entrada_emaillogin, entrada_senhalogin))
botao_logar.pack(pady=2)
# botão voltar
botao_voltarinicial_login = ctk.CTkButton(
    frame_login, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
botao_voltarinicial_login.pack()


##############################################
"""Parte do frame de cadastro"""
frame_cadastro = ctk.CTkFrame(janela, fg_color="#ffffff")
label_cadastro = ctk.CTkLabel(frame_cadastro, text="Informe seus dados:",
                              fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_cadastro.pack(pady=1)


label_aviso = ctk.CTkLabel(frame_cadastro, text=" ",
                           fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_aviso.pack(pady=1)

# 1-Entrada Email
label_email = ctk.CTkLabel(frame_cadastro, text="Digite seu email:",
                           text_color="#000000", anchor="w", width=300)
label_email.pack(pady=(1, 0))

entrada_email = ctk.CTkEntry(frame_cadastro, width=300)
entrada_email.pack(pady=1)

# 2-entrada nome da família
label_nome = ctk.CTkLabel(frame_cadastro, text="Digite o nome da sua família",
                          text_color="#000000", anchor="w", width=300)
label_nome.pack(pady=(1, 0))

entrada_nome = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(
    janela.register(validar_letras_espacos), "%P"))
entrada_nome.pack(pady=1)

# 3-Entrada Senha
label_senha = ctk.CTkLabel(frame_cadastro, text="Senha (mínimo 4 caracteres):",
                           text_color="#000000", anchor="w", width=300)
label_senha.pack(pady=(1, 0))

entrada_senha = ctk.CTkEntry(frame_cadastro, width=300, show="*")
entrada_senha.pack(pady=1)

# 4. Campo Quantidade de membros
label_qmembros = ctk.CTkLabel(
    frame_cadastro, text="Quantidade de membros na família:", text_color="#000000", anchor="w", width=300)
label_qmembros.pack(pady=(1, 0))
entrada_qmembros = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(
    janela.register(validar_numeros), "%P"))
entrada_qmembros.pack(pady=1)

# 5. Número do apartamento
label_numeroap = ctk.CTkLabel(
    frame_cadastro, text="Digite o número do seu apartamento", text_color="#000000", anchor="w", width=300)
label_numeroap.pack(pady=(1, 0))
entrada_numeroap = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(
    janela.register(validar_numeros), "%P"))
entrada_numeroap.pack(pady=1)

# 6. Código verificador
label_verificador = ctk.CTkLabel(
    frame_cadastro, text="Digite seu código verificador (mínimo 4 caracteres):", text_color="#000000", anchor="w", width=300)
label_verificador.pack(pady=(1, 0))

entrada_verificador = ctk.CTkEntry(frame_cadastro, width=300, show="*", validate="key", validatecommand=(
    janela.register(validar_numeros), "%P"))
entrada_verificador.pack(pady=1)


botao_cadastrar = ctk.CTkButton(frame_cadastro, text="Cadastrar", fg_color="blue",
                                text_color="#ffffff", width=300, command=lambda: conferir_cadastrar(entrada_email, entrada_nome, entrada_senha,
                                                                                                    entrada_qmembros,
                                                                                                    entrada_numeroap, entrada_verificador, label_aviso))
botao_cadastrar.pack(pady=1)

# botão de voltar
botao_voltarinicial_cadastro = ctk.CTkButton(
    frame_cadastro, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
botao_voltarinicial_cadastro.pack()


#####################################
"""Parte do frame do modo administrador"""
frame_adm = ctk.CTkFrame(janela, fg_color="#ffffff")
label_adm_title = ctk.CTkLabel(frame_adm, text="Modo Administrador", fg_color="#ffffff", text_color="blue", font=("Arial", 30))
label_adm_title.pack(pady=1)

label_adm_message = ctk.CTkLabel(frame_adm, text=" ", fg_color="#ffffff", text_color="blue", font=("Arial", 25))
label_adm_message.pack(pady=1)

# 1-Entrada do Código de Administrador
label_codigo = ctk.CTkLabel(frame_adm, text="Digite o código de administrador:",
                           text_color="blue", anchor="w", width=300)
label_codigo.pack(pady=(1, 0))

entrada_codigo = ctk.CTkEntry(frame_adm, width=300, show="*") # Máscara de entrada para o código de administrador
entrada_codigo.pack(pady=1)

botao_modoadm = ctk.CTkButton(frame_adm, text="Entrar modo adm", fg_color="blue",
                               text_color="#ffffff", width=300, command=entrar_modoadm)
botao_modoadm.pack(pady=1)
# botão de voltar
botao_voltarinicial_adm = ctk.CTkButton(frame_adm, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
botao_voltarinicial_adm.pack()


######################################################
"""Parte do frame "Sobre Nós" (Conta a história do EcoDrop)"""
frame_sobrenos = ctk.CTkFrame(janela, fg_color="#ffffff")

# Título principal
titulo_sobrenos = ctk.CTkLabel(frame_sobrenos, text="💧 Projeto ECODROP", font=("Arial", 22, "bold"), text_color="#1A73E8")
titulo_sobrenos.pack(pady=(20, 10))

descricao_projeto = ctk.CTkLabel(
    frame_sobrenos,
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
imagem_sobrenos_path = "fotos/fotosobrenos.jpg"
try:
    imagem_sobrenos = Image.open(imagem_sobrenos_path)
    ctk_imagem_sobrenos = ctk.CTkImage(
        light_image=imagem_sobrenos, dark_image=imagem_sobrenos, size=(500, 300))
    label_sobrenos_image = ctk.CTkLabel(frame_sobrenos, image=ctk_imagem_sobrenos, text="")
    label_sobrenos_image.pack()
except FileNotFoundError:
    ctk.CTkLabel(frame_sobrenos, text=f"Imagem '{imagem_sobrenos_path}' não encontrada.", text_color="red").pack()


botao_voltarinicial_sobrenos = ctk.CTkButton(frame_sobrenos, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
botao_voltarinicial_sobrenos.pack(pady=30)

#######################################
"""Parte do frame de aviso (Será usado apenas quando o usuário concluir o cadastro com sucesso, oferecendo a opção de ir para o login ou sair do sistema)"""
frame_aviso=ctk.CTkFrame(janela,fg_color="#ffffff")
# Label de aviso
label_aviso_success = ctk.CTkLabel(frame_aviso, text="Cadastro realizado com sucesso!", font=("Arial", 20), text_color="green")
label_aviso_success.pack(pady=(40, 20))

# Botão para ir para o login
botao_login_aviso = ctk.CTkButton(frame_aviso, text="Ir para Login", width=200, command=mostrar_login)
botao_login_aviso.pack(pady=(0, 10))

# Botão para sair do sistema
botao_sair_aviso = ctk.CTkButton(frame_aviso, text="Sair do Sistema", width=200, fg_color="red", hover_color="#cc0000", command=sair_sitema)
botao_sair_aviso.pack()


###############################################


class Cadastro:
    """
    Esta classe tem o objetivo de cadastrar os usuários, recebendo os dados básicos como parâmetros.
    Ela realiza o cadastro de uma conta e verifica o código de segurança fornecido.
    """

    def __init__(self, email, quantidade_pessoas, senha, nome_familia, apartamento, verificador, label_aviso_widget):
        # Dados básicos de cadastro
        self.email = email
        self.quantidade = quantidade_pessoas
        self.senha = senha
        self.nome_familia = nome_familia
        self.pontos = 0  # Pontos começam zerados
        self.apartamento = apartamento
        self.verificador = verificador
        self.label_aviso_widget = label_aviso_widget # Armazena o label para atualizar as mensagens na GUI
        print("Iniciando processo de cadastro...")
        self.email_valido()

    def email_valido(self):
        """Função utilizada para verificar se o email é válido ou não."""
        dominios_validos = [
            'gmail.com', 'outlook.com', 'hotmail.com',
            'yahoo.com', 'icloud.com'
        ]

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            self.label_aviso_widget.configure(text="FORMATO DE EMAIL INVÁLIDO. Utilize um domínio válido.", text_color="red")
            return

        dominio = self.email.split('@')[1].lower()
        if dominio not in dominios_validos:
            self.label_aviso_widget.configure(text="Domínio não aceito. Use: Gmail, Outlook, Yahoo, iCloud, etc.", text_color="red")
            return

        self.conferir_email()

    def conferir_email(self):
        """Função utilizada para verificar se o email já está cadastrado ou não."""
        global dados_conta # Acessa dados globais

        try:
            with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
                arquivo_lido = json.load(arquivo)
                dados_conta = arquivo_lido.get("senha", {})
        except Exception as e:
            self.label_aviso_widget.configure(text=f"Erro ao carregar dados: {e}", text_color="red")
            return

        if self.email in dados_conta:
            self.label_aviso_widget.configure(text="EMAIL JÁ POSSUI UMA CONTA.", text_color="red")
            return # Interrompe o processo de cadastro
        else:
            self.conferir_ap()

    def conferir_ap(self):
        """Função utilizada para analisar se o apartamento já está cadastrado ou não."""
        global dados_apartamento # Acessa dados globais

        try:
            with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
                arquivo_lido = json.load(arquivo)
                dados_apartamento = arquivo_lido.get("apartamento", {})
        except Exception as e:
            self.label_aviso_widget.configure(text=f"Erro ao carregar dados: {e}", text_color="red")
            return

        # Verifica se o número do apartamento existe em qualquer valor de dados_apartamento
        if self.apartamento in dados_apartamento.values():
            self.label_aviso_widget.configure(text="APARTAMENTO JÁ CADASTRADO.", text_color="red")
            return # Interrompe o processo de cadastro
        else:
            self.cadastrar_conta()

    def cadastrar_conta(self):
        """Função utilizada para cadastrar a conta no banco de dados."""
        global dados_conta, dados_familia, dados_quantidade, dados_pontos, dados_apartamento, dados_codigov

        dados_conta[self.email] = self.senha
        dados_familia[self.email] = self.nome_familia
        dados_quantidade[self.email] = self.quantidade
        dados_pontos[self.email] = self.pontos
        dados_apartamento[self.email] = self.apartamento
        dados_codigov[self.email] = self.verificador

        # É melhor usar "w" para arquivos JSON, pois qualquer erro de formatação pode quebrar o sistema
        try:
            with open(r"banco_dados.JSON", "w", encoding="utf-8") as arquivo:
                json.dump({"senha": dados_conta, "familia": dados_familia, "membros": dados_quantidade, "pontos": dados_pontos,
                            "apartamento": dados_apartamento, "verificador": dados_codigov,
                            "questoes_quiz": dados_questoes_quiz, "ultimo_quiz": dados_ultimo_quiz}, # Inclui dados do quiz
                           arquivo, indent=4, ensure_ascii=False)
            self.label_aviso_widget.configure(text="Cadastro realizado com sucesso!", text_color="green")
            aviso_sistema() # Exibe a tela de sucesso
        except Exception as e:
            self.label_aviso_widget.configure(text=f"Erro ao salvar cadastro: {e}", text_color="red")


janela.mainloop()

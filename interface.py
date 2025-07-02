import customtkinter as ctk
from PIL import Image
import json
import csv
import time
import re
import random

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

# Load data from JSON at startup
# Initialize empty data structures in case the file is not found
with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
    
    # quando usa json.load o arquivo json é transformado em dicionário python
    """
    o objetivo dessa parte do código é abrir o arquivo json e salvar os dicionários em python,facilitando a manipulação
    """
    arquivo_lido = json.load(arquivo)
    dados_conta = arquivo_lido["senha"]
    dados_familia = arquivo_lido["familia"]
    dados_quantidade = arquivo_lido["membros"]
    dados_pontos = arquivo_lido["pontos"]
    dados_apartamento = arquivo_lido["apartamento"]
    dados_codigov = arquivo_lido["verificador"]

# Function to only allow numbers
def validar_numeros(novo_texto):  # Add the parameter
    """Function used to let the user type only numbers, improving error handling"""
    return novo_texto.isdigit() or novo_texto == ""

# Function to only allow letters and spaces
def validar_letras_espacos(novo_texto):  # Add the parameter
    """Function used to let the user type only letters and spaces, improving error handling"""
    return all(c.isalpha() or c.isspace() for c in novo_texto) or novo_texto == ""

def aviso_sistema():
    """Function used to show the frame_aviso, which will only appear if the registration is successfully completed"""
    frame_cadastro.pack_forget()
    frame_aviso.pack(fill="both", expand=True)

def voltar_inicial():
    """Function used to return to the initial screen, if the wrong option was entered"""
    # Frames to "forget"
    frame_cadastro.pack_forget()
    frame_login.pack_forget()
    frame_adm.pack_forget()
    frame_sobrenos.pack_forget()
    frame_aviso.pack_forget() # Ensure the warning frame is also hidden if user navigates from it

    # Repack initial frames
    frame_topo.pack(fill="x")
    frame_conteudo.pack(fill="both", expand=True)
    frame_lateral.pack(side="left", fill="y")
    frame_principal.pack(side="right", fill="both", expand=True, padx=30, pady=30)
    frame_rodape.pack(fill="x", side="bottom")


def mostrar_login():
    """Function used to expand the login frame"""
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget()
    frame_aviso.pack_forget() # Hide aviso frame if navigating from it
    frame_login.pack(fill="both", expand=True)
    label_avisologin.configure(text=" ", text_color="blue") # Clear previous messages
    entrada_emaillogin.delete(0, ctk.END) # Clear email field
    entrada_senhalogin.delete(0, ctk.END) # Clear password field


def conferir_logar(entrada_emaillogin, entrada_senhalogin):
    """Function used to check for blank spaces when pressing the login button"""
    email = entrada_emaillogin.get().strip()
    senha = entrada_senhalogin.get().strip()
    if email == "" or senha == "":
        label_avisologin.configure(text="Preencha todos os campos.", text_color="red")
        return

    login(email, senha, label_avisologin)

def login(email, senha, label_avisologin):
    """Function used to verify if email and password are correct, to then go to the menu"""
    global dados_conta # Ensure global access to updated data

    # Re-read data just in case it was modified externally or by another process
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
    """Function used to expand the registration frame"""
    # frames to forget
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget()
    frame_aviso.pack_forget() # Hide aviso frame if navigating from it

    frame_cadastro.pack(fill="both", expand=True)
    label_aviso.configure(text=" ", text_color="blue") # Clear previous messages
    # Clear entry fields
    entrada_email.delete(0, ctk.END)
    entrada_nome.delete(0, ctk.END)
    entrada_senha.delete(0, ctk.END)
    entrada_qmembros.delete(0, ctk.END)
    entrada_numeroap.delete(0, ctk.END)
    entrada_verificador.delete(0, ctk.END)


def conferir_cadastrar(entrada_email, entrada_nome, entrada_senha,
                    entrada_qmembros,entrada_numeroap, entrada_verificador, label_aviso):
    """
    This function will be used to verify if the entries are filled
    correctly and will call the Cadastro class to register the account.
    """
    email = entrada_email.get().strip()
    nome_familia = entrada_nome.get().strip()
    senha = entrada_senha.get().strip()
    quantidade_pessoas = int(entrada_qmembros.get().strip())
    apartamento = int(entrada_numeroap.get().strip())
    verificador = entrada_verificador.get().strip()

    entradas = [email, nome_familia, senha,quantidade_pessoas,apartamento]

    # Verificação: se algum campo de texto estiver vazio
    if any(campo == "" for campo in entradas):
        label_aviso.configure(text="Todos os campos devem ser preenchidos.", text_color="red")
        return

    # Validação da senha
    if len(senha) < 4 or len(senha) > 20:
        label_aviso.configure(text="A senha deve ter entre 4 e 20 caracteres.", text_color="red")
        return
    
    if len(verificador) < 4 or len(verificador) > 20:
        label_aviso.configure(text="A senha deve ter entre 4 e 20 caracteres.", text_color="red")
        return
    

    verificador=int(verificador)
    conta = Cadastro(email,quantidade_pessoas,senha,nome_familia,apartamento,verificador)


def modo_adm():
    """Function used to expand the frame_adm, when the user wants to go to admin mode"""
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget()
    frame_adm.pack(fill="both", expand=True)


def entrar_modoadm():
    # Placeholder for admin mode entry logic
    print("Entrar modo ADM - Logic to be implemented")
    pass


def sobre_nos():
    """Function used to show the frame_sobrenos (Tells the story of the ecodrop project)"""
    frame_topo.pack_forget()
    frame_conteudo.pack_forget()
    frame_lateral.pack_forget()
    frame_principal.pack_forget()
    frame_rodape.pack_forget()
    frame_sobrenos.pack(fill="both", expand=True)


def mostrar_menu(email, senha):
    """Function used to show the frame_menu, where the available functions of the program will be seen"""
    for widget in janela.winfo_children():
        widget.destroy()

    # Main frame that wraps the menu and content
    frame_menu = ctk.CTkFrame(janela, fg_color="#ffffff")

    # Top of the system with title
    frame_topo_menu = ctk.CTkFrame(frame_menu, fg_color="#1A73E8", height=80)
    frame_topo_menu.pack(fill="x")

    titulo = ctk.CTkLabel(frame_topo_menu, text="EcoDrop", fg_color="#1A73E8", text_color="white",
                              font=("Arial", 24, "bold"))
    titulo.pack(pady=20)

    # Side menu
    frame_lateral_menu = ctk.CTkFrame(frame_menu, fg_color="white", width=200)
    frame_lateral_menu.pack(side="left", fill="y")

    # Content frame
    frame_conteudo_menu = ctk.CTkFrame(frame_menu, fg_color="#f0f2f5")
    frame_conteudo_menu.pack(fill="both", expand=True)

    # Main content frame, where dynamic content will be displayed
    frame_principalmenu = ctk.CTkFrame(frame_conteudo_menu, fg_color="#ffffff")
    frame_principalmenu.pack(fill="both", expand=True, padx=30, pady=30)

    # Helper function to reset the main content area to the default welcome view
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

        imagem_menu = Image.open("fotos/mascoteprincipall.png")
        ctk_imagem_menu = ctk.CTkImage(light_image=imagem_menu, dark_image=imagem_menu, size=(400, 400))

        label_menu_image = ctk.CTkLabel(frame_principalmenu, image=ctk_imagem_menu, text="")
        label_menu_image.pack()


    # ---- Side Menu Buttons ----
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

    # Initial content for frame_principalmenu
    reset_principal_menu_content()

    # Footer Frame
    frame_rodape_menu = ctk.CTkFrame(frame_menu, fg_color="#f0f0f0", height=30)
    frame_rodape_menu.pack(fill="x", side="bottom")

    texto_rodape_menu = ctk.CTkLabel( # Renamed to avoid conflict
    frame_rodape_menu, text="Versão 2.0 • Suporte: ecodropsuporte@gmail.com", text_color="#5f6368", font=("Arial", 10))
    texto_rodape_menu.pack()

    frame_menu.pack(fill="both", expand=True)


def mostrar_dados(email, senha, frame_principalmenu, reset_callback):
    """
    📊 Function: Show Data
    Displays the user's main account data (excluding password and verifier code for security).
    Used for the user to review their registration information.
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="📊 Seus Dados",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    global dados_familia, dados_quantidade, dados_pontos, dados_apartamento # Access global data

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
    🔄 Function: Update Data, where the user will be able to update their data
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="🔄 Atualizar Dados",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    ctk.CTkLabel(frame_principalmenu, text="Funcionalidade de atualização de dados em desenvolvimento.",
                 font=("Arial", 14), text_color="#5f6368").pack(pady=10)

    botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar.pack(pady=20)


def deletar_conta(email, senha, frame_principalmenu, reset_callback):
    """
    🗑 Function: Delete Account
    Allows the user to permanently delete their account from the system.
    After confirmation, the data is removed and they will need to register again.
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
        global dados_conta, dados_familia, dados_quantidade, dados_pontos, dados_apartamento, dados_codigov
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

                    # Update global dictionaries to reflect changes immediately
                    dados_conta = data["senha"]
                    dados_familia = data["familia"]
                    dados_quantidade = data["membros"]
                    dados_pontos = data["pontos"]
                    dados_apartamento = data["apartamento"]
                    dados_codigov = data["verificador"]

                    arquivo.seek(0)  # Go to the beginning of the file
                    json.dump(data, arquivo, indent=4, ensure_ascii=False)
                    arquivo.truncate() # Remove remaining part

                    label_confirmacao.configure(text="Sua conta foi deletada com sucesso.", text_color="green")
                    # After deletion, log out and go to initial screen
                    janela.after(1000, lambda: voltar_inicial()) # Delay a bit for message to show
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
    ✍️ Function: Feedback
    Allows the user to send an opinion with up to 140 characters and a rating from 0 to 10.
    Used to evaluate the system and collect improvement suggestions.
    """
    # Clear existing widgets in the main content frame
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="✍️ Enviar Feedback",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    label_instrucao = ctk.CTkLabel(frame_principalmenu, text="Por favor, deixe sua opinião sobre o sistema EcoDrop:",
                                    font=("Arial", 14), text_color="#333333")
    label_instrucao.pack(pady=(0, 10))

    # Feedback Text Entry
    label_feedback_texto = ctk.CTkLabel(frame_principalmenu, text="Seu Feedback (até 140 caracteres):",
                                         font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
    label_feedback_texto.pack(fill="x", padx=50, pady=(10, 0))
    entrada_feedback = ctk.CTkEntry(frame_principalmenu, width=400, height=80)
    entrada_feedback.pack(padx=50, pady=(0, 10))

    # Rating Scale
    label_nota = ctk.CTkLabel(frame_principalmenu, text="Sua nota para o sistema (0 a 10):",
                              font=("Arial", 12, "bold"), text_color="#5f6368", anchor="w")
    label_nota.pack(fill="x", padx=50, pady=(10, 0))
    entrada_nota = ctk.CTkEntry(frame_principalmenu, width=100, validate="key",
                                validatecommand=(janela.register(lambda text: text.isdigit() and (len(text) <= 2 and int(text) <= 10 if text.strip() else True) or text == ""), "%P"))
    entrada_nota.pack(padx=50, pady=(0, 20), anchor="w")

    # Message Label for validation
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
            with open("feedback.csv", "a+", newline="", encoding="utf-8") as f: # Use "a+" to read and append
                f.seek(0, 2) # Move to the end of the file
                if f.tell() == 0: # Check if file is empty by checking current position
                    # File is empty, write header
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(["Email", "Feedback", "Nota", "Data/Hora"])
                # Now write the data
                csv_writer = csv.writer(f)
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
    🧮 Function: Point Calculation
    Calculates points based on liters saved, number of residents, and average consumption.
    Points are converted into benefits (e.g., vouchers, discounts, miles).
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="🧮 Cálculo de Pontos",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    ctk.CTkLabel(frame_principalmenu, text="Funcionalidade de cálculo de pontos em desenvolvimento.",
                 font=("Arial", 14), text_color="#5f6368").pack(pady=10)

    botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar.pack(pady=20)


def resgatar_premio(email, senha, frame_principalmenu, reset_callback):
    """
    🎁 Function: Redeem Prizes
    Allows the user to redeem rewards using their accumulated points.
    Checks if the balance is sufficient before confirming the redemption.
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="🎁 Resgatar Prêmios",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    ctk.CTkLabel(frame_principalmenu, text="Funcionalidade de resgate de prêmios em desenvolvimento.",
                 font=("Arial", 14), text_color="#5f6368").pack(pady=10)

    botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar.pack(pady=20)


def mostrar_ranking(email, senha, frame_principalmenu, reset_callback):
    """
    🏆 Function: Monthly Ranking
    Displays a list of families that saved the most water in the month.
    Uses daily average consumption as a sorting criterion.
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="🏆 Ranking Mensal",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    global dados_pontos, dados_familia # Access global data

    # Create a list of (family_name, points) tuples
    ranking_data = []
    # Use a copy of dados_pontos.items() to avoid issues if the dictionary changes during iteration (though unlikely here)
    for user_email, points in list(dados_pontos.items()):
        family_name = dados_familia.get(user_email, "N/A") # Get family name, default to N/A if not found
        ranking_data.append({"familia": family_name, "pontos": points})

    # Sort the ranking data by points in descending order
    ranking_data.sort(key=lambda x: x["pontos"], reverse=True)

    # Display the ranking
    if not ranking_data:
        ctk.CTkLabel(frame_principalmenu, text="Nenhum dado de ranking disponível.",
                     font=("Arial", 14), text_color="#5f6368").pack(pady=10)
    else:
        # Create a header for the ranking table
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
    🧠 Function: Weekly Quiz
    Here the user can participate in a weekly quiz.
    """
    for widget in frame_principalmenu.winfo_children():
        widget.destroy()

    label_titulo = ctk.CTkLabel(frame_principalmenu, text="🧠 Quiz Semanal",
                                 font=("Arial", 20, "bold"), text_color="#1A73E8")
    label_titulo.pack(pady=(20, 10))

    ctk.CTkLabel(frame_principalmenu, text="Funcionalidade de quiz semanal em desenvolvimento.",
                 font=("Arial", 14), text_color="#5f6368").pack(pady=10)

    botao_voltar = ctk.CTkButton(frame_principalmenu, text="⬅ Voltar ao Menu",
                                 fg_color="gray", text_color="white",
                                 command=reset_callback)
    botao_voltar.pack(pady=20)


def area_educativa(email, senha, frame_menu):
    """Function used to go to the frame_educativo (we will use the full screen in this function, as it is necessary to have more content.
    Where there will be several reading options about sustainability topics)"""

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
                                 fg_color="blue", # Changed color for consistency
                                 text_color="#ffffff", # Changed color for consistency
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: mostrar_menu(email, senha))
    botao_voltar.pack(pady=20)


def area_educativa1(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Title
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🌍 Investimento de €15 bilhões para combater a crise hídrica na Europa",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # News paragraph
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

    # Highlight: Why this matters?
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

    # Sources
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

    # Back button
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)


def area_educativa2(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Title
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🎒 Extração de água potável do ar usando alimentos",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # News paragraph
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

    # Highlight: Practical impact
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

    # Sources
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

    # Back button
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)


def area_educativa3(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Title
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🏗️ UT Austin constrói o maior centro universitário de reúso de água nos EUA",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # News paragraph
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

    # Highlight: Why this matters?
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

    # Sources
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

    # Back button
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)


def area_educativa4(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Title
    titulo = ctk.CTkLabel(frame_educativo,
                          text="📰 Educação Ambiental na Índia: Estudantes de Uttar Pradesh se tornam embaixadores da limpeza",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # News paragraph
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

    # Highlight: Why this matters?
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

    # Sources
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

    # Back button
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)


def area_educativa5(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Title
    titulo = ctk.CTkLabel(frame_educativo,
                          text="📰 Impacto dos datacenters em áreas com escassez hídrica na América Latina",
                          text_color="#1A73E8",
                          font=("Arial", 20, "bold"),
                          wraplength=800, justify="left")
    titulo.pack(pady=(20, 10))

    # News paragraph
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

    # Highlight: Why this matters?
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

    # Sources
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

    # Back button
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=50)

def area_educativa6(frame_educativo, email, senha, frame_menu):
    for widget in frame_educativo.winfo_children():
        widget.destroy()

    # Smaller main title with less spacing
    titulo = ctk.CTkLabel(frame_educativo,
                          text="🌿 8 Filmes sobre Sustentabilidade para Crianças",
                          text_color="#1A73E8",
                          font=("Arial", 16, "bold"),  # smaller font
                          wraplength=800,
                          justify="left")
    titulo.pack(pady=(10, 5))  # less spacing

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
                                          font=("Arial", 14, "bold"),  # smaller font
                                          wraplength=800,
                                          justify="left")
        label_filme_titulo.pack(padx=20, pady=(8, 2), anchor="w")  # less spacing

        label_filme_desc = ctk.CTkLabel(frame_educativo,
                                        text=descricao,
                                        text_color="#333333",
                                        font=("Arial", 12),  # smaller font
                                        wraplength=800,
                                        justify="left")
        label_filme_desc.pack(padx=20, pady=(0, 6), anchor="w")  # less spacing

    # Back button
    botao_voltar = ctk.CTkButton(frame_educativo,
                                 text="⬅ Voltar",
                                 fg_color="blue",
                                 text_color="#ffffff",
                                 font=("Arial", 12),
                                 cursor="hand2",
                                 command=lambda: area_educativa(email, senha, frame_menu))
    botao_voltar.pack(pady=30)


def sair_sitema():
    """Function used to close the system"""
    janela.destroy()  # Closes the main window


######################################################################
# Main window configuration
janela = ctk.CTk()
janela.title("ECODROP SYSTEM")
janela.geometry("1000x800+400+150")
janela.resizable(False, False)

# Create a frame just for the header at the top
frame_topo = ctk.CTkFrame(janela, fg_color="#1A73E8", height=80)
frame_topo.pack(fill="x")

titulo = ctk.CTkLabel(frame_topo, text="💧 ECODROP",
                      text_color="#f0f0f0", font=("Arial", 24, "bold"))
titulo.pack(pady=20)

# Main content division (side menu and content)
frame_conteudo = ctk.CTkFrame(janela, fg_color="#f0f0f0")
frame_conteudo.pack(fill="both", expand=True)

# Side menu
frame_lateral = ctk.CTkFrame(frame_conteudo, fg_color="#f0f0f0", width=200)
frame_lateral.pack(side="left", fill="y")

# Menu buttons
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
# Main content area
frame_principal = ctk.CTkFrame(frame_conteudo, fg_color="#f0f0f0")
frame_principal.pack(side="left", fill="both", expand=True, padx=30, pady=30)


texto_bem_vindo = ctk.CTkLabel(frame_principal, text="Bem-vindo ao sistema ECODROP",
                               text_color="#202124", font=("Arial", 22, "bold"))
texto_bem_vindo.pack(pady=(0, 20))

texto_instrucao = ctk.CTkLabel(frame_principal, text="Menos consumo, mais consciência, um planeta mais feliz.",
                               text_color="#5f6368", wraplength=500, justify="left", font=("Arial", 18))
texto_instrucao.pack()

image_initial = Image.open("fotos/mascoteprincipall.png") # Renamed to avoid global conflict
ctk_image_initial = ctk.CTkImage(
    light_image=image_initial, dark_image=image_initial, size=(400, 400))

label_initial_image = ctk.CTkLabel(frame_principal, image=ctk_image_initial, text="") # Renamed
label_initial_image.pack()

############################################################
# Footer Frame
frame_rodape = ctk.CTkFrame(frame_principal, fg_color="#f0f0f0", height=30)
frame_rodape.pack(fill="x", side="bottom")

texto_rodape = ctk.CTkLabel(
    frame_rodape, text="Versão 2.0 • Suporte: ecodropsuporte@gmail.com", text_color="#5f6368", font=("Arial", 10))
texto_rodape.pack()

###########################################################
"""Part of the login frame"""

frame_login = ctk.CTkFrame(janela, fg_color="#ffffff")
label_login = ctk.CTkLabel(frame_login, text="Informe seus dados:",
                           fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_login.pack(pady=2)
label_avisologin = ctk.CTkLabel(
    frame_login, text=" ", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_avisologin.pack(pady=2)

# 1-email entry
label_emaillogin = ctk.CTkLabel(
    frame_login, text="Digite seu email:", text_color="#000000", anchor="w", width=300)
label_emaillogin.pack(pady=(2, 0))

entrada_emaillogin = ctk.CTkEntry(frame_login, width=300)
entrada_emaillogin.pack(pady=2)

# 2-password entry
label_senhalogin = ctk.CTkLabel(
    frame_login, text="Digite sua senha:", text_color="#000000", anchor="w", width=300)
label_senhalogin.pack(pady=(2, 0))

entrada_senhalogin = ctk.CTkEntry(frame_login, width=300, show="*")
entrada_senhalogin.pack(pady=2)

# login button
botao_logar = ctk.CTkButton(frame_login, text="Logar", fg_color="blue",
                            text_color="#ffffff", width=300, command=lambda: conferir_logar(entrada_emaillogin, entrada_senhalogin))
botao_logar.pack(pady=2)
# back button
botao_voltarinicial_login = ctk.CTkButton( # Renamed
    frame_login, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
botao_voltarinicial_login.pack()


##############################################
"""Part of the registration frame"""
frame_cadastro = ctk.CTkFrame(janela, fg_color="#ffffff")
label_cadastro = ctk.CTkLabel(frame_cadastro, text="Informe seus dados:",
                              fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_cadastro.pack(pady=1)


label_aviso = ctk.CTkLabel(frame_cadastro, text=" ",
                           fg_color="#ffffff", text_color="blue", font=("Arial", 20))
label_aviso.pack(pady=1)

# 1-Email Entry
label_email = ctk.CTkLabel(frame_cadastro, text="Digite seu email:",
                           text_color="#000000", anchor="w", width=300)
label_email.pack(pady=(1, 0))

entrada_email = ctk.CTkEntry(frame_cadastro, width=300)
entrada_email.pack(pady=1)

# 2-Family Name Entry
label_nome = ctk.CTkLabel(frame_cadastro, text="Digite o nome da sua família",
                          text_color="#000000", anchor="w", width=300)
label_nome.pack(pady=(1, 0))

entrada_nome = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(
    janela.register(validar_letras_espacos), "%P"))
entrada_nome.pack(pady=1)

# 3-Password Entry
label_senha = ctk.CTkLabel(frame_cadastro, text="Senha (mínimo 4 caracteres):",
                           text_color="#000000", anchor="w", width=300)
label_senha.pack(pady=(1, 0))

entrada_senha = ctk.CTkEntry(frame_cadastro, width=300, show="*")
entrada_senha.pack(pady=1)

# 4. Number of Members Field
label_qmembros = ctk.CTkLabel(
    frame_cadastro, text="Quantidade de membros na família:", text_color="#000000", anchor="w", width=300)
label_qmembros.pack(pady=(1, 0))
entrada_qmembros = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(
    janela.register(validar_numeros), "%P"))
entrada_qmembros.pack(pady=1)

# 5. Apartment Number
label_numeroap = ctk.CTkLabel(
    frame_cadastro, text="Digite o número do seu apartamento", text_color="#000000", anchor="w", width=300)
label_numeroap.pack(pady=(1, 0))
entrada_numeroap = ctk.CTkEntry(frame_cadastro, width=300, validate="key", validatecommand=(
    janela.register(validar_numeros), "%P"))
entrada_numeroap.pack(pady=1)

# 6. Verifier Code
label_verificador = ctk.CTkLabel(
    frame_cadastro, text="Digite seu código verificador (mínimo 4 caracteres):", text_color="#000000", anchor="w", width=300)
label_verificador.pack(pady=(1, 0))

entrada_verificador = ctk.CTkEntry(frame_cadastro, width=300, show="*", validate="key", validatecommand=(
    janela.register(validar_numeros), "%P")) # Added validation for verifier code
entrada_verificador.pack(pady=1)


botao_cadastrar = ctk.CTkButton(frame_cadastro, text="Cadastrar", fg_color="blue",
                                text_color="#ffffff", width=300, command=lambda: conferir_cadastrar(entrada_email, entrada_nome, entrada_senha,
                                                                                                    entrada_qmembros,
                                                                                                    entrada_numeroap, entrada_verificador, label_aviso))
botao_cadastrar.pack(pady=1)

# back button
botao_voltarinicial_cadastro = ctk.CTkButton( # Renamed
    frame_cadastro, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial)
botao_voltarinicial_cadastro.pack()


#####################################
"""Part of the admin frame (administrator mode)"""
frame_adm = ctk.CTkFrame(janela, fg_color="#ffffff")
label_adm_title = ctk.CTkLabel(frame_adm, text="Modo Administrador", fg_color="#ffffff", text_color="blue", font=("Arial", 30))
label_adm_title.pack(pady=1)

label_adm_message = ctk.CTkLabel(frame_adm, text=" ", fg_color="#ffffff", text_color="blue", font=("Arial", 25))
label_adm_message.pack(pady=1)

# 1-Admin Code Entry
label_codigo = ctk.CTkLabel(frame_adm, text="Digite o código de administrador:",
                           text_color="blue", anchor="w", width=300)
label_codigo.pack(pady=(1, 0))

entrada_codigo = ctk.CTkEntry(frame_adm, width=300, show="*") # Mask input for admin code
entrada_codigo.pack(pady=1)

botao_modoadm = ctk.CTkButton(frame_adm, text="Entrar modo adm", fg_color="blue",
                               text_color="#ffffff", width=300, command=entrar_modoadm)
botao_modoadm.pack(pady=1)
# back button
botao_voltarinicial_adm = ctk.CTkButton(frame_adm, text="Voltar", fg_color="blue", text_color="#ffffff", width=300, command=voltar_inicial) # Renamed
botao_voltarinicial_adm.pack()


######################################################
"""Part of the about us frame (Tells the story of ecodrop)"""
frame_sobrenos = ctk.CTkFrame(janela, fg_color="#ffffff")

# Main title
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
"""Part of the warning frame (only used when the user correctly completes the registration, with the option to go to login or exit the system)"""
frame_aviso=ctk.CTkFrame(janela,fg_color="#ffffff")
# Warning label
label_aviso_success = ctk.CTkLabel(frame_aviso, text="Cadastro realizado com sucesso!", font=("Arial", 20), text_color="green")
label_aviso_success.pack(pady=(40, 20))

# Button to go to login
botao_login_aviso = ctk.CTkButton(frame_aviso, text="Ir para Login", width=200, command=mostrar_login)
botao_login_aviso.pack(pady=(0, 10))

# Button to exit the system
botao_sair_aviso = ctk.CTkButton(frame_aviso, text="Sair do Sistema", width=200, fg_color="red", hover_color="#cc0000", command=sair_sitema)
botao_sair_aviso.pack()


###############################################

class Cadastro:
    """
    Essa Classe tem o objetivo de cadastrar os usuários, recebendo os dados básicos como parâmetros.
    Ela realiza o cadastro de uma conta e verifica o código de segurança fornecido.
    """

    def __init__(self, email, quantidade_pessoas, senha, nome_familia, apartamento, verificador):
        # Dados básicos de cadastro
        self.email = email
        self.quantidade = quantidade_pessoas
        self.senha = senha
        self.nome_familia = nome_familia
        self.pontos = 0  # Pontos começam zerados
        self.apartamento = apartamento
        self.verificador = verificador
        print("entrei cadastro")
        self.email_valido()

        # Chamada para verificar o código de segurança
        


    def email_valido(self):
        
        #FUNÇÃO UTILIZADA PARA CONFERIR SE O EMAIL É VÁLIDO OU NÃO
        dominios_validos = [
            'gmail.com', 'outlook.com', 'hotmail.com',
            'yahoo.com', 'icloud.com'
        ]

        
            # VERIFICA SE O FORMATO DO EMAIL ESTÁ ESCRITO CORRETAMENTE
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            #label_aviso é uma variável global,não necessitando importar para edita-la
            label_aviso.configure(text="Formato inválido", text_color="red")
            return
            

                  # volta pro início do while para validar de novo,caso esteja correto,irá passar pelo verificador

            # VERIFICA APENAS O DOMÍNIO,SEPARA TODO O RESTO E PEGA APENAS A PARTE DO DOMÍNIO
        dominio = self.email.split('@')[1].lower()
        if dominio not in dominios_validos:
            label_aviso.configure(text="Domínio não aceito", text_color="red")
            return

                # continuar o loop sem parar
                

        # Se chegou aqui, formato e domínio estão corretos
            

        
        self.conferir_email()

    
    def conferir_email(self):
        
        #FUNÇÃO UTILIZADA PARA CONFERIR SE O EMAIL JÁ ESTÁ CADASTRADO OU NÃO
        
        with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
            arquivo_lido = json.load(arquivo)
            dados_conta = arquivo_lido["senha"]
            dados_familia = arquivo_lido["familia"]
            dados_quantidade = arquivo_lido["membros"]
            dados_pontos = arquivo_lido["pontos"]
            dados_apartamento = arquivo_lido["apartamento"]
            dados_codigov = arquivo_lido["verificador"]

            if self.email.strip() in dados_conta:#dessa forma verificará se o email está já cadastrado ou não
                label_aviso.configure(text="Email já cadastrado.",text_color="red")
                return
            
            else:
                self.conferir_ap()  # Continua o processo normalmente

    def conferir_ap(self):
        
       #FUNÇÃO UTILIZADA PARA ANALISAR SE O APARTAMENTO JÁ ESTÁ CADASTRADO OU NÃO
        if self.apartamento in dados_apartamento.values():
            label_aviso.configure(text="APARTAMENTO JÁ CADASTRADO.TENTE NOVAMENTE")
        else:
            self.cadastrar_conta()

    def cadastrar_conta(self):
        
        ##FUNÇÃO UTILIZADA PARA CADASTRAR CONTA NO BANCO DE DADOS

        dados_conta[self.email] = self.senha
        dados_familia[self.email] = self.nome_familia
        dados_quantidade[self.email] = self.quantidade
        dados_pontos[self.email] = self.pontos
        dados_apartamento[self.email] = self.apartamento
        dados_codigov[self.email] = self.verificador

        # PARA ARQUIVO TIPO JSON É MELHOR USAR "w" pois qualquer errinho de formatação pode quebrar o sistema
        with open(r"banco_dados.JSON", "w", encoding="utf-8") as arquivo:
            # Aqui, estamos criando um dicionário com duas chaves:
            json.dump({"senha": dados_conta, "familia": dados_familia, "membros": dados_quantidade, "pontos": dados_pontos,
                       "apartamento": dados_apartamento, "verificador": dados_codigov}, arquivo, indent=4, ensure_ascii=False)
            aviso_sistema()



janela.mainloop()

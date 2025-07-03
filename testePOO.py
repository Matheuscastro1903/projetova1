import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__() #Esse super serve para a classe App herdar os atributos da classe ctk
        self.title("ECODROP SYSTEM")
        self.geometry("1000x800+400+150")
        self.resizable(False, False)

        # Atributos das telas
        self.premenu = None
        self.menu = None
        self.modoadm = None

        # Começa com o pré-menu
        self.mostrar_premenu()

    def ocultar_telas(self):
        for tela in (self.premenu, self.menu, self.modoadm):
            if tela:
                tela.pack_forget()

    def mostrar_premenu(self):
        self.ocultar_telas()
        if not self.premenu:
            self.premenu = PreMenu(self)  # ← passa o App como master
        self.premenu.pack(fill="both", expand=True)

    def mostrar_menu(self):
        self.ocultar_telas()
        if not self.menu:
            self.menu = Menu(self)
        self.menu.pack(fill="both", expand=True)

    def mostrar_modoadm(self):
        self.ocultar_telas()
        if not self.modoadm:
            self.modoadm = ModoAdm(self)
        self.modoadm.pack(fill="both", expand=True)





class PreMenu(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.conjuntodeframes=[]
        self.criar_tela_inicial()
      
        # Começa com a tela inicial
        

    def criar_tela_inicial(self):
        self.ocultar_frames()

        self.frame_topo = ctk.CTkFrame(self, fg_color="#1A73E8", height=80)
        self.frame_topo.pack(fill="x")

        titulo = ctk.CTkLabel(self.frame_topo,text="💧 ECODROP",text_color="#f0f0f0",font=("Arial", 24, "bold"))
        titulo.pack(pady=20)

        # Divisão principal (menu lateral + conteúdo)
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="#f0f0f0")
        self.frame_conteudo.pack(fill="both", expand=True)

        # Menu lateral
        self.frame_lateral = ctk.CTkFrame(self.frame_conteudo, fg_color="#f0f0f0", width=200)
        self.frame_lateral.pack(side="left", fill="y")

        # Botões do menu inicial
        botao1 = ctk.CTkButton(self.frame_lateral,text="Login",fg_color="#f0f0f0",text_color="#1A73E8",font=("Arial", 12),anchor="w",
                               command=self.mostrar_login)
        botao1.pack(fill="x", pady=(20, 10), padx=10)

        botao2 = ctk.CTkButton(self.frame_lateral,text="Cadastro usuário",fg_color="#f0f0f0",text_color="#1A73E8",font=("Arial", 12),anchor="w",
                               command=self.mostrar_cadastro)
        botao2.pack(fill="x", pady=10, padx=10)

        botao3 = ctk.CTkButton(self.frame_lateral,text="Modo administrador",fg_color="#f0f0f0",text_color="#1A73E8",font=("Arial", 12),anchor="w",
            command=self.mostrar_modoadm)
        botao3.pack(fill="x", pady=10, padx=10)

        botao4 = ctk.CTkButton(self.frame_lateral,text="Sobre nós",fg_color="#f0f0f0",text_color="#1A73E8",font=("Arial", 12),anchor="w",
                               command=self.mostrar_sobrenos)
        botao4.pack(fill="x", pady=10, padx=10)

        # Área principal de conteúdo
        self.frame_principal = ctk.CTkFrame(self.frame_conteudo, fg_color="#f0f0f0")
        self.frame_principal.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        texto_bem_vindo = ctk.CTkLabel(self.frame_principal,text="Bem-vindo ao sistema ECODROP",text_color="#202124",font=("Arial", 22, "bold"))
        texto_bem_vindo.pack(pady=(0, 20))

        texto_instrucao = ctk.CTkLabel(self.frame_principal,text="Menos consumo, mais consciência, um planeta mais feliz.",text_color="#5f6368",
                                       wraplength=500,justify="left",font=("Arial", 18))
        texto_instrucao.pack()

        # Rodapé
        self.frame_rodape = ctk.CTkFrame(self.frame_principal, fg_color="#f0f0f0", height=30)
        self.frame_rodape.pack(fill="x", side="bottom")

        texto_rodape = ctk.CTkLabel(self.frame_rodape,text="Versão 2.0 • Suporte: ecodropsuporte@gmail.com",text_color="#5f6368",font=("Arial", 10))
        texto_rodape.pack()        



    def mostrar_login(self):
        self.ocultar_frames()
        if not self.frame_login:
            self.frame_login = ctk.CTkFrame(self)
            ctk.CTkLabel(self.frame_login, text="Login").pack()
            ctk.CTkButton(self.frame_login, text="Entrar", command=self.callback_entrar_menu).pack()
            ctk.CTkButton(self.frame_login, text="Voltar", command=lambda: self.mostrar_tela(self.frame_inicial)).pack()
        self.mostrar_tela(self.frame_login)

    def mostrar_cadastro(self):
        self.ocultar_frames()
        if not self.frame_cadastro:
            self.frame_cadastro = ctk.CTkFrame(self)
            ctk.CTkLabel(self.frame_cadastro, text="Cadastro").pack()
            ctk.CTkButton(self.frame_cadastro, text="Voltar", command=lambda: self.mostrar_tela(self.frame_inicial)).pack()
        self.mostrar_tela(self.frame_cadastro)

    def mostrar_modoadm(self):
        pass

    def mostrar_sobrenos(self):
        self.ocultar_frames()
        if not self.frame_sobrenos:
            self.frame_sobrenos = ctk.CTkFrame(self)
            ctk.CTkLabel(self.frame_sobrenos, text="Sobre nós").pack()
            ctk.CTkButton(self.frame_sobrenos, text="Voltar", command=lambda: self.mostrar_tela(self.frame_inicial)).pack()
        self.mostrar_tela(self.frame_sobrenos)

    
        

    def ocultar_frames(self):
        for f in self.conjuntodeframes:
            if f:
                f.pack_forget()


class Menu(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class ModoAdm (ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)



app = App()
app.mainloop()
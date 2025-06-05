import customtkinter as ctk


# Customização aparência
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("blue")


# Criação das funções de funcionalidade
def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()

    ## Verificar se o usuario é Gabriel e senha 12345
    if usuario == 'Gabriel' and senha == '12345':
        resultado_login.configure(text='Login feito com sucesso', text_color='green')
    else:
        resultado_login.configure(text='Login incorreto', text_color='red')

# Criação da janela principal
app = ctk.CTk()
app.title('Sistema de Login')
app.geometry('350x350') # Aumentado o tamanho da janela para melhor centralização visual

# Criação dos campos
# Rótulo - usuário
label_usuario = ctk.CTkLabel(app, text='Usuário')
label_usuario.pack(pady=(30,5))
# Entrada - usuário
campo_usuario = ctk.CTkEntry(app, placeholder_text='Digite seu usuário', width=200) # Largura diminuída em 20%
campo_usuario.pack(pady=10)

# Rótulo - senha
label_senha = ctk.CTkLabel(app, text='Senha')
label_senha.pack(pady=(30, 5)) # Mantido pady=(30, 5) para distância significativa
# Entrada - senha
campo_senha = ctk.CTkEntry(app, placeholder_text='Digite sua senha', show='*', width=200) # Largura diminuída em 20%
campo_senha.pack(pady=10)

# Botão - login
botao_login = ctk.CTkButton(app, text='Login', command=validar_login)
botao_login.pack(pady=10)
# Campo feedback do login
resultado_login = ctk.CTkLabel(app, text='')
resultado_login.pack(pady=10)


# Iniciar aplicação
app.mainloop()

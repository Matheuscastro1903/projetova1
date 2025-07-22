import customtkinter as ctk
from customtkinter import CTkImage, CTkLabel

from PIL import Image
import json

import pandas as pd
import matplotlib as plt
from collections import Counter
from io import BytesIO
import matplotlib.pyplot as plt



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





class ModoAdm(ctk.CTkFrame):

    def __init__(self, master, voltar_inicial):
        super().__init__(master)
        #define self.operaco como None para criar um objeto da classe
        # operações  apenas se o self.operacao não tiver sido criado ainda
        self.operacao=None
        self.tabela=None
        self.grafico_pizza=None
        self.grafico_consumopessoa=None
        self.grafico_consumoap=None
        self.media=None
        #atributo que serve para controlar a quantidade de tentativas
        self.tentativas=0
        
        
        self.frame_adm = ctk.CTkFrame(self, fg_color="#ffffff")
        label_adm = ctk.CTkLabel(self.frame_adm, text="Insira o código de acesso \npara entrar no modo administrador:",
                                   fg_color="#ffffff", text_color="blue", font=("Arial", 20))
        label_adm.pack(pady=2)
        self.label_avisoadm = ctk.CTkLabel(self.frame_adm, text=" ", fg_color="#ffffff", text_color="blue", font=("Arial", 20))
        self.label_avisoadm.pack(pady=2)

        # 1-entrada email
        #label_emailadm = ctk.CTkLabel(self.frame_adm, text="Digite seu email:", text_color="#000000", anchor="w", width=300)
        #label_emailadm.pack(pady=(2, 0))

        #self.entrada_emailadm = ctk.CTkEntry(self.frame_adm, width=300)
        #self.entrada_emailadm.pack(pady=2)

        # 2-entrada senha
        label_senhaadm= ctk.CTkLabel(self.frame_adm, text="Digite o código de acesso:", text_color="#000000", anchor="w", width=300)
        label_senhaadm.pack(pady=(2, 0))

        self.entrada_senhaadm = ctk.CTkEntry(self.frame_adm, width=300, show="*")
        self.entrada_senhaadm.pack(pady=2)

        # 3-entrada email cond

        # botão logar
        botao_entrar_adm = ctk.CTkButton(self.frame_adm, text="Entrar", fg_color="blue",
                                    text_color="#ffffff", width=300, command=self.conferir_adm)
        botao_entrar_adm.pack(pady=2)
        # botão voltar
        botao_voltarinicial = ctk.CTkButton(self.frame_adm, text="Voltar", fg_color="blue", text_color="#ffffff", width=300,
                                            command=voltar_inicial)
        botao_voltarinicial.pack()

        self.frame_adm.pack(fill="both", expand=True)

    def conferir_adm(self):
            entrada_senha=self.entrada_senhaadm.get().strip()
            if entrada_senha=="!GaMa#1903!":
                self.tela_inicial_adm()
            else:
                self.label_avisoadm.configure(text="Código inválido",text_color="Red")
                self.tentativas+=1
                if self.tentativas==4:
                    self.atencao_adm()

            pass
    
    def atencao_adm(self):
        for widget in self.frame_adm.winfo_children():
            widget.destroy()
       
    

        # Mensagem de título
        titulo = ctk.CTkLabel(self.frame_adm,
                          text="🚫 Limite de Tentativas Atingido",
                          font=("Arial", 20, "bold"),
                          text_color="red")
        titulo.pack(pady=(30, 10))

        # Mensagem adicional
        msg = ctk.CTkLabel(self.frame_adm,
                       text="O sistema será encerrado por segurança.",
                       font=("Arial", 16))
        msg.pack(pady=5)

        # Label de contagem regressiva
        self.label_contador = ctk.CTkLabel(self.frame_adm,
                                       text="Fechando em 7 segundos...",
                                       font=("Arial", 16, "italic"))
        self.label_contador.pack(pady=(20, 10))
        self.after(7000, self.sair_sistema)
    
    
    def tela_inicial_adm(self):
            for widget in self.frame_adm.winfo_children():
                widget.destroy()
            #A IDENTAÇÃO TEM QUE FICAR DESSA FORMA OU A CADA INTERAÇÃO,SERÁ CRIADO MAIS FRAMES DESSA TELA DE INÍCIO DO 
            #MODO ADM
            frame_topo = ctk.CTkFrame(self.frame_adm, fg_color="#1A73E8", height=80)
            frame_topo.pack(fill="x")

            titulo = ctk.CTkLabel(frame_topo, text="💧 MODO ADM",text_color="#f0f0f0", font=("Arial", 24, "bold"))
            titulo.pack(pady=10)

            frame_conteudo = ctk.CTkFrame(self.frame_adm, fg_color="#ffffff")

            botao_ver_dados = ctk.CTkButton(frame_conteudo, text="🔍Ver dados", fg_color="blue",
                                                text_color="#ffffff", width=300, command=self.tela_ver_dados)
            botao_ver_dados.pack(pady=10)

            botao_editar_dados = ctk.CTkButton(frame_conteudo, text="✏️Editar dados", fg_color="blue",
                                                text_color="#ffffff", width=300, command=self.tela_editar_dados)
            botao_editar_dados.pack(pady=10)

            botao_analise_dados = ctk.CTkButton(frame_conteudo, text="📊Analisar dados", fg_color="blue",
                                                text_color="#ffffff", width=300, command=self.tela_analise_dados)
            botao_analise_dados.pack(pady=10)

            imagem = Image.open("fotos/mascoteadm.png")
            ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(400, 400))

            label = ctk.CTkLabel(frame_conteudo, image=ctk_imagem, text="")
            label.pack(pady=30)

            frame_conteudo.pack(fill="both", expand=True)

            
            pass
    
    
    
    def tela_ver_dados(self):
            for widget in self.frame_adm.winfo_children():
                widget.destroy()
            
             
            if self.operacao is None:
                self.operacao=OperacoesAdm()
            if self.tabela is None:
                self.tabela=self.operacao.gerar_tabela()

            frame_topo = ctk.CTkFrame(self.frame_adm, fg_color="#1A73E8", height=80)
            frame_topo.pack(fill="x")

            titulo = ctk.CTkLabel(frame_topo, text="💧 MODO ADM",text_color="#ffffff", font=("Arial", 24, "bold"))
            titulo.pack(pady=20)

        

            #criação de um frame com scroll para que seja possível ver todos os dados
            frame_scroll = ctk.CTkScrollableFrame(self.frame_adm,fg_color="#ffffff")
            frame_scroll.pack(fill="both", expand=True, padx=10, pady=10)
            

            #perguntar o porque é melhor usar a fonte courier
            label_tabela = ctk.CTkLabel(frame_scroll, text=self.tabela, font=("Courier", 12), anchor="w", justify="left")
            label_tabela.pack(padx=10, pady=10)

            label_atencao=ctk.CTkLabel(frame_scroll, text="ATENÇÃO!!", font=("Arial", 20,"bold"), anchor="w", justify="left")
            label_atencao.pack(padx=10)

            label_mensagem_atencao=ctk.CTkLabel(frame_scroll, text="Dados com 'N/A' não possuem valores.", font=("Arial", 20,"bold"), anchor="w", justify="left")
            label_mensagem_atencao.pack(padx=10)

            botao_menuadm=ctk.CTkButton(frame_scroll,width=300,text="Voltar",fg_color="white",text_color="#1A73E8",command=self.tela_inicial_adm)
            botao_menuadm.pack(pady=30)
            

            #fazer botão de voltar para o menu
           
            pass
    
    
    
    def tela_editar_dados(self):
            for widget in self.frame_adm.winfo_children():
                widget.destroy()
            frame_topo = ctk.CTkFrame(self.frame_adm, fg_color="#1A73E8", height=80)
            frame_topo.pack(fill="x")

            titulo = ctk.CTkLabel(frame_topo, text="💧 MODO ADM",text_color="#f0f0f0", font=("Arial", 24, "bold"))
            titulo.pack(pady=20)

            self.frame_conteudo = ctk.CTkFrame(self.frame_adm, fg_color="#f0f0f0")
            self.frame_conteudo.pack(fill="both", expand=True)

            self.label_avisoedicao=ctk.CTkLabel(self.frame_conteudo,text="")
            self.label_avisoedicao.pack()

            # Nome
            label_nome = ctk.CTkLabel(self.frame_conteudo, text="Digite o email da conta que você deseja atualiza(Obrigatório):", 
                                      text_color="#000000", font=("Arial", 16, "bold"))
            label_nome.pack(pady=10)
            self.entrada_email=ctk.CTkEntry(self.frame_conteudo, width=300)
            self.entrada_email.pack(pady=10)

            # Família
            label_familia = ctk.CTkLabel(self.frame_conteudo, text="Digite o nome da família associada à conta(Obrigatório):", 
                                         text_color="#000000", font=("Arial", 16, "bold"))
            label_familia.pack(pady=10)
            self.entrada_familia = ctk.CTkEntry(self.frame_conteudo, width=300,
                                         validate="key",
                                         validatecommand=(self.register(self.validar_letras_espacos), "%P"))
            self.entrada_familia.pack(pady=1)

            # Quantidade de Membros
            label_qmembros = ctk.CTkLabel(self.frame_conteudo, text="Digite a quantidade de membros da família(Obrigatório):", 
                                         text_color="#000000", font=("Arial", 16, "bold"))
            label_qmembros.pack(pady=10)
            self.entrada_qmembros = ctk.CTkEntry(self.frame_conteudo, width=300,
                                             validate="key",
                                             validatecommand=(self.register(self.validar_numeros), "%P"))
            self.entrada_qmembros.pack(pady=1)

            # Apartamento
            label_apartamento = ctk.CTkLabel(self.frame_conteudo, text="Digite o número do apartamento:", 
                                             text_color="#000000", font=("Arial", 16, "bold"))
            label_apartamento.pack(pady=10)
            self.entrada_apartamento = ctk.CTkEntry(self.frame_conteudo, width=300,
                                             validate="key",
                                             validatecommand=(self.register(self.validar_numeros), "%P"))
            self.entrada_apartamento.pack(pady=1)

            # Consumo
            label_consumo = ctk.CTkLabel(self.frame_conteudo, text="Digite o consumo registrado (em m³):\n(Obrigatório)", 
                                         text_color="#000000", font=("Arial", 16, "bold"))
            label_consumo.pack(pady=10)
            self.entrada_consumo = ctk.CTkEntry(self.frame_conteudo, width=300,
                                             validate="key",
                                             validatecommand=(self.register(self.validar_numeros), "%P"))
            self.entrada_consumo.pack(pady=1)




            botao_atualizar_conta=ctk.CTkButton(self.frame_conteudo,text="Atualizar dados",text_color="#1A73E8",width=300,fg_color="#f0f0f0",
                                                command=self.conferir_entradas)
            botao_atualizar_conta.pack(pady=(10,5))

            botao_menuadm=ctk.CTkButton(self.frame_conteudo,width=300,text="Voltar",fg_color="#f0f0f0",text_color="#1A73E8",
                                        command=self.tela_inicial_adm)
            botao_menuadm.pack(pady=5)

            #Apartamento
            #Família
            #Pontos
            #Consumo
            #Membros

    @staticmethod  # Permite usar funções que não estão na classe diretamente,sem precisar passar self
    def validar_numeros(novo_texto):
        """Função utilizada para permitir digitar apenas números"""
        return novo_texto.isdigit() or novo_texto == ""

    @staticmethod  # Permite usar funções que não estão na classe diretamente,sem precisar passar self
    def validar_letras_espacos(novo_texto):
        """Função utilizada para deixar apenas digitar letras e espaços"""
        return all(c.isalpha() or c.isspace() for c in novo_texto) or novo_texto == ""
    
    def conferir_entradas(self):
        print(1)
        self.email=self.entrada_email.get().strip()
        self.apartamento=self.entrada_apartamento.get().strip()
        self.quantidade_pessoas=self.entrada_qmembros.get().strip()
        self.consumo=int(self.entrada_consumo.get().strip())
        self.nome_familia=self.entrada_familia.get().strip()

        entradas = [self.email, self.nome_familia,
                    self.quantidade_pessoas,self.consumo] 
    # Verificação: se algum campo de texto estiver vazio
        if any(campo == "" for campo in entradas):
            self.label_avisoedicao.configure(
                text="Preencha os campos obrigatórios.", text_color="red")
            return

        
        
        if self.apartamento!="":
            possiveis_andares=["10","20","30","40","50","60","70","80","90"]
            possiveis_apartamentos=["01","02","03","04","05"]
            #ESSES VERIFICADORES SERVIRÃO PARA DIZER SE O ANDAR E O APARTAMENTO É VÁLIDO OU NÃO
            numero_valido=False
            andar_valido = False
            apto_valido = False
        
            if len(self.apartamento)==4:
                numero_valido=True

            for andar in possiveis_andares:
                #SÓ VALIDARÁ SE APARTAMENTO INICIAR COM O INTERÁVEL DA LISTA ANDAR
                if self.apartamento.startswith(andar):
                    andar_valido = True
                    #BREAK IRÁ QUEBRAR O LOOP FOR,ACABANDO A INTERAÇÃO
                    break

            for apto in possiveis_apartamentos:
                #SÓ VALIDARÁ SE APARTAMENTO INICIAR COM O INTERÁVEL DA LISTA APARTAMENTO
                if self.apartamento.endswith(apto):
                    apto_valido = True
                    #BREAK IRÁ QUEBRAR O LOOP FOR,ACABANDO COM A INTERAÇÃO
                    break

            if not (andar_valido and apto_valido and numero_valido): #VERIFICA SE AMBOS SÃO VÁLIDOS(TRUE)
                print("Apartamento inváldio")
                self.label_avisoedicao.configure(text="Apartamento inválido", text_color="red")
                #return irá parar a função caso o aviso apareça
                return
        
            self.apartamento=int(self.apartamento)
        else:
            self.apartamento=dados_apartamento[self.email]
        
        self.verificar_email_edicao()

    
    
    
    def verificar_email_edicao(self):
        print(2)
        
        
        
        #Verificação se o email já tinha sido cadastrado anteriormente
        if self.email not in dados_conta:
            self.label_avisoedicao.configure(text="Email não cadastrado anteriormente.",text_color="Red")
            return
        self.salvar_edicao_dados()
        pass
    
    def salvar_edicao_dados(self):
        print(3)
        try:
            # Atualiza os dados que o admin pode alterar no
            dados_familia[self.email] = self.nome_familia
            dados_quantidade[self.email] =int(self.quantidade_pessoas)
            dados_apartamento[self.email] = self.apartamento
            dados_consumo[self.email]=self.consumo
            
            

            # Reescreve o banco de dados inteiro, incluindo os dados que não foram alterados
            with open("banco_dados.JSON", "w", encoding="utf-8") as arquivo:
                json.dump({"senha": dados_conta,"familia": dados_familia,"membros": dados_quantidade,"pontos": dados_pontos,
                           "apartamento": dados_apartamento,"verificador": dados_codigov}, arquivo, indent=4, ensure_ascii=False)
        
            self.mostrar_aviso_adm()
        except Exception as e:
            self.label_avisoedicao.configure(text=f"ERRO {e}.\nTente mais tarde!",text_color="red")
            print("Erro salvamento")

    def mostrar_aviso_adm(self):
        for widget in self.frame_adm.winfo_children():
                widget.destroy()

        frame_topo = ctk.CTkFrame(self.frame_adm, fg_color="#1A73E8", height=80)
        frame_topo.pack(fill="x")

        titulo = ctk.CTkLabel(frame_topo, text="💧 MODO ADM",text_color="#f0f0f0", font=("Arial", 24, "bold"))
        titulo.pack(pady=10)

        frame_conteudo = ctk.CTkFrame(self.frame_adm, fg_color="#ffffff")
        label_sucesso=ctk.CTkLabel(frame_conteudo,text="ATUALIZAÇÃO REALIZADA COM SUCESSO!!",text_color="#1A73E8",font=("arial",25))
        label_sucesso.pack()
        label_aviso_sucesso=ctk.CTkLabel(frame_conteudo,text="REINICIALIZAÇÃO NECESSÁRIA EM 7 SEGUNDOS.",text_color="#1A73E8",font=("arial",25))
        label_aviso_sucesso.pack(pady=10)
        
        imagem = Image.open("fotos/mascoteadm.png")
        ctk_imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(400, 400))

        label = ctk.CTkLabel(frame_conteudo, image=ctk_imagem, text="")
        label.pack(pady=30)


        frame_conteudo.pack(fill="both",expand=True)

        self.after(7000, self.sair_sistema)
    
        pass
    
    def sair_sistema(self):
        """Função utilizada para fechar sistema """
        # Fechando dessa forma irá "destruir" a janela que foi definida no master
        self.master.destroy()  # Fecha a janela principal
   



    def tela_analise_dados(self):
            for widget in self.frame_adm.winfo_children():
                widget.destroy()
            
            frame_topo = ctk.CTkFrame(self.frame_adm, fg_color="#1A73E8", height=80)
            frame_topo.pack(fill="x")

            titulo = ctk.CTkLabel(frame_topo, text="💧 MODO ADM",text_color="#ffffff", font=("Arial", 24, "bold"))
            titulo.pack(pady=20)

            frame_conteudo = ctk.CTkFrame(self.frame_adm, fg_color="#ffffff")
            frame_conteudo.pack(fill="both", expand=True)

            frame_lado_esquerdo=ctk.CTkFrame(frame_conteudo,fg_color="#ffffff")
            frame_lado_esquerdo.pack(side="left",fill="both",expand=True)

            frame_lado_direito=ctk.CTkFrame(frame_conteudo,fg_color="#ffffff")
            frame_lado_direito.pack(side="right",fill="both",expand=True)
            
            #Gerando gráfico de pizza com a porcentagem de famílias que possuem certa quantidade de membros
            if self.operacao is None:
                self.operacao=OperacoesAdm()
            if self.grafico_pizza is None:
                self.grafico_pizza=self.operacao.gerar_grafico_pizza()
            if self.grafico_consumopessoa is None:
                self.grafico_consumopessoa=self.operacao.gerar_grafico2()
            if self.grafico_consumoap is None:
                self.grafico_consumoap=self.operacao.gerar_grafico3()
            if self.media is None:
                self.media=self.operacao.gerar_valor_media()
            

            img_pizza = CTkImage(dark_image=self.grafico_pizza, size=(400, 400))

            label_pizza = CTkLabel(frame_lado_esquerdo, image=img_pizza, text="")
            label_pizza.pack()

            label_dados=CTkLabel(frame_lado_esquerdo,text="Dados importantes:",font=("Arial",20,"bold"))
            label_dados.pack(pady=10)
            
            label_media_brasileira=CTkLabel(frame_lado_esquerdo,text="-Média brasileira de gasto de água por dia é de 154L por pessoa")
            label_media_brasileira.pack(pady=5)
            
            label_media_condominio=CTkLabel(frame_lado_esquerdo,text=f"-Total de água gasto pelo condomínio {self.media}")
            label_media_condominio.pack(pady=5)

            

            
            
            botao_voltar=ctk.CTkButton(frame_lado_esquerdo,text="Voltar",text_color="#ffffff",fg_color="#1A73E8",command=self.tela_inicial_adm)
            botao_voltar.pack(pady=10)
            

            img_grafico2=CTkImage(dark_image=self.grafico_consumopessoa,size=(300,300))
            label_grafico2=CTkLabel(frame_lado_direito,image=img_grafico2, text="")
            label_grafico2.pack()

            img_grafico3=CTkImage(dark_image=self.grafico_consumoap,size=(300,300))
            label_grafico3=CTkLabel(frame_lado_direito,image=img_grafico3, text="")
            label_grafico3.pack(pady=20)

            
            pass
    
class OperacoesAdm():
    def __init__(self):
        print("entrei operações adm")
        
        pass
    
    def gerar_tabela(self):
        
        dados_organizados = []
        
        for email in dados_conta:
            if (email in dados_familia and email in dados_quantidade and email in dados_pontos and 
                email in dados_apartamento and 
                email in dados_codigov):
                if email in dados_consumo:        
                    dados_organizados.append({
                        "Email": email,
                        "Família": dados_familia[email],
                        "Membros": dados_quantidade[email],
                        "Pontos": dados_pontos[email],
                        "Apartamento": dados_apartamento[email],
                        "Verificador": dados_codigov[email],
                        "Consumo":dados_consumo[email]

                    })
                else:
                    dados_organizados.append({
                        "Email": email,
                        "Família": dados_familia[email],
                        "Membros": dados_quantidade[email],
                        "Pontos": dados_pontos[email],
                        "Apartamento": dados_apartamento[email],
                        "Verificador": dados_codigov[email],
                        "Consumo":"N/A"

                    })

        df = pd.DataFrame(dados_organizados)
        tabela_formatada = df.to_string(index=False)
        
        return tabela_formatada

        
    
    def gerar_grafico_pizza(self):
        #Método responsável pela geração do gráfico de pizza que será feito em relação a quantidade de membros 

        #esse counter é uma classe nativa do python que contará a repetição de cada valor do dicionário dados_quantidade 
        #e armazenará em um dicionário por exemplo. {2:5,...}-->o número 2 se repete 5 vezes
        contagem = Counter(dados_quantidade.values())


        #Nesse loop for dentro da variável label,será criado mensagens do tipo "2 membros","3 membros" e armazerá em uma lista na variável.
        #O loop irá rolar e irá criar um label para cada tipo de quantidade "2","3" e etc
        labels = [f"{membros} membros" for membros in contagem.keys()]

        #essa variável sizes irá criar uma lista da quantidade de vezes que o valor aparece.Por exemplo,se o valor 3 aparece 5 vezes,ele terá o valor 5
        sizes = list(contagem.values())

        # Criar gráfico de pizza
        # Criar figura e eixo do gráfico

        #fig é a janela geral do gráfico e area_usada é a área específica onde o gráfico será desenhado
        fig, area_usada = plt.subplots(figsize=(8,8)) #fgsize define o tamanho do gráfico em polegadas
        
        #Desenha o gráfico pizza na área a area_usada
        area_usada.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        #size define o tamanho de cada fatia
        #labels+define o texto de cada fatia
        #autopct='%1.1f%%' mostra as porcentagens dentro da fatia
        #startangle=140: gira o gráfico para ficar mais esteticamente agradável.



        area_usada.set_title("Distribuição de famílias por número de membros", fontsize=20, pad=30)#define o título do gráfico e a fonte

        area_usada.axis('equal')#garante que o gráfico seja um círculo perfeito

        # Salvar o gráfico em memória como imagem PNG
        buffer = BytesIO()#cria um buffer de memória que simula um arquivo png,mas que ficará dentro da memória
        fig.savefig(buffer, format='png', bbox_inches='tight') #salva a figura dentro do buffer
        #bbox_inches='tight' remove os espaços em branco entre o gráfico
        plt.close(fig)  #Fecha o gráfico da memória do matplotlib para liberar RAM e evitar vazamentos.
        buffer.seek(0) #Move o cursor do buffer para o início do conteúdo.

        
        imagem = Image.open(buffer)

        print("gráfico pizza gerado")

        return imagem

    def gerar_grafico2(self):
        #Método responsável por gerar o gráfico de consumo por quantidade
        dicionario_grafico={}

        for email in dados_quantidade:
            if email in dados_consumo:
                qtd_membros = dados_quantidade[email]
                consumo = dados_consumo[email]
                valor_quantidade=str(qtd_membros)

                if valor_quantidade in dicionario_grafico:
                    dicionario_grafico[valor_quantidade] += consumo
                else:
                    dicionario_grafico[valor_quantidade] = consumo

                
        #Lista em ordem das chaves.Foi necessário passar temporariamente para inteiro para ser possível ordenar
        #quantidade=Eixo x
        quantidades = sorted(dicionario_grafico.keys(), key=int)
        
        #Aqui usará um loop for para as quantidades já ordenadas,para ser possível colocar o consumo na ordem correta em
        #relação a cada chave
        #Consumo=Eixo y
        consumos=[]    
        for qtd in quantidades:
            consumos.append(dicionario_grafico[qtd])

        

       # Criar figura e área onde o gráfico será desenhado
       #fig="janela" que será utilizada para armazenar a area_utilizada pela figura
        fig, area_utilizada = plt.subplots(figsize=(10, 6))

        # Criar gráfico de barras de consumo(eixoy) x quantidade(eixo x) com a cor skyblue
        area_utilizada.bar(quantidades, consumos, color="skyblue")

        #Título do gráfico
        area_utilizada.set_title("Consumo total por quantidade de moradores", fontsize=16, pad=20)
        #Título relação eixo x
        area_utilizada.set_xlabel("Quantidade de moradores", fontsize=12)
        #Título relação eixo y
        area_utilizada.set_ylabel("Consumo total (litros ou m³)", fontsize=12)
        #cria linhas no eixo y para ajudar a visualizar na análise de dados
        area_utilizada.grid(axis="y", linestyle="--", alpha=0.7)

        # Função enumerate retorna o índice do valor e o valor que está na lista
        for i, valor in enumerate(consumos):
            #+1 serve para posicionar o texto acima da barra.Valor é o valor no eixo y
            #passa o valor para string para ser possível colocar em texto
            #ha=centraliza o texto
            #
            area_utilizada.text(i, valor + 1, str(valor), ha=
                                "center", va="bottom", fontsize=10)

        #AJUSTA AUTOMATICAMENTE O CONTEÚDO DA FIGURA PARA QUE NENHUM TEXTO OU LABEL FIQUE CORTADO   
        plt.tight_layout()

        #aqui cria um buffer na memória(um arquivo temporário na memória)
        buffer = BytesIO()
        #salva a figura no buffer,como se fosse uma imagem sendo "salva em um frame"
        fig.savefig(buffer, format="png", bbox_inches="tight")
        #bbox_inches='tight' corta os espaços em branco 
        #fecha a imagem para liberar RAM e evitar vazamento de memória
        plt.close(fig)

        
        buffer.seek(0)

        #abre o buffer como imagem PIL
        imagem = Image.open(buffer)

        return imagem



    def gerar_grafico3(self):
        dicionario_grafico2={}
       
        dicionario_andares = {
            "10": 0,
                            "20": 0,
                            "30":0,
                            "40": 0,
                            "50": 0,
                            "60": 0,
                            "70":0,
                            "80": 0,
                            "90": 0}

        for email in dados_apartamento:
            if email in dados_consumo:
                apartamento=str(dados_apartamento[email])
                consumo=dados_consumo[email]
                dicionario_grafico2[apartamento]=consumo

        for apartamentos_validos in dicionario_grafico2:
            if apartamentos_validos.startswith("10"):
                dicionario_andares["10"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("20"):
                dicionario_andares["20"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("30"):
                dicionario_andares["30"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("40"):
                dicionario_andares["40"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("50"):
                dicionario_andares["50"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("60"):
                dicionario_andares["60"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("70"):
                dicionario_andares["70"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("80"):
                dicionario_andares["80"] += dicionario_grafico2[apartamentos_validos]
            elif apartamentos_validos.startswith("90"):
                dicionario_andares["90"] += dicionario_grafico2[apartamentos_validos]
        #Lista em ordem das chaves.Foi necessário passar temporariamente para inteiro para ser possível ordenar
        #quantidade=Eixo x
        
        #Lista os valores das chaves do dicionário
        andares=list(dicionario_andares.keys())

        #Lista os valores das chaves
        consumos=list(dicionario_andares.values())
        

       # Criar figura e área onde o gráfico será desenhado
       #fig="janela" que será utilizada para armazenar a area_utilizada pela figura
        fig, area_utilizada = plt.subplots(figsize=(10, 6))

        # Criar gráfico de barras de consumo(eixoy) x quantidade(eixo x) com a cor skyblue
        area_utilizada.bar(andares, consumos, color="skyblue")

        #Título do gráfico
        area_utilizada.set_title("Consumo total por andar", fontsize=16, pad=20)
        #Título relação eixo x
        area_utilizada.set_xlabel("Andar correspondente", fontsize=12)
        #Título relação eixo y
        area_utilizada.set_ylabel("Consumo total (litros ou m³)", fontsize=12)
        #cria linhas no eixo y para ajudar a visualizar na análise de dados
        area_utilizada.grid(axis="y", linestyle="--", alpha=0.7)

        # Função enumerate retorna o índice do valor e o valor que está na lista
        for i, valor in enumerate(consumos):
            #+1 serve para posicionar o texto acima da barra.Valor é o valor no eixo y
            #passa o valor para string para ser possível colocar em texto
            #ha=centraliza o texto
            #
            area_utilizada.text(i, valor + 1, str(valor), ha="center", va="bottom", fontsize=10)

        #AJUSTA AUTOMATICAMENTE O CONTEÚDO DA FIGURA PARA QUE NENHUM TEXTO OU LABEL FIQUE CORTADO   
        plt.tight_layout()

        #aqui cria um buffer na memória(um arquivo temporário na memória)
        buffer = BytesIO()
        #salva a figura no buffer,como se fosse uma imagem sendo "salva em um frame"
        fig.savefig(buffer, format="png", bbox_inches="tight")
        #bbox_inches='tight' corta os espaços em branco 
        #fecha a imagem para liberar RAM e evitar vazamento de memória
        plt.close(fig)

        
        buffer.seek(0)

        #abre o buffer como imagem PIL
        imagem = Image.open(buffer)

        return imagem

        
        

        
            

    def gerar_valor_media(self):
        
        consumo_listado=list(dados_consumo.values())
        media_consumo_condominio=sum(consumo_listado)
        

        return media_consumo_condominio
    pass
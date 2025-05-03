import sys
import json
import time
import re

# RESOLVER EMAIL
# LOGIN
# ATUALIZAR
# DELETAR


with open(r"D:/github/PERÍODO 1/projetova1/projetova1/banco_dados.JSON", "r", encoding="utf-8") as arquivo:
    # quando usa json.load o arquivo json é transformado em dicionário python
    arquivo_lido = json.load(arquivo)
    dados_conta = arquivo_lido["senha"]
    dados_familia = arquivo_lido["familia"]
    dados_quantidade = arquivo_lido["membros"]
    dados_pontos = arquivo_lido["pontos"]
    dados_apartamento = arquivo_lido["apartamento"]
    dados_codigov = arquivo_lido["verificador"]


def login():
    with open(r"D:/github/PERÍODO 1/projetova1/projetova1/banco_dados.JSON", "r", encoding="utf-8") as arquivo:
    # quando usa json.load o arquivo json é transformado em dicionário python
        arquivo_lido = json.load(arquivo)

        print("Bem vindo a tela de Login ECODROP.")
        email=input("Digite seu email(escreva da forma correta):")
        #"joao.silva@email.com": "48291" dados para teste
        senha=input("Digite sua senha:")
        if email in dados_conta:
            if dados_conta[email]==senha:
                menu()
            else:
                print("SENHA OU EMAIL INCORRETO.")
                tentativas=2
                while tentativas!=0:
                    email=input("Digite seu email(escreva da forma correta):")
                    senha=input("Digite sua senha:")
                    if dados_conta[email]==senha:
                        menu()
                    else:
                        print("SENHA OU EMAIL INCORRETO.")
                        tentativas-=1
                else:
                    print("NÚMERO DE TENTATIVAS EXTRAPOLADAS.TENTE NOVAMENTE MAIS TARDE.")



        
        else:
            print("EMAIL NÃO CADASTRADO.")
            opcao=input("Deseja ir para tela de cadastro ou sair do sistema ??(cadastro/sair)").strip().lower()
            if opcao in ["cadastro", "cadastrar", "criar conta", "novo cadastro"]:
                cadastro_novo=Cadastro()
            elif opcao in ["sair","sair sistema","quitar","sai"]:
                print("Tenha um bom dia!!")
                sys.exit()
                
            











def atualizar():
    pass


def deletar():
    pass


def feedback():
    pass


def ranking():
    pass


def resgatar():
    pass


def calculo():
    pass


def menu():
    tentativas = 3
    print("BEM VINDO AO MENU PRINCIPAL DO ECODROP💧.")
    while tentativas != 0:
        resposta2 = input(
            "Qual tipo de função você deseja ?? (Ranking/Calcular pontos/Atualizar conta/Deletar conta/Feedback/Resgatar recompensas) ").strip().lower()

        if resposta2 in ["ver ranking", "ranking"]:
            ranking()
            return

        elif resposta2 in ["calcular pontos", "calcular", "calculo", "pontos"]:
            calculo()
            return

        elif resposta2 in ["atualizar", "atualização", "atualizar conta", "atualiza conta"]:
            atualizar()
            return

        elif resposta2 in ["deletar", "deletar conta", "excluir", "excluir conta", "apagar conta"]:
            deletar()
            return

        elif resposta2 in ["feedback", "enviar feedback", "sugestao", "sugestão", "critica", "crítica"]:
            feedback()
            return
        elif resposta2 in ["resgatar", "recompensa", "resgatar recompensa", "prêmios", "premio"]:
            resgatar()
            return

        else:
            print("Resposta inválida")
            tentativas -= 1

    else:
        print("Limite de tentativas atingido. Reinicie o programa.")


class Cadastro:
    def __init__(self):
        self.email = input(
            "Digite o email que você gostaria de vincular sua conta:")
        self.quantidade = int(
            input("Informe a quantidade de pessoas na sua residência:"))
        self.senha = input("Digite sua senha(Coloque uma senha forte):")
        self.nome_familia = input(
            "Digite o nome que ficará cadastrado sua família(COLOQUE 1 OU DOIS SOBRENOMES):")
        self.pontos = 0
        self.apartamento = int(input("Digite o número do seu apartamento:"))
        self.verificador = input("Digite seu código verificador:\n"
                               "ATENÇÃO,GUARDE ESSE CÓDIGO DE UMA FORMA SEGURA,CASO VOCÊ ESQUEÇA A SENHA ELE É A ÚNICA FORMA DE CONSEGUIR ACESSAR A CONTA:")
        self.conferir_email()

    # precisa passar o self como parâmetro para conseguir pegar as info do init

   
        

    def conferir_email(self):
        dominios_validos = [
        'gmail.com', 'outlook.com', 'hotmail.com',
        'yahoo.com', 'icloud.com'
        ]

        tentativas_email = 3
        while tentativas_email != 0:
        # Verifica formato
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
                print("FORMATO DE EMAIL INVÁLIDO, UTILIZE UM DOMÍNIO VÁLIDO")
                self.email = input("Digite novamente seu email: ").strip()
                tentativas_email -= 1
                continue  # volta pro início do while para validar de novo

            # Verifica domínio
            dominio = self.email.split('@')[1].lower()
            if dominio not in dominios_validos:
                print("Domínio não aceito. Use: Gmail, Outlook, Yahoo, iCloud, etc.")
                self.email = input("Digite novamente seu email: ").strip()
                tentativas_email -= 1
                continue

        # Se chegou aqui, formato e domínio estão corretos
            break

        else:
            print("Limite de tentativas atingido. Encerrando o processo de cadastro.")
            return

    # Agora verifica se email já está cadastrado
        
        
        
        if self.email in dados_conta:
            print("EMAIL JÁ POSSUI UMA CONTA.")
            tentativas = 3
            while tentativas != 0:
                resposta1 = input("Deseja tentar refazer a conta ou ir para tela de login caso já possua conta? (refazer/login) ").strip().lower()
                if resposta1 in ["login", "tela de login", "logi"]:
                    login()
                    return
                elif resposta1 in ["refazer", "retentar", "conta", "refazer conta"]:
                    self.email = input("Digite novamente seu email: ").strip()
                    self.conferir_email
                    return
                else:
                    print("Resposta inválida")
                    tentativas -= 1
            else:
                print("Limite de tentativas atingido. Encerrando o processo de cadastro.")
                return
        else:
            self.conferir_ap()  # Continua o processo normalmente

        
        
        
        
        
        
        

    def conferir_ap(self):
        # dessa forma oq estará sendo analisado será o valor e não a chave
        if self.apartamento in dados_apartamento.values():
            print("APARTAMENTO JÁ CADASTRADO.")
            tentativas = 3
            while tentativas != 0:
                resposta1 = input("Deseja tentar refazer a conta ou ir para tela de login caso já possua conta ??(refazer/login)").strip().lower()
                if resposta1 in ["login", "tela de login","logi"]:
                    login()
                    return
                elif resposta1 in ["refazer", "retentar","conta","refazer conta"]:
                    Cadastro()
                    return
                else:
                    print("Resposta inválida")
                    tentativas -= 1
            else: # ✅ Só imprime quando zerar tentativas
                print("Limite de tentativas atingido. Encerrando o processo de cadastro.")
        else:
            self.cadastrar_conta()



    def cadastrar_conta(self):
           #print("Bem vindo ao projeto ECODROP do condomínio Village")

        dados_conta[self.email] = self.senha
        dados_familia[self.email] = self.nome_familia
        dados_quantidade[self.email] = self.quantidade
        dados_pontos[self.email] = self.pontos
        dados_apartamento[self.email] = self.apartamento
        dados_codigov[self.email] = self.verificador


        # PARA ARQUIVO TIPO JSON É MELHOR USAR "w" pois qualquer errinho de formatação pode quebrar o sistema
        with open(r"D:/github/PERÍODO 1/projetova1/projetova1/banco_dados.JSON", "w", encoding="utf-8") as arquivo:
            #Aqui, estamos criando um dicionário com duas chaves:
            json.dump({"senha": dados_conta, "familia": dados_familia, "membros":dados_quantidade,"pontos":dados_pontos,
                       "apartamento": dados_apartamento,"verificador":dados_codigov},arquivo, indent=4, ensure_ascii=False)
        menu()


 # Essa parte que vai realmente começar o código
 # Esse código tem que ser escrito de cima pra baixo,mas para puxar ele tem que ser lá embaixo,pois só assim para o código
 # conseguir usar todas as funções
 #
print("OLÁ,BEM VINDO AO SISTEMA ECODROP💧 do condomínio Village")

tentativas = 3  # Por exemplo, 3 tentativas permitidas
while tentativas != 0:
    tipo_servico = input("QUAL TIPO DE SERVIÇO VOCÊ DESEJA ?? (LOGIN/CADASTRO) ").strip().lower()

    if tipo_servico in ["login", "entrar", "acessar", "fazer login"]:
        login()
        break  # Sai do loop se o serviço for válido

    elif tipo_servico in ["cadastro", "cadastrar", "criar conta", "novo cadastro"]:
        novo_cadastro = Cadastro()
        break  # Sai do loop se o serviço for válido

    else:
        print("Serviço inválido. Por favor, tente novamente.")
        tentativas -= 1

else:
    print("Limite de tentativas atingido. Reinicie o programa.")

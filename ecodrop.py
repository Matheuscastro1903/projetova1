import sys
import json
import time

with open(r"D:/github/PERÍODO 1/projetova1/projetova1/banco_dados.JSON", "r", encoding="utf-8") as arquivo:
    arquivo_lido = json.load(arquivo)  # quando usa json.load o arquivo json é transformado em dicionário python
    dados_conta = arquivo_lido["senha"]
    dados_familia = arquivo_lido["familia"]
    dados_quantidade=arquivo_lido["membros"]
    dados_pontos=arquivo_lido["pontos"]
    dados_apartamento=arquivo_lido["apartamento"]
    dados_codigov=arquivo_lido["verificador"]



def login():
    pass
def atualizar():
    pass
def deletar():
    pass

def menu():
    pass

class Cadastro:
    def __init__(self):
        self.email=input("Digite o email que você gostaria de vincular sua conta:")
        self.quantidade=int(input("Informe a quantidade de pessoas na sua residência:"))
        self.senha=input("Digite sua senha(Coloque uma senha forte):")
        self.nome_familia=input("Digite o nome que ficará cadastrado sua família(COLOQUE 1 OU DOIS SOBRENOMES):")
        self.pontos=0
        self.apartamento=int(input("Digite o número do seu apartamento:"))
        self.verificador=input("Digite seu código verificador:\n" \
        "ATENÇÃO,GUARDE ESSE CÓDIGO DE UMA FORMA SEGURA,CASO VOCÊ ESQUEÇA A SENHA ELE É A ÚNICA FORMA DE CONSEGUIR ACESSAR A CONTA.")
        self.conferir_email()



    def conferir_email(self):#precisa passar o self como parâmetro para conseguir pegar as info do init
        
        
        if self.email in dados_conta:
            print("EMAIL JÁ POSSUI UMA CONTA.")
            tentativas=3
            while tentativas !=0:
                resposta1=input("Deseja tentar refazer a conta ou ir para tela de login caso já possua conta ??(refazer/login)").strip().lower()
                if resposta1 in ["login","tela de login","logi"]:
                    login()
                elif resposta1 in ["refazer","retentar","conta","refazer conta"]:
                    Cadastro()
                else:
                    print("Resposta inválida")
                    tentativas-=1
            print("Limite de tentativas atingido. Encerrando o processo de cadastro.")
        else:
            self.conferir_ap()


    def conferir_ap(self):
        #dessa forma oq estará sendo analisado será o valor e não a chave
        if self.apartamento in dados_apartamento.values():
            print("APARTAMENTO JÁ CADASTRADO.")
            tentativas=3
            while tentativas !=0:
                resposta1=input("Deseja tentar refazer a conta ou ir para tela de login caso já possua conta ??(refazer/login)").strip().lower()
                if resposta1 in ["login","tela de login","logi"]:
                    login()
                elif resposta1 in ["refazer","retentar","conta","refazer conta"]:
                    Cadastro()
                else:
                    print("Resposta inválida")
                    tentativas-=1
            print("Limite de tentativas atingido. Encerrando o processo de cadastro.")
        else:
            self.cadastrar_conta()


            
    def cadastrar_conta(self):    
            print("Bem vindo ao projeto ECODROP do condomínio Village")

            dados_conta[self.email]=self.senha
            dados_familia[self.email]=self.nome_familia
            dados_quantidade[self.email]=self.quantidade
            dados_pontos[self.email]=self.pontos
            dados_apartamento[self.email]=self.apartamento
            dados_codigov[self.email]=self.verificador


            
            
            #PARA ARQUIVO TIPO JSON É MELHOR USAR "w" pois qualquer errinho de formatação pode quebrar o sistema
            with open(r"C:\future\python\primeiro\gpt\ajudabanco.JSON", "w", encoding="utf-8") as arq:
            #Aqui, estamos criando um dicionário com duas chaves:
                json.dump({"senha": dados_conta, "familia": dados_familia,"membros":dados_quantidade,"pontos":dados_pontos,
                           "apartamento":dados_apartamento,"verificador":dados_codigov},arquivo, indent=4, ensure_ascii=False)
            self.


            
            tentativas=3
            while tentativas !=0:
                print("BEM VINDO AO MENU PRINCIPAL DO ECODROP💧.")
                
                resposta2=input("Qual tipo de função você deseja ??(Ranking/Calcular pontos/atualizar conta/deletar conta/Feedback)").strip().lower()
                if resposta2 in ["ver ranking","ranking"]:
                    self.ranking()
                elif resposta2 in ["calcular pontos","calcular","calculo","pontos"]:
                    self.calculo()
                elif resposta2 in ["atualizar","atualização","atualizar conta","atualiza conta"]:
                    self.
                else:
                    print("Resposta inválida")
                    tentativas-=1
            print("Limite de tentativas atingido.Reinicie o programa.")
    
   
   
    def ranking(self):
        pass
    def calculo(self):
        pass
            
            



#usuario:Cadastro()


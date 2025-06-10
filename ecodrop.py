import sys
import json
import time
import re
import random
import os
import pyfiglet


#ANOTAÇÃO IMPORTANTE
#Se uma função chama outra função que precisa de argumentos, ela também precisa receber esses argumentos ou criá-los.


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
    

#OBJETIVO DESSA MENSAGEM É SER UMA MENSAGEM DIÁRIA ALEATÓRIA,VISANDO FICAR MAIS INTERATIVO COM O USUÁRIO
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




def barra_progresso():
    #print("Salvando dados")
    for i in range(1, 11):
        blocos = "■" * i
        espacos = "□" * (10 - i)
        porcentagem = i * 10
        sys.stdout.write(f"\r[{blocos}{espacos}] {porcentagem}%")
        sys.stdout.flush()
        time.sleep(0.3)  # tempo entre cada etapa

    print(" ✅ Concluído!")

# Exemplo de uso

import random
import string

def gerar_codigo_resgate():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=4))
    print("Seu código para resgatar a recompensa:")
    print(f"{letras}-{numeros}")

def limpar_tela():
	
    """objetivo dessa função é limpar a tela sempre que passar para outra seção,deixando o projeto mais real"""
    #FUNÇÃO UTILIZADO PARA LIMPAR O TERMINAL,DEIXANDO O SISTEMA MAIS "REAL"
    os.system('cls' if os.name == 'nt' else 'clear')

def login():
    """
    objetivo dessa função é o usuário poder entrar no sistema colocando seus dados da conta.
    Caso ele não possua conta será redirecionado para página de cadastro.Caso ele
    esqueça a senha poderá utilizar o código verificador(definido no cadastro) para recuperar a conta
    """
#FUNÇÃO UTILIZADA PARA O USUÁRIO CONSEGUIR FAZER LOGIN
    
    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
        # quando usa json.load o arquivo json é transformado em dicionário python
        arquivo_lido = json.load(arquivo)
        
        dados_conta = arquivo_lido["senha"]
        dados_familia = arquivo_lido["familia"]
        dados_quantidade = arquivo_lido["membros"]
        dados_pontos = arquivo_lido["pontos"]
        dados_apartamento = arquivo_lido["apartamento"]
        dados_codigov = arquivo_lido["verificador"]


        print("Bem vindo a tela de Login ECODROP💧.")
        #print(random.choice(mensagens_agua))
        time.sleep(1)
        email_login = input("Digite seu email(ex:nome123@gmail.com):")
        # "joao.silva@email.com": "48291" dados para teste
        senha_login = input("Digite sua senha:")
        if email_login in dados_conta:
            if dados_conta[email_login] == senha_login:
                limpar_tela()
                menu(email_login,senha_login)
            else:
                print("EMAIL OU SENHA INCORRETO.")
                tentativas = 2
                while tentativas != 0:
                    email_login = input("Digite seu email(nome123@gmail.com):")
                    senha_login = input("Digite sua senha:")
                    if dados_conta[email_login] == senha_login:
                        limpar_tela()
                        menu(email_login,senha_login)
                        
                        return
                    else:
                        print("SENHA OU EMAIL INCORRETO.")
                        tentativas -= 1
                        print(f"Tentativas restantes {tentativas}")
                else:
                    print("NÚMERO DE TENTATIVAS EXTRAPOLADAS.TENTE NOVAMENTE MAIS TARDE.")
                    tentativas_verificador=3
                    while tentativas_verificador!=0:
                        question1 = input("Deseja tentar entrar usando código verificador ??(sim/não)")
                        if question1 in ["sim", "si", "yes", "codigo", "código verificador", "verificador", "código"]:
                            tryverificador = input("Digite seu código verificador(Você terá apenas 1 chance):")
                            if dados_codigov[email_login] == tryverificador:
                                print("Você conseguiu o acesso.Mude imediatamente sua senha,visando não ter problemas futuros.")
                                menu(email_login,senha_login)
                                return
                            else:
                                print("Você errou o código verificador.")
                                print("Tente novamente mais tarde.Use esse tempo para tentar relembrar seus dados.")
                                sys.exit()
                        elif question1 in ["não", "no", "nao", "sair", "sai"]:
                            print("Tenha um bom dia.")
                            sys.exit()
                        else:
                            print("OPÇÃO INÁLIDA.")
                            tentativas-=1
                            print(f"Número de tentativas restantes {tentativas}")
                    else:
                        print("NÚMERO DE TENTATIVAS EXTRAPOLADAS.TENTE NOVAMENTE MAIS TARDE.")
                        sys.exit()

        else:
            print("EMAIL NÃO CADASTRADO.")
            opcao = input(
                "Deseja ir para tela de cadastro ou sair do sistema ??(cadastro/sair)").strip().lower()
            if opcao in ["cadastro", "cadastrar", "criar conta", "novo cadastro"]:
                cadastro_novo = Cadastro()
            elif opcao in ["sair", "sair sistema", "quitar", "sai"]:
                print("Tenha um bom dia!!")
                sys.exit()
            else:
                print("Opção inválida")
                tentativas3 = 2
                while tentativas3 != 0:
                    opcao = input(
                        "Deseja ir para tela de cadastro ou sair do sistema ??(cadastro/sair)").strip().lower()
                    if opcao in ["cadastro", "cadastrar", "criar conta", "novo cadastro"]:
                        cadastro_novo = Cadastro()
                    elif opcao in ["sair", "sair sistema", "quitar", "sai"]:
                        print("Tenha um bom dia!!")
                        sys.exit()
                    else:
                        print("Opção inválida")
                        print(f"Tentativas restantes {tentativas3}")
                        tentativas3 -= 1

                print("NÚMERO DE TENTATIVAS EXTRAPOLADAS.TENTE NOVAMENTE MAIS TARDE.")
                sys.exit()


def menu(email_login,senha_login):
    """
 	Essa função é utilizada para ir para tela de menu,assim que o usuário entrar no sistema.Aqui ele poderá ver quais opções de serviço ele tem.
 	
    """
    #FUNÇÃO UTILIZADA PARA CONSEGUIR VER AS OPÇOES DE FUNÇÕES
    limpar_tela()
    tentativas = 3
    print("BEM VINDO AO MENU PRINCIPAL DO ECODROP💧.")
    #mensagem estilo minecraft
    print("ECOMENSAGEM DIÁRIA 💧:")
    print("-"*60)
    print(random.choice(mensagens_agua))
    print("-"*60)
    
    time.sleep(2)
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║ 🌍 ESCOLHA UMA OPÇÃO NUMÉRICA                              ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print("║ 1. Ver Ranking 🏆                                          ║")
    print("║ 2. Calcular Pontos 💧                                      ║")
    print("║ 3. Atualizar Dados 🔄                                      ║")
    print("║ 4. Deletar Conta ❌                                        ║")
    print("║ 5. Enviar Feedback ✉️                                       ║")
    print("║ 6. Resgatar Recompensas 🎁                                 ║")
    print("║ 7. Visualizar Dados 📊                                     ║")
    print("║ 8. Sair do Sistema 🚪                                      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    #resposta2 = input("Digite o número da opção desejada: ").strip()
    
    while tentativas != 0:
        
        resposta2 = input("Digite o número da opção desejada: ").strip()

        if resposta2 == "1":
            ranking(email_login,senha_login)
            return

        elif resposta2 == "2":
            calculo(email_login,senha_login)
            return

        elif resposta2 == "3":
            atualizar(email_login, senha_login)
            return

        elif resposta2 == "4":
            deletar(email_login, senha_login)
            return

        elif resposta2 == "5":
            feedback(email_login, senha_login)
            return

        elif resposta2 == "6":
            resgatar(email_login, senha_login)
            return

        elif resposta2 == "7":
            mostrar_dados(email_login, senha_login)
            return

        elif resposta2 == "8":
            print("Tenha um bom dia!!")
            sys.exit()

        else:
            print("❌ Opção inválida. Tente novamente.")
            tentativas -= 1

    print("❗ Limite de tentativas atingido. Reinicie o programa.")
    sys.exit()


def mostrar_dados(email_login,senha_login):
    """
	Nessa função o usuário poderá ver seus dados da conta,como o email vinculado,quantidade de membros,pontos acumulados,apartamento cadastrado e o nome da família
    """
	#FUNÇÃO UTILIZADA PARA MOSTRAR OS DADOS DA CONTA
    limpar_tela()
    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
    # quando usa json.load o arquivo json é transformado em dicionário python
        arquivo_lido = json.load(arquivo)
        dados_conta = arquivo_lido["senha"]
        dados_familia = arquivo_lido["familia"]
        dados_quantidade = arquivo_lido["membros"]
        dados_pontos = arquivo_lido["pontos"]
        dados_apartamento = arquivo_lido["apartamento"]
        dados_codigov = arquivo_lido["verificador"]
        print("\n" + "="*30 + " DADOS DA CONTA " + "="*30)
        print(f"\n• EMAIL CADASTRADO: {email_login}")
        print(f"• QUANTIDADE DE MEMBROS: {dados_quantidade[email_login]}")
        print(f"• PONTOS ACUMULADOS: {dados_pontos[email_login]}")
        print(f"• APARTAMENTO: {dados_apartamento[email_login]}")
        print(f"• NOME DA FAMÍLIA: {dados_familia[email_login]}")
        time.sleep(1)
        tentativas = 3  # Máximo de tentativas permitidas

        print("\n╔════════════════════════════════════════════════════╗")
        print("║ O que você deseja fazer agora?                    ║")
        print("║ 1. Ir para o Menu 💧                              ║")
        print("║ 2. Sair do Sistema 🚪                              ║")
        print("╚════════════════════════════════════════════════════╝")

        while tentativas != 0:
            opcao = input("Digite o número da opção desejada: ").strip()

            if opcao == "1":
                menu(email_login, senha_login)
                break

            elif opcao == "2":
                print("\n📢 Sistema encerrado pelo usuário. Até logo!")
                sys.exit()

            else:
                tentativas -= 1
                print("\n❌ Opção inválida. Por favor, escolha 1 ou 2.")
                print(f"🔁 Tentativas restantes: {tentativas}")

        else:
            print("\n⚠️ Limite de tentativas atingido. Sistema encerrado automaticamente.")
            sys.exit()

        


    pass



def atualizar(email_login,senha_login):
    #FUNÇÃO UTILIZADA PARA MOSTRAR AS OPÇOES DE ATUALIZAÇÃO(ATUALIZAR DADOS PESSOAIS OU DADOS DA CONTA)   
    """
	Essa função irá dar a opção do usuário atualizar os dados da conta(email,senha) ou os dados pessoais(quantidade de membros,apartamento cadastrado e o nome da família),.A partir da sua resposta,ele será 
 	encaminhado para outra aba
    """

    limpar_tela()
    print("╔════════════════════════════════════════════════╗")
    print("║ 🔄 BEM-VINDO À TELA DE ATUALIZAÇÃO DO ECODROP ║")
    print("╚════════════════════════════════════════════════╝")

	
    tentativas = 3
    print("OPÇÕES DE ATUALIZAÇÃO")
    print("╔════════════════════════════╗")
    print("║ 1. Dados da Conta 🔐       ║")
    print("║ 2. Dados Pessoais 👤       ║")
    print("╚════════════════════════════╝")

    while tentativas > 0:
        question1 = input("Digite o número da opção que você deseja:").strip().lower()

        if question1=="1":
            tipo_atualizacao(email_login,senha_login)
            return

        elif question1=="2":
            atualizar_pessoais(email_login,senha_login)
            return

        else:
            print("Opção inválida.")
            tentativas -= 1
            print(f"Tentativas restantes: {tentativas}")

    print("Limite de tentativas atingido. Encerrando o processo de atualização.")

    #pass



def atualizar_pessoais(email_login,senha_login):
    """
	Essa função será utilizada para atualizar os dados pessoais em relação a conta cadastrada
    """
	
	#FUNÇÃO UTILIZADA PARA ATUALIZAR OS DADOS PESSOAIS RELACIONADOS A UMA CONTA
    # Carregar os dados do arquivo
    limpar_tela()
    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
        arquivo_lido = json.load(arquivo)
        dados_conta = arquivo_lido["senha"]
        dados_familia = arquivo_lido["familia"]
        dados_quantidade = arquivo_lido["membros"]
        dados_pontos = arquivo_lido["pontos"]
        dados_apartamento = arquivo_lido["apartamento"]
        dados_codigov = arquivo_lido["verificador"]



        while True:
            try:
                membros_novos = int(input("Digite a quantidade de membros na família (Quantidade em numeral):"))
                break
            except ValueError:
                print("Valor inválido. Digite apenas números inteiros.")
    
        nome_novo = input("Digite o nome da sua família (Ficará registrado no ranking da forma que você escrever):")
        
        #números no meio do print servem para organizar da maneira correta,dizendo que precisa de n espaços para escrever aquilo que desejo
        #deixando todas as colunas alinhadas
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║                     DADOS ATUALIZADOS                   ║")
        print("╠════════════════════════════════════════════════════════╣")
        print(f"║ Quantidade de pessoas na família: {membros_novos:<23}║")
        print(f"║ Nome da família: {nome_novo:<38}║")
        print("╚════════════════════════════════════════════════════════╝\n")

    
    
        print("Cuidado⚠️!!Caso você confirme essa atualização deve ficar ciente que os antigos dados serão atualizados e não poderão ser "
        "acessados novamente")
        time.sleep(1)
    
        tentativas = 3
        while tentativas != 0:
            confirmar = input("Deseja confirmar a atualização dos dados? (sim/não): ").strip().lower()
            if confirmar in ["sim", "si", "confirmar", "confirma", "confirmo"]:
        
                
                dados_conta[email_login] = senha_login
                dados_familia[email_login] = nome_novo
                dados_quantidade[email_login] = membros_novos
                dados_pontos[email_login] = dados_pontos[email_login]
                dados_apartamento[email_login] = dados_apartamento[email_login]
                dados_codigov[email_login] = dados_codigov[email_login]
        
        
        
      
                
                # Salva os dados modificados no arquivo
                with open(r"banco_dados.JSON", "w", encoding="utf-8") as arquivo:
                    json.dump({"senha": dados_conta, "familia": dados_familia,"membros": dados_quantidade, "pontos": dados_pontos,"apartamento": dados_apartamento,
                               "verificador": dados_codigov
                               }, arquivo, indent=4, ensure_ascii=False)
                print("Salvando dados...")    
                barra_progresso()
                print("Conta atualizada com sucesso.")
                time.sleep(1)
                tentativas = 3  # Máximo de tentativas permitidas

                while tentativas != 0:
                    opcao = input("Deseja ir para o login ou sair do sistema ??(Login/sair): ").strip().lower()

                    if opcao in ["login","logi"]:
                        login()
                        break  #Sai do loop e chama a função login

                    elif opcao in ["sair","sai","sair sistema","sai sistema"]:
                        print("Sistema encerrado pelo usuário.")
                        sys.exit()
                        

                    else:
                        tentativas -= 1
                        print("❌ Opção inválida. Tente novamente.")
                        print(f"Tentativas restantes: {tentativas}")
                #caso o usuártio escreva erado

                else:
                    print("Limite de tentativas atingido. Sistema encerrado automaticamente.")

        

            elif confirmar in ["não", "nao", "cancelar", "cancelo", "cancela"]:
                print("Cancelando operação... Voltando para o menu inicial.")
                menu(email_login,senha_login)  # Substitua com sua função de menu, caso necessário
                return
            else:
                print("❌ Opção inválida. Cancelando operação.")
                tentativas-=1
                print(f"Tentativas restantes {tentativas}")
        else:
            print("Limite de tentativas atingido")
            print("Reinicie o sistema")
            sys.exit()

def tipo_atualizacao(email_login, senha_login):
    """
    Essa função tem o objetivo de definir o que será atualizado em relação aos dados da conta(email,senha,ambos)
    """
    
    limpar_tela()
    tentativas = 3
    print("\nO que você deseja atualizar?")
    print("╔════════════════════════════╗")
    print("║ 1. Apenas email 📧          ║")
    print("║ 2. Apenas senha 🔒          ║")
    print("║ 3. Email e senha ✉️🔑      ║")
    print("╚════════════════════════════╝")
    while tentativas != 0:
        opcao = input("Digite o número da opção desejada (1, 2 ou 3): ").strip()

        if opcao == "1":
            valido_apenas_email(email_login, senha_login)
            return
        elif opcao == "2":
            valido_apenas_senha(email_login)
            return
        elif opcao == "3":
            email_valido(email_login, senha_login)
            return
        else:
            print("OPÇÃO INVÁLIDA")
            tentativas -= 1
            print(f"Tentativas restantes = {tentativas}")
    else:
        print("Número de tentativas extrapolaram.")
        print("Reinicie o sistema.")
        sys.exit()





##############################################################################################################
#Conjunto de funções para atualizar ambos(email,senha)
def email_valido(email_login,senha_login):
    """
	Essa função será chamada caso o usuário deseje atualizar os dados da conta(email,senha).Ela tem a função de verificar se o email novo 
 	que será utilizado é válido ou não.Caso seja válido será chamada outra função para continuar o fluxo.
    
    """

    limpar_tela()
     


    dominios_validos = [
            'gmail.com', 'outlook.com', 'hotmail.com',
            'yahoo.com', 'icloud.com'
        ]
    email_novo=input("Digite seu novo email:")


    tentativas_email = 3
    while tentativas_email != 0:
            # VERIFICA SE O FORMATO DO EMAIL ESTÁ ESCRITO CORRETAMENTE
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',email_novo):
            print("FORMATO DE EMAIL INVÁLIDO, UTILIZE UM DOMÍNIO VÁLIDO")
            email_novo = input("Digite novamente seu email: ").strip()
            tentativas_email -= 1
            print(f"Tentativas restantes: {tentativas_email}")
            continue  # volta pro início do while para validar de novo,caso esteja correto,irá passar pelo verificador

            # VERIFICA APENAS O DOMÍNIO,SEPARA TODO O RESTO E PEGA APENAS A PARTE DO DOMÍNIO
        dominio = email_novo.split('@')[1].lower()
        if dominio not in dominios_validos:
            print("Domínio não aceito. Use: Gmail, Outlook, Yahoo, iCloud, etc.")
            email_novo = input("Digite novamente seu email: ").strip()
            tentativas_email -= 1
            print(f"Tentativas restantes: {tentativas_email}")

                # continuar o loop sem parar
            continue

        # Se chegou aqui, formato e domínio estão corretos
        
        return conferir_email(email_novo,email_login,senha_login)

    else:
        print("Limite de tentativas atingido. Encerrando o processo de cadastro.")
        # Agora verifica se email já está cadastrado
        #conferir_email(email_novo)
        #return acabará com a função email válido e para deixar apenas a função conferir email válida
        return None

        

    # Agora verifica se email já está cadastrado


    # Agora verifica se email já está cadastrado

def conferir_email(email_novo,email_login,senha_login):
    """
 	Essa função será utilizada para conferir se o email novo já está cadastrado ou não no banco de dados.Caso não esteja cadastrado será chamada a próxima função
  	"""
	##FUNÇÃO UTILIZADA PARA CONFERIR SE O NOVO EMAIL JÁ EXISTE NO BANCO DE DADOS OU NÃO
    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
    # quando usa json.load o arquivo json é transformado em dicionário python
        arquivo_lido = json.load(arquivo)
        dados_conta = arquivo_lido["senha"]
        dados_familia = arquivo_lido["familia"]
        dados_quantidade = arquivo_lido["membros"]
        dados_pontos = arquivo_lido["pontos"]
        dados_apartamento = arquivo_lido["apartamento"]
        dados_codigov = arquivo_lido["verificador"]


        if email_novo in dados_conta:
            print("EMAIL JÁ POSSUI UMA CONTA.")
            tentativas = 3
            while tentativas != 0:
                resposta1 = input(
                "Deseja tentar refazer a conta ou ir para tela de login caso já possua conta? (refazer/login) ").strip().lower()
                if resposta1 in ["login", "tela de login", "logi"]:
                    login()
                    return
                elif resposta1 in ["refazer", "retentar", "conta", "refazer conta"]:

                

                    email_novo = input("Digite novamente seu email: ")
                
                    conferir_email(email_novo,email_login,senha_login)

                    return
                else:
                    print("Resposta inválida")
                    tentativas -= 1
                    print(f"Tentativas restantes {tentativas}")
            else:
                print("Limite de tentativas atingido. Encerrando o processo de cadastro.")
                return
        else:
            conferir_senha(email_novo, email_login, senha_login)
               # atualizar_conta(email_novo, email_login, senha_login)  # Continua o processo normalmente


def conferir_senha(email_novo, email_login, senha_login):
    """
    Essa função será utilizada para evitar que a nova senha que será cadastrada(ou mantida) terá um tamanho compatível
    """
	#FUNÇÃO UTILIZADA PARA CONFERIR SE A SENHA NOVA PODE SER CADASTRADA
    senha_nova=input("Digite sua senha(No mínimo 4 caracteres no máximo 20):")
    tentativas = 3
    while tentativas > 0:
        if 4 <= len(senha_nova) and  len(senha_nova)<= 20:
            #print("Senha aceita.")
            atualizar_conta(email_novo,senha_nova,email_login,senha_login)  # Chama o próximo passo do cadastro
            #return para a função que estava sendo rodada e deixa rodando apenas a função que rodará
            return
        else:
            print("Número de caracteres inválido. Sua senha deve ter entre 4 e 20 caracteres.")
            senha_nova = input("Digite sua senha novamente: ").strip()
            tentativas -= 1
            print(f"Tentativas restantes: {tentativas}")

    print("Número máximo de tentativas atingido. Tente novamente mais tarde.")


def atualizar_conta(email_novo,senha_nova,email_login,senha_login):
    #ATUALIZAÇÃO DOS DADOS DA CONTA NO BANCO DE DADOS JSON
    """
     essa função será utilizada para atualizar a conta do usuário,atualizazando email e senha
    """

    limpar_tela()
    


    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo_lido_json:
        arquivo_lido = json.load(arquivo_lido_json)

    dados_conta = arquivo_lido["senha"]
    dados_familia = arquivo_lido["familia"]
    dados_quantidade = arquivo_lido["membros"]
    dados_pontos = arquivo_lido["pontos"]
    dados_apartamento = arquivo_lido["apartamento"]
    dados_codigov = arquivo_lido["verificador"]



    print("\n╔════════════════════════════════════════════════════════╗")
    print("║                    DADOS ATUALIZADOS                   ║")
    print("╠════════════════════════════════════════════════════════╣")
    print(f"║ Novo email cadastrado: {email_novo:<29}║")
    print(f"║ Nova senha: {senha_nova:<38}║")
    print("╠════════════════════════════════════════════════════════╣")
    print("║ ⚠️ Cuidado! Caso confirme essa atualização, os dados   ║")
    print("║ antigos serão substituídos e não poderão ser acessados.║")
    print("╚════════════════════════════════════════════════════════╝\n")
    

    time.sleep(1)

    tentativas=3
    while tentativas!=0:
        confirmar = input("Deseja confirmar a atualização dos dados? (sim/não): ").strip().lower()
        
       
        if confirmar in ["sim", "si", "confirmar", "confirma", "confirmo"]:
        

                
                # Copia os dados para o novo e-mail
            dados_conta[email_novo] = senha_nova
            dados_familia[email_novo] = dados_familia[email_login]
            dados_quantidade[email_novo] = dados_quantidade[email_login]
            dados_pontos[email_novo] = dados_pontos[email_login]
            dados_apartamento[email_novo] = dados_apartamento[email_login]
            dados_codigov[email_novo] = dados_codigov[email_login]

            # Remove o antigo e-mail
            del dados_conta[email_login]
            del dados_familia[email_login]
            del dados_quantidade[email_login]
            del dados_pontos[email_login]
            del dados_apartamento[email_login]
            del dados_codigov[email_login]

            # Salva os dados atualizados
            with open(r"banco_dados.JSON", "w", encoding="utf-8") as arquivo:
                json.dump({
                    "senha": dados_conta,
                    "familia": dados_familia,
                    "membros": dados_quantidade,
                    "pontos": dados_pontos,
                    "apartamento": dados_apartamento,
                    "verificador": dados_codigov
                }, arquivo, indent=4, ensure_ascii=False)
                print("Salvando dados...")
                barra_progresso()
                print(f"Dados da conta {email_novo} atualizados com sucesso!")
                print("Conta cadastrada com sucesso.")
                time.sleep(1)
                tentativas = 3  # Máximo de tentativas permitidas

                while tentativas != 0:
                    opcao = input("Deseja ir para o login ou sair do sistema ??(Login/sair): ").strip().lower()

                    if opcao in ["login","logi"]:
                        login()
                        break  #Sai do loop e chama a função login

                    elif opcao in ["sair","sai","sair sistema","sai sistema"]:
                        print("Sistema encerrado pelo usuário.")
                        sys.exit()
                        break  # Sai do loop e fecha o sistema

                    else:
                        tentativas -= 1
                        print("Opção inválida. Por favor, tente novamente.")
                        print(f"Tentativas restantes: {tentativas}")
                #caso o usuártio escreva erado

                else:
                    print("Limite de tentativas atingido. Sistema encerrado automaticamente.")

            
        
        

        elif confirmar in ["não", "nao", "cancelar", "cancelo", "cancela"]:
            print("Cancelando operação... Voltando para o menu inicial.")
            time.sleep(1)
            menu()
            return
        else:
            print("Opção inválida. ")
            tentativas-=1
            print(f"Quantidade de tentativas restantes={tentativas}")

    else:
        print("Limite de tentativas atingido")
        print("Reinicie o sistema")
        sys.exit()

###############################################################################################################
#Parte do código voltado para atualização apenas do email

def valido_apenas_email(email_login, senha_login):
    """
    Essa função tem o objetivo de verificar se o email que será atualizado é valido ou não,caso seja válido poderá continuar 
    para a próxima etapa
    """
    limpar_tela()
    dominios_validos = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com', 'icloud.com']
    tentativas_email = 5
    
    while tentativas_email > 0:
        email_novo = input("Digite seu novo email: ").strip()
        
        # Verifica formato
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_novo):
            print("FORMATO DE EMAIL INVÁLIDO, UTILIZE UM DOMÍNIO VÁLIDO")
            tentativas_email -= 1
            print(f"Tentativas restantes: {tentativas_email}")
            continue

        # Verifica domínio
        dominio = email_novo.split('@')[1].lower()
        if dominio not in dominios_validos:
            print("Domínio não aceito. Use: Gmail, Outlook, Yahoo, iCloud, etc.")
            tentativas_email -= 1
            print(f"Tentativas restantes: {tentativas_email}")
            conferir_apenas_email(email_novo,email_login,senha_login)  
            continue

        return conferir_apenas_email(email_novo,email_login,senha_login)  

    print("Limite de tentativas atingido.")
    print("Reinicie o sistema.")
    sys.exit

def conferir_apenas_email(email_novo,email_login, senha_login):
    """
    Essa função tem o objetivo de conferir se o email que a pessoa está querendo atualizar já está no banco de dados ou não
    """
    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        dados_conta = dados["senha"]
    
    # Valida email

    # Verifica se email já existe
    if email_novo in dados_conta:
        print("EMAIL JÁ POSSUI UMA CONTA.")
        tentativas = 3
        while tentativas > 0:
            resposta = input("Deseja tentar novamente ou ir para login? (refazer/login): ").strip().lower()
            
            if resposta in ["login", "tela de login", "logi"]:
                login()
                return
            elif resposta in ["refazer", "retentar"]:
                return valido_apenas_email(email_login, senha_login)  # Reinicia o processo
            else:
                tentativas -= 1
                print(f"Tentativas restantes: {tentativas}")
        
        print("Limite de tentativas atingido.")
        return
    
    # Se tudo ok, prossegue para atualização
    atualizar_apenas_email(email_novo, email_login, senha_login)

def atualizar_apenas_email(email_novo, email_login, senha_login):
    """
    Essa função tem o objetivo de atualizar um novo email relacionado a conta,excluindo o email passado.
    """
    limpar_tela()
    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo_lido_json:
        arquivo_lido = json.load(arquivo_lido_json)

        dados_conta = arquivo_lido["senha"]
        dados_familia = arquivo_lido["familia"]
        dados_quantidade = arquivo_lido["membros"]
        dados_pontos = arquivo_lido["pontos"]
        dados_apartamento = arquivo_lido["apartamento"]
        dados_codigov = arquivo_lido["verificador"]

        print("\n╔════════════════════════════════════════════════════════╗")
        print("║                    DADOS ATUALIZADOS                   ║")
        print("╠════════════════════════════════════════════════════════╣")
        print(f"║ Novo email cadastrado: {email_novo:<29}║")
        print("╠════════════════════════════════════════════════════════╣")
        print("║ ⚠️ Cuidado! Ao confirmar, os dados anteriores serão     ║")
        print("║ atualizados e não poderão ser recuperados.             ║")
        print("╚════════════════════════════════════════════════════════╝\n")
        time.sleep(1)

        tentativas = 3
        while tentativas != 0:
            confirmar = input("Deseja confirmar a atualização dos dados? (sim/não): ").strip().lower()
        
            if confirmar in ["sim", "si", "confirmar", "confirma", "confirmo"]:
                dados_conta[email_novo] = senha_login
                dados_familia[email_novo] = dados_familia[email_login]
                dados_quantidade[email_novo] = dados_quantidade[email_login]
                dados_pontos[email_novo] = dados_pontos[email_login]
                dados_apartamento[email_novo] = dados_apartamento[email_login]
                dados_codigov[email_novo] = dados_codigov[email_login]

                del dados_conta[email_login]
                del dados_familia[email_login]
                del dados_quantidade[email_login]
                del dados_pontos[email_login]
                del dados_apartamento[email_login]
                del dados_codigov[email_login]

                with open(r"banco_dados.JSON", "w", encoding="utf-8") as arquivo:
                    json.dump({
                        "senha": dados_conta,
                        "familia": dados_familia,
                        "membros": dados_quantidade,
                        "pontos": dados_pontos,
                        "apartamento": dados_apartamento,
                        "verificador": dados_codigov
                    }, arquivo, indent=4, ensure_ascii=False)
                print("Salvando dados...")
                barra_progresso()
                print(f"Email da conta atualizado para {email_novo} com sucesso!")
                time.sleep(1)
            
                tentativas = 3
                while tentativas != 0:
                    opcao = input("Deseja ir para o login ou sair do sistema? (Login/sair): ").strip().lower()

                    if opcao in ["login", "logi"]:
                        login()
                        return

                    elif opcao in ["sair", "sai", "sair sistema", "sai sistema"]:
                        print("Sistema encerrado pelo usuário.")
                        sys.exit()

                    else:
                        tentativas -= 1
                        print("Opção inválida. Por favor, tente novamente.")
                        print(f"Tentativas restantes: {tentativas}")
            
                print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
                sys.exit()

            elif confirmar in ["não", "nao", "cancelar", "cancelo", "cancela"]:
                print("Cancelando operação... Voltando para o menu inicial.")
                time.sleep(1)
                menu(email_login,senha_login)
                return

            else:
                print("Opção inválida.")
                tentativas -= 1
                print(f"Quantidade de tentativas restantes = {tentativas}")
    
        print("Limite de tentativas atingido")
        print("Reinicie o sistema")
        sys.exit()

######################################################################################################################
#Parte do código voltado apenas para atualização da senha
def valido_apenas_senha(email_login):
    """
    Essa função tem o objetivo de verificar se a senha que o usuário deseja cadastrar é valida ou não,caso seja válida poderá continuar para
    a atualização
    """
    limpar_tela()
    senha_nova=input("Digite sua senha(No mínimo 4 caracteres no máximo 20):")
    tentativas = 3
    while tentativas > 0:
        if 4 <= len(senha_nova) <= 20:
            #print("Senha aceita.")
            atualizar_apenas_senha(senha_nova,email_login)  # Chama o próximo passo do cadastro
            #return para a função que estava sendo rodada e deixa rodando apenas a função que rodará
            return
        else:
            print("Número de caracteres inválido. Sua senha deve ter entre 4 e 20 caracteres.")
            senha_nova = input("Digite sua senha novamente: ").strip()
            tentativas -= 1
            print(f"Tentativas restantes: {tentativas}")

    print("Número máximo de tentativas atingido. Tente novamente mais tarde.")

def atualizar_apenas_senha(senha_nova,email_login):
    """
    Essa função tem o objetivo de atualizar apenas a senha em relação a conta do login
    """
    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo_lido_json:
        arquivo_lido = json.load(arquivo_lido_json)

        dados_conta = arquivo_lido["senha"]
        dados_familia = arquivo_lido["familia"]
        dados_quantidade = arquivo_lido["membros"]
        dados_pontos = arquivo_lido["pontos"]
        dados_apartamento = arquivo_lido["apartamento"]
        dados_codigov = arquivo_lido["verificador"]
    
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║                    DADOS ATUALIZADOS                   ║")
        print("╠════════════════════════════════════════════════════════╣")
        print(f"║ Nova senha: {senha_nova:<39}║")
        print("╠════════════════════════════════════════════════════════╣")
        print("║ ⚠️ Cuidado! Ao confirmar, os dados anteriores serão     ║")
        print("║ atualizados e não poderão ser recuperados.             ║")
        print("╚════════════════════════════════════════════════════════╝\n")
        time.sleep(1)


        tentativas=3
        while tentativas!=0:
            confirmar = input("Deseja confirmar a atualização dos dados? (sim/não): ").strip().lower()
            if confirmar in ["sim", "si", "confirmar", "confirma", "confirmo"]:
                
                    # Apenas atualiza a senha mantendo o mesmo email
                dados_conta[email_login] = senha_nova

                    # Salva os dados atualizados
                with open(r"banco_dados.JSON", "w", encoding="utf-8") as arquivo:
                    json.dump({
                        "senha": dados_conta,
                        "familia": dados_familia,
                        "membros": dados_quantidade,
                        "pontos": dados_pontos,
                        "apartamento": dados_apartamento,
                        "verificador": dados_codigov
                    }, arquivo, indent=4, ensure_ascii=False)

                print("Salvando dados...")
                barra_progresso()
                print("Senha atualizada com sucesso!")
                
                time.sleep(1)
                tentativas = 3  # Máximo de tentativas permitidas

                while tentativas != 0:
                    opcao = input("Deseja ir para o login ou sair do sistema??(Login/sair): ").strip().lower()

                    if opcao in ["login","logi"]:
                        login()
                        break  #Sai do loop e chama a função login

                    elif opcao in ["sair","sai","sair sistema","sai sistema"]:
                        print("Sistema encerrado pelo usuário.")
                        sys.exit()
                        break  # Sai do loop e fecha o sistema

                    else:
                        tentativas -= 1
                        print("Opção inválida. Por favor, tente novamente.")
                        print(f"Tentativas restantes: {tentativas}")
                #caso o usuártio escreva erado

                else:
                    print("Limite de tentativas atingido. Sistema encerrado automaticamente.")

            elif confirmar in ["não", "nao", "cancelar", "cancelo", "cancela"]:
                print("Cancelando operação... Voltando para o menu inicial.")
                time.sleep(1)
                menu()
                return
            else:
                print("Opção inválida.")
                tentativas -= 1
                print(f"Quantidade de tentativas restantes = {tentativas}")
        
        else:
            print("Limite de tentativas atingido")
            print("Reinicie o sistema")
            sys.exit()

#########################################################################

##############################################################
#parte do código para deletar conta
def deletar(email_login,senha_login):
    #FUNÇÃO UTILIZADA  PARA DELETAR CONTAS
    """
    Essa funçao será utilizada para deletar a conta do usuário,caso seja da vontade dele
    """
    limpar_tela()
    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo_lido_json:
        arquivo_lido = json.load(arquivo_lido_json)
        dados_conta = arquivo_lido["senha"]
        dados_familia = arquivo_lido["familia"]
        dados_quantidade = arquivo_lido["membros"]
        dados_pontos = arquivo_lido["pontos"]
        dados_apartamento = arquivo_lido["apartamento"]
        dados_codigov = arquivo_lido["verificador"]
        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║                       ⚠️  ATENÇÃO IMPORTANTE  ⚠️              ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║ Você está na aba de deleção de conta.                       ║")
        print("║ Tome cuidado para não realizar uma ação indesejada!         ║")
        print("╚══════════════════════════════════════════════════════════════╝\n")

        tentativas=3
        while tentativas!=0:
            confirmar_deletar=input(f"Você deseja deletar sua conta({email_login}) do sistema ECODROP condomínio village ??(sim/não):").strip().lower()
            if confirmar_deletar in ["sim","yes","si","confirmar"]:
                #removerá todos os dados relacionados a email_login
                del dados_conta[email_login]
                del dados_familia[email_login]
                del dados_quantidade[email_login]
                del dados_pontos[email_login]
                del dados_apartamento[email_login]
                del dados_codigov[email_login]
                with open(r"banco_dados.JSON","w", encoding="utf-8") as arquivo_salvo_json:
                    json.dump(arquivo_lido, arquivo_salvo_json, indent=4, ensure_ascii=False)

                print("Seus dados foram retirados do sistema.")
                print("Tenha um bom dia!")
                sys.exit()
            elif confirmar_deletar in ["não", "nao", "cancelar", "cancelo", "cancela"]:
                print("Cancelando operação... Voltando para o menu inicial.")
                time.sleep(1)
                menu(email_login,senha_login)
                
                return
            else:
                print("Opção inválida. ")
                tentativas-=1
                print(f"Quantidade de tentativas restantes={tentativas}")
            
            
        else:
            print("Limite de tentativas atingido")
            print("Reinicie o sistema")
            sys.exit()



    

'''
Logo abaixo o código permite com que o usuário dê uma nota
e uma opinião quanto ao serviço utilizado, havendo um limite de 
caracteres na aba de comentáios e, após o comentário, ele é
registrado com a nota
'''
import csv
def feedback(email_login, senha_login):
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║                📝 SISTEMA DE AVALIAÇÃO DE SERVIÇO            ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║ O que você achou do nosso serviço?                           ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    
    
     # Comentário com até 140 caracteres
    tentativas_coment=3
    while tentativas_coment!=0:
        comentario = input("Deixe seu comentário(Digite apenas 140 caracteres): ").strip()
        if len(comentario)>140 or len(comentario)==0:
            print("Texto Inválido.Tente novamente")
            tentativas_coment-=1
        elif len(comentario)!=0 and len(comentario)<=140:
            break
    else:
        tentativas = 3
        while tentativas != 0:
            opcao = input("Deseja ir para o menu ou sair do sistema? (Menu/sair): ").strip().lower()

            if opcao in ["menu", "ver menu"]:
                menu(email_login,senha_login)
                return

            elif opcao in ["sair", "sai", "sair sistema", "sai sistema"]:
                print("Sistema encerrado pelo usuário.")
                sys.exit()

            else:
                tentativas -= 1
                print("Opção inválida. Por favor, tente novamente.")
                print(f"Tentativas restantes: {tentativas}")
            
        print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
        sys.exit()

        
    
    # Verifica se a nota está dentro do intervalo permitido
    tentativas_nota=3
    while tentativas_nota!=0:
        nota = float(input("Qual nota você nos dá (0 a 10)? "))
        if nota < 0 and nota > 10:
            print("Nota inválida. Por favor, digite uma nota entre 0 e 10.")
            #nota = float(input("Qual nota você nos dá (0 a 10)? "))
            tentativas_nota-=1
        elif nota>0 and nota<10:
            salvar_feedback(email_login, senha_login, comentario, nota)
            return
    else:
        tentativas = 3
        while tentativas != 0:
            opcao = input("Deseja ir para o menu ou sair do sistema? (Menu/sair): ").strip().lower()

            if opcao in ["menu", "ver menu"]:
                menu(email_login,senha_login)
                return

            elif opcao in ["sair", "sai", "sair sistema", "sai sistema"]:
                print("Sistema encerrado pelo usuário.")
                sys.exit()

            else:
                tentativas -= 1
                print("Opção inválida. Por favor, tente novamente.")
                print(f"Tentativas restantes: {tentativas}")
            
        print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
        sys.exit()
    


    
   
    
import csv

def salvar_feedback(email, senha, comentario, nota):
    with open("feedback.csv", mode="a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([email, comentario, nota])

    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║                🙏 OBRIGADO PELO SEU FEEDBACK!                ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    tentativas = 3
    while tentativas != 0:
        opcao = input("Deseja ir para o login ou sair do sistema? (Menu/sair): ").strip().lower()
            
        if opcao in ["menu", "ver menu"]:
            menu(email, senha)
            return

        elif opcao in ["sair", "sai", "sair sistema", "sai sistema"]:
            print("Sistema encerrado pelo usuário.")
            sys.exit()

        else:
            tentativas -= 1
            print("Opção inválida. Por favor, tente novamente.")
            print(f"Tentativas restantes: {tentativas}")
            
    print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
    sys.exit()

    

    

'''
Abaixo é indicado a posição do usuário em elação a outros
quanto ao seu gasto de água ao longo do mês
'''



def ranking(email_login,senha_login):
    limpar_tela()
    time.sleep(1)
    dia_do_mes = time.strftime("%d", time.localtime())
    if dia_do_mes=="28":
        with open("banco_dados.JSON", "r", encoding="utf-8") as f:
            banco_dados = json.load(f)
            pontos_dict = banco_dados.get("pontos", {})

    # Ordena o dicionário pontos por valor (pontos) decrescente, retorna lista de tuplas (email, pontos)
        ranking_ordenado = sorted(pontos_dict.items(), key=lambda item: item[1], reverse=True)

    
        ranking_ordenado_dict = dict(ranking_ordenado)
        print("Carregando ranking...")
        barra_progresso()
        
        print("Ranking dos usuários por pontos (maior para menor):")
        print("\n╔══════════════════════════════════════════════╗")
        print("║           🏆 RANKING DE PONTOS 🏆            ║")
        print("╠════╦════════════════════════════╦══════════╣")
        print("║ #  ║ Email                      ║ Pontos   ║")
        print("╠════╬════════════════════════════╬══════════╣")
    
        for i, (email, pts) in enumerate(ranking_ordenado, start=1):
            # Limita o email para caber na tabela (por exemplo, 26 caracteres)
            email_formatado = (email[:23] + '...') if len(email) > 26 else email.ljust(26)
            print(f"║ {str(i).ljust(2)} ║ {email_formatado} ║ {str(pts).rjust(8)} ║")
    
            print("╚════╩════════════════════════════╩══════════╝\n")
    else:
        print("Opção de ver ranking apenas é permitido no dia 28 de cada mês")
        tentativas = 3
        while tentativas > 0:
            opcao = input("Deseja ir para o Menu ou sair do sistema? (Menu/sair): ").strip().lower()

            if opcao in ["menu", "menuu"]:
                menu(email_login, senha_login)
                break
            elif opcao in ["sair", "sai", "sair sistema", "sai sistema"]:
                print("Sistema encerrado pelo usuário.")
                sys.exit()
            else:
                tentativas -= 1
                print("Opção inválida. Por favor, tente novamente.")
                print(f"Tentativas restantes: {tentativas}")
        else:
            print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
            sys.exit()
     



'''
O código abaixo oferece inúmeras opções de prêmios ao
usuário que acumula pontos conforme seu desempenho na
economia de água. Dependendo do seu saldo, o usuário 
pode escolher seu prêmio, tendo voucher e descontos, por exemplo
'''
import sys


    
def resgatar(email_login, senha_login):
    limpar_tela()
    time.sleep(1)
    with open("banco_dados.JSON", "r", encoding="utf-8") as f:
        banco_dados = json.load(f)
        pontos_disponiveis = banco_dados["pontos"].get(email_login, 0)

    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║                      🎁 TABELA DE RECOMPENSAS 🎁           ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print("║ 1. Milhas ............................................ 150 pts ║")
    print("║ 2. Desconto no condomínio ............................ 100 pts ║")
    print("║ 3. Voucher ...........................................  80 pts ║")
    print("║ 4. Cupons ............................................  60 pts ║")
    print("║ 5. Descontos .........................................  50 pts ║")
    print("║ 6. Créditos de celular ...............................  40 pts ║")
    print("╚════════════════════════════════════════════════════════════╝")

    custos = {
        "1": 150,
        "2": 100,
        "3": 80,
        "4": 60,
        "5": 50,
        "6": 40
    }

    recompensas = {
        "1": "Milhas",
        "2": "Desconto no condomínio",
        "3": "Voucher",
        "4": "Cupons",
        "5": "Descontos",
        "6": "Créditos de celular"
    }

    tentativas = 3
    while tentativas > 0:
        opcao = input("Digite o número da recompensa que deseja resgatar: ").strip()

        if opcao in custos:
            custo_recompensa = custos[opcao]
            nome_recompensa = recompensas[opcao]

            if pontos_disponiveis >= custo_recompensa:
                pontos_disponiveis -= custo_recompensa
                banco_dados["pontos"][email_login] = pontos_disponiveis

                with open("banco_dados.JSON", "w", encoding="utf-8") as f:
                    json.dump(banco_dados, f, indent=4, ensure_ascii=False)

                print(f"\n🎉 Você resgatou: {nome_recompensa}")
                print(f"✅ Seu novo saldo de pontos é: {pontos_disponiveis}")
                gerar_codigo_resgate()
                time.sleep(1)
                tentativas_finais=3
                while tentativas_finais > 0:
                    escolha = input("\nDeseja ir para o menu ou sair do sistema? (Menu/sair): ").strip().lower()
                    if escolha == "menu":
                        menu(email_login, senha_login)
                        break
                    elif escolha == "sair":
                        print("Sistema encerrado pelo usuário.")
                        sys.exit()
                    else:
                        tentativas_finais -= 1
                        print("Opção inválida. Por favor, tente novamente.")
                        print(f"Tentativas restantes: {tentativas_finais}")
                else:
                    print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
                    sys.exit()

                

            
            else:
                print(f"\n⚠️ Você não possui saldo suficiente")
                tentativas_restantes = 3
                while tentativas_restantes > 0:
                    opcao_final = input("Deseja ir para o menu ou sair do sistema? (Menu/sair): ").strip().lower()

                    if opcao_final == "menu":
                        menu(email_login, senha_login)
                        break
                    elif opcao_final == "sair":
                        print("Sistema encerrado pelo usuário.")
                        sys.exit()
                    else:
                        tentativas_restantes -= 1
                        print("Opção inválida. Por favor, tente novamente.")
                        print(f"Tentativas restantes: {tentativas_restantes}")

                else:
                    print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
                    sys.exit()

        else:
            tentativas -= 1
            print("Opção inválida. Por favor, tente novamente.")
            print(f"Tentativas restantes: {tentativas}")

    else:
        tentativas_restantes = 3
        while tentativas_restantes > 0:
            opcao_final = input("Deseja ir para o menu ou sair do sistema? (Menu/sair): ").strip().lower()

            if opcao_final == "menu":
                menu(email_login, senha_login)
                break
            elif opcao_final == "sair":
                print("Sistema encerrado pelo usuário.")
                sys.exit()
            else:
                tentativas_restantes -= 1
                print("Opção inválida. Por favor, tente novamente.")
                print(f"Tentativas restantes: {tentativas_restantes}")

        else:
            print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
            sys.exit()


'''
Abaixo o código orienta a realização do cálculo de pontos,
ou seja, ocorre a conversão da quantidade de água economizada 
em pontos
'''
import time
import json
import sys
import datetime
# Variáveis globais


def calculo(email_login, senha_login):
    limpar_tela()
    time.sleep(1)
    dia_do_mes = time.strftime("%d", time.localtime())

    if dia_do_mes == "27":
        with open("dados_usuarios.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            gasto_real = dados["consumo"].get(email_login)
            verificar_calculo = dados["calculo_realizado"].get(email_login)
        with open("banco_dados.JSON", "r", encoding="utf-8") as f:
            banco_dados1=json.load(f)
            quantidade_membros = banco_dados1["membros"].get(email_login, 0)  # retorna 0 se o email não existir

        
            

        if verificar_calculo == False:
    
            if gasto_real is None:
                print("❌ Gasto de água não registrado para este e-mail. Peça ao seu síndico a atualização do banco de dados.")
                print("Voltando para o menu...")
                menu(email_login, senha_login)
                return

            gasto_estimado = quantidade_membros * 150 * 30

            print("\n╔══════════════════════════════════════════════════════════════╗")
            print("║                 💧 CÁLCULO DE ECONOMIA DE ÁGUA                ║")
            print("╠══════════════════════════════════════════════════════════════╣")
            print(f"║ Membros na residência: {quantidade_membros}")
            print(f"║ Gasto estimado (litros): {gasto_estimado}")
            print(f"║ Gasto real (litros): {gasto_real}")
            print("╚══════════════════════════════════════════════════════════════╝")

            if gasto_real < gasto_estimado:
                print("\n🎉 Parabéns, você economizou água e ganhou pontos!")
                #Atualizando os pontos em relação ao email
                banco_dados1["pontos"][email_login] = banco_dados1["pontos"].get(email_login, 0) + 50
                with open(r"banco_dados.JSON", "w", encoding="utf-8") as f:
                    json.dump(banco_dados1, f, indent=4, ensure_ascii=False)
                dados["calculo_realizado"][email_login]=True
                with open(r"dados_usuarios.json", "w", encoding="utf-8") as f:
                    json.dump(dados, f, indent=4, ensure_ascii=False)
            
            else:
                print("\n🚫 Você não economizou esse mês. Continue tentando!")
                banco_dados1["pontos"][email_login] = banco_dados1["pontos"].get(email_login, 0) + 50
                with open(r"banco_dados.JSON", "w", encoding="utf-8") as f:
                    json.dump(banco_dados1, f, indent=4, ensure_ascii=False)
                dados["calculo_realizado"][email_login]=True
                with open(r"dados_usuarios.json", "w", encoding="utf-8") as f:
                    json.dump(dados, f, indent=4, ensure_ascii=False)

            tentativas = 3
            while tentativas > 0:
                opcao = input("Deseja ir para o Menu ou sair do sistema? (Menu/sair): ").strip().lower()

                if opcao in ["menu", "menuu"]:
                    menu(email_login, senha_login)
                    break
                elif opcao in ["sair", "sai", "sair sistema", "sai sistema"]:
                    print("Sistema encerrado pelo usuário.")
                    sys.exit()
                else:
                    tentativas -= 1
                    print("Opção inválida. Por favor, tente novamente.")
                    print(f"Tentativas restantes: {tentativas}")
            else:
                print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
                sys.exit()
        if verificar_calculo==True:
            print("Você já realizou o cálculo mensal.")
            time.sleep(1)
            tentativas = 3
            while tentativas > 0:
                opcao = input("Deseja ir para o menu ou sair do sistema? (Menu/sair): ").strip().lower()
                if opcao == "menu":
                    menu(email_login, senha_login)
                    return
                elif opcao == "sair":
                    print("Sistema encerrado pelo usuário.")
                    sys.exit()
                else:
                    tentativas -= 1
                    print("Opção inválida. Por favor, tente novamente.")
                    print(f"Tentativas restantes: {tentativas}")
            else:
                print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
                sys.exit()



    
    
    
    else:
        print("\n📅 Hoje não é dia 27, o cálculo de economia está indisponível.")
    
        tentativas = 3
        while tentativas > 0:
            opcao = input("Deseja ir para o menu ou sair do sistema? (Menu/sair): ").strip().lower()
            if opcao == "menu":
                menu(email_login, senha_login)
                return
            elif opcao == "sair":
                print("Sistema encerrado pelo usuário.")
                sys.exit()
            else:
                tentativas -= 1
                print("Opção inválida. Por favor, tente novamente.")
                print(f"Tentativas restantes: {tentativas}")
        else:
            print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
            sys.exit()




class Cadastro:
    """
    Essa Classe tem o objetivo de cadastrar os usuários,recebendo os dados básicos para ser possível fazer a conta,conferir se os dados são permitidos
    e assim cadastrar a conta
    """
    def __init__(self):
        #RECEBE OS DADOS NECESSÁRIOS PARA CADASTRAR UMA CONTA
        self.email = input("Digite o email que você gostaria de vincular sua conta:")
        self.quantidade = int(input("Informe a quantidade de pessoas na sua residência:"))
        self.senha = input("Digite sua senha(No mínimo 4 caracteres no máximo 20):").strip()
        self.nome_familia = input("Digite o nome que ficará cadastrado sua família(COLOQUE 1 OU DOIS SOBRENOMES):")
        self.pontos = 0
        self.apartamento = int(input("Digite o número do seu apartamento:"))
        self.verificador = input("Digite seu código verificador:\n"
                                 "ATENÇÃO,GUARDE ESSE CÓDIGO DE UMA FORMA SEGURA,CASO VOCÊ ESQUEÇA A SENHA ELE É A ÚNICA FORMA DE CONSEGUIR ACESSAR A CONTA:").strip()
        #chama função conferir código
        self.conferir_codigo()

    # precisa passar o self como parâmetro para conseguir pegar as informações  do init
    def conferir_codigo(self):
        #FUNÇÃO UTILIZADA PARA CONFERIR SE O CÓDIGO VERIFICADOR É VÁLIDO OU NÃO
        limpar_tela()

        tentativas = 3
        while tentativas > 0:
            #codigo_digitado = input("Digite novamente seu código verificador para confirmar: ")

            if len(self.verificador)>=4 and  len(self.verificador)<=20:
                self.conferir_senha()
                return  # Código está correto, pode continuar
            else:
                print("Número de caracteres inválidos para código verificador. Seu código  deve ter entre 4 a 20 caracteres.")
                self.verificador = input("Digite sua senha novamente: ").strip()
                tentativas -= 1
                print(f"Tentativas restantes: {tentativas}")

        print("Número máximo de tentativas atingido. Tente novamente mais tarde.")


    def conferir_senha(self):
        #FUNÇÃO UTILIZADA PARA CONFERIR SE A SENHA É VÁLIDA OU NÃO
        tentativas = 3
        while tentativas > 0:
            if 4 <= len(self.senha) and len(self.senha) <= 20:
                #print("Senha aceita.")
                self.email_valido()  # Chama o próximo passo do cadastro
            #return para a função que estava sendo rodada e deixa rodando apenas a função que rodará
                return
            else:
                print("Número de caracteres inválido. Sua senha deve ter entre 4 e 20 caracteres.")
                self.senha = input("Digite sua senha novamente: ").strip()
                tentativas -= 1
                print(f"Tentativas restantes: {tentativas}")

        print("Número máximo de tentativas atingido. Tente novamente mais tarde.")

    def email_valido(self):
        #FUNÇÃO UTILIZADA PARA CONFERIR SE O EMAIL É VÁLIDO OU NÃO
        dominios_validos = [
            'gmail.com', 'outlook.com', 'hotmail.com',
            'yahoo.com', 'icloud.com'
        ]

        tentativas_email = 3
        while tentativas_email != 0:
            # VERIFICA SE O FORMATO DO EMAIL ESTÁ ESCRITO CORRETAMENTE
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
                print("FORMATO DE EMAIL INVÁLIDO, UTILIZE UM DOMÍNIO VÁLIDO")
                self.email = input("Digite novamente seu email: ").strip()
                tentativas_email -= 1
                print(f"Tentativas restantes: {tentativas_email}")

                continue  # volta pro início do while para validar de novo,caso esteja correto,irá passar pelo verificador

            # VERIFICA APENAS O DOMÍNIO,SEPARA TODO O RESTO E PEGA APENAS A PARTE DO DOMÍNIO
            dominio = self.email.split('@')[1].lower()
            if dominio not in dominios_validos:
                print("Domínio não aceito. Use: Gmail, Outlook, Yahoo, iCloud, etc.")
                self.email = input("Digite novamente seu email: ").strip()
                tentativas_email -= 1
                print(f"Tentativas restantes: {tentativas_email}")

                # continuar o loop sem parar
                continue

        # Se chegou aqui, formato e domínio estão corretos
            break

        else:
            print("Limite de tentativas atingido. Encerrando o processo de cadastro.")
            return

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

            if self.email in dados_conta:
                print("EMAIL JÁ POSSUI UMA CONTA.")
                tentativas = 3
                while tentativas != 0:
                    resposta1 = input(
                    "Deseja tentar refazer a conta ou ir para tela de login caso já possua conta? (refazer/login) ").strip().lower()
                    if resposta1 in ["login", "tela de login", "logi"]:
                        login()
                        return
                    elif resposta1 in ["refazer", "retentar", "conta", "refazer conta"]:
                        self.email = input("Digite novamente seu email: ").strip()
                        self.conferir_email()
                        return
                    else:
                        print("Resposta inválida")
                        tentativas -= 1
                        print(f"Tentativas restantes {tentativas}")
                else:
                    print(
                    "Limite de tentativas atingido. Encerrando o processo de cadastro.")
                    return
            else:
                self.conferir_ap()  # Continua o processo normalmente

    def conferir_ap(self):
       #FUNÇÃO UTILIZADA PARA ANALISAR SE O APARTAMENTO JÁ ESTÁ CADASTRADO OU NÃO
        if self.apartamento in dados_apartamento.values():
            print("APARTAMENTO JÁ CADASTRADO.")
            tentativas = 3
            while tentativas != 0:
                resposta1 = input(
                    "Deseja tentar refazer a conta ou ir para tela de login caso já possua conta ??(refazer/login)").strip().lower()
                if resposta1 in ["login", "tela de login", "logi"]:
                    login()
                    return
                elif resposta1 in ["refazer", "retentar", "conta", "refazer conta"]:
                    Cadastro()
                    return
                else:
                    print("Resposta inválida")
                    tentativas -= 1
                    print(f"Tentativas restantes {tentativas}")
            else:  # ✅ Só imprime quando zerar tentativas
                print(
                    "Limite de tentativas atingido. Encerrando o processo de cadastro.")
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
        limpar_tela()
        print("Conta cadastrada com sucesso.")
        time.sleep(1)
        tentativas = 3  # Máximo de tentativas permitidas

        while tentativas != 0:
            opcao = input("DIGITE 'LOGIN' PARA ENTRAR OU 'SAIR' PARA ENCERRAR: ").strip().lower()

            if opcao in ["login","logi"]:
                login()
                break  #Sai do loop e chama a função login

            elif opcao in ["sair","sai","sair sistema","sai sistema"]:
                print("Sistema encerrado pelo usuário.")
                sys.exit()
                break  # Sai do loop e fecha o sistema

            else:
                tentativas -= 1
                print("Opção inválida. Por favor, tente novamente.")
                print(f"Tentativas restantes: {tentativas}")
                #caso o usuártio escreva erado

        else:
            print("Limite de tentativas atingido. Sistema encerrado automaticamente.")
        


 # Essa parte que vai realmente começar o código
 # Esse código tem que ser escrito de cima pra baixo,mas para puxar ele tem que ser lá embaixo,pois só assim para o código
 # conseguir usar todas as funções
 #
class Condominio:
    """
    Classe para cadastrar um novo condomínio no sistema.
    Valida o formato do email e armazena os dados no arquivo condominios.json.
    """

    def __init__(self):
        self.email = input("Digite o email do condomínio: ").strip()
        self.rua = input("Digite o nome da rua do condomínio: ").strip()
        self.numero = input("Digite o número do condomínio: ").strip()
        self.cep = input("Digite o CEP do condomínio: ").strip()
        self.codigo = input("Digite um código identificador do condomínio: ").strip()

        self.validar_emailcondominio()

    def validar_emailcondominio(self):
        
        #FUNÇÃO UTILIZADA PARA CONFERIR SE O EMAIL É VÁLIDO OU NÃO
        dominios_validos = [
            'gmail.com', 'outlook.com', 'hotmail.com',
            'yahoo.com', 'icloud.com'
        ]

        tentativas_email = 3
        while tentativas_email != 0:
            # VERIFICA SE O FORMATO DO EMAIL ESTÁ ESCRITO CORRETAMENTE
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
                print("FORMATO DE EMAIL INVÁLIDO, UTILIZE UM DOMÍNIO VÁLIDO")
                self.email = input("Digite novamente seu email: ").strip()
                tentativas_email -= 1
                print(f"Tentativas restantes: {tentativas_email}")

                continue  # volta pro início do while para validar de novo,caso esteja correto,irá passar pelo verificador

            # VERIFICA APENAS O DOMÍNIO,SEPARA TODO O RESTO E PEGA APENAS A PARTE DO DOMÍNIO
            dominio = self.email.split('@')[1].lower()
            if dominio not in dominios_validos:
                print("Domínio não aceito. Use: Gmail, Outlook, Yahoo, iCloud, etc.")
                self.email = input("Digite novamente seu email: ").strip()
                tentativas_email -= 1
                print(f"Tentativas restantes: {tentativas_email}")

                # continuar o loop sem parar
                continue

        # Se chegou aqui, formato e domínio estão corretos
            break

        #Esse else só será puxado se o número de tentativas zerar
        else:
            print("Limite de tentativas atingido. Encerrando o processo de cadastro.")
            return

        self.conferir_emailcondominio()

    def conferir_emailcondominio(self):
        
        pass
        



#Início do sistema 
import pyfiglet

ascii_banner = pyfiglet.figlet_format("ECODROP")
print(ascii_banner)
 
print("OLÁ,BEM VINDO AO SISTEMA ECODROP💧 do condomínio Village")

tentativas = 3  #  3 tentativas permitidas
while tentativas != 0:
    tipo_servico = input(
        "QUAL TIPO DE SERVIÇO VOCÊ DESEJA ??(LOGIN/CADASTRO) ").strip().lower()

    if tipo_servico in ["login", "entrar", "acessar", "fazer login"]:
        login()
        break  # Sai do loop e puxa a função login

    elif tipo_servico in ["cadastro", "cadastrar", "criar conta", "novo cadastro"]:
        novo_cadastro = Cadastro()
        break  # Sai do loop e puxa a função cadastro

    else:
        #OPÇÃO INVÁLIDA
        print("Serviço inválido. Por favor, tente novamente.")
        tentativas -= 1
        print(f"Tentativas restantes {tentativas}")

else:
    #LIMITE DE OPÇÕES ATINGIDO
    print("Limite de tentativas atingido. Reinicie o programa.")
    
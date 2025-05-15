import sys
import json
import time
import re
import random
import os

#ANOTAÇÃO IMPORTANTE
#Se uma função chama outra função que precisa de argumentos, ela também precisa receber esses argumentos ou criá-los.


with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo:
    # quando usa json.load o arquivo json é transformado em dicionário python
	"""o objetivo dessa parte do código é abrir o arquivo json e salvar os dicionários em python,facilitando a manipulação"""
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

def limpar_tela():
	"""objetivo dessa função é limpar a tela sempre que passar para outra seção,deixando o projeto mais real"""
    #FUNÇÃO UTILIZADO PARA LIMPAR O TERMINAL,DEIXANDO O SISTEMA MAIS "REAL"
    os.system('cls' if os.name == 'nt' else 'clear')

def login():
	"""
 	objetivo dessa função é o usuário poder entrar no sistema colocando seus dados da conta.Caso ele não possua conta será redirecionado para página de cadastro.Caso ele
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
                        # return serve para interromper a função login de continuar rodando e deixar apenas a função menu
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
                            sys.exit
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
    print(f"MENSAGEM DIÁRIA:{random.choice(mensagens_agua)}")
    time.sleep(1)
    while tentativas != 0:
        resposta2 = input("Qual tipo de função você deseja ?? (Ranking/Calcular pontos/Atualizar dados/Deletar conta/Feedback/Resgatar recompensas/Visualizar dados/sair sistema):").strip().lower()

        if resposta2 in ["ver ranking", "ranking"]:
            ranking()
            return

        elif resposta2 in ["calcular pontos", "calcular", "calculo", "pontos"]:
            calculo()
            return

        elif resposta2 in ["atualizar", "atualização", "atualizar dados", "atualiza dados"]:
            atualizar(email_login,senha_login)
            return

        elif resposta2 in ["deletar", "deletar conta", "excluir", "excluir conta", "apagar conta"]:
            deletar(email_login,senha_login)
            return

        elif resposta2 in ["feedback", "enviar feedback", "sugestao", "sugestão", "critica", "crítica"]:
            feedback()
            return
        elif resposta2 in ["resgatar", "recompensa", "resgatar recompensa", "prêmios", "premio"]:
            resgatar_premio()
            return
        elif resposta2 in ["sair","sai","sair sistema","sai sistema","quit"]:
            print("Tenha um bom dia!!")
            sys.exit()
        elif resposta2 in ["visualizar dados","ver dados","conferir dados"]:
            mostrar_dados(email_login,senha_login)
            return

        else:
            print("Resposta inválida")
            tentativas -= 1

    else:
        print("Limite de tentativas atingido. Reinicie o programa.")
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
        while tentativas != 0:
            opcao = input("Deseja ir para o login ou sair do sistema?(Login/sair): ").strip().lower()

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
        


    pass



def atualizar(email_login,senha_login):
    #FUNÇÃO UTILIZADA PARA MOSTRAR AS OPÇOES DE ATUALIZAÇÃO(ATUALIZAR DADOS PESSOAIS OU DADOS DA CONTA)   
    """
	Essa função irá dar a opção do usuário atualizar os dados da conta(email,senha) ou os dados pessoais(quantidade de membros,apartamento cadastrado e o nome da família),.A partir da sua resposta,ele será 
 	encaminhado para outra aba
    """
	limpar_tela()
    print("Bem-vindo à tela de atualização do ECODROP.")
    tentativas = 3

    while tentativas > 0:
        question1 = input(
            "O que você deseja atualizar na sua conta? (dados conta / dados pessoais): ").strip().lower()

        if question1 in ["dados conta", "conta", "dados da conta", "conta dados"]:
            email_valido(email_login,senha_login)
            return

        elif question1 in ["dados pessoais", "pessoais", "informações pessoais", "info pessoais"]:
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
        print(f"Dados atualizados:\nQuantidade de pessoas na família: {membros_novos}\nNome da família: {nome_novo}")

    
    
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
                print("ATUALIZAÇÃO FEITA COM SUCESSO \n"
                    "REDIRECIONANDO PARA MENU")
                time.sleep(1)
                menu(email_login,senha_login)
                return

        

            elif confirmar in ["não", "nao", "cancelar", "cancelo", "cancela"]:
                print("Cancelando operação... Voltando para o menu inicial.")
                menu(email_login,senha_login)  # Substitua com sua função de menu, caso necessário
                return
            else:
                print("Opção inválida. Cancelando operação.")
                tentativas-=1
                print(f"Tentativas restantes {tentativas}")
        else:
            print("Limite de tentativas atingido")
            print("Reinicie o sistema")
            sys.exit()



def email_valido(email_login,senha_login):
    """
	Essa função será chamada caso o usuário deseje atualizar os dados da conta(email,senha).Ela tem a função de verificar se o email novo 
 	 que será utilizado é válido ou não.Caso seja válido será chamada outra função para continuar o fluxo.
    """
	##FUNÇÃO UTILIZADA PARA CONFERIR SE O NOVO EMAIL QUE SERÁ CADASTRADO É VÁLIDO OU NÇAO(ESSA FUNÇÃO SÓ SERÁ CHAMADA 
    #CASO O USUÁRIO QUEIRA ATUALIZAR OS DADOS DA CONTA)

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
                
                    conferir_email(email_novo)

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
        if 4 <= len(senha_nova) <= 20:
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
    """essa função será utilizada para atualizar a conta do usuário,podendo atualizar apenas o email,apenas a senha ou atualizar ambos os dados"""

    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo_lido_json:
        arquivo_lido = json.load(arquivo_lido_json)

    dados_conta = arquivo_lido["senha"]
    dados_familia = arquivo_lido["familia"]
    dados_quantidade = arquivo_lido["membros"]
    dados_pontos = arquivo_lido["pontos"]
    dados_apartamento = arquivo_lido["apartamento"]
    dados_codigov = arquivo_lido["verificador"]

    #senha_nova = input("Digite sua nova senha: ")
    opcao=input("Você deseja atualizar apenas o email,apenas a senha ou ambos ??(email,senha,ambos):").strip().lower()
    
    #ALTERA APENAS O EMAIL
    if opcao in ["email","alterar email","apenas email"]:
        print(f"Dados atualizados:\nNovo email cadastrado:{email_novo}")
        
        print("Cuidado⚠️!!Caso você confirme essa atualização deve ficar ciente que os antigos dados serão atualizados e não poderão ser "
        "acessados novamente")
        time.sleep(1)

        tentativas=3
        while tentativas!=0:
            confirmar = input("Deseja confirmar a atualização dos dados? (sim/não): ").strip().lower()
            if confirmar in ["sim", "si", "confirmar", "confirma", "confirmo"]:
                
                    # Copia os dados para o novo email (mantendo a senha antiga)
                dados_conta[email_novo] = senha_login  # Mantém a senha antiga
                dados_familia[email_novo] = dados_familia[email_login]
                dados_quantidade[email_novo] = dados_quantidade[email_login]
                dados_pontos[email_novo] = dados_pontos[email_login]
                dados_apartamento[email_novo] = dados_apartamento[email_login]
                dados_codigov[email_novo] = dados_codigov[email_login]

                    # Remove o antigo                    
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

                print(f"Email da conta atualizado para {email_novo} com sucesso!")
                print("Conta cadastrada com sucesso.")
                time.sleep(1)
                tentativas = 3  # Máximo de tentativas permitidas
                while tentativas != 0:
                    opcao = input("Deseja ir para o login ou sair do sistema?(Login/sair): ").strip().lower()

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


    elif opcao in ["senha","apenas a senha","alterar senha"]:

        print(f"Dados atualizados\nNova senha:{senha_nova}")
        print("Cuidado⚠️!!Caso você confirme essa atualização deve ficar ciente que os antigos dados serão atualizados e não poderão ser "
        "acessados novamente")
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
    

    elif opcao in ["ambas","alterar ambas","atualizar email e senha","alterar ambos","ambos"]:



        print(f"Dados atualizados:\nNovo email cadastrado: {email_novo}\nNova senha: {senha_nova}")
        print("Cuidado⚠️!!Caso você confirme essa atualização deve ficar ciente que os antigos dados serão atualizados e não poderão ser "
        "acessados novamente")
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


def deletar(email_login,senha_login):
    #FUNÇÃO UTILIZADA  PARA DELETAR CONTAS
	"""Essa funçao será utilizada para deletar a conta do usuário,caso seja da vontade dele"""
    limpar_tela()
    with open(r"banco_dados.JSON", "r", encoding="utf-8") as arquivo_lido_json:
        arquivo_lido = json.load(arquivo_lido_json)
        dados_conta = arquivo_lido["senha"]
        dados_familia = arquivo_lido["familia"]
        dados_quantidade = arquivo_lido["membros"]
        dados_pontos = arquivo_lido["pontos"]
        dados_apartamento = arquivo_lido["apartamento"]
        dados_codigov = arquivo_lido["verificador"]
        print("ATENÇÃO⚠️\n" \
    "Você está na aba de deleção de conta,tome cuidado para não fazer algo indesejado.")
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



    


def feedback():

    print("========Sistema de avaliação========")


    print("O que você achou do nosso serviço?")
    nome = (input("Digite seu nome: ")
    nota = float(input("Qual nota você nos dá (0 a 10)? "))
    
    # Verifica se a nota está dentro do intervalo permitido
    if nota < 0 or nota > 10:
        print("Nota inválida. Por favor, digite uma nota entre 0 e 10.")
        return
    
    comentario = input("Deixe seu comentário: ")
    
    # Armazenar o feedback como um dicionário
    feedback = {
        "nome": nome,
        "nota": nota,
        "comentario": comentario
    }
    
    feedbacks.append(feedback)
    print("\n✅ Feedback registrado com sucesso!\n")

# Função para exibir todos os feedbacks
def exibir_feedbacks():
    if not feedbacks:
        print("Ainda não há feedbacks registrados.\n")
        return

 def salvar_dados(dados):
    with open("dados.csv", "w") as f:
        f.write(dados)
    atualizar_dados()

def atualizar_dados():
    print("Atualizando os dados com as últimas alterações...")

print("Você deseja retornar ao menu? (s/n)")
    if resposta == "s":
        print("Retornando ao menu...")
        # Aqui podemos chamar a função do menu, por exemplo:
        # mostrar_menu()
    elif resposta == "n":
        print("Encerrando o programa.")
        import sys
        sys.exit()
    else:
        print("Opção inválida. Tente novamente.")

pass


def ranking():
   if dia do mês 28:
	    import json
	    
	    # Lê os dados do arquivo JSON
	    with open('dados_usuarios.json', 'r', encoding='utf-8') as arquivo:
	        dados = json.load(arquivo)
	    
	    # Extrai os pontos
	        pontos = dados['pontos']
	    
	    # Gera uma lista de tuplas com email e pontos
	        ranking = sorted(pontos.items(), key=lambda item: item[1], reverse=True)
	    
	    # Mostra o ranking com outros dados (nome da família e apartamento)
	        print("🏆 RANKING DOS USUÁRIOS POR PONTOS:\n")
	        for posicao, (email, ponto) in enumerate(ranking, start=1):
	            familia = dados['familia'].get(email, 'Desconhecido')
	            ap = dados['apartamento'].get(email, '???')
	            print(f"{posicao}º lugar: Família {familia} (Apt {ap}) - {ponto} pontos")
		print("Você deseja ver os rankings passados? (s/n)")
			if resposta == "s":
	            print("\n--- Rankings Passados ---")
    			for ranking in rankings_passados:
       				 print(ranking)
	        elif resposta == "n":
	            print("Encerrando o programa.")
	            import sys
	            sys.exit()
  	else:
        print("Você deseja ver os rankings passados? (s/n)")
	        if resposta == "s":
	             print("\n--- Rankings Passados ---")
    			for ranking in rankings_passados:
       				 print(ranking)
	        elif resposta == "n":
	            print("Encerrando o programa.")
	            import sys
	            sys.exit()
		else:
		    print("Opção inválida")
	                

    
pass



def resgatar():
    print("===Tabela de recompensas===")

	if saldo suficiente:
	print("Resgate seu prêmio")
		if voucher:
			premio = voucher
		elif cupons:
			premio = cupons
		elif descontos:
			premio = descontos
		elif milhas:
			premio= milhas
		else:
			print("Encerrando o programa.")
	            	import sys
	            	sys.exit()
	   def salvar_dados(dados):
    	with open("dados.csv", "w") as f:
        f.write(dados)
    	atualizar_dados()

	                
	 else: 
		print("Saldo insuficiente")
		print("Encerrando o programa.")
	            import sys
	            sys.exit()
	
	                
			

#def resgatar():
def resgatar_premio(litros_economizados):
    if litros_economizados >= 1000:
        premio = "Viagem para uma reserva ecológica por 1 final de semana"
    elif litros_economizados >= 500:
        premio = "Assinatura de um serviço de streaming por 3 meses"
    elif litros_economizados >= 200:
        premio = "Desconto em um produto de limpeza ecológico"
    elif litros_economizados >= 100:
        premio = "Cartão presente de R$50"
    elif litros_economizados >= 50:
        premio = "Garrafa d'água ecológica"
    else:
        premio = "Você ainda não tem pontos suficientes para resgatar prêmios."

    print("\n🎁 Resgate de Prêmios:")
    print(f"Você pode resgatar: {premio}")

 if pontos >= 200:
        recompensa = recompensas[200]
    elif pontos >= 100:
        recompensa = recompensas[100]
    elif pontos >= 50:
        recompensa = recompensas[50]
    elif pontos >= 20:
        recompensa = recompensas[20]
    else:
        recompensa = "Você não tem pontos suficientes para resgatar recompensas."
    
    print(f"Você pode resgatar: {recompensa}")


pass


def calculo():

    if dia do mês == 28:
		with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
        	json.dump(dados, arquivo, indent=4, ensure_ascii=False)
		calculo = int(input("[quantidade de pessoas*quantidade de dias*consumo individual]/[média mundial de consumo individual])
			if calculo < media_mundial_de_consumo_individual:
				print("Parabéns, você acumulou pontos!!)
			else:
				print("Você não pontuou")
		print("Você deseja ver seu ranking? (s/n)"
			if resposta == "s":
				print("🏆 RANKING DOS USUÁRIOS POR PONTOS:\n")
	        		for posicao, (email, ponto) in enumerate(ranking, start=1):
	           		familia = dados['familia'].get(email, 'Desconhecido')
	            		ap = dados['apartamento'].get(email, '???')
	            		print(f"{posicao}º lugar: Família {familia} (Apt {ap}) - {ponto} pontos")	
			else:
				print("Encerrando o programa.")
	            		import sys
	            		sys.exit()
		   	
				  
	else:
		print("Você deseja ver seu ranking? (s/n)"
			if resposta == "s":
				print("🏆 RANKING DOS USUÁRIOS POR PONTOS:\n")
	        		for posicao, (email, ponto) in enumerate(ranking, start=1):
	            		familia = dados['familia'].get(email, 'Desconhecido')
	            		ap = dados['apartamento'].get(email, '???')
	           		print(f"{posicao}º lugar: Família {familia} (Apt {ap}) - {ponto} pontos")
			else: 
				print("Retornando ao menu")  
				
				

    # Função para calcular os pontos com base na economia de água em litros

#def calcular_pontos_por_litros(litros_economizados):
    # Definir uma relação entre litros economizados e pontos
    pontos_por_litro = 0.5  # Cada litro economizado gera 0.5 ponto
    pontos_totais = litros_economizados * pontos_por_litro
    return pontos_totais

# Função para exibir a pontuação final
def exibir_resultado(pontos):
    print("\n🏅 Resultado da Economia de Água:")
    print(f"Você economizou {pontos/0.5} litros de água e acumulou {pontos:.2f} pontos!")
    return pontos


pass









class Cadastro:
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
            if 4 <= len(self.senha) <= 20:
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




#Início do sistema  
print("OLÁ,BEM VINDO AO SISTEMA ECODROP💧 do condomínio Village")

tentativas = 3  #  3 tentativas permitidas
while tentativas != 0:
    tipo_servico = input(
        "QUAL TIPO DE SERVIÇO VOCÊ DESEJA ?? (LOGIN/CADASTRO) ").strip().lower()

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

import sys
import json
import time
import re
import random
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



def login():
    with open(r"D:/github/PERÍODO 1/projetova1/projetova1/banco_dados.JSON", "r", encoding="utf-8") as arquivo:
        # quando usa json.load o arquivo json é transformado em dicionário python
        arquivo_lido = json.load(arquivo)

        print("Bem vindo a tela de Login ECODROP💧.")
        #print(random.choice(mensagens_agua))
        time.sleep(1)
        email = input("Digite seu email(ex:nome123@gmail.com):")
        # "joao.silva@email.com": "48291" dados para teste
        senha = input("Digite sua senha:")
        if email in dados_conta:
            if dados_conta[email] == senha:
                menu()
            else:
                print("EMAIL OU SENHA INCORRETO.")
                tentativas = 2
                while tentativas != 0:
                    email = input("Digite seu email(nome123@gmail.com):")
                    senha = input("Digite sua senha:")
                    if dados_conta[email] == senha:
                        menu()
                        # return serve para interromper a função login de continuar rodando e deixar apenas a função menu
                        return
                    else:
                        print("SENHA OU EMAIL INCORRETO.")
                        tentativas -= 1
                        print(f"Tentativas restantes {tentativas}")
                else:
                    print(
                        "NÚMERO DE TENTATIVAS EXTRAPOLADAS.TENTE NOVAMENTE MAIS TARDE.")
                    question1 = input(
                        "Deseja tentar entrar usando código verificador ??(sim/não)")
                    if question1 in ["sim", "si", "yes", "codigo", "código verificador", "verificador", "código"]:
                        tryverificador = input(
                            "Digite seu código verificador(Você terá apenas 1 chance):")
                        if dados_codigov[email] == tryverificador:
                            print(
                                "Você conseguiu o acesso.Mude imediatamente sua senha,visando não ter problemas futuros.")
                            menu()
                            return
                        else:
                            print("Você errou o código verificador.")
                            print(
                                "Tente novamente mais tarde.Use esse tempo para tentar relembrar seus dados.")
                            sys.exit()
                    if question1 in ["não", "no", "nao", "sair", "sai"]:
                        print("Tenha um bom dia.")
                        sys.exit

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
#######


def atualizar():
    print("Bem-vindo à tela de atualização do ECODROP.")
    tentativas = 3

    while tentativas > 0:
        question1 = input(
            "O que você deseja atualizar na sua conta? (dados conta / dados pessoais): ").strip().lower()

        if question1 in ["dados conta", "conta", "dados da conta", "conta dados"]:
            atualizar_conta()
            return

        elif question1 in ["dados pessoais", "pessoais", "informações pessoais", "info pessoais"]:
            atualizar_pessoais()
            return

        else:
            print("Opção inválida.")
            tentativas -= 1
            print(f"Tentativas restantes: {tentativas}")

    print("Limite de tentativas atingido. Encerrando o processo de atualização.")

    pass


def atualizar_pessoais():
    import json
import sys

def atualizar_pessoais():
    # Carregar os dados do arquivo
    with open(r"D:/github/PERÍODO 1/projetova1/projetova1/banco_dados.JSON", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    while True:
        try:
            membros_novos = int(input("Digite a quantidade de membros na família (Quantidade em numeral):"))
            break
        except ValueError:
            print("Valor inválido. Digite apenas números inteiros.")
    
    nome_novo = input("Digite o nome da sua família (Ficará registrado no ranking da forma que você escrever):")
    print(f"Dados atualizados:\nQuantidade de pessoas na família: {membros_novos}\nNome da família: {nome_novo}")
    
    confirmar = input("Deseja confirmar a atualização dos dados? (sim/não): ").strip().lower()
    if confirmar in ["sim", "si", "confirmar", "confirma", "confirmo"]:
        print("DIGITE SEUS DADOS NOVAMENTE PARA A SEGURANÇA DA SUA CONTA")
        email = input("Digite seu e-mail (ex:nome123@gmail.com): ")
        senha = input("Digite sua senha: ")
        
        # Verifica se o e-mail existe e se a senha está correta
        if email in dados["senha"]:
            if dados["senha"][email] == senha:
                # Atualiza os dados
                dados["familia"][email] = nome_novo
                dados["membros"][email] = membros_novos
                print("Dados atualizados com sucesso!")
                
                # Salva os dados modificados no arquivo
                with open(r"D:/github/PERÍODO 1/projetova1/projetova1/banco_dados.JSON", "w", encoding="utf-8") as arquivo:
                    json.dump({
                        "senha": dados["senha"],
                        "familia": dados["familia"],
                        "membros": dados["membros"],
                        "pontos": dados["pontos"],
                        "apartamento": dados["apartamento"],
                        "verificador": dados["verificador"]
                    }, arquivo, indent=4, ensure_ascii=False)
                return
            else:
                print("E-mail ou senha incorretos.")
                tentativas = 2
                while tentativas > 0:
                    email = input("Digite seu e-mail (nome123@gmail.com): ")
                    senha = input("Digite sua senha: ")
                    if dados["senha"].get(email) == senha:
                        dados["familia"][email] = nome_novo
                        dados["membros"][email] = membros_novos
                        print("Dados atualizados com sucesso!")
                        # Salva os dados modificados no arquivo
                        with open(r"D:/github/PERÍODO 1/projetova1/projetova1/banco_dados.JSON", "w", encoding="utf-8") as arquivo:
                            json.dump({
                                "senha": dados["senha"],
                                "familia": dados["familia"],
                                "membros": dados["membros"],
                                "pontos": dados["pontos"],
                                "apartamento": dados["apartamento"],
                                "verificador": dados["verificador"]
                            }, arquivo, indent=4, ensure_ascii=False)
                        return
                    else:
                        print("E-mail ou senha incorretos.")
                        tentativas -= 1
                        print(f"Tentativas restantes: {tentativas}")
                print("Número de tentativas excedido. Tente novamente mais tarde.")
                sys.exit()
        else:
            print("E-mail não encontrado no banco de dados.")
            sys.exit()

    elif confirmar in ["não", "nao", "cancelar", "cancelo", "cancela"]:
        print("Cancelando operação... Voltando para o menu inicial.")
        menu()  # Substitua com sua função de menu, caso necessário
    else:
        print("Opção inválida. Cancelando operação.")
        menu()

# Exemplo de chamada da função
#atualizar_pessoais()



def atualizar_conta():
    pass


def deletar():
    # usar arquivo csv para guardar as possíveis reclamações
    # usar a biblioteca time para capturar a data
    # usuário e motivo
    pass


def feedback():
    print("======Sistema de avaliação"========")

    print("O que você achou do nosso serviço?")
    nome = input("Digite seu nome: ")
    nota = float(input("Qual sua nota (0 a 10)? "))
    
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
    
    print("\n📋 Lista de Feedbacks Recebidos:")
    for i, f in enumerate(feedbacks, start=1):
        print(f"\n{i} - Nome: {f['nome']}")
        print(f"Nota: {f['nota']}/10")
        print(f"Comentário: {f['comentario']}")



def ranking():
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
pass


def resgatar():
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
    # Função para calcular os pontos com base na economia de água em litros
def calcular_pontos_por_litros(litros_economizados):
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

def menu():
    tentativas = 3
    print("BEM VINDO AO MENU PRINCIPAL DO ECODROP💧.")
    #mensagem estilo minecraft
    print(random.choice(mensagens_agua))
    time.sleep(1)
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
        self.email_valido()

    # precisa passar o self como parâmetro para conseguir pegar as info do init

    def email_valido(self):
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

    # Agora verifica se email já está cadastrado
    def conferir_email(self):
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
        # dessa forma oq estará sendo analisado será o valor e não a chave
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
        # print("Bem vindo ao projeto ECODROP do condomínio Village")

        dados_conta[self.email] = self.senha
        dados_familia[self.email] = self.nome_familia
        dados_quantidade[self.email] = self.quantidade
        dados_pontos[self.email] = self.pontos
        dados_apartamento[self.email] = self.apartamento
        dados_codigov[self.email] = self.verificador

        # PARA ARQUIVO TIPO JSON É MELHOR USAR "w" pois qualquer errinho de formatação pode quebrar o sistema
        with open(r"D:/github/PERÍODO 1/projetova1/projetova1/banco_dados.JSON", "w", encoding="utf-8") as arquivo:
            # Aqui, estamos criando um dicionário com duas chaves:
            json.dump({"senha": dados_conta, "familia": dados_familia, "membros": dados_quantidade, "pontos": dados_pontos,
                       "apartamento": dados_apartamento, "verificador": dados_codigov}, arquivo, indent=4, ensure_ascii=False)
        menu()


 # Essa parte que vai realmente começar o código
 # Esse código tem que ser escrito de cima pra baixo,mas para puxar ele tem que ser lá embaixo,pois só assim para o código
 # conseguir usar todas as funções
 #
print("OLÁ,BEM VINDO AO SISTEMA ECODROP💧 do condomínio Village")

tentativas = 3  # Por exemplo, 3 tentativas permitidas
while tentativas != 0:
    tipo_servico = input(
        "QUAL TIPO DE SERVIÇO VOCÊ DESEJA ?? (LOGIN/CADASTRO) ").strip().lower()

    if tipo_servico in ["login", "entrar", "acessar", "fazer login"]:
        login()
        break  # Sai do loop se o serviço for válido

    elif tipo_servico in ["cadastro", "cadastrar", "criar conta", "novo cadastro"]:
        novo_cadastro = Cadastro()
        break  # Sai do loop se o serviço for válido

    else:
        print("Serviço inválido. Por favor, tente novamente.")
        tentativas -= 1
        print(f"Tentativas restantes {tentativas}")

else:
    print("Limite de tentativas atingido. Reinicie o programa.")

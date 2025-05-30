#PROJETO ECODROP  
A ideia do projeto é ser um sistema para condomínios que estimule as pessoas a gastar menos água no dia a dia.Caso o objetivo seja alcançado,o usuário ganhará pontos para trocar por recompensas.

Bibliotecas usadas para o projeto.
Sys=Fechar o sistema no momento que desejarmos e fazer a barra de atualização usando um for
JSON=Conseguir passar o arquivo JSON para dicionário python para se tornar mais fácil seu uso
Time=Usado para dar uma  sensação maior de realidade no sistema,usando a função sleep() para pausar o funcionamento do código por um intervalo de tempo
re=Verificar o formato do email
Pyfliget=Usado para criar um mural com o nome "ECODROP" escrito com caracteres.

FUNCIONALIDADES ELABORADAS:

Class Cadastro=Usei a classe cadastro para conseguir fazer o cadastro do usuário.Dentro dessa classe tem um init,que receberá os dados principais para a conta(email,senha,quantidade de membros,apartamento,nome da família,código verificador) ser cadastrada.Os dados como email,senha e apartamento serão tratados para evitar erros de duplicação ou invalidação.Para assim ser possível o usuário cadastrar sua conta e começar a utilizar as funcionalidades do sistema.

Função Login=Nessa função o usuário poderá logar no sistema caso email e senha(que foram cadastrados anteriormente) estejam corretos.Para assim ser possível o usuário ir para tela de menu.

Função Menu=Nessa opção o usuário será recebido em nosso menu e poderá escolher qual funcionalidade dentro do sistema ele deseja.

Função mostrar dados=A função mostrar dados printará os principais dados(menos a senha e o código verificador,por serem confidenciais) na tela para o usuário que deseja conferir algo.

Função atualização=Nessa função o usuário terá a opção de escolher qual tipo de atualização deseja,atualizar dados da conta(email ou senha) ou dados pessoais(nome da família,quantidade de membros,apartamento).Dependendo da opção que ele escolher irá puxar outras funções mais específicas.Cada uma tendo um tratamento de erro para caso o usuário coloque uma opção inválida ou já cadastrada no email.O objetivo é o usuário ter de forma simples e fácil a opção de atualizar seus dados,de forma segura.

Função deletar=Nessa função o usuário poderá deletar sua conta caso deseje.Se ele concluir essa ação,não poderá mais acessar aquela conta,necessitando fazer outro cadastro para entrar no sistema.

Função feedbcack = Nessa função o usuário tem a opção de escrever a sua opinião acerca do serviço oferecido pelo sistema, comentando se gostou ou não e tendo até 140 caracteres para digitar na aba de feedback mostrada. O usuário também pode dar uma nota de 0 a 10, julgando conforme sua experiência.

Função cálculo = Nessa função o sistema é direcionado a realizar um cálculo de pontos com base nos litros economizados, na quantidade de pessoas na residência e, também, no consumo médio diário de água. Ao efetuar o cálculo, o sistema concede uma certa quantidade de pontos ao usuário e esses pontos são convertidos em prêmios como: voucher, milhas, descontos, créditos de celular, descontos na residência.

Função resgatar = Essa função permite com que o usuário resgate certo prêmio, analisando se o usuário apresenta saldo suficiente para resgatar determinado prêmio.

Função ranking = Essa função realiza um ranqueamento de famílias com base nos litros economizados no mês. Ocupa as posições mais altas aqueles que economizaram mais água ao longo do mês, tomando como critério o consumo médio diário de água.




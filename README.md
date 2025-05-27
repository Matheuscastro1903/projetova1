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







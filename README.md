#PROJETO ECODROP  
Esse repositório é responsável por guardar o código do projeto EcoDrop.O projeto ECODROP surge com o objetivo de incentivar práticas sustentáveis em residências, por meio de um sistema que gamefica o processo de economia de água, visando incentivar os usuários a usarem esse recurso essencial de uma forma mais consciente.

Bibliotecas usadas para o projeto.

Biblioteca "json"=Conseguir passar o arquivo JSON para dicionário python para se tornar mais fácil seu uso

Biblioteca "csv"= 

Biblioteca "re"=Responsável por fazer a verificação do formato do email

Biblioteca "random"=

Biblioteca "datetime"=

Biblioteca "PIL"=

Biblioteca "io"=

Biblioteca "pandas"=

Biblioteca "collection"=

Biblioteca "matplotlib"=

Biblioteca "datetime"=







ORGANIZAÇÃO DO PROJETO:

A organização do nosso projeto foi feita inteiramente em POO,visando um melhor entendimento e manutenção do código.
O projeto EcoDrop deve ser rodado no arquivo "main.py",que importa todas classes necessárias para o seu bom funcionamento.

Arquivos e Classes:
Dividimos cada classe importante em seu devido arquivo.

• Arquivo "main.py".

Esse arquivo é responsável por armazenar a classe master("App").Ela que "comandará" as trocas de tela durante todo o projeto e o funcionamento de cada parte do sistema.

•Arquivo "Telainicial.py".

Esse arquivo recebe a classe TelaInicial.Essa classe será responsável por guardar a parte da interface destinada a tela inicial do sistema.Na qual,o usuário poderá transitar entre 4 opções(login,cadastro,modo administrador e sobre nós).

•Arquivo "Login.py".

Recebe a classe Login.Essa classe é responsável por toda a operação de login,desde o surgimento da interface,até o processo de validação.Após o processo de login ser feito,o usuário será redirecionado para a tela de menu principal do sistema.

•Arquivo "Usuario.py"

Recebe a classe Usuario.Essa classe é responsável por armazenar tudo que diz a respeito do cadastro de usuário. Ela irá mostrar a parte da interface destinada ao cadastro,irá fazer o tratamento dos erros e salvar no arquivo json os novos dados.Caso a pessoas que estiver utilizando o sistema e tenha finalizado a etapa de cadastro de usuário,terá a opção depois de ir para o login ou sair do sistema.

•Arquivo "ModoAdm.py".

Esse arquivo Armazena as classes ModoAdm e OperacoesAdm.A classe ModoAdm é responsável por armazenar tudo a respeito do modo administrador.Desde a entrada,que deve ser feita com um código único(!GaMa#1903!) até as 3 opções que é dada no modo admnistrador(Ver dados,Editar dados e Analisar Dados).
A classe OperacoesAdm é responsável por fazer as operações necessárias para mostrar tabela,média e gráficos dos métodos Ver dados e Analisar Dados.
A ideia do modo administrador é o síndico poder ter um olhar mais crítico em relação aos dados dos usuários.

-Método Ver dados=Juntamente com a classe OperacoesAdm,mostrará uma tabela organizada com dados não sensíveis dos usuários.

-Método Editar dados=Esse método da a opção do síndico editar dados que foram cadastrados de forma errada e ter maior controle sobre tudo que ocorre no sistema.

-Método Analisar dados=Juntamente com a classe OperacoesAdm,esse método irá mostrar gráficos para que o administrador consiga analisar quais andares gastam mais água,qual o gasto de água em relação a quantidade de pessoas no apartamento e outros tipos de análise.A ideia é fazer uma análise crítica,visando fazer estimativas e evitar erros.


•Arquivo "Sobrenos.py"=Esse arquivo guarda a classe SobreNos,na qual é responsável por guardar a parte da interface que será usada para mostra um texto sobre a história do ECODROP e uma foto dos criadores do projeto.


•Arquivo "UsarioLogado.py"=


#####################################################################################
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



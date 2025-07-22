
"""
Esse arquivo será usado para guardar duas funções importantíssimas para o tratamento de erro.Nossa ideia foi
evitar ao máximo várias etapas de validação  com as funções "validar_numeros"=responsável por deixar o usuário 
digitar apenas números e a função  "validar_letras_espacos"=responsável por permitir o usuário digitar apenas texto.

Dessa forma,evitamos vários erros de tratamento de erros e deixamos o código mais limpo

 """


def validar_numeros(novo_texto):
    """Função utilizada para permitir digitar apenas números"""
    return novo_texto.isdigit() or novo_texto == ""

def validar_letras_espacos(novo_texto):
    """Função utilizada para deixar apenas digitar letras e espaços"""
    return all(c.isalpha() or c.isspace() for c in novo_texto) or novo_texto == ""
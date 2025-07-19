# Funções de validação
def validar_numeros(novo_texto):
    """Função utilizada para permitir digitar apenas números"""
    return novo_texto.isdigit() or novo_texto == ""

def validar_letras_espacos(novo_texto):
    """Função utilizada para deixar apenas digitar letras e espaços"""
    return all(c.isalpha() or c.isspace() for c in novo_texto) or novo_texto == ""
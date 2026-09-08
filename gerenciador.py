import os
from modelos import Idioma
def salvar_idioma(idioma, arq_nome="idiomas.txt"):
    with open(arq_nome, "a+", encoding="utf-8") as arq:
        arq.seek(0, os.SEEK_END)  # Move o cursor para o final do arquivo
        offset = arq.tell()  # Obtém o offset atual (posição no arquivo)
        linha = f"{idioma.codigo},{idioma.descricao}\n"
        arq.write(linha)
        return offset  # Retorna o offset onde o idioma foi salvo


def ler_idioma_offset(offset, arq_nome="idiomas.txt"):
    with open(arq_nome, "r", encoding="utf-8") as arq:
        arq.seek(offset)  # Move o cursor para o offset fornecido
        linha = arq.readline()
        if not linha:
            return None  # Retorna None se não houver linha
        codigo, descricao = linha.strip().split(",")#o strip() remove espaços em branco e o split() separa a linha em duas partes, usando a vírgula como delimitador
        return Idioma(codigo, descricao)  # Retorna um objeto Idioma
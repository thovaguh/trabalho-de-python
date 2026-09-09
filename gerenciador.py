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
    
    def carregar_indices_idiomas(arvore, arq_nome="idiomas.txt"):
        if not os.path.exists(arq_nome):#evita o erro de que o arq nao existe na primeira vez que for rodar
            return
        
        with open(arq_nome, "r", encoding="utf-8") as arq:
            while True:
                offset = arq.tell()
                
                linha = arq.readline()
                
                if not linha:#condição de parada do while
                    break
                
                partes = linha.strip().split(",")
                
                if len(partes) >= 2:
                    codigo = int(partes[0])
                    
                    arvore.inserir(codigo, offset) #reconstroi o no na arvore que esta na RAM
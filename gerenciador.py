import os
from modelos import Idioma, Licao, Exercicio, Usuario

#     IDIOMAS.TXT
def salvar_idioma(idioma, arq_nome="idiomas.txt"):
    # O bloco 'with' abre o arquivo e garante o fechamento automático no final (dispensa o fclose).
    # O modo "a+" (Append) abre para adição, protegendo os dados antigos e indo para o final.
    with open(arq_nome, "a+", encoding="utf-8") as arq:
        arq.seek(0, os.SEEK_END) # Força a agulha ir para o último byte do arquivo
        
        # tell() é o "GPS": pega a coordenada exata em bytes de onde a linha vai começar
        offset = arq.tell() 
        
        linha = f"{idioma.codigo},{idioma.descricao}\n"
        arq.write(linha)
        
        return offset # Devolvemos a coordenada para a Árvore Binária guardar na RAM


def ler_idioma_offset(offset, arq_nome="idiomas.txt"):
    # O modo "r" (Read) abre apenas para leitura.
    with open(arq_nome, "r", encoding="utf-8") as arq:
        # seek() é o "Teletransporte": pula instantaneamente para a coordenada (offset) passada
        arq.seek(offset) 
        
        linha = arq.readline() # Lê apenas a linha daquela coordenada
        
        if not linha:
            return None
        
        # strip() limpa sujeiras como o "\n" do final da linha
        # split(",") corta a string onde tem vírgula, transformando em um vetor: ["1", "Ingles"]
        codigo, descricao = linha.strip().split(",")
        
        return Idioma(codigo, descricao)


def carregar_indices_idiomas(arvore, arq_nome="idiomas.txt"):
    # Evita erro na primeira vez que o programa roda e o arquivo ainda não existe
    if not os.path.exists(arq_nome):
        return

    with open(arq_nome, "r", encoding="utf-8") as arq:
        while True:
            # Captura a posição em bytes (GPS) ANTES de ler a linha atual
            offset = arq.tell()
            
            linha = arq.readline()
            
            # Se a linha vier vazia, chegamos ao Fim do Arquivo (EOF), então quebra o laço
            if not linha:
                break
            
            # Separa os dados pelo delimitador (vírgula)
            partes = linha.strip().split(",")
            
            if len(partes) >= 2:
                codigo = int(partes[0]) # Pega apenas a chave primária (ID)
                
                # Reconstrói a estrutura na memória RAM inserindo a chave e a coordenada (offset)
                arvore.inserir(codigo, offset)


#   LIÇÕES.TXT

def salvar_licao(licao, arq_nome="licoes.txt"):
    with open(arq_nome, "a+", encoding="utf-8") as arq:
        arq.seek(0, os.SEEK_END)
        offset = arq.tell()
        
        # Salva os 3 atributos: ID da lição, Título e ID do Idioma pai
        linha = f"{licao.codigo},{licao.codigo_idioma},{licao.niveis_total}\n"
        arq.write(linha)
        
        return offset


def ler_licao_offset(offset, arq_nome="licoes.txt"):
    with open(arq_nome, "r", encoding="utf-8") as arq:
        arq.seek(offset)
        linha = arq.readline()
        if not linha:
            return None
        
        codigo, codigo_idioma, niveis_total = linha.strip().split(",")
        return Licao(codigo, codigo_idioma, niveis_total)


def carregar_indices_licoes(arvore, arq_nome="licoes.txt"):
    if not os.path.exists(arq_nome):
        return

    with open(arq_nome, "r", encoding="utf-8") as arq:
        while True:
            offset = arq.tell()
            linha = arq.readline()
            if not linha:
                break
            partes = linha.strip().split(",")
            if len(partes) >= 3:
                codigo = int(partes[0])
                arvore.inserir(codigo, offset)


#   EXERCÍCIOS.TXT

def salvar_exercicio(exercicio, arq_nome="exercicios.txt"):
    with open(arq_nome, "a+", encoding="utf-8") as arq:
        arq.seek(0, os.SEEK_END)
        offset = arq.tell()
        
        # Salva os 4 atributos: ID do exercício, Enunciado, Resposta e ID da Lição pai
        linha = f"{exercicio.codigo},{exercicio.codigo_licao},{exercicio.nivel_dificuldade},{exercicio.descricao},{exercicio.opcoes_resposta},{exercicio.resposta_correta},{exercicio.pontuacao}\n"
        arq.write(linha)
        
        return offset


def ler_exercicio_offset(offset, arq_nome="exercicios.txt"):
    with open(arq_nome, "r", encoding="utf-8") as arq:
        arq.seek(offset)
        linha = arq.readline()
        if not linha:
            return None
        
        codigo, codigo_licao, nivel_dificuldade, descricao, opcoes_resposta, resposta_correta, pontuacao = linha.strip().split(",")
        return Exercicio(codigo, codigo_licao, nivel_dificuldade, descricao, opcoes_resposta, resposta_correta, pontuacao)


def carregar_indices_exercicios(arvore, arq_nome="exercicios.txt"):
    if not os.path.exists(arq_nome):
        return

    with open(arq_nome, "r", encoding="utf-8") as arq:
        while True:
            offset = arq.tell()
            linha = arq.readline()
            if not linha:
                break
            partes = linha.strip().split(",")
            if len(partes) >= 7:
                codigo = int(partes[0])
                arvore.inserir(codigo, offset)


#   USUÁRIOS.TXT

def salvar_usuario(usuario, arq_nome="usuarios.txt"):
    with open(arq_nome, "a+", encoding="utf-8") as arq:
        arq.seek(0, os.SEEK_END)
        offset = arq.tell()
        
        # Salva os 3 atributos: ID do usuário, Nome e Email
        linha = f"{usuario.codigo},{usuario.nome},{usuario.codigo_idioma},{usuario.nivel_atual},{usuario.pontuacao_total}\n"
        arq.write(linha)
        
        return offset


def ler_usuario_offset(offset, arq_nome="usuarios.txt"):
    with open(arq_nome, "r", encoding="utf-8") as arq:
        arq.seek(offset)
        linha = arq.readline()
        if not linha:
            return None
        
        codigo, nome, codigo_idioma, nivel_atual, pontuacao_total = linha.strip().split(",")
        return Usuario(codigo, nome, codigo_idioma, nivel_atual, pontuacao_total)


def carregar_indices_usuarios(arvore, arq_nome="usuarios.txt"):
    if not os.path.exists(arq_nome):
        return

    with open(arq_nome, "r", encoding="utf-8") as arq:
        while True:
            offset = arq.tell()
            linha = arq.readline()
            if not linha:
                break
            partes = linha.strip().split(",")
            if len(partes) >= 5:
                codigo = int(partes[0])
                arvore.inserir(codigo, offset)
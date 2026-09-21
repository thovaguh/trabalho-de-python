import os
from modelos import Idioma, Licao, Exercicio, Usuario

# ==========================================
#               IDIOMAS.TXT
# ==========================================

def salvar_idioma(idioma, arq_nome="idiomas.txt"):
    with open(arq_nome, "a+", encoding="utf-8") as arq:
        arq.seek(0, os.SEEK_END)  
        offset = arq.tell()  
        
        linha = f"{idioma.codigo},{idioma.descricao}\n"
        arq.write(linha)
        
        return offset

def ler_idioma_offset(offset, arq_nome="idiomas.txt"):
    with open(arq_nome, "r", encoding="utf-8") as arq:
        arq.seek(offset) 
        linha = arq.readline() 
        
        if not linha:
            return None
        
        codigo, descricao = linha.strip().split(",")
        return Idioma(codigo, descricao)

def carregar_indices_idiomas(arvore, arq_nome="idiomas.txt"):
    if not os.path.exists(arq_nome):
        return

    with open(arq_nome, "r", encoding="utf-8") as arq:
        while True:
            offset = arq.tell()
            linha = arq.readline()
            
            if not linha:
                break
            
            partes = linha.strip().split(",")
            if len(partes) >= 2:
                codigo = int(partes[0])
                arvore.inserir(codigo, offset)


# ==========================================
#               LIÇÕES.TXT
# ==========================================

def salvar_licao(licao, arq_nome="licoes.txt"):
    with open(arq_nome, "a+", encoding="utf-8") as arq:
        arq.seek(0, os.SEEK_END)
        offset = arq.tell()
        
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


# ==========================================
#             EXERCÍCIOS.TXT
# ==========================================

def salvar_exercicio(exercicio, arq_nome="exercicios.txt"):
    with open(arq_nome, "a+", encoding="utf-8") as arq:
        arq.seek(0, os.SEEK_END)
        offset = arq.tell()
        
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


# ==========================================
#              USUÁRIOS.TXT
# ==========================================

def salvar_usuario(usuario, arq_nome="usuarios.txt"):
    with open(arq_nome, "a+", encoding="utf-8") as arq:
        arq.seek(0, os.SEEK_END)
        offset = arq.tell()
        
        linha = f"{usuario.codigo},{usuario.nome},{usuario.codigo_idioma},{usuario.nivel_atual},{usuario.pontuacao_total},{usuario.exercicios_concluidos}\n"
        arq.write(linha)
        
        return offset

def ler_usuario_offset(offset, arq_nome="usuarios.txt"):
    with open(arq_nome, "r", encoding="utf-8") as arq:
        arq.seek(offset)
        linha = arq.readline().strip()
        
        if not linha:
            return None
            
        partes = linha.split(",")
        
        cod = int(partes[0])
        nome = partes[1]
        cod_idioma = int(partes[2])
        nivel = int(partes[3])
        pts = int(partes[4])
        concluidos = partes[5] if len(partes) > 5 else ""
        
        return Usuario(cod, nome, cod_idioma, nivel, pts, concluidos)

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
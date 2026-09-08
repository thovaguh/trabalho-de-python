class Idioma:
    def __init__(self, idioma_cod, descricao):
        self.codigo = int(idioma_cod)
        self.descricao = descricao


class Licao:
    def __init__(self, licao_cod, idioma_cod, niveis_total):
        self.licao_cod = int(licao_cod)
        self.idioma_cod = int(idioma_cod)
        self.niveis_total = int(niveis_total)


class Exercicio:
    def __init__(self, exercicio_cod, licao_cod, nivel_dificuldade, descricao, opcoes_resposta, resposta_correta, pontuacao):
        self.exercicio_cod = int(exercicio_cod)
        self.licao_cod = int(licao_cod)
        self.nivel_dificuldade = int(nivel_dificuldade)
        self.descricao = descricao
        self.opcoes_resposta = opcoes_resposta  # Ex: lista ["a", "b", "c", "d"]
        self.resposta_correta = resposta_correta
        self.pontuacao = int(pontuacao)


class Usuario:
    def __init__(self, usuario_cod, nome, cod_idioma, nivel_atual=1, pontuacao_total=0): # aqui temos variaveis ja recebendo valores de entrada
        self.usuario_cod = int(usuario_cod)
        self.nome = nome
        self.cod_idioma = int(cod_idioma)
        self.nivel_atual = int(nivel_atual)
        self.pontuacao_total = int(pontuacao_total)
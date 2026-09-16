class Idioma:
    def __init__(self, codigo, descricao):
        self.codigo = int(codigo)
        self.descricao = descricao


class Licao:
    def __init__(self, codigo, codigo_idioma, niveis_total):
        self.codigo = int(codigo)
        self.codigo_idioma = int(codigo_idioma)
        self.niveis_total = int(niveis_total)


class Exercicio:
    def __init__(self, codigo, codigo_licao, nivel_dificuldade, descricao, opcoes_resposta, resposta_correta, pontuacao):
        self.codigo = int(codigo)
        self.codigo_licao = int(codigo_licao)
        self.nivel_dificuldade = int(nivel_dificuldade)
        self.descricao = descricao
        

        # PROTEÇÃO CONTRA CONFLITO DE DELIMITADORES
        # O arquivo .txt usa a vírgula (,) para separar as colunas do "banco de dados".
        # Se salvarmos uma lista normal, suas vírgulas internas quebrarão o split(",") na leitura.
    
            # O isinstance() verifica se 'opcoes_resposta' é uma lista (um vetor).
        if isinstance(opcoes_resposta, list):
            # O .join() pega o vetor ["A", "B", "C", "D"] e "costura" tudo em um texto só.
            # Usamos o "|" (pipe) no meio para não dar conflito com a vírgula do gerenciador.
            # Resultado salvo no disco: "A|B|C|D"
            self.opcoes_resposta = "|".join(opcoes_resposta)
        else:
            # Se não for uma lista (ex: já é o texto lido diretamente do arquivo .txt),
            # ignora a conversão e guarda a string do jeito que está.
            self.opcoes_resposta = opcoes_resposta
            
        self.resposta_correta = resposta_correta
        self.pontuacao = int(pontuacao)

class Usuario:
    # Adicionamos o exercicios_concluidos="" no final
    def __init__(self, codigo, nome, codigo_idioma, nivel_atual=1, pontuacao_total=0, exercicios_concluidos=""):
        self.codigo = codigo
        self.nome = nome
        self.codigo_idioma = codigo_idioma
        self.nivel_atual = nivel_atual
        self.pontuacao_total = pontuacao_total
        self.exercicios_concluidos = exercicios_concluidos
# nó
class No:
    def __init__(self, chave, offset):
        self.chave = int(chave)
        self.offset = int(offset)
        self.esquerda = None
        self.direita = None

# arvore
class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    # inserir
    def inserir(self, chave, offset):
        if self.raiz is None:
            self.raiz = No(chave, offset)
        else:
            self._inserir_recursivo(self.raiz, chave, offset)

    def _inserir_recursivo(self, no_atual, chave, offset):
        chave = int(chave)
        if chave < no_atual.chave:
            if no_atual.esquerda is None:
                no_atual.esquerda = No(chave, offset)
            else:
                self._inserir_recursivo(no_atual.esquerda, chave, offset)
        elif chave > no_atual.chave:
            if no_atual.direita is None:
                no_atual.direita = No(chave, offset)
            else:
                self._inserir_recursivo(no_atual.direita, chave, offset)
        else:
            print(f"Erro: Chave {chave} já existe no índice.")

    # buscar
    def buscar(self, chave):
        return self._buscar_recursivo(self.raiz, int(chave))  # Converte para int antes de iniciar a busca recursiva

    def _buscar_recursivo(self, no_atual, chave):
        if no_atual is None:
            return None 
        
        if chave == no_atual.chave:
            return no_atual.offset
        elif chave < no_atual.chave:
            return self._buscar_recursivo(no_atual.esquerda, chave)
        else:
            return self._buscar_recursivo(no_atual.direita, chave)
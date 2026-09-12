class No: #esse é o bloco de memoria que vai armazenar a chave e o offset do arquivo
    def __init__(self, chave, offset):
        self.chave = int(chave)
        self.offset = int(offset)
        self.esquerda = None
        self.direita = None

# o self é como: guarde.essa variavel = nessa variavel
class ArvoreBinaria: # essa parte é a arvore binaria que vai armazenar os blocos de memoria
    def __init__(self):
        self.raiz = None

    def inserir(self, chave, offset): #aqui é a função que vai inserir uma nova chave e seu offset no arquivo
        if self.raiz is None:
            self.raiz = No(chave, offset)
        else:
            self._inserir_recursivo(self.raiz, chave, offset)#aqui temos um else que chama a função recursiva para inserir a chave e o offset no lugar correto da arvore

    def _inserir_recursivo(self, no_atual, chave, offset):#aqui é a função recursiva que vai percorrer a arvore e inserir a chave e o offset no lugar correto
        if chave < no_atual.chave:
            if no_atual.esquerda is None:
                no_atual.esquerda = No(chave, offset)
            else:
                self._inserir_recursivo(no_atual.esquerda, chave, offset)#esse else chama a função recursiva novamente para percorrer a arvore e encontrar o lugar correto para inserir a chave e o offset
        elif chave > no_atual.chave:
            if no_atual.direita is None:
                no_atual.direita = No(chave, offset)#esse elif chama a função recursiva novamente para percorrer a arvore e encontrar o lugar correto para inserir a chave e o offset
            else:
                self._inserir_recursivo(no_atual.direita, chave, offset)#aqui testa se a chave é maior que a chave do nó atual, se for, ele vai para a direita da arvore e chama a função recursiva novamente para percorrer a arvore e encontrar o lugar correto para inserir a chave e o offset
        else:
            print(f"Erro: Chave {chave} já existe no índice.")

    def buscar(self, chave):#esse trecho é a função que vai buscar uma chave no arquivo e retornar o offset correspondente
        return self._buscar_recursivo(self.raiz, chave)

    def _buscar_recursivo(self, no_atual, chave):
        if no_atual is None:
            return None  # Chave não encontrada
        
        if chave == no_atual.chave:
            return no_atual.offset  # Encontrou! Retorna a posição no arquivo.
        elif chave < no_atual.chave:
            return self._buscar_recursivo(no_atual.esquerda, chave)
        else:
            return self._buscar_recursivo(no_atual.direita, chave)
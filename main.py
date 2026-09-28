# Importa a biblioteca tkinter, usada para criar a interface gráfica (a janela do programa). 
# O 'as tk' é um apelido para não precisarmos digitar 'tkinter' toda hora.
import tkinter as tk 

# Importa especificamente as caixas de alerta (pop-ups de erro e sucesso) da biblioteca tkinter.
from tkinter import messagebox 

# Importa recursos do sistema operacional. Vamos usar para checar se os arquivos .txt existem.
import os 

# Importa as classes que definem o formato dos nossos dados (criadas no arquivo modelos.py).
from modelos import Idioma, Licao, Exercicio, Usuario 

# Importa a estrutura de dados Árvore Binária (criada no arquivo arvore.py) para buscar dados rápido na memória.
from arvore import ArvoreBinaria 

# Importa o arquivo gerenciador.py, que contém as funções de leitura e salvamento originais.
import gerenciador 

# Função que cria dados básicos no sistema para que ele não inicie completamente vazio.
def inicializar_banco_padrao(arvore_idiomas, arvore_exercicios, arvore_licoes):
    # Verifica na árvore se o idioma 1 (Inglês) já existe. Se retornar None (vazio), ele cria.
    if arvore_idiomas.buscar(1) is None:
        # Cria o objeto Idioma, salva no arquivo TXT e insere a posição dele na árvore.
        arvore_idiomas.inserir(1, gerenciador.salvar_idioma(Idioma(1, "Inglês")))
        
    # Faz a mesma verificação e criação para o idioma 2 (Espanhol).
    if arvore_idiomas.buscar(2) is None:
        arvore_idiomas.inserir(2, gerenciador.salvar_idioma(Idioma(2, "Espanhol")))
    
    # Verifica se a lição base do Inglês (código 1) existe. Se não, cria com 5 níveis no total.
    if arvore_licoes.buscar(1) is None:
        arvore_licoes.inserir(1, gerenciador.salvar_licao(Licao(1, 1, 5))) 
        
    # Verifica se a lição base do Espanhol (código 2) existe. Se não, cria com 5 níveis.
    if arvore_licoes.buscar(2) is None:
        arvore_licoes.inserir(2, gerenciador.salvar_licao(Licao(2, 2, 5)))

# Classe principal que controla toda a janela e as telas do aplicativo.
class MaxLanguageApp:
    
    # O método __init__ é o que roda automaticamente assim que o aplicativo é aberto.
    def __init__(self, root):
        self.root = root # Guarda a janela principal do sistema operacional na variável 'root'.
        self.root.title("MaxLanguage") # Define o título que aparece na barra superior da janela.
        self.root.geometry("400x500") # Define o tamanho inicial da janela (400 pixels de largura por 500 de altura).
        
        # Cria árvores binárias vazias na memória RAM para cada tipo de dado.
        self.arvore_idiomas = ArvoreBinaria()
        self.arvore_licoes = ArvoreBinaria()
        self.arvore_exercicios = ArvoreBinaria()
        self.arvore_usuarios = ArvoreBinaria()
        
        # Lê os arquivos TXT e preenche as árvores com as posições (índices) de cada registro.
        gerenciador.carregar_indices_idiomas(self.arvore_idiomas)
        gerenciador.carregar_indices_licoes(self.arvore_licoes)
        gerenciador.carregar_indices_exercicios(self.arvore_exercicios)
        gerenciador.carregar_indices_usuarios(self.arvore_usuarios)
        
        # Chama a função lá de cima para garantir que Inglês e Espanhol existam no sistema.
        inicializar_banco_padrao(self.arvore_idiomas, self.arvore_exercicios, self.arvore_licoes)
        
        # Variável que vai guardar os dados do aluno que fizer login. Começa vazia (None).
        self.usuario_logado = None
        
        # Cria uma "caixa" invisível (Frame) que vai segurar todos os botões e textos.
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True) # Manda essa caixa preencher toda a janela.
        
        # Chama a função que desenha a tela inicial do jogo.
        self.mostrar_tela_inicial()

    # Função utilitária para apagar tudo o que está na tela antes de desenhar uma tela nova.
    def limpar_tela(self):
        # Passa por todos os elementos (widgets) dentro do container e destrói (apaga) um por um.
        for widget in self.container.winfo_children():
            widget.destroy()

    # --- LÓGICA DE ARQUIVOS (Salvar e Apagar) ---

    # Função para cadastrar um usuário pela primeira vez direto no arquivo TXT.
    def salvar_novo_usuario_no_txt(self, usuario):
        # Abre o arquivo 'usuarios.txt' no modo "a" (append = adicionar no final). Se não existir, ele cria.
        with open("usuarios.txt", "a", encoding="utf-8") as f:
            # Pega a mochila de exercícios concluídos. Se não tiver, usa texto vazio "".
            mochila = getattr(usuario, 'exercicios_concluidos', "")
            
            # Escreve os dados do usuário separados por vírgula e pula uma linha (\n) no final.
            f.write(f"{usuario.codigo},{usuario.nome},{usuario.codigo_idioma},{usuario.nivel_atual},{usuario.pontuacao_total},{mochila}\n")
        
        # Como adicionamos um aluno novo, limpamos a árvore de usuários e carregamos de novo para atualizar a memória.
        self.arvore_usuarios = ArvoreBinaria()
        gerenciador.carregar_indices_usuarios(self.arvore_usuarios)

    # Função para modificar (salvar progresso) ou apagar um usuário existente.
    def atualizar_txt(self, codigo_usuario, apagar=False):
        # Se o arquivo usuarios.txt ainda não existir no computador, interrompe a função para não dar erro.
        if not os.path.exists("usuarios.txt"): return
        
        # Abre o arquivo no modo "r" (read = ler) e guarda todas as linhas numa lista chamada 'linhas'.
        with open("usuarios.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
        
        # Abre o mesmo arquivo no modo "w" (write = escrever). ISSO APAGA O ARQUIVO ANTIGO para escrevermos um novo por cima.
        with open("usuarios.txt", "w", encoding="utf-8") as f:
            # Passa linha por linha da lista que guardamos.
            for linha in linhas:
                # Corta a linha nas vírgulas para separar os dados (ID, Nome, etc).
                dados = linha.strip().split(",")
                
                # Verifica se a linha não está vazia e se o ID da linha é igual ao ID do aluno que queremos mexer.
                if dados and dados[0] == str(codigo_usuario):
                    
                    # Se a ordem for para apagar (Exclusão)...
                    if apagar == True:
                        continue # O comando 'continue' pula para a próxima linha sem escrever esta no arquivo novo.
                    
                    # Se não for para apagar (Atualização de progresso)...
                    else:
                        mochila = getattr(self.usuario_logado, 'exercicios_concluidos', "")
                        # Escreve a linha novamente, mas com os dados atualizados de Nível e XP.
                        f.write(f"{self.usuario_logado.codigo},{self.usuario_logado.nome},{self.usuario_logado.codigo_idioma},{self.usuario_logado.nivel_atual},{int(self.usuario_logado.pontuacao_total)},{mochila}\n")
                
                # Se o ID da linha for de OUTRO aluno, apenas reescreve a linha do jeito que estava.
                else:
                    f.write(linha)
                    
        # Limpa e recarrega a árvore de usuários para que a memória saiba das mudanças feitas no arquivo TXT.
        self.arvore_usuarios = ArvoreBinaria()
        gerenciador.carregar_indices_usuarios(self.arvore_usuarios)


    # --- TELAS DO SISTEMA (Frontend) ---

    # Função que desenha o Menu Principal.
    def mostrar_tela_inicial(self):
        self.limpar_tela() # Limpa rastros de telas anteriores.
        
        # Cria um texto (Label) e o coloca na tela com .pack(pady=20), que dá um espaço (margem) de 20 pixels em cima e embaixo.
        tk.Label(self.container, text="Menu Principal - MaxLanguage").pack(pady=20)
        
        # Cria botões. 'command' indica qual função vai rodar quando o botão for clicado.
        tk.Button(self.container, text="Criar Conta", command=self.mostrar_tela_matricula).pack(pady=5)
        tk.Button(self.container, text="Fazer Login", command=self.mostrar_tela_login).pack(pady=5)
        tk.Button(self.container, text="Ver Ranking", command=self.mostrar_tela_ranking).pack(pady=5)
        tk.Button(self.container, text="Apagar Conta", command=self.mostrar_tela_remover).pack(pady=5)
        
        # self.root.quit é um comando nativo que fecha o aplicativo.
        tk.Button(self.container, text="Sair do Jogo", command=self.root.quit).pack(pady=20)

    # Função que desenha a tela de criação de conta.
    def mostrar_tela_matricula(self):
        self.limpar_tela()
        tk.Label(self.container, text="Cadastro de Aluno").pack(pady=20)
        
        # tk.Entry cria uma caixinha branca para o usuário digitar informações.
        tk.Label(self.container, text="ID (número):").pack()
        entry_id = tk.Entry(self.container)
        entry_id.pack(pady=5)
        
        tk.Label(self.container, text="Nome:").pack()
        entry_nome = tk.Entry(self.container)
        entry_nome.pack(pady=5)
        
        tk.Label(self.container, text="Idioma (1 para Inglês | 2 para Espanhol):").pack()
        entry_idioma = tk.Entry(self.container)
        entry_idioma.pack(pady=5)
        
        # Função interna que só roda quando o botão "Salvar" for clicado.
        def salvar():
            try:
                # Pega (.get) o que foi digitado nas caixas e converte para número (int) ou texto.
                codigo = int(entry_id.get())
                nome = entry_nome.get()
                cod_idioma = int(entry_idioma.get())
                
                # Busca na árvore para ver se o ID já existe. Se achar algo diferente de None, o ID está em uso.
                if self.arvore_usuarios.buscar(codigo) is not None:
                    messagebox.showerror("Erro", "ID já existe!") # Mostra pop-up de erro.
                    return # Para a função aqui.
                
                # Busca se o idioma digitado existe (1 ou 2).
                if self.arvore_idiomas.buscar(cod_idioma) is None:
                    messagebox.showerror("Erro", "Idioma inválido!")
                    return
                
                # Instancia (cria) um objeto Usuário com Nível 1 e 0 Pontos.
                try:
                    novo_usu = Usuario(codigo, nome, cod_idioma, 1, 0, "")
                except TypeError:
                    novo_usu = Usuario(codigo, nome, cod_idioma, 1, 0)
                    
                # Aciona a nossa função para salvar esse objeto no final do arquivo TXT.
                self.salvar_novo_usuario_no_txt(novo_usu)
                
                # Mostra sucesso e devolve o usuário para o menu inicial.
                messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
                self.mostrar_tela_inicial()
                
            except ValueError:
                # Cai aqui se o usuário digitar letras onde o programa esperava converter para número (int).
                messagebox.showerror("Erro", "Use apenas números no ID e Idioma.")

        tk.Button(self.container, text="Salvar", command=salvar).pack(pady=10)
        tk.Button(self.container, text="Voltar", command=self.mostrar_tela_inicial).pack(pady=5)

    # Função que desenha a tela de Login.
    def mostrar_tela_login(self):
        self.limpar_tela()
        tk.Label(self.container, text="Login").pack(pady=20)
        
        tk.Label(self.container, text="Digite seu ID:").pack()
        entry_id = tk.Entry(self.container)
        entry_id.pack(pady=5)
        
        def logar():
            try:
                id_usu = int(entry_id.get())
                
                # Pede para a árvore procurar a posição (offset) do ID no arquivo TXT.
                offset = self.arvore_usuarios.buscar(id_usu)
                
                if offset is None:
                    messagebox.showerror("Erro", "Aluno não encontrado!")
                    return
                    
                # Usa a posição encontrada para ir no arquivo e carregar os dados completos do aluno.
                self.usuario_logado = gerenciador.ler_usuario_offset(offset)
                
                # Manda o usuário para a tela das fases.
                self.mostrar_dashboard_aluno()
            except ValueError:
                messagebox.showerror("Erro", "Digite um número.")

        tk.Button(self.container, text="Entrar", command=logar).pack(pady=10)
        tk.Button(self.container, text="Voltar", command=self.mostrar_tela_inicial).pack(pady=5)

    # Função que desenha as fases (Níveis).
    def mostrar_dashboard_aluno(self):
        self.limpar_tela()
        usu = self.usuario_logado
        
        # --- VERIFICAÇÃO SE ELE JÁ ZEROU O JOGO ---
        offset_licao = self.arvore_licoes.buscar(int(usu.codigo_idioma))
        if offset_licao is not None:
            licao = gerenciador.ler_licao_offset(offset_licao)
            
            # Puxa o total de níveis previstos para esse idioma.
            total_niveis = int(licao.niveis_total) 
            
            # Se o nível do aluno for maior que o total de níveis do idioma, mostra o certificado.
            if int(usu.nivel_atual) > total_niveis:
                self.mostrar_tela_certificado()
                return # Interrompe a execução para não desenhar o resto da tela.
        
        # Mostra o status do aluno.
        tk.Label(self.container, text=f"Aluno: {usu.nome} | Nível: {usu.nivel_atual} | XP: {usu.pontuacao_total}").pack(pady=20)
        tk.Label(self.container, text="Escolha a fase:").pack()
        
        # Cria um botão de fase usando um laço de repetição. Cria do nível 1 até o nível atual do aluno.
        for n in range(1, int(usu.nivel_atual) + 1):
            # lambda lvl=n: passa o número do botão clicado para a próxima função.
            tk.Button(self.container, text=f"Nível {n}", command=lambda lvl=n: self.mostrar_tela_exercicios(lvl)).pack(pady=5)
                            
        tk.Button(self.container, text="Sair da Conta", command=self.mostrar_tela_inicial).pack(pady=20)

    # Função que mostra as perguntas disponíveis dentro de uma fase específica.
    def mostrar_tela_exercicios(self, nivel_selecionado):
        self.limpar_tela()
        usu = self.usuario_logado
        
        tk.Label(self.container, text=f"Exercícios do Nível {nivel_selecionado}").pack(pady=20)
        
        # Pega a lista de IDs de exercícios que o aluno já resolveu e separa pelo traço.
        concluidos = getattr(usu, 'exercicios_concluidos', "").split("-")
        
        if os.path.exists("exercicios.txt"):
            with open("exercicios.txt", "r", encoding="utf-8") as arq:
                # Lê o banco de dados de exercícios linha por linha.
                for linha in arq:
                    partes = linha.strip().split(",")
                    if len(partes) >= 7:
                        cod_exer = int(partes[0])
                        cod_licao = int(partes[1])
                        nivel_req = int(partes[2])
                        descricao = partes[3]
                        
                        # Filtra: Só exibe se for da mesma lição (idioma) do aluno e se o nível do exercício for o nível que ele clicou.
                        if nivel_req == nivel_selecionado and cod_licao == int(usu.codigo_idioma):
                            
                            # Se o ID deste exercício já estiver na mochila de 'concluidos', cria o botão desativado.
                            if str(cod_exer) in concluidos:
                                tk.Button(self.container, text=f"[Feito] {descricao}", state="disabled").pack(pady=5)
                            # Se for novo, cria botão clicável que leva para responder a pergunta.
                            else:
                                tk.Button(self.container, text=f"[Jogar] {descricao}", command=lambda c=cod_exer: self.iniciar_exercicio(c)).pack(pady=5)
                            
        tk.Button(self.container, text="Voltar", command=self.mostrar_dashboard_aluno).pack(pady=20)

    # Função onde o aluno responde de fato a questão.
    def iniciar_exercicio(self, id_exercicio):
        self.limpar_tela()
        
        # Busca o exercício completo no TXT usando o ID clicado.
        offset_exer = self.arvore_exercicios.buscar(id_exercicio)
        exer = gerenciador.ler_exercicio_offset(offset_exer) 
        
        # Exibe o texto da pergunta na tela.
        tk.Label(self.container, text=exer.descricao).pack(pady=20)
        
        # Função interna que confere se o botão que o aluno clicou tem o texto igual à resposta correta.
        def checar_resposta(resposta_escolhida):
            # .lower() converte tudo para minúsculo para garantir que não haja erro de letras maiúsculas/minúsculas.
            if resposta_escolhida.lower() == exer.resposta_correta.lower():
                
                # Soma os pontos do exercício nos pontos do aluno.
                self.usuario_logado.pontuacao_total = int(self.usuario_logado.pontuacao_total) + int(exer.pontuacao)
                
                # Adiciona o ID do exercício na string da mochila, separando por traço.
                if hasattr(self.usuario_logado, 'exercicios_concluidos'):
                    if self.usuario_logado.exercicios_concluidos == "":
                        self.usuario_logado.exercicios_concluidos = str(exer.codigo)
                    else:
                        self.usuario_logado.exercicios_concluidos += f"-{exer.codigo}"
                
                # Calcula o nível atual. A cada 100 pontos, ele sobe 1 nível (usando divisão inteira '//').
                novo_nivel = (int(self.usuario_logado.pontuacao_total) // 100) + 1
                mensagem = f"Acertou! Ganhou {exer.pontuacao} XP."
                
                # Se o cálculo resultou num nível maior que o atual dele, ele sobe de nível.
                if novo_nivel > int(self.usuario_logado.nivel_atual):
                    self.usuario_logado.nivel_atual = novo_nivel
                    mensagem += f"\nSubiu para o nível {novo_nivel}!"
                
                messagebox.showinfo("Certo", mensagem)
                
            else:
                # SE ERROU: Calcula 10% do valor da questão para subtrair do usuário.
                penalidade = int(int(exer.pontuacao) * 0.10)
                pontos = int(self.usuario_logado.pontuacao_total)
                
                # A função 'max' impede que a conta fique negativa. Se pontos - penalidade for menor que zero, ele fica com 0.
                self.usuario_logado.pontuacao_total = max(0, pontos - penalidade) 
                
                messagebox.showerror("Erro", f"Errou! Perdeu {penalidade} XP.\nResposta correta: {exer.resposta_correta}")
                
            # Seja erro ou acerto, chamamos a função que vai lá no TXT reescrever a linha dele com o XP atualizado.
            self.atualizar_txt(self.usuario_logado.codigo, apagar=False)
            
            # Devolve o aluno para a tela de escolhas.
            self.mostrar_dashboard_aluno()

        # As opções de resposta vêm do TXT juntas e separadas por uma barra vertical '|'. Aqui dividimos elas.
        opcoes = exer.opcoes_resposta.split("|")
        # Para cada opção dividida, criamos um botão.
        for op in opcoes:
            tk.Button(self.container, text=op, command=lambda o=op: checar_resposta(o)).pack(pady=5)
            
        tk.Button(self.container, text="Pular / Voltar", command=self.mostrar_dashboard_aluno).pack(pady=20)

    # Função que exibe a tela de vitória quando o jogo acaba.
    def mostrar_tela_certificado(self):
        self.limpar_tela()
        tk.Label(self.container, text="CERTIFICADO CONCLUÍDO!").pack(pady=20)
        tk.Label(self.container, text=f"Parabéns, {self.usuario_logado.nome}!").pack(pady=10)
        tk.Label(self.container, text=f"XP Final: {self.usuario_logado.pontuacao_total}").pack(pady=10)
        tk.Button(self.container, text="Sair para o Menu", command=self.mostrar_tela_inicial).pack(pady=20)

    # Função que constrói um Top 5 dos alunos lendo diretamente o arquivo TXT.
    def mostrar_tela_ranking(self):
        self.limpar_tela()
        tk.Label(self.container, text="Ranking de Alunos").pack(pady=20)
        
        if os.path.exists("usuarios.txt"):
            with open("usuarios.txt", "r", encoding="utf-8") as f:
                linhas = f.readlines() # Lê todas as linhas do banco.
            
            lista = []
            for linha in linhas:
                partes = linha.strip().split(",")
                # Verifica se a linha tem o mínimo de dados esperado para evitar erros.
                if len(partes) >= 5:
                    # Adiciona à 'lista' uma tupla contendo o Nome e convertendo o XP para inteiro.
                    lista.append((partes[1], int(partes[4]))) 
            
            # Ordena a lista usando o XP (x[1]) como base, e 'reverse=True' coloca do maior para o menor.
            lista.sort(key=lambda x: x[1], reverse=True)
            
            # Mostra apenas os 5 primeiros da lista usando um laço com contador 'i'.
            for i, (nome, pontos) in enumerate(lista[:5]): 
                tk.Label(self.container, text=f"{i+1}º lugar: {nome} - {pontos} XP").pack(pady=2)
        
        tk.Button(self.container, text="Voltar", command=self.mostrar_tela_inicial).pack(pady=20)

    # Função que exibe a tela de remoção de cadastro.
    def mostrar_tela_remover(self):
        self.limpar_tela()
        tk.Label(self.container, text="Apagar Conta").pack(pady=20)
        
        tk.Label(self.container, text="ID para apagar:").pack()
        entry_id = tk.Entry(self.container)
        entry_id.pack(pady=5)
        
        def apagar():
            try:
                codigo = int(entry_id.get())
                
                # Checa na árvore se esse ID está cadastrado.
                if self.arvore_usuarios.buscar(codigo) is None:
                    messagebox.showerror("Erro", "ID não encontrado!")
                    return
                
                # Cria um pop-up com botões de Sim e Não.
                if messagebox.askyesno("Confirmação", "Apagar aluno definitivamente?"):
                    # Se clicou "Sim", chama a função de atualizar txt com a ordem de apagar (apagar=True).
                    self.atualizar_txt(codigo, apagar=True) 
                    messagebox.showinfo("Sucesso", "Conta apagada.")
                    self.mostrar_tela_inicial()
            except ValueError:
                messagebox.showerror("Erro", "Digite um número.")

        tk.Button(self.container, text="Confirmar Exclusão", command=apagar).pack(pady=10)
        tk.Button(self.container, text="Voltar", command=self.mostrar_tela_inicial).pack(pady=5)

# Este bloco verifica se este é o arquivo principal rodando. 
# Se for, ele cria a janela do tkinter, entrega pra nossa classe controlar, e mantém a janela aberta no loop.
if __name__ == "__main__":
    janela = tk.Tk()
    app = MaxLanguageApp(janela)
    janela.mainloop()
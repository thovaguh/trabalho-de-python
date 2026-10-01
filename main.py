import tkinter as tk
from tkinter import messagebox
import os
from modelos import Idioma, Licao, Exercicio, Usuario
from arvore import ArvoreBinaria
import gerenciador

# =======================================================
# 1. CONFIGURAÇÃO INICIAL E VARIÁVEIS GLOBAIS
# =======================================================
# Aqui criamos a janela principal do aplicativo e definimos seu tamanho.
janela = tk.Tk()
janela.title("MaxLanguage")
janela.geometry("400x500")

# O container é uma caixa invisível onde vamos colocar e tirar os botões.
container = tk.Frame(janela)
container.pack(fill="both", expand=True)

# Criamos as Árvores Binárias vazias na memória RAM.
arvore_idiomas = ArvoreBinaria()
arvore_licoes = ArvoreBinaria()
arvore_exercicios = ArvoreBinaria()
arvore_usuarios = ArvoreBinaria()

# Variável global que vai guardar os dados do aluno quando ele fizer login.
usuario_logado = None 

# =======================================================
# 2. FUNÇÕES DE PREPARAÇÃO DOS DADOS
# =======================================================
def carregar_dados_do_disco_para_memoria():
    # Lê os arquivos .txt (disco) e anota a posição de cada item nas árvores (memória)
    gerenciador.carregar_indices_idiomas(arvore_idiomas)
    gerenciador.carregar_indices_licoes(arvore_licoes)
    gerenciador.carregar_indices_exercicios(arvore_exercicios)
    gerenciador.carregar_indices_usuarios(arvore_usuarios)

def inicializar_banco_padrao():
    # Cria Inglês (1) e Espanhol (2) no sistema caso o arquivo txt esteja vazio.
    if arvore_idiomas.buscar(1) is None:
        arvore_idiomas.inserir(1, gerenciador.salvar_idioma(Idioma(1, "Inglês")))
    if arvore_idiomas.buscar(2) is None:
        arvore_idiomas.inserir(2, gerenciador.salvar_idioma(Idioma(2, "Espanhol")))
    
    if arvore_licoes.buscar(1) is None:
        arvore_licoes.inserir(1, gerenciador.salvar_licao(Licao(1, 1, 5))) 
    if arvore_licoes.buscar(2) is None:
        arvore_licoes.inserir(2, gerenciador.salvar_licao(Licao(2, 2, 5)))

# aqui temos o container que é a caixa criada para segurar os textos na tela, o .winfo é uma função do tkinter
#que pega o texto que se encontra no container
#o for widget é um loop que vai pegar as listar geradas e vai percorrer uma por uma
#o widget destroy serve para apagar o elemento da memoria ram
def limpar_tela():
    for widget in container.winfo_children():
        widget.destroy()

# =======================================================
# 3. FUNÇÕES DE MANIPULAÇÃO DO ARQUIVO TXT
# =======================================================
def salvar_novo_usuario_no_txt(novo_usuario):
    # Abre o arquivo em modo "a" (adicionar) e escreve os dados no final.
    with open("usuarios.txt", "a", encoding="utf-8") as f:
        # Pega os exercícios concluídos ou deixa vazio se não tiver.
        mochila = getattr(novo_usuario, 'exercicios_concluidos', "")
        #aq o f serve para vc conseguir usar a virgla e outros tipos de string para poder armazenas no txt
        f.write(f"{novo_usuario.codigo},{novo_usuario.nome},{novo_usuario.codigo_idioma},{novo_usuario.nivel_atual},{novo_usuario.pontuacao_total},{mochila}\n")
    
    # Recarrega a árvore para ela saber que tem um aluno novo.
    global arvore_usuarios
    arvore_usuarios = ArvoreBinaria()
    gerenciador.carregar_indices_usuarios(arvore_usuarios)

def atualizar_ou_apagar_usuario_no_txt(codigo_usuario, apagar=False):
    global usuario_logado
    global arvore_usuarios
    
    if not os.path.exists("usuarios.txt"): return
    
    # Lê todas as linhas do arquivo e guarda na memória.
    with open("usuarios.txt", "r", encoding="utf-8") as f:
        linhas = f.readlines()
    
    # Abre o arquivo em modo "w" (escrever por cima) para criar um arquivo limpo.
    with open("usuarios.txt", "w", encoding="utf-8") as f:
        for linha in linhas:
            dados = linha.strip().split(",") # Separa os dados pela vírgula
           # o strip() serve para limpar a sujidade do final, como os \n
            # o split(",") serve como tesoura para cortar a frase nas vírgulas e separar os dados
                        
            # Se achou a linha do usuário que queremos modificar...
            if dados and dados[0] == str(codigo_usuario):
                if apagar == True:
                    continue # Pula a linha (o que faz com que ela seja apagada do arquivo).
                else:
                    # Escreve a linha novamente, mas com XP e Nível atualizados.
                    mochila = getattr(usuario_logado, 'exercicios_concluidos', "")
                    f.write(f"{usuario_logado.codigo},{usuario_logado.nome},{usuario_logado.codigo_idioma},{usuario_logado.nivel_atual},{int(usuario_logado.pontuacao_total)},{mochila}\n")
            else:
                f.write(linha) # Mantém as linhas dos outros usuários intactas.
                
    # Recarrega a árvore de usuários.
    arvore_usuarios = ArvoreBinaria()
    gerenciador.carregar_indices_usuarios(arvore_usuarios)

# =======================================================
# 4. TELAS DA INTERFACE GRÁFICA
# =======================================================
def mostrar_tela_inicial():
    limpar_tela()
    tk.Label(container, text="Menu Principal - MaxLanguage").pack(pady=20)
    
    # Botões do menu chamando as funções correspondentes.
    tk.Button(container, text="Criar Conta", command=mostrar_tela_matricula).pack(pady=5)
    tk.Button(container, text="Fazer Login", command=mostrar_tela_login).pack(pady=5)
    tk.Button(container, text="Ver Ranking", command=mostrar_tela_ranking).pack(pady=5)
    tk.Button(container, text="Apagar Conta", command=mostrar_tela_remover).pack(pady=5)
    tk.Button(container, text="Sair do Jogo", command=janela.quit).pack(pady=20)

def mostrar_tela_matricula():
    limpar_tela()
    tk.Label(container, text="Cadastro de Aluno").pack(pady=20)
    #o entry serve para criar uma caixa de texto para o usuario digitar, e o pack serve para colocar na tela
    tk.Label(container, text="ID (número):").pack()
    entry_id = tk.Entry(container)
    entry_id.pack(pady=5)
    
    tk.Label(container, text="Nome:").pack()
    entry_nome = tk.Entry(container)
    entry_nome.pack(pady=5)
    
    tk.Label(container, text="Idioma (1-Inglês | 2-Espanhol):").pack()
    entry_idioma = tk.Entry(container)
    entry_idioma.pack(pady=5)
    
    def salvar():
        try:
            codigo = int(entry_id.get())
            nome = entry_nome.get()
            cod_idioma = int(entry_idioma.get())
            
            if arvore_usuarios.buscar(codigo) is not None:
                messagebox.showerror("Erro", "ID já existe!")
                return
            if arvore_idiomas.buscar(cod_idioma) is None:
                messagebox.showerror("Erro", "Idioma inválido!")
                return
            
            try:
                novo_usu = Usuario(codigo, nome, cod_idioma, 1, 0, "")
            except TypeError:
                novo_usu = Usuario(codigo, nome, cod_idioma, 1, 0)
                
            salvar_novo_usuario_no_txt(novo_usu)
            #o messagebox serve para criar uma caixa de mensagem de popup na tela, e o showinfo serve para mostrar uma mensagem de sucesso
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            mostrar_tela_inicial()
        except ValueError:
            messagebox.showerror("Erro", "Use números no ID e Idioma.")

    tk.Button(container, text="Salvar", command=salvar).pack(pady=10)
    tk.Button(container, text="Voltar", command=mostrar_tela_inicial).pack(pady=5)

def mostrar_tela_login():
    limpar_tela()
    tk.Label(container, text="Login").pack(pady=20)
    #o tk.label serve para criar um texto na tela, e o pack serve para colocar na tela
    tk.Label(container, text="Digite seu ID:").pack()
    entry_id = tk.Entry(container)
    entry_id.pack(pady=5)
    
    def logar():
        global usuario_logado # Avisa o Python que vamos alterar a variável global
        try:
            id_usu = int(entry_id.get())
            offset = arvore_usuarios.buscar(id_usu) # Procura onde o ID está no txt
            
            if offset is None:
                messagebox.showerror("Erro", "Aluno não encontrado!")
                return
                
            usuario_logado = gerenciador.ler_usuario_offset(offset)
            mostrar_dashboard_aluno()
        except ValueError:
            messagebox.showerror("Erro", "Digite um número.")

    tk.Button(container, text="Entrar", command=logar).pack(pady=10)
    tk.Button(container, text="Voltar", command=mostrar_tela_inicial).pack(pady=5)

def mostrar_dashboard_aluno():
    limpar_tela()
    global usuario_logado
    
    # Verifica se o aluno já passou do total de níveis daquele idioma
    offset_licao = arvore_licoes.buscar(int(usuario_logado.codigo_idioma))
    if offset_licao is not None:
        licao = gerenciador.ler_licao_offset(offset_licao)
        total_niveis = int(licao.niveis_total) 
        
        if int(usuario_logado.nivel_atual) > total_niveis:
            mostrar_tela_certificado()
            return
    
    tk.Label(container, text=f"Aluno: {usuario_logado.nome} | Nível: {usuario_logado.nivel_atual} | XP: {usuario_logado.pontuacao_total}").pack(pady=20)
    tk.Label(container, text="Escolha a fase:").pack()
    
    # Gera os botões dos níveis
    for n in range(1, int(usuario_logado.nivel_atual) + 1):
        # O comando lambda é usado para "lembrar" qual o número da fase o botão representa.
        tk.Button(container, text=f"Nível {n}", command=lambda lvl=n: mostrar_tela_exercicios(lvl)).pack(pady=5)
                        
    tk.Button(container, text="Sair da Conta", command=mostrar_tela_inicial).pack(pady=20)

def mostrar_tela_exercicios(nivel_selecionado):
    limpar_tela()
    global usuario_logado
    
    tk.Label(container, text=f"Exercícios do Nível {nivel_selecionado}").pack(pady=20)
    concluidos = getattr(usuario_logado, 'exercicios_concluidos', "").split("-")
    
    if os.path.exists("exercicios.txt"):
        with open("exercicios.txt", "r", encoding="utf-8") as arq:
            for linha in arq:
                partes = linha.strip().split(",")
                #o len serve para contar quantos elementos tem na lista, e o if len(partes) >= 7 serve para verificar se a linha tem todos os dados necessários
                if len(partes) >= 7:
                    cod_exer = int(partes[0])
                    cod_licao = int(partes[1])
                    nivel_req = int(partes[2])
                    descricao = partes[3]
                    
                    if nivel_req == nivel_selecionado and cod_licao == int(usuario_logado.codigo_idioma):
                        if str(cod_exer) in concluidos:
                            tk.Button(container, text=f"[Feito] {descricao}", state="disabled").pack(pady=5)
                        else:
                            tk.Button(container, text=f"[Jogar] {descricao}", command=lambda c=cod_exer: iniciar_exercicio(c)).pack(pady=5)
                        
    tk.Button(container, text="Voltar", command=mostrar_dashboard_aluno).pack(pady=20)

def iniciar_exercicio(id_exercicio):
    limpar_tela()
    global usuario_logado
    
    offset_exer = arvore_exercicios.buscar(id_exercicio)
    exer = gerenciador.ler_exercicio_offset(offset_exer) 
    
    tk.Label(container, text=exer.descricao).pack(pady=20)
    
    def checar_resposta(resposta_escolhida):
        if resposta_escolhida.lower() == exer.resposta_correta.lower():
            # Acertou
            usuario_logado.pontuacao_total = int(usuario_logado.pontuacao_total) + int(exer.pontuacao)
            
            if hasattr(usuario_logado, 'exercicios_concluidos'):
                if usuario_logado.exercicios_concluidos == "":
                    usuario_logado.exercicios_concluidos = str(exer.codigo)
                else:
                    usuario_logado.exercicios_concluidos += f"-{exer.codigo}"
            
            novo_nivel = (int(usuario_logado.pontuacao_total) // 100) + 1
            mensagem = f"Acertou! Ganhou {exer.pontuacao} XP."
            
            if novo_nivel > int(usuario_logado.nivel_atual):
                usuario_logado.nivel_atual = novo_nivel
                mensagem += f"\nSubiu para o nível {novo_nivel}!"
            
            messagebox.showinfo("Certo", mensagem)
        else:
            # Errou
            penalidade = int(int(exer.pontuacao) * 0.10)
            pontos = int(usuario_logado.pontuacao_total)
            usuario_logado.pontuacao_total = max(0, pontos - penalidade) 
            
            messagebox.showerror("Erro", f"Errou! Perdeu {penalidade} XP.\nResposta correta: {exer.resposta_correta}")
            
        atualizar_ou_apagar_usuario_no_txt(usuario_logado.codigo, apagar=False)
        mostrar_dashboard_aluno()

    opcoes = exer.opcoes_resposta.split("|")
    for op in opcoes:
        tk.Button(container, text=op, command=lambda o=op: checar_resposta(o)).pack(pady=5)
        
    tk.Button(container, text="Voltar", command=mostrar_dashboard_aluno).pack(pady=20)

def mostrar_tela_certificado():
    limpar_tela()
    global usuario_logado
    tk.Label(container, text="CERTIFICADO CONCLUÍDO!").pack(pady=20)
    tk.Label(container, text=f"Parabéns, {usuario_logado.nome}!").pack(pady=10)
    tk.Label(container, text=f"XP Final: {usuario_logado.pontuacao_total}").pack(pady=10)
    tk.Button(container, text="Sair para o Menu", command=mostrar_tela_inicial).pack(pady=20)

def mostrar_tela_ranking():
    limpar_tela()
    tk.Label(container, text="Ranking de Alunos").pack(pady=20)
    
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
        
        lista = []
        for linha in linhas:
            partes = linha.strip().split(",")
            if len(partes) >= 5:
                lista.append((partes[1], int(partes[4]))) 
        
        # sort=Ordena do maior XP para o menor XP   o x[1] é o x da linha (aluno, xp). entao faz o sort ordenar por xp
        lista.sort(key=lambda x: x[1], reverse=True)#usa o reverse pq o sort ordena do menor para o maior, e o reverse inverte a ordem
        
        for i, (nome, pontos) in enumerate(lista[:5]): 
            tk.Label(container, text=f"{i+1}º lugar: {nome} - {pontos} XP").pack(pady=2)
    
    tk.Button(container, text="Voltar", command=mostrar_tela_inicial).pack(pady=20)

def mostrar_tela_remover():
    limpar_tela()
    tk.Label(container, text="Apagar Conta").pack(pady=20)
    
    tk.Label(container, text="ID para apagar:").pack()
    entry_id = tk.Entry(container)
    entry_id.pack(pady=5)
    
    def apagar():
        try:
            codigo = int(entry_id.get())
            if arvore_usuarios.buscar(codigo) is None:
                messagebox.showerror("Erro", "ID não encontrado!")
                return

            #askysno cria uma pegunta de sim ou nao, e se o usuario clicar em sim, ele vai apagar a conta
            if messagebox.askyesno("Confirmação", "Apagar aluno definitivamente?"):
                atualizar_ou_apagar_usuario_no_txt(codigo, apagar=True) 
                messagebox.showinfo("Sucesso", "Conta apagada.")
                mostrar_tela_inicial()
        except ValueError:
            messagebox.showerror("Erro", "Digite um número.")

    tk.Button(container, text="Confirmar Exclusão", command=apagar).pack(pady=10)
    tk.Button(container, text="Voltar", command=mostrar_tela_inicial).pack(pady=5)


# =======================================================
# 5. INICIALIZAÇÃO DO PROGRAMA
# =======================================================
# Estas três linhas são as que realmente dão o "start" no programa.
carregar_dados_do_disco_para_memoria()
inicializar_banco_padrao()
mostrar_tela_inicial()

# Mantém a janela aberta esperando o usuário clicar em algo.
janela.mainloop()
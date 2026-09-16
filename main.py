import tkinter as tk
from tkinter import messagebox
import os
from modelos import Idioma, Licao, Exercicio, Usuario
from arvore import ArvoreBinaria
import gerenciador 

# CORES TEMA DUOLINGO
DUO_BG = "#ffffff"       
DUO_GREEN = "#58cc02"    
DUO_BLUE = "#1cb0f6"     
DUO_RED = "#ff4b4b"      
DUO_GRAY = "#e5e5e5"     
DUO_DARK = "#4b4b4b"     
DUO_GOLD = "#ffc800"     

def inicializar_banco_padrao(arvore_idiomas, arvore_exercicios, arvore_licoes):
    if arvore_idiomas.buscar(1) is None:
        arvore_idiomas.inserir(1, gerenciador.salvar_idioma(Idioma(1, "Inglês")))
    if arvore_idiomas.buscar(2) is None:
        arvore_idiomas.inserir(2, gerenciador.salvar_idioma(Idioma(2, "Espanhol")))
    if arvore_licoes.buscar(1) is None:
        arvore_licoes.inserir(1, gerenciador.salvar_licao(Licao(1, 1, 5))) 
    if arvore_licoes.buscar(2) is None:
        arvore_licoes.inserir(2, gerenciador.salvar_licao(Licao(2, 2, 5)))

class MaxLanguageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MAXLanguage - Learn & Play")
        self.root.geometry("600x600")
        self.root.configure(bg=DUO_BG)
        
        # Inicia o Banco de Dados
        self.arvore_idiomas = ArvoreBinaria()
        self.arvore_licoes = ArvoreBinaria()
        self.arvore_exercicios = ArvoreBinaria()
        self.arvore_usuarios = ArvoreBinaria()
        
        gerenciador.carregar_indices_idiomas(self.arvore_idiomas)
        gerenciador.carregar_indices_licoes(self.arvore_licoes)
        gerenciador.carregar_indices_exercicios(self.arvore_exercicios)
        gerenciador.carregar_indices_usuarios(self.arvore_usuarios)
        
        inicializar_banco_padrao(self.arvore_idiomas, self.arvore_exercicios, self.arvore_licoes)
        self.usuario_logado = None
        
        self.container = tk.Frame(self.root, bg=DUO_BG)
        self.container.pack(fill="both", expand=True)
        
        self.mostrar_tela_inicial()

    def limpar_tela(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_tela_inicial(self):
        self.limpar_tela()
        tk.Label(self.container, text="maxlanguage", font=("Arial Rounded MT Bold", 32, "bold"), fg=DUO_GREEN, bg=DUO_BG).pack(pady=40)
        
        tk.Button(self.container, text="JÁ TENHO UMA CONTA", font=("Arial", 12, "bold"), width=30, height=2, bg=DUO_BLUE, fg="white", relief="flat", command=self.mostrar_tela_login).pack(pady=10)
        tk.Button(self.container, text="COMEÇAR AGORA", font=("Arial", 12, "bold"), width=30, height=2, bg=DUO_GREEN, fg="white", relief="flat", command=self.mostrar_tela_matricula).pack(pady=10)
        tk.Button(self.container, text="REMOVER ALUNO", font=("Arial", 12, "bold"), width=30, height=2, bg=DUO_RED, fg="white", relief="flat", command=self.mostrar_tela_remover).pack(pady=10)
        
        tk.Button(self.container, text="SAIR DO JOGO", font=("Arial", 10, "bold"), width=30, bg=DUO_GRAY, fg=DUO_DARK, relief="flat", command=self.root.quit).pack(pady=30)

    def mostrar_tela_matricula(self):
        self.limpar_tela()
        tk.Label(self.container, text="Crie seu Perfil", font=("Arial Rounded MT Bold", 20, "bold"), fg=DUO_DARK, bg=DUO_BG).pack(pady=20)
        
        tk.Label(self.container, text="Escolha um ID (número):", fg=DUO_DARK, bg=DUO_BG, font=("Arial", 12, "bold")).pack()
        entry_id = tk.Entry(self.container, font=("Arial", 14), bg="#f7f7f7", relief="solid")
        entry_id.pack(pady=5)
        
        tk.Label(self.container, text="Qual o seu nome?:", fg=DUO_DARK, bg=DUO_BG, font=("Arial", 12, "bold")).pack()
        entry_nome = tk.Entry(self.container, font=("Arial", 14), bg="#f7f7f7", relief="solid")
        entry_nome.pack(pady=5)
        
        tk.Label(self.container, text="O que quer aprender?\n(1 - Inglês | 2 - Espanhol)", fg=DUO_DARK, bg=DUO_BG, font=("Arial", 12, "bold")).pack(pady=10)
        entry_idioma = tk.Entry(self.container, font=("Arial", 14), bg="#f7f7f7", relief="solid")
        entry_idioma.pack(pady=5)
        
        def salvar_matricula():
            try:
                codigo = int(entry_id.get())
                nome = entry_nome.get()
                cod_idioma = int(entry_idioma.get())
                
                if self.arvore_usuarios.buscar(codigo) is not None:
                    messagebox.showerror("Oops!", "Este ID já está em uso!")
                    return
                if self.arvore_idiomas.buscar(cod_idioma) is None:
                    messagebox.showerror("Oops!", "Idioma inválido! Use 1 ou 2.")
                    return
                
                # Defesa: Tenta salvar com o campo de mochilas, se falhar salva normal
                try:
                    novo_usu = Usuario(codigo, nome, cod_idioma, 1, 0, "")
                except TypeError:
                    novo_usu = Usuario(codigo, nome, cod_idioma, 1, 0)
                    
                offset = gerenciador.salvar_usuario(novo_usu)
                self.arvore_usuarios.inserir(codigo, offset)
                
                messagebox.showinfo("Sucesso!", f"Tudo pronto, {nome}!\nVocê vai começar no Nível 1.")
                self.mostrar_tela_inicial()
            except ValueError:
                messagebox.showerror("Erro", "Preencha os campos com números onde for pedido!")

        tk.Button(self.container, text="SALVAR", font=("Arial", 12, "bold"), bg=DUO_GREEN, fg="white", relief="flat", width=25, height=2, command=salvar_matricula).pack(pady=20)
        tk.Button(self.container, text="VOLTAR", font=("Arial", 10, "bold"), command=self.mostrar_tela_inicial, relief="flat", bg=DUO_GRAY, fg=DUO_DARK, width=25).pack()

    def mostrar_tela_login(self):
        self.limpar_tela()
        tk.Label(self.container, text="Bem-vindo de volta!", font=("Arial Rounded MT Bold", 20, "bold"), fg=DUO_DARK, bg=DUO_BG).pack(pady=40)
        tk.Label(self.container, text="Digite seu ID de aluno:", fg=DUO_DARK, bg=DUO_BG, font=("Arial", 12, "bold")).pack(pady=5)
        
        entry_id = tk.Entry(self.container, font=("Arial", 16), justify="center", bg="#f7f7f7", relief="solid")
        entry_id.pack(pady=10)
        
        def tentar_logar():
            try:
                id_usu = int(entry_id.get())
                offset = self.arvore_usuarios.buscar(id_usu)
                if offset is None:
                    messagebox.showerror("Oops!", "Aluno não encontrado! Você já criou uma conta?")
                    return
                    
                usu = gerenciador.ler_usuario_offset(offset)
                if int(usu.nivel_atual) == -1:
                    messagebox.showerror("Acesso Negado", "Esta conta foi inativada.")
                    return
                    
                self.usuario_logado = usu
                self.mostrar_dashboard_aluno()
            except ValueError:
                messagebox.showerror("Erro", "O ID precisa ser um número!")

        tk.Button(self.container, text="ENTRAR", font=("Arial", 12, "bold"), bg=DUO_BLUE, fg="white", relief="flat", command=tentar_logar, width=20, height=2).pack(pady=20)
        tk.Button(self.container, text="VOLTAR", font=("Arial", 10, "bold"), command=self.mostrar_tela_inicial, relief="flat", bg=DUO_GRAY, fg=DUO_DARK, width=20).pack()

    def mostrar_dashboard_aluno(self):
        self.limpar_tela()
        usu = self.usuario_logado
        
        frame_status = tk.Frame(self.container, bg=DUO_BG, pady=10)
        frame_status.pack(fill="x")
        tk.Label(frame_status, text=f"🔥 {usu.nome}   |   ⭐ Nível: {usu.nivel_atual}   |   🏆 {usu.pontuacao_total} XP", font=("Arial", 14, "bold"), fg=DUO_GOLD, bg=DUO_BG).pack()
        
        tk.Label(self.container, text="SUA JORNADA", font=("Arial Rounded MT Bold", 18, "bold"), fg=DUO_DARK, bg=DUO_BG).pack(pady=20)
        
        # Botões de fases
        for n in range(1, int(usu.nivel_atual) + 1):
            btn = tk.Button(self.container, text=f"NÍVEL {n}", font=("Arial", 14, "bold"), bg=DUO_GREEN, fg="white", relief="flat", width=25, height=2, command=lambda lvl=n: self.mostrar_tela_exercicios_por_nivel(lvl))
            btn.pack(pady=5)
                            
        tk.Button(self.container, text="SAIR", font=("Arial", 10, "bold"), bg=DUO_GRAY, fg=DUO_DARK, relief="flat", command=self.mostrar_tela_inicial, width=15).pack(pady=30)

    def mostrar_tela_exercicios_por_nivel(self, nivel_selecionado):
        self.limpar_tela()
        usu = self.usuario_logado
        
        tk.Label(self.container, text=f"MISSÕES DO NÍVEL {nivel_selecionado}", font=("Arial Rounded MT Bold", 18, "bold"), fg=DUO_DARK, bg=DUO_BG).pack(pady=20)
        frame_lista = tk.Frame(self.container, bg=DUO_BG)
        frame_lista.pack(fill="both", expand=True, padx=40)
        
        # Resgata de forma segura os exercícios que já foram feitos
        concluidos = getattr(usu, 'exercicios_concluidos', "").split("-")
        
        if os.path.exists("exercicios.txt"):
            with open("exercicios.txt", "r", encoding="utf-8") as arq:
                for linha in arq:
                    partes = linha.strip().split(",")
                    if len(partes) >= 7:
                        cod_exer, cod_licao, nivel_req, descricao = int(partes[0]), int(partes[1]), int(partes[2]), partes[3]
                        
                        if nivel_req == nivel_selecionado and cod_licao == int(usu.codigo_idioma):
                            # Se já foi feito, bloqueia o botão!
                            if str(cod_exer) in concluidos:
                                btn = tk.Button(frame_lista, text=f"✅ {descricao}", font=("Arial", 12, "bold"), bg=DUO_GRAY, fg="#a0a0a0", relief="flat", anchor="w", state="disabled")
                            else:
                                btn = tk.Button(frame_lista, text=f"⭐ {descricao}", font=("Arial", 12, "bold"), bg=DUO_BLUE, fg="white", relief="flat", anchor="w", command=lambda c=cod_exer: self.iniciar_exercicio(c))
                            btn.pack(fill="x", pady=5)
                            
        tk.Button(self.container, text="VOLTAR", font=("Arial", 10, "bold"), bg=DUO_GRAY, fg=DUO_DARK, relief="flat", command=self.mostrar_dashboard_aluno, width=15).pack(pady=20)

    def iniciar_exercicio(self, id_exercicio):
        self.limpar_tela()
        offset_exer = self.arvore_exercicios.buscar(id_exercicio)
        exer = gerenciador.ler_exercicio_offset(offset_exer)
        
        tk.Label(self.container, text="TRADUZA OU RESPONDA", font=("Arial Rounded MT Bold", 14, "bold"), fg=DUO_DARK, bg=DUO_BG).pack(pady=10)
        tk.Label(self.container, text=exer.descricao, font=("Arial", 18, "bold"), fg=DUO_BLUE, bg=DUO_BG, wraplength=500).pack(pady=20)
        
        def checar_resposta(resposta_escolhida):
            if resposta_escolhida.lower() == exer.resposta_correta.lower():
                self.usuario_logado.pontuacao_total = int(self.usuario_logado.pontuacao_total) + int(exer.pontuacao)
                
                # Salva a mochila (defensivo)
                if hasattr(self.usuario_logado, 'exercicios_concluidos'):
                    if self.usuario_logado.exercicios_concluidos == "":
                        self.usuario_logado.exercicios_concluidos = str(exer.codigo)
                    else:
                        self.usuario_logado.exercicios_concluidos += f"-{exer.codigo}"
                
                novo_nivel = (self.usuario_logado.pontuacao_total // 100) + 1
                mensagem = "Incível! Você acertou! +10 XP"
                
                if novo_nivel > int(self.usuario_logado.nivel_atual):
                    self.usuario_logado.nivel_atual = novo_nivel
                    mensagem += f"\n\n🎉 LEVEL UP! Você desbloqueou o NÍVEL {novo_nivel}!"
                
                novo_offset = gerenciador.salvar_usuario(self.usuario_logado)
                self.arvore_usuarios.inserir(self.usuario_logado.codigo, novo_offset)
                messagebox.showinfo("Excelente!", mensagem)
            else:
                messagebox.showerror("Puxa vida!", f"Resposta Incorreta.\nA correta era: {exer.resposta_correta}")
                
            self.mostrar_dashboard_aluno()

        for op in exer.opcoes_resposta.split("|"):
            tk.Button(self.container, text=op, font=("Arial", 14, "bold"), bg=DUO_BG, fg=DUO_DARK, relief="solid", bd=2, height=2, command=lambda o=op: checar_resposta(o)).pack(fill="x", padx=60, pady=8)
            
        tk.Button(self.container, text="PULAR", font=("Arial", 10, "bold"), bg=DUO_GRAY, fg=DUO_DARK, relief="flat", command=self.mostrar_dashboard_aluno, width=15).pack(pady=30)

    def mostrar_tela_remover(self):
        self.limpar_tela()
        tk.Label(self.container, text="Área de Risco", font=("Arial Rounded MT Bold", 20, "bold"), fg=DUO_RED, bg=DUO_BG).pack(pady=40)
        tk.Label(self.container, text="ID do aluno para exclusão:", fg=DUO_DARK, bg=DUO_BG, font=("Arial", 12, "bold")).pack(pady=5)
        
        entry_id = tk.Entry(self.container, font=("Arial", 14), bg="#f7f7f7", relief="solid")
        entry_id.pack(pady=10)
        
        def deletar_aluno():
            try:
                codigo = int(entry_id.get())
                offset = self.arvore_usuarios.buscar(codigo)
                
                if offset is None:
                    messagebox.showerror("Erro", "ID não encontrado!")
                    return
                    
                usu = gerenciador.ler_usuario_offset(offset)
                
                if int(usu.nivel_atual) == -1:
                    messagebox.showerror("Erro", "Esta conta já foi excluída!")
                    return
                
                confirmacao = messagebox.askyesno("Cuidado!", f"Você vai perder todo o progresso de '{usu.nome}'.\nTem certeza disso?")
                
                if confirmacao:
                    usu.nivel_atual = -1 
                    novo_offset = gerenciador.salvar_usuario(usu)
                    self.arvore_usuarios.inserir(usu.codigo, novo_offset)
                    messagebox.showinfo("Deletado", "Conta removida para sempre.")
                    self.mostrar_tela_inicial()
                    
            except ValueError:
                messagebox.showerror("Erro", "Digite apenas números.")

        tk.Button(self.container, text="EXCLUIR CONTA", font=("Arial", 12, "bold"), bg=DUO_RED, fg="white", relief="flat", command=deletar_aluno, width=20, height=2).pack(pady=20)
        tk.Button(self.container, text="VOLTAR", font=("Arial", 10, "bold"), command=self.mostrar_tela_inicial, bg=DUO_GRAY, fg=DUO_DARK, relief="flat", width=20).pack()

if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = MaxLanguageApp(janela_principal)
    janela_principal.mainloop()
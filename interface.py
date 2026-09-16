import tkinter as tk
from tkinter import messagebox
import os
from modelos import Usuario
import gerenciador 

class MaxLanguageApp:
    def __init__(self, root, arvore_idiomas, arvore_licoes, arvore_exercicios, arvore_usuarios):
        self.root = root
        self.root.title("MAXLanguage Platform")
        self.root.geometry("600x550")
        self.root.configure(bg="#2c3e50")
        
        self.arvore_idiomas = arvore_idiomas
        self.arvore_licoes = arvore_licoes
        self.arvore_exercicios = arvore_exercicios
        self.arvore_usuarios = arvore_usuarios
        
        self.usuario_logado = None
        
        self.container = tk.Frame(self.root, bg="#2c3e50")
        self.container.pack(fill="both", expand=True)
        
        self.mostrar_tela_inicial()

    def limpar_tela(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # --- TELA 1: MENU PRINCIPAL ---
    def mostrar_tela_inicial(self):
        self.limpar_tela()
        tk.Label(self.container, text="MAXLANGUAGE", font=("Arial", 26, "bold"), fg="#f1c40f", bg="#2c3e50").pack(pady=40)
        
        tk.Button(self.container, text="1. Entrar (Sessão de Estudos)", font=("Arial", 14), width=30, bg="#3498db", fg="white", command=self.mostrar_tela_login).pack(pady=10)
        tk.Button(self.container, text="2. Matricular Novo Aluno", font=("Arial", 14), width=30, bg="#2ecc71", fg="white", command=self.mostrar_tela_matricula).pack(pady=10)
        tk.Button(self.container, text="3. Remover Aluno", font=("Arial", 14), width=30, bg="#e67e22", fg="white", command=self.mostrar_tela_remover).pack(pady=10)
        tk.Button(self.container, text="0. Sair", font=("Arial", 14), width=30, bg="#e74c3c", fg="white", command=self.root.quit).pack(pady=20)

    # --- TELA 2: MATRÍCULA ---
    def mostrar_tela_matricula(self):
        self.limpar_tela()
        tk.Label(self.container, text="Matrícula de Aluno", font=("Arial", 20, "bold"), fg="white", bg="#2c3e50").pack(pady=20)
        
        tk.Label(self.container, text="Crie um ID numérico:", fg="white", bg="#2c3e50", font=("Arial", 12)).pack()
        entry_id = tk.Entry(self.container, font=("Arial", 12))
        entry_id.pack(pady=5)
        
        tk.Label(self.container, text="Seu Nome:", fg="white", bg="#2c3e50", font=("Arial", 12)).pack()
        entry_nome = tk.Entry(self.container, font=("Arial", 12))
        entry_nome.pack(pady=5)
        
        tk.Label(self.container, text="Idioma (1-Inglês | 2-Espanhol):", fg="white", bg="#2c3e50", font=("Arial", 12)).pack()
        entry_idioma = tk.Entry(self.container, font=("Arial", 12))
        entry_idioma.pack(pady=5)
        
        def salvar_matricula():
            try:
                codigo = int(entry_id.get())
                nome = entry_nome.get()
                cod_idioma = int(entry_idioma.get())
                
                if self.arvore_usuarios.buscar(codigo) is not None:
                    messagebox.showerror("Erro", "Este ID já está em uso!")
                    return
                if self.arvore_idiomas.buscar(cod_idioma) is None:
                    messagebox.showerror("Erro", "Idioma inválido! Use 1 ou 2.")
                    return
                    
                novo_usu = Usuario(codigo, nome, cod_idioma, 1, 0)
                offset = gerenciador.salvar_usuario(novo_usu)
                self.arvore_usuarios.inserir(codigo, offset)
                
                messagebox.showinfo("Sucesso", f"Bem-vindo(a), {nome}! Você está no Nível 1.")
                self.mostrar_tela_inicial()
            except ValueError:
                messagebox.showerror("Erro", "Preencha os campos corretamente!")

        tk.Button(self.container, text="Salvar Matrícula", font=("Arial", 12), bg="#2ecc71", fg="white", command=salvar_matricula, width=20).pack(pady=20)
        tk.Button(self.container, text="Voltar", font=("Arial", 12), command=self.mostrar_tela_inicial, width=20).pack()

    # --- TELA 3: LOGIN ---
    def mostrar_tela_login(self):
        self.limpar_tela()
        tk.Label(self.container, text="Acesso do Aluno", font=("Arial", 20, "bold"), fg="white", bg="#2c3e50").pack(pady=40)
        tk.Label(self.container, text="Digite seu ID de aluno:", fg="white", bg="#2c3e50", font=("Arial", 12)).pack(pady=5)
        
        entry_id = tk.Entry(self.container, font=("Arial", 14))
        entry_id.pack(pady=10)
        
        def tentar_logar():
            try:
                id_usu = int(entry_id.get())
                offset = self.arvore_usuarios.buscar(id_usu)
                if offset is None:
                    messagebox.showerror("Erro", "Aluno não encontrado! Faça sua matrícula.")
                    return
                    
                usu = gerenciador.ler_usuario_offset(offset)
                if int(usu.nivel_atual) == -1:
                    messagebox.showerror("Acesso Negado", "Esta conta foi excluída.")
                    return
                    
                self.usuario_logado = usu
                self.mostrar_dashboard_aluno()
            except ValueError:
                messagebox.showerror("Erro", "Digite um ID numérico válido!")

        tk.Button(self.container, text="Entrar", font=("Arial", 12), bg="#3498db", fg="white", command=tentar_logar, width=15).pack(pady=10)
        tk.Button(self.container, text="Voltar", font=("Arial", 12), command=self.mostrar_tela_inicial, width=15).pack()

    # --- TELA 4: DASHBOARD (MENU DO ALUNO) ---
    def mostrar_dashboard_aluno(self):
        self.limpar_tela()
        usu = self.usuario_logado
        
        frame_status = tk.Frame(self.container, bg="#34495e", pady=10)
        frame_status.pack(fill="x")
        
        tk.Label(frame_status, text=f"🎓 Aluno: {usu.nome}   |   ⭐ Nível: {usu.nivel_atual}   |   🏆 Pontos: {usu.pontuacao_total}", font=("Arial", 12, "bold"), fg="#f1c40f", bg="#34495e").pack()
        tk.Label(self.container, text="Missões Desbloqueadas:", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50").pack(pady=15)
        
        frame_lista = tk.Frame(self.container, bg="#2c3e50")
        frame_lista.pack(fill="both", expand=True, padx=20)
        
        if os.path.exists("exercicios.txt"):
            with open("exercicios.txt", "r", encoding="utf-8") as arq:
                for linha in arq:
                    partes = linha.strip().split(",")
                    if len(partes) >= 7:
                        cod_exer, cod_licao, nivel_req, descricao = int(partes[0]), int(partes[1]), int(partes[2]), partes[3]
                        
                        # FILTRO APLICADO: Só mostra se for do nível dele E do idioma que ele escolheu
                        if nivel_req <= int(usu.nivel_atual) and cod_licao == int(usu.codigo_idioma):
                            btn = tk.Button(frame_lista, text=f"Nível {nivel_req} - {descricao}", font=("Arial", 11), anchor="w", 
                                            command=lambda c=cod_exer: self.iniciar_exercicio(c))
                            btn.pack(fill="x", pady=2)
                            
        tk.Button(self.container, text="Deslogar", font=("Arial", 12), bg="#e74c3c", fg="white", command=self.mostrar_tela_inicial).pack(pady=20)

    # --- TELA 5: RESOLVER O EXERCÍCIO ---
    def iniciar_exercicio(self, id_exercicio):
        self.limpar_tela()
        offset_exer = self.arvore_exercicios.buscar(id_exercicio)
        exer = gerenciador.ler_exercicio_offset(offset_exer)
        
        tk.Label(self.container, text=f"Questão {exer.codigo}", font=("Arial", 18, "bold"), fg="#f1c40f", bg="#2c3e50").pack(pady=20)
        tk.Label(self.container, text=exer.descricao, font=("Arial", 14), fg="white", bg="#2c3e50", wraplength=500).pack(pady=20)
        
        def checar_resposta(resposta_escolhida):
            if resposta_escolhida.lower() == exer.resposta_correta.lower():
                self.usuario_logado.pontuacao_total = int(self.usuario_logado.pontuacao_total) + int(exer.pontuacao)
                novo_nivel = (self.usuario_logado.pontuacao_total // 100) + 1
                mensagem = "✅ ACERTOU! Muito bem!"
                
                if novo_nivel > int(self.usuario_logado.nivel_atual):
                    self.usuario_logado.nivel_atual = novo_nivel
                    mensagem += f"\n\n🎉 LEVEL UP! Você alcançou o Nível {novo_nivel}!"
                
                novo_offset = gerenciador.salvar_usuario(self.usuario_logado)
                self.arvore_usuarios.inserir(self.usuario_logado.codigo, novo_offset)
                messagebox.showinfo("Resultado", mensagem)
            else:
                messagebox.showerror("Resultado", f"❌ Errado!\nA resposta correta era: {exer.resposta_correta}")
                
            self.mostrar_dashboard_aluno()

        for op in exer.opcoes_resposta.split("|"):
            tk.Button(self.container, text=op, font=("Arial", 12), bg="white", height=2, command=lambda o=op: checar_resposta(o)).pack(fill="x", padx=40, pady=5)
            
        tk.Button(self.container, text="Cancelar / Voltar", font=("Arial", 10), command=self.mostrar_dashboard_aluno).pack(pady=30)

    # --- TELA 6: REMOVER ALUNO (O DELETE DO CRUD) ---
    def mostrar_tela_remover(self):
        self.limpar_tela()
        tk.Label(self.container, text="Cancelar Matrícula", font=("Arial", 20, "bold"), fg="white", bg="#2c3e50").pack(pady=40)
        tk.Label(self.container, text="Digite o ID do aluno para exclusão:", fg="white", bg="#2c3e50", font=("Arial", 12)).pack(pady=5)
        
        entry_id = tk.Entry(self.container, font=("Arial", 14))
        entry_id.pack(pady=10)
        
        def deletar_aluno():
            try:
                codigo = int(entry_id.get())
                offset = self.arvore_usuarios.buscar(codigo)
                
                if offset is None:
                    messagebox.showerror("Erro", "Aluno não encontrado!")
                    return
                    
                usu = gerenciador.ler_usuario_offset(offset)
                
                if int(usu.nivel_atual) == -1:
                    messagebox.showerror("Erro", "Este aluno já foi removido do sistema!")
                    return
                
                confirmacao = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir a conta de '{usu.nome}' permanentemente?")
                
                if confirmacao:
                    usu.nivel_atual = -1 # Exclusão lógica
                    novo_offset = gerenciador.salvar_usuario(usu)
                    self.arvore_usuarios.inserir(usu.codigo, novo_offset)
                    messagebox.showinfo("Sucesso", "Conta removida com sucesso!")
                    self.mostrar_tela_inicial()
                    
            except ValueError:
                messagebox.showerror("Erro", "Digite um ID numérico válido!")

        tk.Button(self.container, text="Remover Aluno", font=("Arial", 12), bg="#e74c3c", fg="white", command=deletar_aluno, width=20).pack(pady=10)
        tk.Button(self.container, text="Voltar", font=("Arial", 12), command=self.mostrar_tela_inicial, width=20).pack()
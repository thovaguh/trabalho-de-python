import os
from modelos import Idioma, Licao, Exercicio, Usuario
from arvore import ArvoreBinaria
import gerenciador 

# =================================================================================
# 1. FUNÇÃO DE INICIALIZAÇÃO (SEMENTE DO BANCO DE DADOS)
# =================================================================================
def inicializar_banco_padrao(arvore_idiomas, arvore_exercicios, arvore_licoes):
    # Garante que os idiomas 1 e 2 sempre existam no disco e na RAM
    if arvore_idiomas.buscar(1) is None:
        offset = gerenciador.salvar_idioma(Idioma(1, "Inglês"))
        arvore_idiomas.inserir(1, offset)
        
    if arvore_idiomas.buscar(2) is None:
        offset = gerenciador.salvar_idioma(Idioma(2, "Espanhol"))
        arvore_idiomas.inserir(2, offset)

    # Garante que a Lição Padrão (ID 1, vinculada ao Inglês) exista
    if arvore_licoes.buscar(1) is None:
        offset = gerenciador.salvar_licao(Licao(1, 1, 5)) 
        arvore_licoes.inserir(1, offset)
    
    # Garante que a Lição de Espanhol (ID 2, vinculada ao Idioma 2) exista
    if arvore_licoes.buscar(2) is None:
        offset = gerenciador.salvar_licao(Licao(2, 2, 5)) # Lição 2, Idioma 2, 5 níveis
        arvore_licoes.inserir(2, offset)


# =================================================================================
# 2. MENU DE USUÁRIOS (APENAS CADASTRO)
# =================================================================================
def cadastrar_aluno(arvore_usuarios, arvore_idiomas):
    print("\n--- MATRÍCULA DE NOVO ALUNO ---")
    codigo = int(input("Crie um ID numérico para você: "))
    
    if arvore_usuarios.buscar(codigo) is not None:
        print("Erro: Este ID já está em uso! Tente outro.")
        return
        
    nome = input("Seu Nome: ")
    print("Idiomas disponíveis: 1 - Inglês | 2 - Espanhol")
    codigo_idioma = int(input("Código do Idioma que deseja aprender: "))
    
    if arvore_idiomas.buscar(codigo_idioma) is None:
        print("Erro: Idioma inválido!")
        return
    
    # O aluno começa automaticamente no Nível 1, com 0 pontos.
    novo_usuario = Usuario(codigo, nome, codigo_idioma, 1, 0)
    
    offset = gerenciador.salvar_usuario(novo_usuario)
    arvore_usuarios.inserir(codigo, offset)
    print(f"\nMatrícula concluída! Bem-vindo(a), {nome}. Você está no Nível 1.")


# =================================================================================
# 3. LISTAGEM DE EXERCÍCIOS PERMITIDOS
# =================================================================================
def listar_exercicios_disponiveis(nivel_usuario):
    print("\n--- QUESTÕES DESBLOQUEADAS PARA VOCÊ ---")
    encontrou = False
    
    if os.path.exists("exercicios.txt"):
        with open("exercicios.txt", "r", encoding="utf-8") as arq:
            for linha in arq:
                partes = linha.strip().split(",")
                if len(partes) >= 7:
                    cod_exer = int(partes[0])
                    nivel_req = int(partes[2])
                    descricao = partes[3]
                    
                    if nivel_req <= nivel_usuario:
                        print(f"ID: {cod_exer} | Nível: {nivel_req} | Pergunta: {descricao}")
                        encontrou = True
                        
    if not encontrou:
        print("Nenhuma questão encontrada. Verifique seu arquivo exercicios.txt.")


# =================================================================================
# 4. MODO JOGO (A SESSÃO DE ESTUDOS)
# =================================================================================
def sessao_de_estudos(arvore_usuarios, arvore_exercicios):
    print("\n=== SESSÃO DE ESTUDOS ===")
    id_usuario = int(input("Digite o seu ID de aluno para logar: "))
    
    offset_usu = arvore_usuarios.buscar(id_usuario)
    if offset_usu is None:
        print("Aluno não encontrado! Faça sua matrícula primeiro.")
        return
        
    usuario = gerenciador.ler_usuario_offset(offset_usu)
    
    # Trava de segurança: Bloqueia acesso de usuários deletados
    if int(usuario.nivel_atual) == -1:
        print("⚠️ Acesso Negado: Esta conta foi excluída do sistema.")
        return
    
    while True:
        print(f"\n=======================================================")
        print(f" ALUNO: {usuario.nome} | NÍVEL: {usuario.nivel_atual} | PONTOS: {usuario.pontuacao_total} ")
        print(f"=======================================================")
        
        listar_exercicios_disponiveis(int(usuario.nivel_atual))
        
        opcao = input("\nDigite o ID do exercício que quer resolver (ou 0 para sair): ")
        
        if opcao == "0":
            print(f"Até a próxima aula, {usuario.nome}!")
            break
            
        id_exer = int(opcao)
        offset_exer = arvore_exercicios.buscar(id_exer)
        
        if offset_exer is None:
            print("Este ID de exercício não existe!")
            continue
            
        exer = gerenciador.ler_exercicio_offset(offset_exer)
        
        if int(exer.nivel_dificuldade) > int(usuario.nivel_atual):
            print(f"\n[BLOQUEADO] Este exercício é do Nível {exer.nivel_dificuldade}.")
            print("Você não tem nível suficiente para acessá-lo ainda!")
            continue
            
        print(f"\n>> EXERCÍCIO {exer.codigo}: {exer.descricao}")
        opcoes = exer.opcoes_resposta.split("|")
        for op in opcoes:
            print(f" - {op}")
            
        resposta = input("\nEscreva a sua resposta exatamente como na opção: ").strip()
        
        if resposta.lower() == exer.resposta_correta.lower():
            print("\n✅ ACERTOU! Muito bem!")
            
            usuario.pontuacao_total = int(usuario.pontuacao_total) + int(exer.pontuacao)
            
            # SISTEMA DE LEVEL UP: A cada 100 pontos, o usuário sobe de nível
            novo_nivel = (usuario.pontuacao_total // 100) + 1
            
            if novo_nivel > int(usuario.nivel_atual):
                usuario.nivel_atual = novo_nivel
                print(f"🎉 LEVEL UP! Você evoluiu para o Nível {usuario.nivel_atual}!")
                print("Novas questões mais difíceis foram desbloqueadas!")
                
            novo_offset = gerenciador.salvar_usuario(usuario)
            arvore_usuarios.inserir(usuario.codigo, novo_offset)
            print(f"-> Progresso salvo! Pontos atuais: {usuario.pontuacao_total}")
            
        else:
            print(f"\n❌ Errado! A resposta correta era: {exer.resposta_correta}")


# =================================================================================
# 5. REMOVER ALUNO (CRUD: DELETE)
# =================================================================================
def remover_aluno(arvore_usuarios):
    print("\n--- CANCELAR MATRÍCULA (REMOVER ALUNO) ---")
    codigo = int(input("Digite o ID do aluno que deseja remover: "))
    
    offset = arvore_usuarios.buscar(codigo)
    if offset is None:
        print("Erro: Aluno não encontrado!")
        return
        
    usuario = gerenciador.ler_usuario_offset(offset)
    
    if int(usuario.nivel_atual) == -1:
        print("Erro: Este aluno já foi removido do sistema!")
        return
    
    confirmacao = input(f"Tem certeza que deseja excluir a conta de {usuario.nome}? (S/N): ")
    
    if confirmacao.upper() == "S":
        # EXCLUSÃO LÓGICA: Nível -1 indica conta inativa
        usuario.nivel_atual = -1
        
        novo_offset = gerenciador.salvar_usuario(usuario)
        arvore_usuarios.inserir(usuario.codigo, novo_offset)
        print("✅ Conta removida com sucesso!")
    else:
        print("Operação cancelada.")


# =================================================================================
# 6. INICIALIZAÇÃO DO PROGRAMA
# =================================================================================
def main():
    arvore_idiomas = ArvoreBinaria()
    arvore_licoes = ArvoreBinaria()
    arvore_exercicios = ArvoreBinaria()
    arvore_usuarios = ArvoreBinaria()
    
    gerenciador.carregar_indices_idiomas(arvore_idiomas)
    gerenciador.carregar_indices_licoes(arvore_licoes)
    gerenciador.carregar_indices_exercicios(arvore_exercicios)
    gerenciador.carregar_indices_usuarios(arvore_usuarios)
    
    # Executa a semente de dados vitais
    inicializar_banco_padrao(arvore_idiomas, arvore_exercicios, arvore_licoes)
    
    while True:
        print("\n===============================")
        print("      MAXLANGUAGE PLATFORM     ")
        print("===============================")
        print("1. Entrar (Sessão de Estudos)")
        print("2. Matricular Novo Aluno")
        print("3. Remover Aluno")
        print("0. Fechar Programa")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            sessao_de_estudos(arvore_usuarios, arvore_exercicios)
        elif opcao == "2":
            cadastrar_aluno(arvore_usuarios, arvore_idiomas)
        elif opcao == "3":
            remover_aluno(arvore_usuarios)
        elif opcao == "0":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
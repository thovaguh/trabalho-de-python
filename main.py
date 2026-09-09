from modelos import Idioma
from arvore import ArvoreBinaria
from gerenciador import salvar_idioma, ler_idioma_offset, carregar_indices_idiomas

def menu_idiomas(arvore_idiomas):
    while True:
        print("GERENCIAR IDIOMAS")
        print("1. Cadastrar idioma")
        print("2. Consultar idioma")
        print("0. voltar")
        
        opcao = input("Escolha uma opcao: ")
        
        if opcao =="1":
            codigo = int(input("Codigo do idioma: "))
            
            if arvore_idiomas.buscar(codigo) is not None:
                print ("Erro: ja existe um idioma cadastrado com este codigo!")
                continue
            
            descricao = input("Descricao (ex: Inglês, Espanhol): ")
            
            novo_idioma = Idioma(codigo, descricao)
            
            offset = salvar_idioma(novo_idioma)
            
            arvore_idiomas.inserir(codigo, offset)
            
            print(f"Idioma '{descricao}' cadastrado com sucesso!")
            
        elif opcao == "2":
            codigo = int(input("Digite o codigo do idioma que deseja buscar: "))
            
            offset_encontrado = arvore_idiomas.buscar(codigo)
            
            if offset_encontrado is not None:
                
                idioma = ler_idioma_offset(offset_encontrado)
                print(f"[REGISTRO ENCONTRADO NO DISCO]")
                print(f"codigo: {idioma.codigo}")
                print(f"Descricao: {idioma.descricao}")
            else:
                print("idioma não encontrado!")
                
        elif opcao == "0":
            break
        else:
            print("Opção invalida!")
            
def main():
    arvore_idiomas = ArvoreBinaria()
    
    carregar_indices_idiomas(arvore_idiomas)
    
    while True:
        print("SISTEMA DE APRENDIZADO")
        print("1. modulos de Idiomas")
        print("0. sair")
        
        opcao = input("Opção: ")

        if opcao == "1":
            menu_idiomas(arvore_idiomas)
        elif opcao == "0":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida!")
        


if __name__ == "__main__":
    main()
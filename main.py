from alunos import menu_alunos
from funcionarios import menu_funcionarios
from treinos import menu_treinos
from planos import menu_planos


while True:

    print("\n=== FITFLOW ===")
    print("1 - Alunos")
    print("2 - Funcionários")
    print("3 - Treinos")
    print("4 - Planos")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        menu_alunos()

    elif opcao == "2":
        menu_funcionarios()

    elif opcao == "3":
        menu_treinos()

    elif opcao == "4":
        menu_planos()

    elif opcao == "0":
        print("Encerrando sistema...")
        break

    else:
        print("Opção inválida!")
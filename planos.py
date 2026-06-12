planos = []
def menu_planos():

    while True:
        print("\n=== MENU DE PLANOS ===")
        print("1 - Cadastrar Plano")
        print("2 - Listar Planos")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_plano()

        elif opcao == "2":
            listar_planos()

        elif opcao == "3":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")

def cadastrar_plano():
    print("\n=== Cadastro de Plano ===")

    nome = input("Nome do plano: ")
    valor = float(input("Valor do plano (R$): "))
    duracao = input("Duração (Mensal, Trimestral, Semestral, Anual): ")

    plano = {
        "nome": nome,
        "valor": valor,
        "duracao": duracao
    }

    planos.append(plano)

    print("\nPlano cadastrado com sucesso!")

def listar_planos():
    print("\n=== PLANOS CADASTRADOS ===")

    if len(planos) == 0:
        print("Nenhum plano cadastrado.")
        return

    for i, plano in enumerate(planos, start=1):
        print(f"{i}. {plano['nome']} - R${plano['valor']:.2f} - {plano['duracao']}")


menu_planos()

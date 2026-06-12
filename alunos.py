import pickle

arquivo = "alunos.pkl"

try:
    with open(arquivo, "rb") as f:
        alunos = pickle.load(f)
except:
    alunos = []

while True:
    print("SISTEMA DE ALUNOS")
    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")
    print("3 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Nome do aluno: ")
        idade = input("Idade: ")

        aluno = {
            "nome": nome,
            "idade": idade
        }

        alunos.append(aluno)

        with open(arquivo, "wb") as f:
            pickle.dump(alunos, f)

        print("Aluno cadastrado com sucesso!")

    elif opcao == "2":
        print("\n=== ALUNOS CADASTRADOS ===")

        if len(alunos) == 0:
            print("Nenhum aluno cadastrado.")

        for aluno in alunos:
            print(f"Nome: {aluno['nome']} | Idade: {aluno['idade']}")

    elif opcao == "3":
        print("Encerrando...")
        break

    else:
        print("Opção inválida!")

'''Sistema de cadastro de alunos'''

from database import conexao, cursor

def menu_alunos():

    while True:
        print("SISTEMA DE ALUNOS")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do aluno: ")
            idade = input("Idade: ")

            cursor.execute(
                "INSERT INTO alunos (nome, idade) VALUES (?, ?)",
                (nome, idade)
            )

            conexao.commit()

            print("Aluno cadastrado com sucesso!")

        elif opcao == "2":
            print("ALUNOS CADASTRADOS")

            cursor.execute("SELECT nome, idade FROM alunos")

            alunos = cursor.fetchall()

            if len(alunos) == 0:
                print("Nenhum aluno cadastrado.")

            else:
                for aluno in alunos:
                    print(f"Nome: {aluno[0]} | Idade: {aluno[1]}")

        elif opcao == "3":
            print("Encerrando...")
            conexao.close()
            break

        else:
            print("Opção inválida!")
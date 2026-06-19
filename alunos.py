'''Sistema de cadastro de alunos'''
from database import conexao, cursor

def cadastrar_aluno():
    nome = input("Nome do aluno: ").strip()
    try:
        idade = int(input("Idade: "))
    except ValueError:
        print("Idade inválida!")
        return
    cpf = input("CPF: ").strip()
    email = input("E-mail: ").strip()
    telefone = input("Telefone: ").strip()
    cursor.execute(
        "INSERT INTO alunos (nome, idade, cpf, email, telefone) VALUES (?, ?, ?, ?, ?)",
        (nome, idade, cpf, email, telefone)
    )
    conexao.commit()
    print("Aluno cadastrado com sucesso!")

def listar_alunos():
    cursor.execute("SELECT id, nome, idade, cpf, email, telefone FROM alunos")
    alunos = cursor.fetchall()
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    print("| ALUNOS |")
    for aluno in alunos:
        print(
            f"ID: {aluno[0]} | "
            f"Nome: {aluno[1]} | "
            f"Idade: {aluno[2]} | "
            f"CPF: {aluno[3]} | "
            f"E-mail: {aluno[4]} | "
            f"Telefone: {aluno[5]}"
        )

def buscar_aluno():
    nome = input("Digite o nome do aluno: ")
    cursor.execute(
        "SELECT id, nome, idade, cpf, email, telefone FROM alunos WHERE nome LIKE ?",
        ('%' + nome + '%',)
    )
    alunos = cursor.fetchall()
    if not alunos:
        print("Aluno não encontrado.")
        return
    for aluno in alunos:
        print(
            f"ID: {aluno[0]} | "
            f"Nome: {aluno[1]} | "
            f"Idade: {aluno[2]} | "
            f"CPF: {aluno[3]} | "
            f"E-mail: {aluno[4]} | "
            f"Telefone: {aluno[5]}"
        )

def atualizar_aluno():
    listar_alunos()
    try:
        id_aluno = int(input("ID do aluno: "))
        nova_idade = int(input("Nova idade: "))
    except ValueError:
        print("Valor inválido!")
        return
    novo_cpf = input("Novo CPF: ").strip()
    novo_email = input("Novo e-mail: ").strip()
    novo_telefone = input("Novo telefone: ").strip()
    cursor.execute(
        "UPDATE alunos SET idade = ?, cpf = ?, email = ?, telefone = ? WHERE id = ?",
        (nova_idade, novo_cpf, novo_email, novo_telefone, id_aluno)
    )
    conexao.commit()
    if cursor.rowcount > 0:
        print("Aluno atualizado com sucesso!")
    else:
        print("Aluno não encontrado.")

def excluir_aluno():
    listar_alunos()
    try:
        id_aluno = int(input("ID do aluno: "))
    except ValueError:
        print("ID inválido!")
        return
    cursor.execute(
        "DELETE FROM alunos WHERE id = ?",
        (id_aluno,)
    )
    conexao.commit()
    if cursor.rowcount > 0:
        print("Aluno removido com sucesso!")
    else:
        print("Aluno não encontrado.")

def menu_alunos():
    while True:
        print("| SISTEMA DE ALUNOS |")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Buscar aluno")
        print("4 - Atualizar aluno")
        print("5 - Excluir aluno")
        print("6 - Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar_aluno()
        elif opcao == "2":
            listar_alunos()
        elif opcao == "3":
            buscar_aluno()
        elif opcao == "4":
            atualizar_aluno()
        elif opcao == "5":
            excluir_aluno()
        elif opcao == "6":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")
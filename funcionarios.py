from database import conexao, cursor


def cadastro_funcionarios():
    print('| Cadastro de Funcionário |')

    nome = input('Nome: ')
    cpf = input('CPF: ')
    cargo = input('Cargo: ')
    salario = float(input('Salário: '))
    telefone = input('Telefone: ')
    horario = input('Horário de trabalho: ')

    cursor.execute("""
        INSERT INTO funcionarios
        (nome, cpf, cargo, salario, telefone, horario)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, cpf, cargo, salario, telefone, horario))

    conexao.commit()

    print('Funcionário cadastrado com sucesso!')


def listar_funcionarios():

    cursor.execute("""
        SELECT nome, cpf, cargo, salario, telefone, horario
        FROM funcionarios
    """)

    funcionarios = cursor.fetchall()

    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        return

    for funcionario in funcionarios:
        print(f'''
Nome: {funcionario[0]}
CPF: {funcionario[1]}
Cargo: {funcionario[2]}
Salário: R$ {funcionario[3]}
Telefone: {funcionario[4]}
Horário: {funcionario[5]}
''')


def editar_funcionario():

    print('| Editar Funcionário |')

    cpf = input('Digite o CPF do funcionário: ')

    cursor.execute(
        "SELECT * FROM funcionarios WHERE cpf = ?",
        (cpf,)
    )

    funcionario = cursor.fetchone()

    if not funcionario:
        print('Funcionário não encontrado.')
        return

    nome = input('Novo nome: ')
    cargo = input('Novo cargo: ')
    salario = input('Novo salário: ')
    telefone = input('Novo telefone: ')
    horario = input('Novo horário: ')

    if nome:
        cursor.execute(
            "UPDATE funcionarios SET nome = ? WHERE cpf = ?",
            (nome, cpf)
        )

    if cargo:
        cursor.execute(
            "UPDATE funcionarios SET cargo = ? WHERE cpf = ?",
            (cargo, cpf)
        )

    if salario:
        cursor.execute(
            "UPDATE funcionarios SET salario = ? WHERE cpf = ?",
            (float(salario), cpf)
        )

    if telefone:
        cursor.execute(
            "UPDATE funcionarios SET telefone = ? WHERE cpf = ?",
            (telefone, cpf)
        )

    if horario:
        cursor.execute(
            "UPDATE funcionarios SET horario = ? WHERE cpf = ?",
            (horario, cpf)
        )

    conexao.commit()

    print('Funcionário editado com sucesso!')


def excluir_funcionario():

    print('| Excluir Funcionário |')

    cpf = input('Digite o CPF do funcionário: ')

    cursor.execute(
        "DELETE FROM funcionarios WHERE cpf = ?",
        (cpf,)
    )

    conexao.commit()

    print('Funcionário excluído com sucesso!')


def menu_funcionarios():

    while True:

        print("| FUNCIONÁRIOS |")
        print("1 - Cadastrar funcionário")
        print("2 - Listar funcionários")
        print("3 - Editar funcionário")
        print("4 - Excluir funcionário")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastro_funcionarios()

        elif opcao == "2":
            listar_funcionarios()

        elif opcao == "3":
            editar_funcionario()

        elif opcao == "4":
            excluir_funcionario()

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")
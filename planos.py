from database import conexao, cursor


def cadastrar_plano():

    print('| Cadastro de Plano |')

    nome = input('Nome do plano: ')

    try:
        valor = float(input('Valor do plano (R$): '))
    except ValueError:
        print('Valor inválido.')
        return

    duracao = input(
        'Duração (Mensal, Trimestral, Semestral, Anual): '
    )

    cursor.execute("""
        INSERT INTO planos
        (nome, valor, duracao)
        VALUES (?, ?, ?)
    """, (nome, valor, duracao))

    conexao.commit()

    print('Plano cadastrado com sucesso!')


def listar_planos():

    cursor.execute("""
        SELECT id, nome, valor, duracao
        FROM planos
    """)

    planos = cursor.fetchall()

    if not planos:
        print('Nenhum plano cadastrado.')
        return

    for plano in planos:

        print(f'''
ID: {plano[0]}
Nome: {plano[1]}
Valor: R$ {plano[2]}
Duração: {plano[3]}
''')


def editar_plano():

    print('| Editar Plano |')

    listar_planos()

    try:
        id_plano = int(input('Digite o ID do plano: '))
    except ValueError:
        print('ID inválido.')
        return

    cursor.execute(
        "SELECT * FROM planos WHERE id = ?",
        (id_plano,)
    )

    plano = cursor.fetchone()

    if not plano:
        print('Plano não encontrado.')
        return

    print('Deixe em branco para manter o valor atual.')

    nome = input('Novo nome: ')

    valor = input('Novo valor: ')

    duracao = input('Nova duração: ')

    if nome:

        cursor.execute(
            "UPDATE planos SET nome = ? WHERE id = ?",
            (nome, id_plano)
        )

    if valor:

        cursor.execute(
            "UPDATE planos SET valor = ? WHERE id = ?",
            (float(valor), id_plano)
        )

    if duracao:

        cursor.execute(
            "UPDATE planos SET duracao = ? WHERE id = ?",
            (duracao, id_plano)
        )

    conexao.commit()

    print('Plano editado com sucesso!')


def excluir_plano():

    print('| Excluir Plano |')

    listar_planos()

    try:
        id_plano = int(input('Digite o ID do plano: '))
    except ValueError:
        print('ID inválido.')
        return

    cursor.execute(
        "DELETE FROM planos WHERE id = ?",
        (id_plano,)
    )

    conexao.commit()

    print('Plano excluído com sucesso!')


def menu_planos():

    while True:

        print("\n| PLANOS |")

        print("1 - Cadastrar plano")

        print("2 - Listar planos")

        print("3 - Editar plano")

        print("4 - Excluir plano")

        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":

            cadastrar_plano()

        elif opcao == "2":

            listar_planos()

        elif opcao == "3":

            editar_plano()

        elif opcao == "4":

            excluir_plano()

        elif opcao == "0":

            break

        else:

            print("Opção inválida!")

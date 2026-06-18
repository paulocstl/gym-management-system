from database import conexao, cursor
from alunos import listar_alunos
from funcionarios import listar_funcionarios


def cadastrar_treino():

    print("| Cadastro de Treino |")

    nome = input("Nome do treino: ")
    objetivo = input("Objetivo: ")
    nivel = input("Nível: ")

    listar_alunos()

    try:
        aluno_id = int(input("ID do aluno: "))
    except ValueError:
        print("ID inválido!")
        return

    print("\n| FUNCIONÁRIOS |")
    listar_funcionarios()

    try:
        funcionario_id = int(input("ID do funcionário responsável: "))
    except ValueError:
        print("ID inválido!")
        return

    cursor.execute("""
        INSERT INTO treinos
        (nome, objetivo, nivel, aluno_id, funcionario_id)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, objetivo, nivel, aluno_id, funcionario_id))

    conexao.commit()

    print("Treino cadastrado com sucesso!")


def listar_treinos():

    cursor.execute("""
        SELECT
            treinos.id,
            treinos.nome,
            treinos.objetivo,
            treinos.nivel,
            alunos.nome,
            funcionarios.nome
        FROM treinos
        LEFT JOIN alunos
            ON treinos.aluno_id = alunos.id
        LEFT JOIN funcionarios
            ON treinos.funcionario_id = funcionarios.id
    """)

    treinos = cursor.fetchall()

    if not treinos:
        print("Nenhum treino cadastrado.")
        return

    print("| TREINOS |")

    for treino in treinos:

        print(f"""
ID: {treino[0]}
Nome: {treino[1]}
Objetivo: {treino[2]}
Nível: {treino[3]}
Aluno: {treino[4]}
Funcionário: {treino[5]}
""")


def visualizar_treino():

    listar_treinos()

    try:
        treino_id = int(input("Digite o ID do treino: "))
    except ValueError:
        print("ID inválido!")
        return

    cursor.execute("""
        SELECT
            treinos.nome,
            treinos.objetivo,
            treinos.nivel,
            alunos.nome,
            funcionarios.nome
        FROM treinos
        LEFT JOIN alunos
            ON treinos.aluno_id = alunos.id
        LEFT JOIN funcionarios
            ON treinos.funcionario_id = funcionarios.id
        WHERE treinos.id = ?
    """, (treino_id,))

    treino = cursor.fetchone()

    if not treino:
        print("Treino não encontrado.")
        return

    print(f"""
Nome: {treino[0]}
Objetivo: {treino[1]}
Nível: {treino[2]}
Aluno: {treino[3]}
Funcionário: {treino[4]}
""")

    cursor.execute("""
        SELECT exercicios.nome
        FROM treino_exercicios
        INNER JOIN exercicios
        ON treino_exercicios.exercicio_id = exercicios.id
        WHERE treino_exercicios.treino_id = ?
    """, (treino_id,))

    exercicios = cursor.fetchall()

    print("Exercícios:")

    if not exercicios:
        print("Nenhum exercício vinculado.")
        return

    for exercicio in exercicios:
        print(f"- {exercicio[0]}")


def editar_treino():

    listar_treinos()

    try:
        treino_id = int(input("ID do treino: "))
    except ValueError:
        print("ID inválido!")
        return

    cursor.execute(
        "SELECT * FROM treinos WHERE id = ?",
        (treino_id,)
    )

    treino = cursor.fetchone()

    if not treino:
        print("Treino não encontrado.")
        return

    print("Deixe em branco para manter o valor atual.")

    nome = input("Novo nome: ")
    objetivo = input("Novo objetivo: ")
    nivel = input("Novo nível: ")

    if nome:
        cursor.execute(
            "UPDATE treinos SET nome = ? WHERE id = ?",
            (nome, treino_id)
        )

    if objetivo:
        cursor.execute(
            "UPDATE treinos SET objetivo = ? WHERE id = ?",
            (objetivo, treino_id)
        )

    if nivel:
        cursor.execute(
            "UPDATE treinos SET nivel = ? WHERE id = ?",
            (nivel, treino_id)
        )

    conexao.commit()

    print("Treino atualizado com sucesso!")


def excluir_treino():

    listar_treinos()

    try:
        treino_id = int(input("ID do treino: "))
    except ValueError:
        print("ID inválido!")
        return

    cursor.execute(
        "DELETE FROM treino_exercicios WHERE treino_id = ?",
        (treino_id,)
    )

    cursor.execute(
        "DELETE FROM treinos WHERE id = ?",
        (treino_id,)
    )

    conexao.commit()

    print("Treino excluído com sucesso!")


def cadastrar_exercicio():

    print("| Cadastro de Exercício |")

    nome = input("Nome do exercício: ")
    grupo_muscular = input("Grupo muscular: ")
    equipamento = input("Equipamento: ")
    descricao = input("Descrição: ")

    cursor.execute("""
        INSERT INTO exercicios
        (nome, grupo_muscular, equipamento, descricao)
        VALUES (?, ?, ?, ?)
    """, (nome, grupo_muscular, equipamento, descricao))

    conexao.commit()

    print("Exercício cadastrado com sucesso!")


def listar_exercicios():

    cursor.execute("""
        SELECT
            id,
            nome,
            grupo_muscular,
            equipamento
        FROM exercicios
    """)

    exercicios = cursor.fetchall()

    if not exercicios:
        print("Nenhum exercício cadastrado.")
        return

    print("| EXERCÍCIOS |")

    for exercicio in exercicios:

        print(
            f"{exercicio[0]} - "
            f"{exercicio[1]} | "
            f"{exercicio[2]} | "
            f"{exercicio[3]}"
        )


def adicionar_exercicio_treino():

    listar_treinos()

    try:
        treino_id = int(input("ID do treino: "))
    except ValueError:
        print("ID inválido!")
        return

    listar_exercicios()

    try:
        exercicio_id = int(input("ID do exercício: "))
    except ValueError:
        print("ID inválido!")
        return

    cursor.execute("""
        INSERT INTO treino_exercicios
        (treino_id, exercicio_id)
        VALUES (?, ?)
    """, (treino_id, exercicio_id))

    conexao.commit()

    print("Exercício adicionado ao treino!")


def remover_exercicio_treino():

    listar_treinos()

    try:
        treino_id = int(input("ID do treino: "))
    except ValueError:
        print("ID inválido!")
        return

    cursor.execute("""
        SELECT
            exercicios.id,
            exercicios.nome
        FROM treino_exercicios
        INNER JOIN exercicios
        ON treino_exercicios.exercicio_id = exercicios.id
        WHERE treino_exercicios.treino_id = ?
    """, (treino_id,))

    exercicios = cursor.fetchall()

    if not exercicios:
        print("Nenhum exercício encontrado.")
        return

    for exercicio in exercicios:
        print(f"{exercicio[0]} - {exercicio[1]}")

    try:
        exercicio_id = int(input("ID do exercício para remover: "))
    except ValueError:
        print("ID inválido!")
        return

    cursor.execute("""
        DELETE FROM treino_exercicios
        WHERE treino_id = ?
        AND exercicio_id = ?
    """, (treino_id, exercicio_id))

    conexao.commit()

    print("Exercício removido do treino!")


def menu_exercicios():

    while True:

        print("| GERENCIAR EXERCÍCIOS |")
        print("1 - Cadastrar exercício")
        print("2 - Listar exercícios")
        print("3 - Adicionar exercício ao treino")
        print("4 - Remover exercício do treino")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_exercicio()

        elif opcao == "2":
            listar_exercicios()

        elif opcao == "3":
            adicionar_exercicio_treino()

        elif opcao == "4":
            remover_exercicio_treino()

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")


def menu_treinos():

    while True:

        print("| TREINOS |")
        print("1 - Cadastrar treino")
        print("2 - Listar treinos")
        print("3 - Visualizar treino")
        print("4 - Editar treino")
        print("5 - Excluir treino")
        print("6 - Gerenciar exercícios")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_treino()

        elif opcao == "2":
            listar_treinos()

        elif opcao == "3":
            visualizar_treino()

        elif opcao == "4":
            editar_treino()

        elif opcao == "5":
            excluir_treino()

        elif opcao == "6":
            menu_exercicios()

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")
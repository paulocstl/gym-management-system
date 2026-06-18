import sqlite3

conexao = sqlite3.connect("academia.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS planos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    valor REAL,
    duracao TEXT
)
""")

conexao.commit()


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

    cursor.execute(
        """
        INSERT INTO planos (nome, valor, duracao)
        VALUES (?, ?, ?)
        """,
        (nome, valor, duracao)
    )

    conexao.commit()

    print("\nPlano cadastrado com sucesso!")


def listar_planos():

    print("\n=== PLANOS CADASTRADOS ===")

    cursor.execute("SELECT * FROM planos")

    planos = cursor.fetchall()

    if len(planos) == 0:
        print("Nenhum plano cadastrado.")
        return

    for plano in planos:

        print(
            f"{plano[0]}. "
            f"{plano[1]} - "
            f"R${plano[2]:.2f} - "
            f"{plano[3]}"
        )

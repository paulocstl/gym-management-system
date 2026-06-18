from database import conexao, cursor
from datetime import date

try:
    from alunos import listar_alunos
except ImportError:
    def listar_alunos():
        print("(Módulo de alunos não encontrado.)")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        grupo_muscular TEXT,
        equipamento TEXT,
        descricao TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS treinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        objetivo TEXT,
        nivel TEXT,
        aluno_id INTEGER,
        data_criacao TEXT,
        FOREIGN KEY (aluno_id) REFERENCES alunos(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS treino_exercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        treino_id INTEGER NOT NULL,
        exercicio_id INTEGER NOT NULL,
        series INTEGER,
        repeticoes INTEGER,
        carga REAL,
        descanso_segundos INTEGER,
        ordem INTEGER,
        FOREIGN KEY (treino_id) REFERENCES treinos(id),
        FOREIGN KEY (exercicio_id) REFERENCES exercicios(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_execucoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        treino_id INTEGER NOT NULL,
        aluno_id INTEGER,
        data_execucao TEXT,
        concluido INTEGER,
        observacoes TEXT,
        FOREIGN KEY (treino_id) REFERENCES treinos(id),
        FOREIGN KEY (aluno_id) REFERENCES alunos(id)
    )
""")
conexao.commit()

def cadastrar_exercicio():
    print('| Cadastro de Exercício |')
    nome = input('Nome do exercício: ')
    grupo_muscular = input('Grupo muscular: ')
    equipamento = input('Equipamento utilizado: ')
    descricao = input('Descrição/observações: ')
    cursor.execute("""
        INSERT INTO exercicios (nome, grupo_muscular, equipamento, descricao)
        VALUES (?, ?, ?, ?)
    """, (nome, grupo_muscular, equipamento, descricao))
    conexao.commit()
    print('Exercício cadastrado com sucesso!')


def listar_exercicios():
    cursor.execute("""
        SELECT id, nome, grupo_muscular, equipamento, descricao
        FROM exercicios
    """)
    exercicios = cursor.fetchall()
    if not exercicios:
        print("Nenhum exercício cadastrado.")
        return
    for exercicio in exercicios:
        print(f'''
ID: {exercicio[0]}
Nome: {exercicio[1]}
Grupo muscular: {exercicio[2]}
Equipamento: {exercicio[3]}
Descrição: {exercicio[4]}
''')


def editar_exercicio():
    print('| Editar Exercício |')
    listar_exercicios()
    try:
        id_exercicio = int(input('Digite o ID do exercício: '))
    except ValueError:
        print('ID inválido.')
        return
    cursor.execute("SELECT * FROM exercicios WHERE id = ?", (id_exercicio,))
    exercicio = cursor.fetchone()
    if not exercicio:
        print('Exercício não encontrado.')
        return
    print('Deixe em branco para manter o valor atual.')
    nome = input('Novo nome: ')
    grupo_muscular = input('Novo grupo muscular: ')
    equipamento = input('Novo equipamento: ')
    descricao = input('Nova descrição: ')
    if nome:
        cursor.execute("UPDATE exercicios SET nome = ? WHERE id = ?", (nome, id_exercicio))
    if grupo_muscular:
        cursor.execute("UPDATE exercicios SET grupo_muscular = ? WHERE id = ?", (grupo_muscular, id_exercicio))
    if equipamento:
        cursor.execute("UPDATE exercicios SET equipamento = ? WHERE id = ?", (equipamento, id_exercicio))
    if descricao:
        cursor.execute("UPDATE exercicios SET descricao = ? WHERE id = ?", (descricao, id_exercicio))
    conexao.commit()
    print('Exercício editado com sucesso!')


def excluir_exercicio():
    print('| Excluir Exercício |')
    listar_exercicios()
    try:
        id_exercicio = int(input('Digite o ID do exercício: '))
    except ValueError:
        print('ID inválido.')
        return
    cursor.execute("DELETE FROM exercicios WHERE id = ?", (id_exercicio,))
    conexao.commit()
    print('Exercício excluído com sucesso!')


def menu_exercicios():
    while True:
        print("\n| EXERCÍCIOS |")
        print("1 - Cadastrar exercício")
        print("2 - Listar exercícios")
        print("3 - Editar exercício")
        print("4 - Excluir exercício")
        print("0 - Voltar")
        opcao = input("Escolha: ")
        if opcao == "1":
            cadastrar_exercicio()
        elif opcao == "2":
            listar_exercicios()
        elif opcao == "3":
            editar_exercicio()
        elif opcao == "4":
            excluir_exercicio()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def adicionar_exercicios_ao_treino(treino_id):
    """Loop para adicionar 1 ou mais exercícios a um treino já existente."""
    cursor.execute("SELECT COALESCE(MAX(ordem), 0) FROM treino_exercicios WHERE treino_id = ?", (treino_id,))
    ordem = cursor.fetchone()[0] + 1

    while True:
        listar_exercicios()
        try:
            exercicio_id = int(input('Digite o ID do exercício a adicionar (0 para parar): '))
        except ValueError:
            print('ID inválido.')
            continue
        if exercicio_id == 0:
            break
        cursor.execute("SELECT id FROM exercicios WHERE id = ?", (exercicio_id,))
        if not cursor.fetchone():
            print('Exercício não encontrado.')
            continue
        try:
            series = int(input('Número de séries: '))
            repeticoes = int(input('Número de repetições: '))
            carga = float(input('Carga (kg): '))
            descanso = int(input('Descanso entre séries (segundos): '))
        except ValueError:
            print('Valor inválido, exercício não adicionado.')
            continue
        cursor.execute("""
            INSERT INTO treino_exercicios
            (treino_id, exercicio_id, series, repeticoes, carga, descanso_segundos, ordem)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (treino_id, exercicio_id, series, repeticoes, carga, descanso, ordem))
        conexao.commit()
        ordem += 1
        print('Exercício adicionado ao treino!')


def cadastrar_treino():
    print('| Cadastro de Treino |')
    nome = input('Nome do treino (ex: Treino A - Peito/Tríceps): ')
    objetivo = input('Objetivo (ex: Hipertrofia, Perda de peso, Condicionamento): ')
    nivel = input('Nível (Iniciante/Intermediário/Avançado): ')

    listar_alunos()
    try:
        aluno_id = int(input('ID do aluno vinculado: '))
    except ValueError:
        print('ID inválido.')
        return

    cursor.execute("SELECT id FROM alunos WHERE id = ?", (aluno_id,))
    if not cursor.fetchone():
        print('Aluno não encontrado. Cadastre o aluno primeiro.')
        return

    data_criacao = date.today().strftime('%d/%m/%Y')

    cursor.execute("""
        INSERT INTO treinos (nome, objetivo, nivel, aluno_id, data_criacao)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, objetivo, nivel, aluno_id, data_criacao))
    conexao.commit()

    treino_id = cursor.lastrowid
    print(f'Treino cadastrado com sucesso! (ID: {treino_id})')

    adicionar = input('Deseja adicionar exercícios a este treino agora? (s/n): ')
    if adicionar.lower() == 's':
        adicionar_exercicios_ao_treino(treino_id)


def listar_treinos():
    cursor.execute("""
        SELECT treinos.id, treinos.nome, treinos.objetivo, treinos.nivel,
               alunos.nome, treinos.data_criacao
        FROM treinos
        LEFT JOIN alunos ON alunos.id = treinos.aluno_id
    """)
    treinos = cursor.fetchall()
    if not treinos:
        print("Nenhum treino cadastrado.")
        return
    for treino in treinos:
        print(f'''
ID: {treino[0]}
Nome: {treino[1]}
Objetivo: {treino[2]}
Nível: {treino[3]}
Aluno: {treino[4] or "(sem vínculo)"}
Criado em: {treino[5]}
''')


def ver_treino_detalhado():
    print('| Detalhes do Treino |')
    listar_treinos()
    try:
        treino_id = int(input('Digite o ID do treino: '))
    except ValueError:
        print('ID inválido.')
        return
    cursor.execute("""
        SELECT treinos.nome, treinos.objetivo, treinos.nivel,
               alunos.nome, treinos.data_criacao
        FROM treinos
        LEFT JOIN alunos ON alunos.id = treinos.aluno_id
        WHERE treinos.id = ?
    """, (treino_id,))
    treino = cursor.fetchone()
    if not treino:
        print('Treino não encontrado.')
        return
    print(f'''
Treino: {treino[0]}
Objetivo: {treino[1]}
Nível: {treino[2]}
Aluno: {treino[3] or "(sem vínculo)"}
Criado em: {treino[4]}
''')
    cursor.execute("""
        SELECT exercicios.nome, treino_exercicios.series, treino_exercicios.repeticoes,
               treino_exercicios.carga, treino_exercicios.descanso_segundos, treino_exercicios.ordem
        FROM treino_exercicios
        JOIN exercicios ON exercicios.id = treino_exercicios.exercicio_id
        WHERE treino_exercicios.treino_id = ?
        ORDER BY treino_exercicios.ordem
    """, (treino_id,))
    exercicios = cursor.fetchall()
    if not exercicios:
        print('Nenhum exercício cadastrado neste treino ainda.')
        return
    print('Exercícios:')
    for exercicio in exercicios:
        print(f'  {exercicio[5]}. {exercicio[0]} - {exercicio[1]}x{exercicio[2]} - {exercicio[3]}kg - descanso {exercicio[4]}s')


def editar_treino():
    print('| Editar Treino |')
    listar_treinos()
    try:
        treino_id = int(input('Digite o ID do treino: '))
    except ValueError:
        print('ID inválido.')
        return
    cursor.execute("SELECT * FROM treinos WHERE id = ?", (treino_id,))
    treino = cursor.fetchone()
    if not treino:
        print('Treino não encontrado.')
        return
    print('Deixe em branco para manter o valor atual.')
    nome = input('Novo nome: ')
    objetivo = input('Novo objetivo: ')
    nivel = input('Novo nível: ')
    if nome:
        cursor.execute("UPDATE treinos SET nome = ? WHERE id = ?", (nome, treino_id))
    if objetivo:
        cursor.execute("UPDATE treinos SET objetivo = ? WHERE id = ?", (objetivo, treino_id))
    if nivel:
        cursor.execute("UPDATE treinos SET nivel = ? WHERE id = ?", (nivel, treino_id))
    conexao.commit()
    print('Treino editado com sucesso!')

    resposta = input('Deseja adicionar mais exercícios a este treino? (s/n): ')
    if resposta.lower() == 's':
        adicionar_exercicios_ao_treino(treino_id)


def excluir_treino():
    print('| Excluir Treino |')
    listar_treinos()
    try:
        treino_id = int(input('Digite o ID do treino: '))
    except ValueError:
        print('ID inválido.')
        return
    cursor.execute("DELETE FROM treino_exercicios WHERE treino_id = ?", (treino_id,))
    cursor.execute("DELETE FROM historico_execucoes WHERE treino_id = ?", (treino_id,))
    cursor.execute("DELETE FROM treinos WHERE id = ?", (treino_id,))
    conexao.commit()
    print('Treino excluído com sucesso!')


def registrar_execucao():
    print('| Registrar Execução de Treino |')
    listar_treinos()
    try:
        treino_id = int(input('Digite o ID do treino executado: '))
    except ValueError:
        print('ID inválido.')
        return
    cursor.execute("SELECT aluno_id FROM treinos WHERE id = ?", (treino_id,))
    treino = cursor.fetchone()
    if not treino:
        print('Treino não encontrado.')
        return
    aluno_id = treino[0]
    data_execucao = date.today().strftime('%d/%m/%Y')
    resposta = input('O treino foi concluído? (s/n): ')
    concluido = 1 if resposta.lower() == 's' else 0
    observacoes = input('Observações (opcional): ')
    cursor.execute("""
        INSERT INTO historico_execucoes (treino_id, aluno_id, data_execucao, concluido, observacoes)
        VALUES (?, ?, ?, ?, ?)
    """, (treino_id, aluno_id, data_execucao, concluido, observacoes))
    conexao.commit()
    print('Execução registrada com sucesso!')


def listar_historico():
    print('| Histórico de Execuções |')
    cursor.execute("""
        SELECT historico_execucoes.id, treinos.nome, alunos.nome,
               historico_execucoes.data_execucao, historico_execucoes.concluido,
               historico_execucoes.observacoes
        FROM historico_execucoes
        JOIN treinos ON treinos.id = historico_execucoes.treino_id
        LEFT JOIN alunos ON alunos.id = historico_execucoes.aluno_id
        ORDER BY historico_execucoes.data_execucao DESC
    """)
    historico = cursor.fetchall()
    if not historico:
        print('Nenhuma execução registrada ainda.')
        return
    for registro in historico:
        status = 'Concluído' if registro[4] == 1 else 'Não concluído'
        print(f'''
ID: {registro[0]}
Treino: {registro[1]}
Aluno: {registro[2] or "(sem vínculo)"}
Data: {registro[3]}
Status: {status}
Observações: {registro[5]}
''')


def historico_por_aluno():
    print('| Histórico por Aluno |')
    listar_alunos()
    try:
        aluno_id = int(input('Digite o ID do aluno: '))
    except ValueError:
        print('ID inválido.')
        return
    cursor.execute("""
        SELECT treinos.nome, historico_execucoes.data_execucao,
               historico_execucoes.concluido, historico_execucoes.observacoes
        FROM historico_execucoes
        JOIN treinos ON treinos.id = historico_execucoes.treino_id
        WHERE historico_execucoes.aluno_id = ?
        ORDER BY historico_execucoes.data_execucao DESC
    """, (aluno_id,))
    historico = cursor.fetchall()
    if not historico:
        print('Nenhuma execução encontrada para este aluno.')
        return
    for registro in historico:
        status = 'Concluído' if registro[2] == 1 else 'Não concluído'
        print(f'''
Treino: {registro[0]}
Data: {registro[1]}
Status: {status}
Observações: {registro[3]}
''')

def menu_treinos():
    while True:
        print("\n| TREINOS |")
        print("1 - Cadastrar treino")
        print("2 - Listar treinos")
        print("3 - Ver treino detalhado")
        print("4 - Editar treino")
        print("5 - Excluir treino")
        print("6 - Gerenciar exercícios")
        print("7 - Registrar execução de treino")
        print("8 - Listar histórico de execuções")
        print("9 - Histórico por aluno")
        print("0 - Voltar")
        opcao = input("Escolha: ")
        if opcao == "1":
            cadastrar_treino()
        elif opcao == "2":
            listar_treinos()
        elif opcao == "3":
            ver_treino_detalhado()
        elif opcao == "4":
            editar_treino()
        elif opcao == "5":
            excluir_treino()
        elif opcao == "6":
            menu_exercicios()
        elif opcao == "7":
            registrar_execucao()
        elif opcao == "8":
            listar_historico()
        elif opcao == "9":
            historico_por_aluno()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu_treinos()


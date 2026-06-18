import sqlite3

conexao = sqlite3.connect("academia.db")

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    cargo TEXT NOT NULL,
    salario REAL NOT NULL,
    telefone TEXT,
    horario TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS planos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    valor REAL NOT NULL,
    duracao TEXT NOT NULL
)
""")

conexao.commit()

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
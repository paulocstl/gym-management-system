
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "rb") as f:
            return pickle.load(f)
    return []

def salvar(treinos):
    with open(ARQUIVO, "wb") as f:
        pickle.dump(treinos, f)

def cadastrar_treino():
    treinos = carregar()

    nome = input("Nome do treino: ").strip()
    tipo = input("Tipo (ex: Musculação, Cardio, Funcional): ").strip()
    nivel = input("Nível (Iniciante / Intermediário / Avançado): ").strip()
    duracao = input("Duração em minutos: ").strip()

    treino = {
        "id": len(treinos) + 1,
        "nome": nome,
        "tipo": tipo,
        "nivel": nivel,
        "duracao": duracao,
        "exercicios": []    
    }

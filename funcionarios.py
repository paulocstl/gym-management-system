funcionarios = []

def cadastro_funcionarios():
    print('===Cadastro de Funcionário===')
    nome = input('Nome: ')
    cpf = input('CPF: ')
    cargo = input('Cargo: ')
    salario = float(input('Salário: '))
    telefone = input('Telefone: ')
    horario = input('Horário de trabalho: ')

    funcionario = {
        'nome': nome,
        'cpf': cpf,
        'cargo': cargo,
        'salario': salario,
        'telefone': telefone,
        'horario': horario
    }
    funcionarios.append(funcionario)
    print('Funcionário cadastrado com sucesso!')

def listar_funcionarios():
    for funcionario in funcionarios:
        print(f'Nome: {funcionario["nome"]}')


def menu_funcionarios():

    while True:

        print("\n=== FUNCIONÁRIOS ===")
        print("1 - Cadastrar funcionário")
        print("2 - Listar funcionários")
        print('3 - Editar funcionário')
        print("4 - Excluir funcionário")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "0":
            break
        elif opcao == '1':
            cadastro_funcionarios()
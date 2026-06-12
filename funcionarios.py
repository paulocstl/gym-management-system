'''sistema para cadastro de funcionário'''

funcionarios = []

def cadastro_funcionarios():
    print('| Cadastro de Funcionário |')
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

# Terminar função de editar funcionário 

def editar_funcionario():
    print('| Editar Funcionário |')
    cpf = input('Digite o CPF do funcionário a ser editado: ')
    for funcionario in funcionarios:
        if funcionario['cpf'] == cpf:
            print('Funcionario encontrado. Digite os novos dados ou deixe em branco para manter o dado')
            nome = input('Digite o novo nome: ')
            cargo = input('Digite o novo cargo:')
            salario = input('Digite o novo salário: ')
            telefone = input('Digite o novo telefone: ')
            horario = input('Digite o novo horário de trabalho: ')

#Fazer teste para ver funcionamento 

def menu_funcionarios():

    while True:

        print("| FUNCIONÁRIOS |")
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

#perguntar se tem algo a mudar para o professor             
import database
database.criar_tabela()
database.extrato()
import cadastro
import login
import menu
from datetime import datetime

print("""\n=== Bem-vindo ao OtanerBank! ===

O OtanerBank é um projeto desenvolvido por um estudante amante da programação
e desenvolvimento de sistemas. Criado com o objetivo de praticar e aprimorar
seu conhecimento, lógica, e criação de aplicações, o projeto busca simular o
funcionamento básico de um banco digital, você pode criar sua conta, fazer
login, depositar, sacar, transferir e ver o extrato.""")

while True:
    try:
        escolha = int(input("""\nO que deseja fazer?

    1 - Criar uma conta.
    2 - Entrar em uma conta existente.
    3 - Sair.

"""))

    except ValueError:
        print("\nDigite o número da opção escolhido.")
        continue

    if escolha == 1:

        tipo = "Cadastro"
        usuario = cadastro.cadastrar_usuario()
        nome = cadastro.criar_nome()
        senha = cadastro.criar_senha()

        data =  datetime.now()
        data = data.strftime("%d/%m/%Y às %H:%M:%S")

        database.salvar_extrato(usuario, tipo, data = data, valor = None, usuario_relacionado = None)

        database.salvar_dados(usuario, nome, senha)

        print("\nConta criada com sucesso!")

        while True:

            quer_fz_login = input('\nDeseja realizar login agora? Digite "Sim" ou "Não": ').lower().replace("não", "nao")

            if quer_fz_login == "sim":
                resultado_login = login.fazer_login()

                if resultado_login:
                    usuario_logado = resultado_login[1]
                    menu.menu(usuario_logado)

                exit()

            elif quer_fz_login == "nao":
                print("\nOk, obrigado por usar OtanerBank, volte quando quiser!")
                exit()

            else:
                print('\nDigite apenas "Sim" ou "Não".')

    elif escolha == 2:
        resultado_login = login.fazer_login()

        if resultado_login:
            usuario_logado = resultado_login[1]
            menu.menu(usuario_logado)

    elif escolha == 3:

        confirmacao = input('\nDeseja realmente sair? Digite "Sim" ou "Não": ').lower().replace("não", "nao")

        if confirmacao == "sim":
            print("\nVocê saiu!") 

            while True:
                enter = input("\nPressione Enter para entrar novamente. ")
                if enter == "":
                    break

                else:
                    continue

    else:
        print("\nEscolha uma opção válida.")
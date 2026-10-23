import sqlite3
from datetime import datetime
import database
import hashlib

def obter_saldo(usuario):
    conexao = sqlite3.connect("banco_de_dados.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT saldo FROM usuarios WHERE usuario = ?",
                   (usuario,)
    )

    saldo = cursor.fetchone()[0]
    conexao.close()

    return saldo

def depositar(usuario):
    tipo =  "Depósito"
    while True:
        try:
            valor_deposito = float(input("\n=== Depósito ===\nDigite o valor que você deseja depositar: ").replace(",","."))

        except ValueError:
            print("\nDigite um valor válido.")
            continue

        if valor_deposito <= 0:
            print("\nVocê não pode depositar um valor menor ou igual a R$ 0,00. Digite outro valor.")
            continue
            
        else:
            deposito_outro_valor = False
            while True:
                escolha = input(f'\nDeseja depositar R$ {valor_deposito:,.2f}? Digite "Sim" ou "Não": ').lower().replace("não", "nao").strip()

                if escolha == "sim":
                    confirmar_senha = input("\nOk, verifique sua senha: ")
                    cod = confirmar_senha.encode("utf-8")
                    hash_senha = hashlib.sha256(cod).hexdigest()
            
                    conexao = sqlite3.connect("banco_de_dados.db")
                    cursor = conexao.cursor()
                    conexao = sqlite3.connect("banco_de_dados.db")
                    cursor = conexao.cursor()

                    cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?",
                                (usuario,)
                    )

                    resultado = cursor.fetchone()

                    if resultado and resultado[0] == hash_senha:
                        saldo_atual = obter_saldo(usuario)
                        novo_saldo = saldo_atual + valor_deposito

                        cursor.execute("UPDATE usuarios SET saldo = ? WHERE usuario = ?",
                                    (novo_saldo, usuario)
                        )

                        conexao.commit()
                        conexao.close()

                        print(f"\nR$ {valor_deposito:,.2f} depositado com sucesso! Seu saldo atual é de {novo_saldo:,.2f}. ")
                        data =  datetime.now()
                        data = data.strftime("%d/%m/%Y às %H:%M:%S")

                        database.salvar_extrato(usuario, tipo, valor_deposito, data, usuario_relacionado = None)

                        return

                    else: 
                        conexao.close()
                        print("\nSenha incorreta. Depósito cancelado.")

                        while True:
                            escolha = input("""\nO que deseja fazer?
                        
    1 - Depositar outro valor
    2 - Voltar ao menu

""")
                            if escolha == "1":
                                deposito_outro_valor = True
                                break

                            elif escolha == "2":
                                return

                            else:
                                print("\nDigite um valor válido.")
                                continue
            
                if deposito_outro_valor:
                    break

                elif escolha == "nao":
                    
                    while True:
                        escolha = input("""\nOk, o que deseja fazer?
                            
    1 - Depositar outro valor
    2 - Voltar ao menu

""")
                        if escolha == "1":
                            deposito_outro_valor = True
                            break
        
                        elif escolha == "2":
                            return

                        else:
                            print("\nDigite um valor válido.")
                            continue
                    
                if deposito_outro_valor:
                    break
                    
                else:
                    print('Digite "Sim" ou "Não".')
                    continue

def sacar(usuario):
    tipo = "Saque"
    saldo = obter_saldo(usuario)
    while True:
        try:
            valor_saque = float(input("\n=== Saque ===\nDigite o valor que você deseja sacar: ").replace(",","."))

        except ValueError:
            print("\nDigite um valor válido.")
            continue

        if valor_saque > saldo:
            print(f"\nVocê não pode sacar um valor maior que seu saldo atual (R$ {saldo:,.2f}). Digite outro valor.")
            continue

        elif valor_saque <= 0:
                    print("\nVocê não pode sacar um valor menor ou igual a R$ 0,00. Digite outro valor.")
                    continue

        else:
            saque_outro_valor = False
            while True:
                escolha = input(f'\nDeseja sacar R$ {valor_saque:,.2f}? Digite "Sim" ou "Não": ').lower().replace("não","nao").strip()

                if escolha == "sim":
                    confirmar_senha = input("\nOk, verifique sua senha: ")
                    cod = confirmar_senha.encode("utf-8")
                    hash_senha = hashlib.sha256(cod).hexdigest()
                    conexao = sqlite3.connect("banco_de_dados.db")
                    cursor = conexao.cursor()

                    cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?",
                    (usuario,)
                    )

                    resultado = cursor.fetchone()

                    if resultado and resultado[0] == hash_senha:

                        saldo_atual = obter_saldo(usuario)
                        novo_saldo = saldo_atual - valor_saque

                        cursor.execute("UPDATE usuarios SET saldo = ? WHERE usuario = ?",
                        (novo_saldo, usuario)
                        )

                        conexao.commit()
                        conexao.close()

                        print(f"\nR$ {valor_saque:,.2f} sacado com sucesso! Seu saldo atual é de {novo_saldo:,.2f}.")
                        data =  datetime.now()
                        data = data.strftime("%d/%m/%Y às %H:%M:%S")

                        database.salvar_extrato(usuario, tipo, valor_saque, data, usuario_relacionado = None)

                        return

                    else:
                        conexao.close() 
                        print("\nSenha incorreta. Saque cancelado.")
                        
                        while True:
                            
                            escolha = input("""\nO que deseja fazer?
                                                    
    1 - Sacar outro valor
    2 - Voltar ao menu
                        
""")
                            if escolha == "1":
                                saque_outro_valor = True
                                break
                                
                            elif escolha == "2":
                                return

                            else:
                                print("\nDigite um valor válido.")
                                continue

                if saque_outro_valor:
                    break

                elif escolha == "nao":
                    
                    while True:
                        escolha = input("""\nOk, o que deseja fazer?
                                        
    1 - Sacar outro valor
    2 - Voltar ao menu
                
""")
                        if escolha == "1":
                            saque_outro_valor = True
                            break
                            
                        elif escolha == "2":
                            return
                    
                        else:
                            print("\nDigite um valor válido.")
                            continue

                if saque_outro_valor:
                    break
            
                else:
                    print('\nDigite "Sim" ou "Não".')
                    continue

def transferir(usuario):
    tipo = "Transferência"
    saldo = obter_saldo(usuario)
    print("\n=== Transferência ===")
    while True:
        voltar_para_nome = False
        destinatario = input("\nDigite o nome de usuario da pessoa que você deseja enviar a transferência: ").strip()

        if destinatario == usuario:
            print("\nVocê não pode efetuar uma transferência para si mesmo.")
            continue

        conexao = sqlite3.connect("banco_de_dados.db")
        cursor = conexao.cursor()
        
        cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ?",
        (destinatario,)
        )
        
        resultado = cursor.fetchone()
        conexao.close()

        if resultado is None:
            print("\nUsuário não encontrado. Digite-o corretamente.")
            continue

        elif destinatario == resultado[1]:
            while True:
                nome = resultado[2]
                partes = nome.split()

                try:
                    valor_transferencia = float(input(f"\nDigite o valor que deseja transferir para {partes[0]} {partes[-1][0]}.: ").replace(",","."))

                    if valor_transferencia <= 0:
                        print("Você não pode transferir um valor menor ou igual a R$ 0,00. Tente novamente.")
                        continue

                    elif valor_transferencia > saldo:
                        print(f"\nVocê não pode transferir um valor maior que seu saldo atual (R$ {saldo:,.2f}). Digite outro valor.")
                        continue

                    else:
                        transfere_outro_valor = False
                        while True:
                            escolha = input(f'\nDeseja transferir R$ {valor_transferencia:,.2f} para {partes[0]} {partes[-1][0]}.? Digite "Sim" ou "Não": ').lower().replace("não","nao").strip()

                            if escolha == "sim":
                                confirmar_senha = input("\nOk, verifique sua senha: ")
                                cod = confirmar_senha.encode("utf-8")
                                hash_senha = hashlib.sha256(cod).hexdigest()

                                conexao = sqlite3.connect("banco_de_dados.db")
                                cursor = conexao.cursor()

                                cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?",
                                (usuario,)
                                )

                                resultado_senha = cursor.fetchone()

                                if resultado_senha and resultado_senha[0] == hash_senha:

                                    saldo_atual = obter_saldo(usuario)
                                    novo_saldo = saldo_atual - valor_transferencia

                                    cursor.execute("UPDATE usuarios SET saldo = ? WHERE usuario = ?",
                                    (novo_saldo, usuario)
                                    )

                                    saldo_atual_destinatario = obter_saldo(destinatario)
                                    novo_saldo_destinatario = saldo_atual_destinatario + valor_transferencia

                                    cursor.execute("UPDATE usuarios SET saldo = ? WHERE usuario = ?",
                                    (novo_saldo_destinatario, destinatario)
                                    )

                                    conexao.commit()
                                    conexao.close()
                                    print(f"\nR$ {valor_transferencia:,.2f} transferido para {partes[0]} {partes[-1][0]}. com sucesso! Seu saldo atual é de {novo_saldo:,.2f}.")

                                    data =  datetime.now()
                                    data = data.strftime("%d/%m/%Y às %H:%M:%S")

                                    database.salvar_extrato(usuario, "Transferência enviada", valor_transferencia, data, destinatario)
                                    database.salvar_extrato(destinatario, "Transferência recebida", valor_transferencia, data, usuario)

                                    return

                                else: 
                                    conexao.close()
                                    print("\nSenha incorreta. Transferência cancelado.")
                                    
                                    while True:
                                        escolha = input("""\nO que deseja fazer?
                        
    1 - Transferir outro valor
    2 - Voltar ao menu

""")
                                        if escolha == "1":
                                            transfere_outro_valor = True
                                            break

                                        elif escolha == "2":
                                            return

                                        else:
                                            print("\nDigite um valor válido.")
                                            continue

                                if transfere_outro_valor:
                                    break

                            elif escolha == "nao":
                                while True:
                                    escolha = input("""\nOk, o que deseja fazer?
                        
    1 - Transferir o valor
    2 - Trocar o destinatário
    3 - Voltar ao menu
    
""")
                                    if escolha == "1":
                                        transfere_outro_valor = True
                                        break   

                                    elif escolha == "2":
                                        voltar_para_nome = True
                                        break
                        
                                    elif escolha == "3":
                                        return

                                    else:
                                        print("\nDigite um valor válido.")
                                    continue

                                if transfere_outro_valor:
                                    break
                                
                            else:
                                print('\nDigite "Sim" ou "Não".')
                                continue

                            if voltar_para_nome:
                                break

                    if voltar_para_nome:
                        break

                except ValueError:
                    print("\nDigite um valor válido.")
                    continue

def ver_extrato(usuario):
    conexao = sqlite3.connect("banco_de_dados.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM extrato WHERE usuario = ?",
                    (usuario,)
        )
    extrato = cursor.fetchall()
    extrato = extrato[::-1]
    conexao.close()

    for transacoes in extrato:
        tipo = transacoes[2]
        valor = transacoes[3]
        data = transacoes[4]
        relacionado = transacoes[5]

        if relacionado:
            conexao = sqlite3.connect("banco_de_dados.db")
            cursor = conexao.cursor()

            cursor.execute(
            "SELECT nome FROM usuarios WHERE usuario = ?",
            (relacionado,)
            )

            resultado = cursor.fetchone()
            conexao.close()

            nome = resultado[0]
            partes = nome.split()

        if tipo == "Saque":
            print(f"\n{tipo} // {data}\nR$ -{valor:,.2f}")

        elif tipo == "Depósito":
            print(f"\n{tipo} // {data}\nR$ +{valor:,.2f}")

        elif tipo == "Transferência recebida":
            print(f"\n{tipo} de {partes[0]} {partes[-1][0]}. // {data}\nR$ +{valor:,.2f}")

        elif tipo == "Transferência enviada":
            print(f"\n{tipo} para {partes[0]} {partes[-1][0]}. // {data}\nR$ -{valor:,.2f}")

        elif tipo == "Cadastro":
            print(f"\nUsuário cadastrado em {data}")

    while True:
        enter = input("\nPressione Enter para voltar ao menu. ")
        if enter == "":
            return True

        else:
            continue

def alterar_senha(usuario):
    while True:
        senha = input("""\n=== Alterar senha ===
A senha deve ter pelo menos 8 caracteres, contendo letras maiúsculas, minúsculas, números e caracteres especiais, como !@#$%&*.

Digite sua senha: """)
        cod = senha.encode("utf-8")
        hash_senha = hashlib.sha256(cod).hexdigest()

        conexao = sqlite3.connect("banco_de_dados.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?",
                    (usuario,)
        )

        resultado = cursor.fetchone()

        while True:
            if resultado and resultado[0] == hash_senha:
                nova_senha = input("\nDigite a nova senha escolhida: ")
                cod = nova_senha.encode("utf-8")
                hash_nova_senha = hashlib.sha256(cod).hexdigest()

                if len(nova_senha) < 8:
                    print("A senha deve ter pelo menos 8 caracteres.")
                    continue

                elif not any(caractere.isdigit() for caractere in nova_senha):
                    print("A senha deve conter pelo menos um número.")
                    continue

                elif not any(caractere.isupper() for caractere in nova_senha) or not any(caractere.islower() for caractere in nova_senha):
                    print("A senha deve conter letras maiúsculas e minúsculas.")
                    continue

                elif not any(not caractere.isalnum() for caractere in nova_senha):
                    print("A senha deve conter pelo menos um caractere especial.")
                    continue

                confirmar_senha = input("Confirme a nova senha: ")

                if nova_senha != confirmar_senha:
                    print("As senhas não se coincidem. Tente novamente.")
                    continue

                else:
                    cursor.execute("UPDATE usuarios SET senha = ? WHERE usuario = ?",
                    (hash_nova_senha, usuario)
                    )  

                    conexao.commit()
                    conexao.close()

                    print("\nSenha alterada com sucesso!")
                    return

            else: 
                conexao.close()
                print("Senha incorreta. Tente novamente!")
                break

def excluir_conta(usuario):
    while True:
        confirmacao = input('\nTem certeza que quer excluir sua conta? Essa ação não poderá ser desfeita. Digite "Sim" ou "Não": ').lower().replace("não", "nao").strip()
        
        if confirmacao == "sim":
            confirmar_senha = input("\nOk, verifique sua senha: ")
            cod = confirmar_senha.encode("utf-8")
            hash_senha = hashlib.sha256(cod).hexdigest()
    
            conexao = sqlite3.connect("banco_de_dados.db")
            cursor = conexao.cursor()
            conexao = sqlite3.connect("banco_de_dados.db")
            cursor = conexao.cursor()

            cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?",
                        (usuario,)
            )

            resultado = cursor.fetchone()

            if resultado and resultado[0] == hash_senha:
                conexao = sqlite3.connect("banco_de_dados.db")
                cursor = conexao.cursor()
            
                cursor.execute("""DELETE FROM usuarios WHERE usuario = ?""",
                (usuario,))
            
                conexao.commit()
                conexao.close()

                print("\nConta excluída com sucesso. Obrigado por usar OtanerBank.")
                while True:
                    enter = input("\nPressione Enter para entrar novamente. ")
                    if enter == "":
                        return True
    
                    else:
                        continue
        
            else: 
                print("\nSenha incorreta. Exclusão cancelada.")
                return

        elif confirmacao == "nao":
            return
            
        else:
            print('\nDigite apenas "Sim" ou "Não".')
            continue

def sair(usuario):
    while True:
        confirmacao = input('\nDeseja realmente sair? Digite "Sim" ou "Não": ').lower().replace("não", "nao").strip()

        if confirmacao == "sim":
            print("\nVocê saiu!")
            while True:
                enter = input("\nPressione Enter para entrar novamente. ")
                if enter == "":
                    return True

                else:
                    continue

        elif confirmacao == "nao":
            return False
            
        else:
            print('\nDigite apenas "Sim" ou "Não".')
            continue

def menu(usuario):
    while True:
        try:
            escolha = int(input("""\n=== Menu ===
O que deseja fazer?

    1 - Depositar
    2 - Sacar
    3 - Transferir
    4 - Extrato
    5 - Alterar senha
    6 - Sair
    7 - Excluir conta

"""))

            if escolha == 1:
                depositar(usuario)
                
            elif escolha == 2:
                sacar(usuario)
                
            elif escolha == 3:
                transferir(usuario)
                
            elif escolha == 4:
                ver_extrato(usuario)
                
            elif escolha == 5:
                alterar_senha(usuario)
            
            elif escolha == 6:
                if sair(usuario):
                    return True

            elif escolha == 7:
                if excluir_conta(usuario):
                    return
                
            else:
                print("\nDigite um valor válido.")
                continue

        except ValueError:
            print("\nDigite o número da opção escolhida.")
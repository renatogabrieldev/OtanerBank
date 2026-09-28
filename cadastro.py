import database
import hashlib
from datetime import datetime 

def cadastrar_usuario():

    print("""\n=== Crie seu nome de usuário! ===
O nome de usuário devem incluir de 3 a 20 caracteres e podem incluir letras, números, sublinhados e pontos.""")
    
    while True:
        usuario = input("\nDigite o nome de usuario: ").lower()

        if len(usuario) < 3 or len(usuario) > 20:
            print("O nome de usuário deve ter entre 3 a 20 caractere.")
            continue

        elif usuario[0] == "." or usuario[-1] == ".":
            print("O nome de usuário não pode começar nem terminar com pontos.")
            continue

        elif ".." in usuario or "__" in usuario:
            print("O nome não pode conter dois ou mais pontos e sublinhados seguidos.")
            continue

        elif not any(caractere.isalpha() for caractere in usuario):
            print("Seu nome de usuário deve conter letras.")
            continue

        elif database.usuario_existe(usuario):
            print("Esse usuário já existe.")
            continue

        valido = True

        for caractere in usuario:
            if not (caractere.isalnum() or caractere in "._" ):
                valido = False
                break

        if not valido:
            print("o usuário não pode conter caracteres especiais além de pontos e sublinhados.")
            continue

        return usuario

def criar_nome():

    print("""\n=== Insira seu nome! ===
Você deve inserir seu primeiro e segundo nome. Ele eve conter apenas letras.""")

    while True:
        nome = input("\nDigite seu nome: ").title()

        if len(nome) < 3:
            print("\nSeu nome deve conter pelo menos 3 caracteres.")
            continue

        valido = True

        for caractere in nome:
            if not (caractere.isalpha() or caractere in " "):
                valido = False
                break

        if not valido:
            print("\nSeu nome deve conter apenas letras.")
            continue

        partes = nome.split()

        if len(partes) < 2:
            print("\nDigite também seu segundo nome.")
            continue

        elif len(partes[1]) < 3:
            print("\nSeu segundo nome também deve conter pelo menos 3 caracteres.")
            continue
            
        break

    return nome

def criar_senha():

    print("""\n=== Crie sua senha! ===
A senha deve ter pelo menos 8 caracteres, contendo letras maiúsculas, minúsculas, números e caracteres especiais, como !@#$%&*.""")

    while True:
        senha = input("\nDigite a senha: ")
        cod = senha.encode("utf-8")
        hash_senha = hashlib.sha256(cod).hexdigest()

        if len(senha) < 8:
            print("A senha deve ter pelo menos 8 caracteres.")
            continue

        elif not any(caractere.isdigit() for caractere in senha):
            print("A senha deve conter pelo menos um número.")
            continue

        elif not any(caractere.isupper() for caractere in senha) or not any(caractere.islower() for caractere in senha):
            print("A senha deve conter letras maiúsculas e minúsculas.")
            continue

        elif not any(not caractere.isalnum() for caractere in senha):
            print("A senha deve conter pelo menos um caractere especial.")
            continue

        confirmar_senha = input("Confirme sua senha: ")

        if confirmar_senha != senha:
            print("A senhas precisam ser iguais.")
            continue

        return hash_senha
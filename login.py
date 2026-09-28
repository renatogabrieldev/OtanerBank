import sqlite3
import hashlib

def fazer_login():
    tentativa = 1

    print(f"""\n=== Faça o login! ===
Para realizar login, digite seu nome de usuário e sua senha. Você terá 5 tentativas.

=== Tentativa {tentativa} ===""")

    while True:
        usuario = input("\nDigite seu nome de usuário: ")
        senha = input("\nDigite sua senha: ")

        cod = senha.encode("utf-8")
        hash_senha = hashlib.sha256(cod).hexdigest()

        conexao = sqlite3.connect("banco_de_dados.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = ? AND senha = ?",
            (usuario, hash_senha)
        )

        resultado = cursor.fetchone()
        conexao.close()
        

        if resultado:
            nome = resultado[2]
            partes = nome.split()

            print(f"\nLogin realizado com sucesso! Olá {partes[0]} {partes[-1][0]}.")
            return resultado
            
        else:
            tentativa += 1
            if tentativa > 5:
                print("Você ultrapassou o limite máximo de tentativas")
                break

        print(f"""\n=== Tentativa {tentativa} ===
Usuário ou senha incorretos. Tente novamente!""")
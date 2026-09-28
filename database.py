import sqlite3

def criar_tabela():
    
    conexao = sqlite3.connect("banco_de_dados.db")
    cursor = conexao.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY,
    usuario TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    saldo REAL NOT NULL,
    senha TEXT NOT NULL)""")

    conexao.commit()
    conexao.close()

def salvar_dados(usuario, nome, senha):

    conexao = sqlite3.connect("banco_de_dados.db")
    cursor = conexao.cursor()

    cursor.execute("""INSERT INTO usuarios
    (usuario, nome, saldo, senha)
    VALUES (?, ?, ?, ?)""", 
    (usuario, nome, 0, senha))

    conexao.commit()
    conexao.close()

def usuario_existe(usuario):
    conexao = sqlite3.connect("banco_de_dados.db")
    cursor = conexao.cursor()

    cursor.execute("""SELECT usuario FROM usuarios WHERE usuario = ?""",
        (usuario,))

    resultado = cursor.fetchone()
    conexao.close()

    return resultado is not None

def extrato():
    conexao = sqlite3.connect("banco_de_dados.db")
    cursor = conexao.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS extrato(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    tipo TEXT NOT NULL,
    valor REAL,
    data TEXT NOT NULL,
    usuario_relacionado TEXT)""")

    conexao.commit()
    conexao.close()

def salvar_extrato(usuario, tipo, valor, data, usuario_relacionado):

    conexao = sqlite3.connect("banco_de_dados.db")
    cursor = conexao.cursor()

    cursor.execute("""INSERT INTO extrato
    (usuario, tipo, valor, data, usuario_relacionado)
    VALUES (?, ?, ?, ?, ?)""", 
    (usuario, tipo, valor, data, usuario_relacionado))

    conexao.commit()
    conexao.close()
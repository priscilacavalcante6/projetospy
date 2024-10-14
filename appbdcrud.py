import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('crud.db')
cursor = conn.cursor()

# Criar tabela de usuários se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
''')

# Função para criar um usuário
def create_user(name, email):
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        print(f"Usuário {name} criado com sucesso.")
    except sqlite3.IntegrityError:
        print("Erro: O email já existe.")

# Função para ler todos os usuários
def read_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    if users:
        for user in users:
            print(user)
    else:
        print("Nenhum usuário encontrado.")

# Função para atualizar um usuário pelo ID
def update_user(user_id, new_name, new_email):
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (new_name, new_email, user_id))
    conn.commit()
    if cursor.rowcount == 0:
        print("Usuário não encontrado.")
    else:
        print("Usuário atualizado com sucesso.")

# Função para deletar um usuário pelo ID
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    if cursor.rowcount == 0:
        print("Usuário não encontrado.")
    else:
        print("Usuário deletado com sucesso.")

# Menu CRUD
def crud_menu():
    while True:
        print("\n--- MENU CRUD ---")
        print("1. Criar usuário")
        print("2. Ler usuários")
        print("3. Atualizar usuário")
        print("4. Deletar usuário")
        print("5. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            name = input("Nome: ")
            email = input("Email: ")
            create_user(name, email)
        elif choice == '2':
            read_users()
        elif choice == '3':
            user_id = int(input("ID do usuário a ser atualizado: "))
            new_name = input("Novo nome: ")
            new_email = input("Novo email: ")
            update_user(user_id, new_name, new_email)
        elif choice == '4':
            user_id = int(input("ID do usuário a ser deletado: "))
            delete_user(user_id)
        elif choice == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executa o menu CRUD
crud_menu()

# Fechar a conexão com o banco de dados
conn.close()

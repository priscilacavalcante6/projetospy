import sqlite3
import tkinter as tk
from tkinter import messagebox

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

# Funções CRUD (modificadas para GUI)
def create_user():
    name = entry_name.get()
    email = entry_email.get()

    if name == "" or email == "":
        messagebox.showwarning("Aviso", "Todos os campos são obrigatórios")
        return

    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Usuário {name} criado com sucesso.")
        clear_entries()
        read_users()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "O email já existe.")

def read_users():
    listbox_users.delete(0, tk.END)  # Limpa a lista
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        listbox_users.insert(tk.END, user)  # Exibe cada usuário

def update_user():
    try:
        user_id = int(entry_id.get())
        new_name = entry_name.get()
        new_email = entry_email.get()

        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (new_name, new_email, user_id))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showerror("Erro", "Usuário não encontrado.")
        else:
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso.")
            clear_entries()
            read_users()
    except ValueError:
        messagebox.showerror("Erro", "ID inválido")

def delete_user():
    try:
        user_id = int(entry_id.get())
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showerror("Erro", "Usuário não encontrado.")
        else:
            messagebox.showinfo("Sucesso", "Usuário deletado com sucesso.")
            clear_entries()
            read_users()
    except ValueError:
        messagebox.showerror("Erro", "ID inválido")

def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Configuração da interface gráfica
app = tk.Tk()
app.title("Login de Usuários")
app.geometry("500x500")
app.configure(bg="#F0F0F0")
# Labels e Entradas
tk.Label(app, text="ID").pack(pady=5)
entry_id = tk.Entry(app)
entry_id.pack(pady=5)

tk.Label(app, text="Nome").pack(pady=5)
entry_name = tk.Entry(app)
entry_name.pack(pady=5)

tk.Label(app, text="Email").pack(pady=5)
entry_email = tk.Entry(app)
entry_email.pack(pady=5)

# Botões de CRUD
tk.Button(app, text="Criar", command=create_user).pack(pady=5)
tk.Button(app, text="Atualizar", command=update_user).pack(pady=5)
tk.Button(app, text="Deletar", command=delete_user).pack(pady=5)

# Lista para exibir usuários
listbox_users = tk.Listbox(app)
listbox_users.pack(pady=20, fill=tk.BOTH, expand=True)

# Carregar os usuários na lista
read_users()

# Executar o loop principal da interface gráfica
app.mainloop()

# Fechar a conexão com o banco de dados
conn.close()

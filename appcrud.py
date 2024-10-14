import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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
    listbox_users.delete(*listbox_users.get_children())  # Limpa a lista
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        listbox_users.insert("", "end", values=user)  # Exibe cada usuário

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
app.title("CRUD de Usuários Melhorado")
app.geometry("500x650")
app.resizable(False, False)

# Alterar a cor de fundo para lilás
lilas_color = "#DDA0DD"
app.configure(bg=lilas_color)

# Estilo usando ttk (não afeta a cor de fundo diretamente)
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", font=('Arial', 10))
style.configure("TLabel", padding=6, font=('Arial', 10))

# Frame para entrada de dados (alteração da cor de fundo)
frame_form = ttk.Frame(app)
frame_form.pack(pady=20, padx=10, fill="x")

# Labels e Entradas (alteração da cor de fundo dos campos)
label_id = ttk.Label(frame_form, text="ID (para Atualizar/Deletar)")
label_id.pack(anchor="w")
entry_id = ttk.Entry(frame_form)
entry_id.pack(fill="x", pady=5)

label_name = ttk.Label(frame_form, text="Nome")
label_name.pack(anchor="w")
entry_name = ttk.Entry(frame_form)
entry_name.pack(fill="x", pady=5)

label_email = ttk.Label(frame_form, text="Email")
label_email.pack(anchor="w")
entry_email = ttk.Entry(frame_form)
entry_email.pack(fill="x", pady=5)

# Frame para botões
frame_buttons = ttk.Frame(app)
frame_buttons.pack(pady=10)

# Botões de CRUD
ttk.Button(frame_buttons, text="Criar", command=create_user).pack(side="left", padx=5)
ttk.Button(frame_buttons, text="Atualizar", command=update_user).pack(side="left", padx=5)
ttk.Button(frame_buttons, text="Deletar", command=delete_user).pack(side="left", padx=5)

# Frame para exibição de usuários
frame_users = ttk.Frame(app)
frame_users.pack(pady=10, padx=10, fill="both", expand=True)

# Listbox de exibição dos usuários com scrollbar
cols = ('ID', 'Nome', 'Email')
listbox_users = ttk.Treeview(frame_users, columns=cols, show='headings')
for col in cols:
    listbox_users.heading(col, text=col)

listbox_users.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_users, orient="vertical", command=listbox_users.yview)
listbox_users.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Carregar os usuários na lista
read_users()

# Executar o loop principal da interface gráfica
app.mainloop()

# Fechar a conexão com o banco de dados
conn.close()

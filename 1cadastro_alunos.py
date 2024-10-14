import sqlite3
from tkinter import *
from tkinter import messagebox

# Função para conectar ao banco de dados
def connect():
    conn = sqlite3.connect("alunos.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            curso TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função para inserir aluno
def inserir_aluno():
    if nome_var.get() == "" or idade_var.get() == "" or curso_var.get() == "":
        messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
    else:
        conn = sqlite3.connect("alunos.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO alunos (nome, idade, curso) VALUES (?, ?, ?)", 
                    (nome_var.get(), idade_var.get(), curso_var.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Aluno inserido com sucesso!")
        limpar_campos()
        visualizar_alunos()

# Função para visualizar alunos
def visualizar_alunos():
    conn = sqlite3.connect("alunos.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM alunos")
    rows = cur.fetchall()
    conn.close()
    
    # Limpa a lista atual antes de inserir novos dados
    lista_alunos.delete(0, END)
    
    for row in rows:
        lista_alunos.insert(END, row)

# Função para selecionar um aluno
def selecionar_aluno(event):
    try:
        global aluno_selecionado
        index = lista_alunos.curselection()[0]
        aluno_selecionado = lista_alunos.get(index)
        
        # Preencher os campos com os dados do aluno selecionado
        nome_entry.delete(0, END)
        nome_entry.insert(END, aluno_selecionado[1])
        idade_entry.delete(0, END)
        idade_entry.insert(END, aluno_selecionado[2])
        curso_entry.delete(0, END)
        curso_entry.insert(END, aluno_selecionado[3])
    except IndexError:
        pass

# Função para atualizar um aluno
def atualizar_aluno():
    if nome_var.get() == "" or idade_var.get() == "" or curso_var.get() == "":
        messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
    else:
        conn = sqlite3.connect("alunos.db")
        cur = conn.cursor()
        cur.execute("UPDATE alunos SET nome = ?, idade = ?, curso = ? WHERE id = ?", 
                    (nome_var.get(), idade_var.get(), curso_var.get(), aluno_selecionado[0]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Dados do aluno atualizados com sucesso!")
        limpar_campos()
        visualizar_alunos()

# Função para deletar aluno
def deletar_aluno():
    conn = sqlite3.connect("alunos.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM alunos WHERE id = ?", (aluno_selecionado[0],))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Aluno deletado com sucesso!")
    limpar_campos()
    visualizar_alunos()

# Função para limpar os campos de entrada
def limpar_campos():
    nome_entry.delete(0, END)
    idade_entry.delete(0, END)
    curso_entry.delete(0, END)

# Interface gráfica usando Tkinter
root = Tk()
root.title("Sistema de Registro de Alunos")

# Variáveis de entrada
nome_var = StringVar()
idade_var = StringVar()
curso_var = StringVar()

# Layout
Label(root, text="Nome").grid(row=0, column=0, padx=10, pady=10)
nome_entry = Entry(root, textvariable=nome_var)
nome_entry.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Idade").grid(row=1, column=0, padx=10, pady=10)
idade_entry = Entry(root, textvariable=idade_var)
idade_entry.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Curso").grid(row=2, column=0, padx=10, pady=10)
curso_entry = Entry(root, textvariable=curso_var)
curso_entry.grid(row=2, column=1, padx=10, pady=10)

# Lista de alunos
lista_alunos = Listbox(root, height=8, width=50)
lista_alunos.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
lista_alunos.bind('<<ListboxSelect>>', selecionar_aluno)

# Botões de ação
Button(root, text="Inserir Aluno", command=inserir_aluno).grid(row=4, column=0, padx=10, pady=10)
Button(root, text="Atualizar Aluno", command=atualizar_aluno).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Deletar Aluno", command=deletar_aluno).grid(row=5, column=0, padx=10, pady=10)
Button(root, text="Limpar Campos", command=limpar_campos).grid(row=5, column=1, padx=10, pady=10)

# Iniciar o programa e conectar ao banco de dados
connect()
visualizar_alunos()

root.mainloop()

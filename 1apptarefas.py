#IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS
import sqlite3
import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter import PhotoImage

# Inicialização da variável frame_em_edicao
frame_em_edicao = None  # Variável inicializada como None

# CONFIGURAR A JANELA PRINCIPAL
janela = tk.Tk()
janela.geometry("500x600")

# Carregar ícones (assegure-se que os arquivos estão na mesma pasta que o script)
icon_editar = PhotoImage(file="icon.editar.png").subsample(3, 3)  # Ajuste conforme necessário
icon_deletar = PhotoImage(file="icon.deletar.png").subsample(3, 3)  # Ajuste conforme necessário

# Função para conectar ao banco de dados e criar a tabela, se não existir
def connect_db():
    conn = sqlite3.connect("tarefas.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarefa TEXT NOT NULL,
            status INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Função para adicionar uma tarefa ao banco de dados
def adicionar_tarefa():
    global frame_em_edicao  # Referência à variável global
    tarefa = entrada_tarefa.get().strip()
    if tarefa and tarefa != "Escreva sua tarefa aqui":
        if frame_em_edicao is not None:
            atualizar_tarefa(tarefa)
            frame_em_edicao = None
        else:
            inserir_tarefa_db(tarefa)  # Inserir tarefa no banco de dados
        entrada_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning("Entrada Inválida", "Por favor, insira uma tarefa válida.")

# ... Resto do código permanece o mesmo
# Função para adicionar item de tarefa à interface e ao banco de dados
def adicionar_item_tarefa(tarefa, id=None, status=0):
    frame_tarefa = tk.Frame(canvas_interior, bg="white", bd=1, relief=tk.SOLID)
    frame_tarefa.task_id = id  # Armazenar o ID no frame da tarefa

    label_tarefa = tk.Label(frame_tarefa, text=tarefa, font=("Garamond", 16), bg="white", width=25, height=2, anchor="w")
    label_tarefa.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)

    botao_editar = tk.Button(frame_tarefa, image=icon_editar, command=lambda f=frame_tarefa, l=label_tarefa: preparar_edicao(f, l), bg="white", relief=tk.FLAT)
    botao_editar.pack(side=tk.RIGHT, padx=5)

    botao_deletar = tk.Button(frame_tarefa, image=icon_deletar, command=lambda f=frame_tarefa: deletar_tarefa(f), bg="white", relief=tk.FLAT)
    botao_deletar.pack(side=tk.RIGHT, padx=5)

    frame_tarefa.pack(fill=tk.X, padx=5, pady=5)

    checkbutton = ttk.Checkbutton(frame_tarefa, command=lambda label=label_tarefa: alternar_sublinhado(label))
    checkbutton.pack(side=tk.RIGHT, padx=5)

    if status == 1:
        alternar_sublinhado(label_tarefa)

    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Função para inserir tarefa no banco de dados
def inserir_tarefa_db(tarefa):
    try:
        conn = sqlite3.connect("tarefas.db")
        cur = conn.cursor()
        # Inserir a tarefa e definir o status como 0 (pendente)
        cur.execute("INSERT INTO tarefas (tarefa, status) VALUES (?, ?)", (tarefa, 0))
        conn.commit()
        # Obter o ID da tarefa recém-criada e adicioná-la à interface
        tarefa_id = cur.lastrowid
        conn.close()
        adicionar_item_tarefa(tarefa, id=tarefa_id)
    except sqlite3.Error as e:
        messagebox.showerror("Erro no banco de dados", f"Erro ao inserir tarefa: {e}")

# Função para preparar a edição de uma tarefa
def preparar_edicao(frame_tarefa, label_tarefa):
    global frame_em_edicao
    frame_em_edicao = frame_tarefa
    entrada_tarefa.delete(0, tk.END)
    entrada_tarefa.insert(0, label_tarefa.cget("text"))

# Função para atualizar tarefa no banco de dados
def atualizar_tarefa(nova_tarefa):
    global frame_em_edicao
    if frame_em_edicao:
        for widget in frame_em_edicao.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(text=nova_tarefa)
                id = frame_em_edicao.task_id  # Obter o ID armazenado no frame
                atualizar_tarefa_db(id, nova_tarefa)

# Função para atualizar tarefa no banco de dados
def atualizar_tarefa_db(id, nova_tarefa):
    try:
        conn = sqlite3.connect("tarefas.db")
        cur = conn.cursor()
        cur.execute("UPDATE tarefas SET tarefa = ? WHERE id = ?", (nova_tarefa, id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Erro no banco de dados", f"Erro ao atualizar tarefa: {e}")

# Função para deletar tarefa
def deletar_tarefa(frame_tarefa):
    id = frame_tarefa.task_id  # Obter o ID armazenado no frame
    frame_tarefa.destroy()
    deletar_tarefa_db(id)
    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Função para deletar tarefa do banco de dados
def deletar_tarefa_db(id):
    try:
        conn = sqlite3.connect("tarefas.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM tarefas WHERE id = ?", (id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Erro no banco de dados", f"Erro ao deletar tarefa: {e}")

# Função para alternar sublinhado (tarefa concluída)
def alternar_sublinhado(label):
    fonte_atual = label.cget("font")
    if "overstrike" in fonte_atual:
        nova_fonte = fonte_atual.replace(" overstrike", "")
    else:
        nova_fonte = fonte_atual + " overstrike"
    label.config(font=nova_fonte)

# Função para carregar tarefas do banco de dados ao iniciar o programa
def carregar_tarefas():
    try:
        conn = sqlite3.connect("tarefas.db")
        cur = conn.cursor()
        cur.execute("SELECT id, tarefa, status FROM tarefas")
        rows = cur.fetchall()
        conn.close()
        for row in rows:
            adicionar_item_tarefa(row[1], id=row[0], status=row[2])
    except sqlite3.Error as e:
        messagebox.showerror("Erro no banco de dados", f"Erro ao carregar tarefas: {e}")

#CONFIGURAR A ENTRADA E BOTÃO DE ADIÇÃO DE TAREFA
def ao_clicar_entrada(event):
    if entrada_tarefa.get() == "Escreva sua tarefa aqui":
        entrada_tarefa.delete(0, tk.END)
        entrada_tarefa.configure(fg="black")

def ao_sair_foco(event):
    if not entrada_tarefa.get().strip():
        entrada_tarefa.delete(0, tk.END)
        entrada_tarefa.insert(0, "Escreva sua tarefa aqui")
        entrada_tarefa.configure(fg="red")

# Criar uma fonte para o cabeçalho
fonte_cabecalho = font.Font(family="PapyruAlgerian", size=24, weight="bold")

# Criar um rótulo de cabeçalho
rotulo_cabecalho = tk.Label(janela, text="Meu App de Tarefas", font=fonte_cabecalho, bg="#F0F0F0", fg="#333")
rotulo_cabecalho.pack(pady=20)

frame = tk.Frame(janela, bg="#F0F0F0")
frame.pack(pady=10)

entrada_tarefa = tk.Entry(frame, font=("Garamond", 14), relief=tk.FLAT, bg="white", fg="grey", width=30)
entrada_tarefa.insert(0, "Escreva sua tarefa aqui")
entrada_tarefa.bind("<FocusIn>", ao_clicar_entrada)
entrada_tarefa.bind("<FocusOut>", ao_sair_foco)
entrada_tarefa.pack(side=tk.LEFT, padx=10)

botao_adicionar = tk.Button(frame, text="Adicionar Tarefa", command=adicionar_tarefa, bg="#4CAF50", fg="white", height=1, width=15, font=("Roboto", 11), relief=tk.FLAT)
botao_adicionar.pack(side=tk.LEFT, padx=10)

#CRIAR UMA LISTA DE TAREFAS COM BARRA DE ROLAGEM
frame_lista_tarefas = tk.Frame(janela, bg="white")
frame_lista_tarefas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
canvas = tk.Canvas(frame_lista_tarefas, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(frame_lista_tarefas, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas_interior = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=canvas_interior, anchor="nw")
canvas_interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Executar conexão com o banco de dados e carregar tarefas
connect_db()
carregar_tarefas()

#EXECUTAR LOOP PRINCIPAL
janela.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tarefas import adicionar_tarefa, editar_tarefa, excluir_tarefa, listar_tarefas
from notificacoes import verificar_prazos

def iniciar_interface():
    root = tk.Tk()
    root.title("Gerenciador de Tarefas")
    root.geometry("900x650")
    root.config(bg="#696969")

    # Estilo dos widgets
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white", font=("Arial", 10, "bold"))
    style.configure("TLabel", font=("Arial", 12), background="#00bfff")
    style.configure("TEntry", padding=5, font=("Arial", 12))
    style.configure("TCombobox", padding=5, font=("Arial", 12))

    # Título
    tk.Label(root, text="Gerenciador de Tarefas", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white").pack(fill="x", pady=20)

    # Frame para os campos de entrada
    frame_entrada = tk.Frame(root, bg="#f0f0f0")
    frame_entrada.pack(pady=10, padx=40, fill="x")

    tk.Label(frame_entrada, text="Título", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    titulo_entry = tk.Entry(frame_entrada, width=40)
    titulo_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_entrada, text="Descrição", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    descricao_entry = tk.Entry(frame_entrada, width=40)
    descricao_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_entrada, text="Data Limite", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    data_entry = tk.Entry(frame_entrada, width=40)
    data_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame_entrada, text="Prioridade", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    prioridade_entry = tk.Entry(frame_entrada, width=40)
    prioridade_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(frame_entrada, text="Status", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    status_var = tk.StringVar(value="Pendente")
    status_combo = ttk.Combobox(frame_entrada, textvariable=status_var, values=["Pendente", "Concluída"], width=38)
    status_combo.grid(row=4, column=1, padx=10, pady=5)

    # Frame para os botões
    frame_botoes = tk.Frame(root, bg="#228b22")
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Adicionar", command=lambda: adicionar()).grid(row=0, column=0, padx=20, pady=10)
    tk.Button(frame_botoes, text="Editar", command=lambda: editar()).grid(row=0, column=1, padx=20, pady=10)
    tk.Button(frame_botoes, text="Excluir", command=lambda: excluir()).grid(row=0, column=2, padx=20, pady=10)
    tk.Button(frame_botoes, text="Filtrar Status", command=lambda: filtrar_status()).grid(row=0, column=3, padx=20, pady=10)

    # Lista de tarefas
    tree = ttk.Treeview(root, columns=("ID", "Título", "Descrição", "Data", "Prioridade", "Status"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Título", text="Título")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Data", text="Data")
    tree.heading("Prioridade", text="Prioridade")
    tree.heading("Status", text="Status")
    tree.column("ID", width=40, anchor="center")
    tree.column("Título", width=150, anchor="center")
    tree.column("Descrição", width=200, anchor="center")
    tree.column("Data", width=100, anchor="center")
    tree.column("Prioridade", width=100, anchor="center")
    tree.column("Status", width=80, anchor="center")
    tree.pack(pady=20, padx=40, fill="x")

    def atualizar_lista(filtro=None):
        for row in tree.get_children():
            tree.delete(row)
        tarefas = listar_tarefas(filtro)
        for t in tarefas:
            tree.insert('', 'end', values=t)

    def adicionar():
        titulo = titulo_entry.get()
        descricao = descricao_entry.get()
        data_limite = data_entry.get()
        prioridade = prioridade_entry.get()
        if titulo and data_limite:
            try:
                datetime.strptime(data_limite, "%Y-%m-%d")
                adicionar_tarefa(titulo, descricao, data_limite, prioridade)
                atualizar_lista()
                # Limpar os campos após adicionar
                titulo_entry.delete(0, tk.END)
                descricao_entry.delete(0, tk.END)
                data_entry.delete(0, tk.END)
                prioridade_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Data inválida! Use o formato YYYY-MM-DD.")
        else:
            messagebox.showwarning("Aviso", "Título e Data são obrigatórios.")

    def editar():
        item = tree.focus()
        if not item:
            return messagebox.showinfo("Selecione", "Selecione uma tarefa para editar.")
        valores = tree.item(item, 'values')
        id_tarefa = valores[0]
        editar_tarefa(id_tarefa, titulo_entry.get(), descricao_entry.get(), data_entry.get(), prioridade_entry.get(), status_var.get())
        atualizar_lista()

    def excluir():
        item = tree.focus()
        if not item:
            return messagebox.showinfo("Selecione", "Selecione uma tarefa para excluir.")
        id_tarefa = tree.item(item, 'values')[0]
        excluir_tarefa(id_tarefa)
        atualizar_lista()

    def filtrar_status():
        status = status_var.get()
        atualizar_lista(filtro=status)

    def preencher_campos(event):
        item = tree.focus()
        if not item:
            return
        valores = tree.item(item, 'values')
        titulo_entry.delete(0, tk.END)
        titulo_entry.insert(0, valores[1])
        descricao_entry.delete(0, tk.END)
        descricao_entry.insert(0, valores[2])
        data_entry.delete(0, tk.END)
        data_entry.insert(0, valores[3])
        prioridade_entry.delete(0, tk.END)
        prioridade_entry.insert(0, valores[4])
        status_var.set(valores[5])

    tree.bind('<<TreeviewSelect>>', preencher_campos)

    # Notificações
    tarefas_urgentes = verificar_prazos()
    if tarefas_urgentes:
        msg = "\n".join([f"- {t[0]} (prazo: {t[1]})" for t in tarefas_urgentes])
        messagebox.showinfo("⚠️ Tarefas com prazo próximo!", msg)

    atualizar_lista()
    root.mainloop()


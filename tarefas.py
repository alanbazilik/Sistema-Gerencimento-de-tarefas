from database import conectar

def adicionar_tarefa(titulo, descricao, data_limite, prioridade):
    conn = conectar()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO tarefas (titulo, descricao, data_limite, prioridade)
        VALUES (%s, %s, %s, %s)
    ''', (titulo, descricao, data_limite, prioridade))
    conn.commit()
    cur.close()
    conn.close()

def editar_tarefa(id, titulo, descricao, data_limite, prioridade, status):
    conn = conectar()
    cur = conn.cursor()
    cur.execute('''
        UPDATE tarefas
        SET titulo=%s, descricao=%s, data_limite=%s, prioridade=%s, status=%s
        WHERE id=%s
    ''', (titulo, descricao, data_limite, prioridade, status, id))
    conn.commit()
    cur.close()
    conn.close()

def excluir_tarefa(id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute('DELETE FROM tarefas WHERE id=%s', (id,))
    conn.commit()
    cur.close()
    conn.close()

def listar_tarefas(filtro=None):
    conn = conectar()
    cur = conn.cursor()
    if filtro:
        cur.execute('SELECT * FROM tarefas WHERE status=%s ORDER BY data_limite', (filtro,))
    else:
        cur.execute('SELECT * FROM tarefas ORDER BY data_limite')
    tarefas = cur.fetchall()
    cur.close()
    conn.close()
    return tarefas

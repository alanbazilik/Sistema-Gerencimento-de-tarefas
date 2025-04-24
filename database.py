import psycopg2

def conectar():
    return psycopg2.connect(
        dbname="tarefas_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5433"
    )

def criar_tabela():
    conn = conectar()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            descricao TEXT,
            data_limite DATE,
            prioridade VARCHAR(10),
            status VARCHAR(15) DEFAULT 'Pendente'
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
if __name__ == "__main__":
    criar_tabela()
    print("Tabela criada com sucesso!")

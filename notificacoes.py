from datetime import date, timedelta
from database import conectar

def verificar_prazos():
    hoje = date.today()
    aviso = hoje + timedelta(days=1)

    conn = conectar()
    cur = conn.cursor()
    cur.execute('''
        SELECT titulo, data_limite 
        FROM tarefas 
        WHERE data_limite BETWEEN %s AND %s AND status = %s
    ''', (hoje, aviso, 'Pendente'))
    
    tarefas = cur.fetchall()
    cur.close()
    conn.close()  
    return tarefas

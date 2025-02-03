import sqlite3

def create_database_table():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            deadline TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL
        )'''
    )
    conn.commit()
    conn.close()
create_database_table()

def add_task(description,deadline,status='Pending',priority='medium'):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''INSERT INTO tasks(description,deadline,status,priority) VALUES(?,?,?,?)''',(description,deadline,status,priority))
    conn.commit()
    conn.close()
    
def get_all_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM tasks''')
    tasks = c.fetchall()
    conn.close()
    return tasks

def update_task(task_id,new_description, new_deadline, new_status,new_priority):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''UPDATE tasks SET description=?,deadline=?,status=?,priority=? WHERE id=?''',
              (new_description, new_deadline, new_status,new_priority,task_id))
    conn.commit()
    conn.close()

def delete_tasks(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''DELETE FROM tasks WHERE id=?''', (task_id,))
    conn.commit()
    conn.close()
    
def search_task_by_description(keyword):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM tasks WHERE description LIKE ?''', (f'%{keyword}%',))
    tasks = c.fetchall()
    conn.close()
    if tasks:
        return tasks
    return "no task found for this search"

def sortby_deadline_status(sort_by='status'):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    
    if sort_by=='status':
        query = '''
        SELECT * FROM tasks
        ORDER BY 
            CASE status
                WHEN 'Completed' THEN 1
                    WHEN 'In Progress' THEN 2
                    WHEN 'Pending' THEN 3
                END
        '''
    elif sort_by=='priority':
        query = '''
        SELECT * FROM tasks
        ORDER BY 
            CASE status
                WHEN 'High' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 3
                END
        '''
    elif sort_by=='deadline':
        query = 'SELECT * FROM tasks ORDER BY deadline ASC'
    else:
        return 'the sort by value incorrect'
    c.execute(query)
    tasks = c.fetchall()
    conn.close()
    if tasks:
        return tasks
    return 'no tasks found'

if __name__ == '__main__':
    create_database_table()
    
    #addind task 
    add_task('Finish project', '2025-02-10','Complete',"Low")
    add_task('Buy groceries', '2025-02-05', 'In Progress','medium')
    add_task('Call John', '2025-02-07', 'Pending','High')
    
    task = get_all_tasks()
    # print(task)
    #update task
    update_task(1, 'rework on project ', '2025-02-09', 'In Progress','High')
    
    search_result = search_task_by_description('sree')
    # print(search_result)
    
    sort_task = sortby_deadline_status(sort_by='priority')
    print(sort_task)
    
    # delete_tasks(3)

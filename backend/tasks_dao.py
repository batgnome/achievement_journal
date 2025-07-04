from backend.sql_connector_3 import get_conn

def get_all_tasks(connection):
    
    cursor = connection.cursor()
    query = "Select t.id,t.name,t.description,t.archived,t.type_id,ty.name as type_name,t.completed,t.difficulty_id, d.name as difficulty_name from tasks t " \
    "left join types ty on ty.type_id = t.type_id " \
    "left join difficulty d on d.difficulty_id = t.difficulty_id"
    cursor.execute(query)
    response = []
    for (id, name, description, archived,type_id,type_name,completed,difficulty_id,difficulty_name) in cursor:
       response.append(
           {
            'id':id ,
            'name':name,	
            'description':description ,	
            'archived':archived,
            'type_id':type_id,
            'type_name': type_name,
            'difficulty_id' : difficulty_id,
            'difficulty_name': difficulty_name,
            'completed' : completed
            }

       ) 
      

    # connection.close()
    return response

def create_task(connection,task):
    print(task)
    cursor = connection.cursor()
    query =("insert into tasks (name, description, archived,type_id,difficulty_id)" \
    "values(?, ?, ?, ?, ?)")
    data =( task['name'],task['description'],task['archived'],task['type_id'],task['difficulty_id'])
    cursor.execute(query,data)

    connection.commit()
    return cursor.lastrowid

def delete_task(connection,task_id):
    cursor = connection.cursor()
    query =("delete from tasks where id=" +str(task_id))
    cursor.execute(query)
    connection.commit()

def update_task(connection, task_id, task):
    cursor = connection.cursor()
    cursor.execute("SELECT name, description, archived FROM tasks WHERE id = ?", (task_id,))
    init_task = cursor.fetchone()
    if init_task is None:
        print("Task not found.")
        return

    current_name, current_description, current_archived,current_type_id,current_difficulty_id = init_task
    new_name = task.get('name', current_name)
    new_description = task.get('description', current_description)
    new_archived = task.get('archived', current_archived)
    new_type_id = task.get('type_id', current_type_id)
    new_difficulty_id = task.get('difficulty_id',current_difficulty_id)

    query = "UPDATE tasks SET name = ?, description = ?, archived = ?, type_id = ?, difficulty_id = ? WHERE id = ?"
    data = (new_name, new_description, new_archived, new_type_id, new_difficulty_id, task_id)
    cursor.execute(query, data)
    connection.commit()

# if __name__ == '__main__':
#     connection = get_conn()
#     print(get_all_tasks(connection=connection))

#     # print(insert_new_task(connection, {
#     #     'name': 'potatoes',
#     #     'description': 1,
#     #     'archived': 10.0
#     # }))
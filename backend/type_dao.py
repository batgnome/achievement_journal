from backend.sql_connector_3 import get_conn

def get_all_types(connection):
    
    cursor = connection.cursor()
    query = "Select * from types t "
    
    cursor.execute(query)
    response = []
    for (id, name) in cursor:
       response.append(
           {
            'id':id ,
            'name':name
            }

       ) 
    # connection.close()
    return response

def create_type(connection,type):
 
    cursor = connection.cursor()
    query =("insert into types (name)" \
    "values(?)")
    data =( [type])
    cursor.execute(query,data)

    connection.commit()
    return cursor.lastrowid

def delete_type(connection,type_id):
    cursor = connection.cursor()
    query =("delete from types where id=" +str(type_id))
    cursor.execute(query)
    connection.commit()

def update_type(connection, type_id, type):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM types WHERE id = ?", (type_id,))
    init_type = cursor.fetchone()
    if init_type is None:
        print("type not found.")
        return

    current_name = init_type
    new_name = type.get('name', current_name)

    query = "UPDATE types SET name = ? WHERE id = ?"
    data = (new_name, type_id)
    cursor.execute(query, data)
    connection.commit()


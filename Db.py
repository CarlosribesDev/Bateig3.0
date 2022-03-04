
import sqlite3 as sql


def get_material(id):
    
    connection = sql.connect('datos.db')
    cursor = connection.cursor()
    query = f'select nombre from materiales where id={id}'
    cursor.execute(query)
    resulset = cursor.fetchall()
    if(len(resulset) > 0): material = resulset[0][0]
    else: material = 'Nuevo'
    connection.commit()
    connection.close()
  
    return material

def get_operators():
    connection = sql.connect('datos.db')
    cursor = connection.cursor()
    query = 'select nombre from Operarios'
    cursor.execute(query)
    resulset = cursor.fetchall()
    operarios = []

    for ele in resulset:
        operarios.append(ele[0])
    connection.commit()
    connection.close()

    return operarios

def get_directory(name):
    connection = sql.connect('datos.db')
    cursor = connection.cursor()
    query = f"select ruta from Directorios where nombre='{name}'"
    cursor.execute(query)
    resulset = cursor.fetchall()
    if(len(resulset) > 0): directory = resulset[0][0]
    else: directory = ''
    connection.commit()
    connection.close()

    return directory

def set_directory(directory,name):
 
    connection = sql.connect('datos.db')
    cursor = connection.cursor()
    query = f"update Directorios set ruta='{directory}' where nombre='{name}'"
   
    cursor.execute(query)
    connection.commit()
    connection.close()

def add_material(id,material):
    connection = sql.connect('datos.db')
    cursor = connection.cursor()
    query = f"insert into materiales(id,nombre) values({id},'{material}')"
    cursor.execute(query)
    connection.commit()
    connection.close()


if __name__== '__main__':
    print(get_directory('Unloading_txt'))
    pass
    


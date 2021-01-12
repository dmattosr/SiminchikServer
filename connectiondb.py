# -*- coding: utf-8 -*-
import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding('Cp1252')

DB_HOST = 'localhost' 
DB_USER = 'root' 
DB_PASS = 'root2' 
DB_NAME = 'app_quechua'
 
def run_query(query,data):
    
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
 
    conn = MySQLdb.connect(*datos) # Conectar a la base de datos
    conn.set_character_set('utf8') 
    cursor = conn.cursor()         # Crear un cursor
    if data == "":
        cursor.execute(query) # Ejecutar una consulta 
    else:
        cursor.execute(query,data) # Ejecutar una consulta 
 
    if query.upper().startswith('SELECT'): 
        data = cursor   # Traer los resultados de un select 
    else: 
        conn.commit()   # Hacer efectiva la escritura de datos 
        data = None 
 
    cursor.close()      # Cerrar el cursor 
    conn.close()        # Cerrar la conexión 
 
    return data

import pyodbc
import time


def create_db_conn():
  server = 'tcp:everst.database.windows.net' 
  database = 'everst' 
  username = 'everst' 
  password = 'bankapp33#' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  return cnxn

def insert_new_user (conn , query):
  cnxn = conn
  cursor = cnxn.cursor()
  cursor.execute(query)
  cnxn.commit()
  cursor.close()
  cnxn.close()

def insert_to_orders_table(conn , query):
  cnxn = conn
  cursor = cnxn.cursor()
  cursor.execute(query)
  cursor.nextset()
  for id in cursor:
      cursor_id = id
  print(int(cursor_id[0]))
  cnxn.commit()
  cursor.close()
  cnxn.close()
  return int(cursor_id[0])

def insert_to_transaction_tracking_table(conn , query):
  cnxn = conn
  cursor = cnxn.cursor()
  cursor.execute(query)
  # cursor.nextset()
  # for id in cursor:
  #     cursor_id = id[0]
  cnxn.commit()
  cursor.close()
  cnxn.close()
  #return cursor_id

def query_insert_user(user_email,user_name,ms_id):
  query = """INSERT INTO dbo.users( email , name, ms_id) 
  VALUES (
  '%s',
  '%s',
  '%s'
  )"""
  final_query = query%(user_email,user_name,ms_id)
  return final_query


def query_insert_order(ms_id,country,bank_id):
  start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
  query = """INSERT INTO dbo.orders( ms_id ,created_date , country,  bank_id) 
  VALUES (
  '%s',
  '%s',
  '%s',
  '%s'
  )
  ;SELECT SCOPE_IDENTITY() as id;"""
  final_query = query%(ms_id , start_time, country,bank_id)
  return final_query
  


def query_insert_transaction_tracking(ms_id,state_name,payload,id_order):
  start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
  query = """INSERT INTO dbo.transaction_tracking( ms_id ,state_name , payload, id_order ,created_date ) 
  VALUES (
  '%s',
  '%s',
  '%s',
  '%s',
  '%s'
  );"""
  #SELECT SCOPE_IDENTITY() as id_transaction_tracking;"""
  final_query = query%(ms_id, state_name, payload, id_order, start_time,)
  return final_query

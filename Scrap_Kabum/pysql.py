import csv, pyodbc
import pandas as pd
from datetime import datetime
from pathlib import Path
import pandas.io.sql as psql

# set up some constants
#MDB = 'I:/Documentos_GED/Chave_atendimento.mdb'
DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'
PWD = 'pw'
pyodbc.pooling = False
MDB = Path('C:/Users/Victor/OneDrive/Projetos/Scrap_Kabum/scrap_kabum.mdb')
#MDB = Path('C:/Users/Victor/Documents/scrap_kabum.mdb')
# connect to db
fmt='%d/%m/%Y'

def LOAD_DATABASE():
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()
    SQL_Query = pd.read_sql_query('''SELECT * FROM bd_precos;''', con)
    df = pd.DataFrame(SQL_Query)
    con.commit()
    cur.close()
    con.close()
    return df

def INSERT_DATAFRAME(df_insert,TABLE):
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()
    df_insert.fillna('')
    for Index,row in df_insert.iterrows():
        mydict = dict(row)
        columns = ', '.join("[" + str(x) + "]" for x in mydict.keys())
        values = ', '.join("'" + str(x) + "'" for x in mydict.values())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (TABLE, columns, values)
        #sql = sql.replace("'","")
        cur.execute(sql)
        con.commit()
    cur.close()
    con.close()

def RUNSQL(sql):
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

def UPDATE_DOC_STATUS(Cod,status):
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()
    SQL = "UPDATE bd_precos SET [UPLOAD_GED] = '" + status + "' WHERE [Código] = " + Cod
    cur.execute(SQL)
    SQL = "UPDATE bd_precos SET [TEMPO_UPLOAD_GED] = '" + status + "' WHERE [Código] = " + Cod
    cur.execute(SQL)
    con.commit()
    cur.close()
    con.close()

def UPDATE_DOC_TIME(Cod,time):
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()
    SQL = "UPDATE bd_precos SET [TEMPO_UPLOAD_GED] = '" + time + "' WHERE [Código] = " + Cod
    cur.execute(SQL)
    con.commit()
    cur.close()
    con.close()

def UPDATE_FIELD(Cod,field,value):
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()
    SQL = "UPDATE bd_precos SET ["+str(field)+"] = '" + str(value) + "' WHERE [Código] = " + str(Cod)
    cur.execute(SQL)
    con.commit()
    cur.close()
    con.close()

def UPDATE_FIELD_MATRICULA(Cod,field,value):
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()
    SQL = "UPDATE bd_precos SET ["+str(field)+"] = '" + str(value) + "' WHERE [Matricula] = '" + str(Cod) + "'"
    cur.execute(SQL)
    con.commit()
    cur.close()
    con.close()

LOAD_DATABASE()
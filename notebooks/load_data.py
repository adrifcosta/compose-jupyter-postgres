import os 
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
from io import StringIO

data_files = list(filter(lambda x: '.csv' in x, os.listdir('data/')))
instance_names = [filename.replace('.csv', '') for filename in data_files]

#this can be used to create more than one db instance
for instance_name in instance_names:
    try:
        con = psycopg2.connect(host='postgres', port=5432, user='postgres',
                            password='postgres')
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # obtain a DB Cursor
        cursor  = con.cursor();

        # database create statement
        sql_create_database = "create database "+instance_name+";"

        # create the database 
        cursor.execute(sql_create_database);

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    conn = psycopg2.connect(host='postgres', port=5432, user='postgres',
                            password='postgres', dbname=instance_name)

    try:

        cur = conn.cursor()

        # create table
        cur.execute("""
        CREATE TABLE titanic_passengers(
        Survived boolean,
        Pclass varchar,
        Name varchar,
        Sex varchar,
        Age float,
        Siblings_Spouses_Aboard int,
        Parents_Children_Aboard int,
        Fare float
        )
        """)
        
        df = pd.read_csv(os.path.join("data", instance_name+'.csv'))
        
        # remove first column
        df = df[['Survived', 'Pclass', 'Name', 'Sex', 'Age', 'Siblings_Spouses_Aboard', 'Parents_Children_Aboard', 'Fare']]

        # initialize a string buffer
        sio = StringIO()
        sio.write(df.to_csv(index=None, header=None))  # write the Pandas DataFrame as a csv to the buffer
        sio.seek(0)  #

        with conn.cursor() as c:
            c.copy_from(sio, 'titanic_passengers', columns=df.columns, sep=',')
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
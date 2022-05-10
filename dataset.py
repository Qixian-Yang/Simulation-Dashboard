import pyodbc

#connect to sql by Channel_Id
def connected_to_SQL (Channel_Id):
    server = 'des-server.database.windows.net'
    database = 'DESAdapter'
    username = 'DESadministrator'
    password = '{Aa123456789}'
    driver= '{ODBC Driver 17 for SQL Server}'
    result=[[],[]]

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("Select Channel_UUID from Channels where Channel_Id = "+Channel_Id)
            row = cursor.fetchone()
            while row:
                result[0].append(row[0])
                row = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("Select Session_UUID from Sessions where Channel_UUId = '"+result[0][0]+"'")
            row = cursor.fetchone()
            while row:
                result[1].append(row[0])
                row = cursor.fetchone()

    return result

#connect to sql by Topic
def connected_to_SQLt (Topic):
    server = 'des-server.database.windows.net'
    database = 'DESAdapter'
    username = 'DESadministrator'
    password = '{Aa123456789}'
    driver= '{ODBC Driver 17 for SQL Server}'
    result=[[],[]]

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("Select Session_UUID from SessionTopics where Topic = "+Topic)
            row = cursor.fetchone()
            while row:
                result[1].append(row[0])
                row = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("Select Channel_UUID from Sessions where Session_UUID = '"+result[1][0]+"'")
            row = cursor.fetchone()
            while row:
                result[0].append(row[0])
                row = cursor.fetchone()
    return result
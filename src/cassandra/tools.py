from cassandra.cluster import Cluster

def  get_connection(conn):
    return Cluster(conn)

def  get_session(cass,keyspace):
    return cass.connect(keyspace)

def  get_keyspaces(sess):
    old = sess.keyspace
    sess.set_keyspace("system")
    
    rows = sess.execute("select keyspace_name from schema_keyspaces")
    
    keyspaces=[]
    
    for row in rows:
        keyspaces.append(row[0])

    sess.set_keyspace(old)
    return keyspaces

def get_tables(sess):
    old = sess.keyspace
    sess.set_keyspace("system")
    rows = sess.execute("select columnfamily_name from schema_columnfamilies where keyspace_name='"+old+"'")
    
    tables = []
    
    for row in rows:
        tables.append(row[0])  
       
    sess.set_keyspace(old) 
    return tables  

def get_data(sess, sql):
    return sess.execute(sql)

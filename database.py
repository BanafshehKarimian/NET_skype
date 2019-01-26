import mysql.connector as connector
from mysql.connector import errorcode
connectionParams = {'user' : 'root',
                      'password' : 'password',
                      'host' : 'localhost',
						'database' : 'EmpData' }

class db:
    _connection = connector.connect(**connectionParams)
    cursor = _connection.cursor()
    def __init__(self):
        print('initializing the database')
        try:
            self._connection = connector.connect(**connectionParams)
            self.cursor = self._connection.cursor()
            self.create_usersTable()
            self.create_contactsTable()            
            self.create_textMassages()
            self.create_awaiting()

        except connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('ERR: access to db denied')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('ERR: bad db')
            else:
                print(err)
            self._connection.close()

#-----------------------------------create tabels----------------------------------------------------------
    def create_usersTable(self):
        createQuery = '''CREATE TABLE IF NOT EXISTS usersTable (
                         ID INT AUTO_INCREMENT KEY, 
                         username VARCHAR(255) NOT NULL, 
                         password VARCHAR(255) NOT NULL)'''
        print('usersTable created')
        self.cursor.execute(createQuery)
        self._connection.commit()
    def create_contactsTable(self):
        createQuery = '''CREATE TABLE IF NOT EXISTS contactsTable (
                         ID INT AUTO_INCREMENT KEY, 
                         user1 VARCHAR(255) NOT NULL, 
                         user2 VARCHAR(255) NOT NULL)'''
        print('contactsTable created')
        self.cursor.execute(createQuery)
        self._connection.commit()
    def create_textMassages(self):
        createQuery = '''CREATE TABLE IF NOT EXISTS textMassages (
                         ID INT AUTO_INCREMENT KEY, 
                         chatRoomID INT NOT NULL, 
                         sender VARCHAR(255) NOT NULL,
                         content text NOT NULL,
                         timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''
        print('textMassagesTable created')
        self.cursor.execute(createQuery)
        self._connection.commit()
    def create_awaiting(self):
        createQuery = '''CREATE TABLE IF NOT EXISTS awaiting (
                         ID INT AUTO_INCREMENT KEY, 
                         caller VARCHAR(255) NOT NULL,
                         callee VARCHAR(255) NOT NULL)'''
        print('awaitingTable created')
        self.cursor.execute(createQuery)
        self._connection.commit()
    
#-----------------------------------insert in tabels-------------------------------------------------------
    
    def insert_awaitingUser(self, caller,callee):
        insertQuery = 'INSERT INTO awaiting (caller,callee) VALUES(%s,%s)'
        self.cursor.execute(insertQuery, (caller,callee,))
        searchNr = self.cursor.lastrowid
        self._connection.commit()
        return searchNr

    def delete_awaitingUser(self, caller,callee):
        insertQuery = 'delete from awaiting where caller=%s and callee=%s'
        self.cursor.execute(insertQuery, (caller,callee,))
        searchNr = self.cursor.lastrowid
        self._connection.commit()
        return searchNr
    def insert_textMassage(self, chatRoomID, sender, content):
        insertQuery = 'INSERT INTO textMassages (chatRoomID,sender,content) VALUES(%s,%s,%s)'
        self.cursor.execute(insertQuery, (chatRoomID,sender,content,))
        searchNr = self.cursor.lastrowid
        self._connection.commit()
        return searchNr

    def insert_contact(self, contact1, contact2):
        insertQuery = 'INSERT INTO contactsTable (user1,user2) VALUES(%s,%s)'
        if contact1 > contact2:
        	self.cursor.execute(insertQuery, (contact1,contact2,))
        else:
        	self.cursor.execute(insertQuery, (contact2,contact1,))
        searchNr = self.cursor.lastrowid
        self._connection.commit()
        return searchNr
    def insert_user(self, user , pas):
        insertQuery = 'INSERT INTO usersTable (username,password) VALUES(%s,%s)'
        self.cursor.execute(insertQuery, (user,pas,))
        searchNr = self.cursor.lastrowid
        self._connection.commit()
        return searchNr
#-----------------------------------select from tabels-----------------------------------------------------

    def select_awaitingUser(self, caller,callee):
        insertQuery = 'SELECT * from awaiting where caller=%s and callee=%s'
        self.cursor.execute(insertQuery, (caller,callee,))
        data = self.cursor.fetchall()
        searchNr = self.cursor.lastrowid
        if(len(data)!=0):
        	return data[0]
        else:
        	return None
    def select_textMassage(self, chatRoomID):
        insertQuery = 'SELECT * from  textMassages where chatRoomID=%s'
        self.cursor.execute(insertQuery, (chatRoomID,))
        data = self.cursor.fetchall()
        searchNr = self.cursor.lastrowid
        return data

    def select_contact(self, contact1, contact2):
        insertQuery = 'SELECT * from contactsTable where user1 = %s and user2 = %s'
        if contact1 > contact2:
        	self.cursor.execute(insertQuery, (contact1,contact2,))
        else:
        	self.cursor.execute(insertQuery, (contact2,contact1,))
        data = self.cursor.fetchall()
        searchNr = self.cursor.lastrowid
        if(len(data)!=0):
        	return data[0]
        else:
        	return None
    def get_contacts(self, name):
        insertQuery = 'SELECT * from contactsTable where user1 = %s or user2 = %s'
        self.cursor.execute(insertQuery, (name,name,))
        data = self.cursor.fetchall()
        return data

    def select_user(self, user , pas):
        insertQuery = 'SELECT * from usersTable where username = %s and password = %s'
        self.cursor.execute(insertQuery, (user,pas,))
        data = self.cursor.fetchall()
        searchNr = self.cursor.lastrowid
        if(len(data)!=0):
        	return data[0]
        else:
        	return None

    def select_username(self, user):
        insertQuery = 'SELECT * from usersTable where username = %s'
        self.cursor.execute(insertQuery, (user,))
        data = self.cursor.fetchall()
        searchNr = self.cursor.lastrowid
        if(len(data)!=0):
        	return data[0]
        else:
        	return None


#--------------------------------connection-----------------------------------------------------------------
    def close_connection(self):
        self._connection.close()

    def get_connection(self):
        return self._connection

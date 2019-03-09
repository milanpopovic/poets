import mysql.connector
from mysql.connector import errorcode
import hashlib
import json

def md5(s):
  m = hashlib.md5()
  m.update(s.encode())
  return m.hexdigest()

class Model:
    def __init__(self,dbuser,dbname):
        try:
            self.cnx = mysql.connector.connect(user=dbuser, database=dbname)
            print("Connected to database:",dbname)
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
    
    def create_tables(self, tables):
        for table_name in tables:
            table_description = tables[table_name]
            try:
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)

    def get_all_users(self):
        self.cursor.execute("select * from user;")
        return self.cursor.fetchall()
        
    def get_user_id(self,email):
        self.cursor.execute("select id from user where email='{}';".format(email))
        users = self.cursor.fetchone()
        if users != None:
            return users[0]
        else:
            return -1
    
    def get_user_credentials(self,email):
        self.cursor.execute("select * from user where email='{}'".format(email))
        id, name, email, passw, country, is_admin = self.cursor.fetchone()
        credentials = {'id': id, 'name': name, 'email': email, 'is_admin': is_admin}
        return credentials
            
    def get_user_bio(self,userid):
        self.cursor.execute("select content from bio where user_id='{}';".format(userid))
        return self.cursor.fetchone()
        
    def poetId(self,poetName):
        self.cursor.execute("select id from user where name='{}';".format(poetName))
        return self.cursor.fetchall()[0][0]
    
    def poetName(self,poetId):
        self.cursor.execute("select name from user where id={};".format(poetId))
        return self.cursor.fetchone()[0]
        
    def get_all_poems_of_poet(self,poet_id):
        self.cursor.execute("select id,title,content from poem where user_id='{}';".format(poet_id))
        return self.cursor.fetchall()
    
    def get_poem(self, poem_id):
        self.cursor.execute("select title,poem_type, content, id from poem where id='{}';".format(poem_id))
        return self.cursor.fetchone()
        
    def delete_poem(self, poem_id):
        self.cursor.execute("delete from poem where id={};".format(poem_id))
        self.cnx.commit()
        return "deleted"
        
    def poetsList(self):
        self.cursor.execute("select user_id from poem;")
        poets = self.cursor.fetchall()
        poetlist =[]
        for poet in poets:
            if poet[0] not in poetlist:
                poetlist.append(poet[0])
        namelist=[]
        for id in poetlist:
            self.cursor.execute("select name from user where id='{}'".format(id))
            name = self.cursor.fetchone()[0]
            namelist.append((name,id))
        return namelist
        
    def check_password(self,email, passw):
        self.cursor.execute("select * from user where email='{}' and password='{}'".format(email,md5(passw)))
        if self.cursor.fetchone() != None:
            return True
        else:
            return False
            
    def change_password(self,email,new_password):
        sql = "update user set password='{}' where email='{}'".format(new_password,email)
        try:
            self.cursor.execute(sql)
            
            return 'Password changed.'
        except:
            return 'Password not changed'
        
    def add_new_user(self, name, email, password, country, is_admin):
        sql="insert into user (name, email, country, password,  is_admin) values('{}','{}','{}','{}', {});".format(name,email,country,md5(password),is_admin)
        try:
            self.cursor.execute(sql)
            self.cnx.commit()
            return 'User registered succesfully.'
        except:
            return 'Not registered, check your data.'
    
    def add_new_poem(self, userid, type, title, content, year='2019'):
        sql="insert into poem (user_id, poem_type, title, content, year) values('{}','{}','{}','{}','{}');".format(userid, type, title, content,year)
        try:
            self.cursor.execute(sql)
            self.cnx.commit()
            return 'Poem saved.'
        except:
            return 'Not saved , check your data'
            
    def update_poem(self,poem_id,poem_type,title,content):
        sql="update poem set poem_type='{}', title='{}', content='{}' where id={};".format(poem_type,title,content,poem_id)
        self.cursor.execute(sql)
        self.cnx.commit()
        return 'Poem updated'
        
    def add_new_bio(self, userid, content):
        self.cursor.execute("delete from bio where user_id={}".format(userid))
        sql="insert into bio (user_id,content) values('{}','{}');".format(userid,content)
        try:
            self.cursor.execute(sql)
            self.cnx.commit()
            return 'Bio saved.'
        except:
            return 'Not saved , check your data'
        
    def close(self):
        self.cursor.close()
        self.cnx.close()
        
TABLES = {}
TABLES['user'] = (
"CREATE TABLE IF NOT EXISTS user ("
  "id INT(11) NOT NULL AUTO_INCREMENT,"
  "name VARCHAR(45) NOT NULL,"
  "email VARCHAR(100) NOT NULL,"
  "country varchar(2) DEFAULT NULL,"
  "password CHAR(32) NOT NULL,"
  "is_admin TINYINT(1) NOT NULL,"
  "PRIMARY KEY (id))"
  "ENGINE = InnoDB;")

TABLES['poem'] = (
"CREATE TABLE IF NOT EXISTS poem ("
"id INT(11) NOT NULL AUTO_INCREMENT,"
"poem_type varchar(20) DEFAULT NULL,"
"user_id  INT(11) NOT NULL,"
"title VARCHAR(45) NOT NULL,"
"content LONGTEXT NOT NULL,"
"year YEAR NULL,"
"PRIMARY KEY (id),"
"INDEX fk_poem_user_idx (user_id ASC),"
"CONSTRAINT fk_poem_user"
"    FOREIGN KEY (user_id)"
"    REFERENCES user (id)"
"    ON DELETE NO ACTION"
"    ON UPDATE NO ACTION)"
"ENGINE = InnoDB;")

TABLES['bio'] = (
"CREATE TABLE IF NOT EXISTS bio ("
"   id INT(11) NOT NULL AUTO_INCREMENT,"
"   user_id INT(11) NOT NULL,"
"   content LONGTEXT NOT NULL,"
"   PRIMARY KEY (id),"
"  INDEX fk_bio_user_idx (user_id ASC),"
"  CONSTRAINT fk_bio_user"
"    FOREIGN KEY (user_id)"
"    REFERENCES user (id)"
"    ON DELETE NO ACTION"
"    ON UPDATE NO ACTION)"
"ENGINE = InnoDB;")

model = Model('popovicmilan','c9')
model.create_tables(TABLES)
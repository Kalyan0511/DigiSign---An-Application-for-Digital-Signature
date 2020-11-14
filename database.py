# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Schema:
#Users:
#usersInfo(username,name,password,email) - username is primay key
#usersKeys(username,privateKey,publicKey)- username is primary key
 
#Documents:
#Documents(docId,docName,requestedBy,signer,status)
#status can be 0-Not Signed
#              1-Used SHA
#              2-Used md5
 
 
import mysql.connector
 
#Use username and password of your mysql in the follwoing command
#Getting connection to mysql database 
mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="1234"
      )
 
 
# Input:name of database
# Output: nothing...Just create a database
def createDatabase(databaseName):
     
      query = "create database "+databaseName
      myCursor = mydb.cursor()
      try:
          myCursor.execute(query)
          print(databaseName+" is successfully created")
      except mysql.connector.IntegrityError as error:
          print("Error: {}".format(error))
      finally:
          myCursor.close()
          
     
#Inputs:
# tablename: Name of table to be created
# tableAttributes : Names ofattributes/columns in form of list
# databaseName: Name of database
 
# Output:Nothing...Creates a table named tableName in databaseName
def createTable(tableName, tableAttributes, databaseName):
      query = "use "+databaseName
      myCursor = mydb.cursor()
     
      try:
          myCursor.execute(query)
          print("Using database:"+databaseName)
     
      except mysql.connector.IntegrityError as error:
          print("Error: {}".format(error))
      finally:
          query1 = "create table "+tableName
          query1 = query1+"(";
          for i in tableAttributes:
                if i=="username":
                    query1 = query1 +" "+i+" varchar(256) primary key,"
                elif i=="privateKey" or i=="publicKey":
                    query1 = query1+" "+i+" longtext,"
                else:
                    query1 = query1+" "+i+" varchar(256),"
                    
          query1 = query1[:-1]
          query1 = query1+")"
          print(query1)
          myCursor.execute(query1)
          myCursor.close()
          
     
#Inputs:
# tablename: Name of table to be created
# userAttributeValues: values ofattributes/columns in form of list
# databaseName: Name of database
 
# Output:Nothing...Inserts user information into the table
def insert( tableName, databaseName, userAttributeValues):
     myCursor = mydb.cursor()
     query = "use "+databaseName
     myCursor.execute(query)
     query = "insert into "+tableName+" values ("
     try:
          for value in userAttributeValues:
            value="'"+value+"'"
            query=query+value+","
          query = query[:-1]+")"
          myCursor.execute(query)
          mydb.commit()
          # print(query)
          
     except mysql.connector.IntegrityError as error:
          print("Error: {}".format(error))
     finally:
          myCursor.close()
     
     
     
#Inputs:
# tablename: Name of table to be created
# databaseName: Name of database
 
# Output: returns the valuies stored in the table in form of list
def getTableValues(tableName, databaseName):
     myCursor = mydb.cursor()
     query = "use "+databaseName
     myCursor.execute(query)
     
     query = "select * from "+tableName
     myCursor.execute(query)
     usersInfo = myCursor.fetchall()
     
     for value in usersInfo:
          print(value)
          
     return usersInfo
 
#return users information of 'username' in form of list
def getUserInfo(username):
     myCursor = mydb.cursor()
     query = "use Docusign"
     myCursor.execute(query)
     
     query = "select * from usersInfo where usersInfo.username = "
     username = "'"+username +"'"
     query=query+username
     # print(query)
     myCursor.execute(query)
     userInfo = myCursor.fetchall()
     # for i in userInfo:
     #       print(i)
     return userInfo
 
#returns privateKey and publicKey of the username as tuple
def getKeys(username):
     myCursor = mydb.cursor()
     query = "use Docusign"
     myCursor.execute(query)
     
     query="select * from usersKeys where username = "
     username = "'"+username+"'"
     query = query+username
     myCursor.execute(query)
     keys=myCursor.fetchall()
     keys=keys[0][1:]
     #print(keys)
     return keys
     
#returns documents with one of the following parameters passed
#1-docid
#2-requestedBy
#3-signer         
def getDocument(queryParam):
     myCursor = mydb.cursor()
     query = "use Docusign"
     myCursor.execute(query)
     
     queryParam = "'"+queryParam+"'"
     query = "select * from documents where docid ="
     query = query+queryParam
     query = query+" OR requestedBy ="+queryParam +" OR signer="+queryParam
     myCursor.execute(query)
     print(query)
     return myCursor.fetchall()
     
def checkstatus(username):
     myCursor = mydb.cursor()
     query = "use Docusign"
     myCursor.execute(query)
     
     query = "select docName,signer,status from documents where documents.requestedBy =  " 
     username = "'"+username+"'"
     query = query + username
     myCursor.execute(query)
     usersInfo = myCursor.fetchall()
     
     # for value in usersInfo:
     #      print(value)
     return usersInfo     
 
# createDatabase("Docusign")
# createTable("usersInfo",["username","name","password","email"],"Docusign")
# createTable("usersKeys",["username","privateKey","publicKey"],"Docusign")
     
# insert("usersInfo","Docusign",["reddy14651","reddysekhar","hello123","reddy@gmail.com"])
# insert("usersInfo","Docusign",["satya","satyanarayana","hellosatya","satya@gmail.com"])
 
# getTableValues("usersInfo","Docusign")
# insert("usersKeys","Docusign",["reddy14651","reddysekharprivate","reddysekharpublic"])
# insert("usersKeys","Docusign",["satya","satyaprivate","satyapublic"])
 
#####
def databaseSetUp():
     createDatabase("Docusign")
     createTable("usersInfo",["username","name","password","email"],"Docusign")
     createTable("usersKeys",["username","privateKey","publicKey"],"Docusign")
     createTable("documents",["docid","docName","requestedBy","signer","status"],"Docusign")
     

#databaseSetUp()



def display_signer_documents(username):
     myCursor = mydb.cursor()
     query = "use Docusign"
     myCursor.execute(query)
     
     query = "select docName,requestedBy,docid from documents where documents.signer =  " 
     username = "'"+username+"'"
     query = query + username
     query = query + "AND status = 0" 
     myCursor.execute(query)
     usersInfo = myCursor.fetchall()
     
     # for value in usersInfo:
     #      print(value)
     return usersInfo   
    
  
def display_verifier_documents(username):
     myCursor = mydb.cursor()
     query = "use Docusign"
     myCursor.execute(query)
     
     query = "select docName,signer,docid,status from documents where documents.requestedBy =  " 
     username = "'"+username+"'"
     query = query + username
     query = query + "AND status = 1 or status=2" 
     myCursor.execute(query)
     usersInfo = myCursor.fetchall()
     
     # for value in usersInfo:
     #      print(value)
     return usersInfo  

def update_sign_status(docID,status):
    myCursor = mydb.cursor()
    query = "use Docusign"
    myCursor.execute(query)
    
    query = "UPDATE documents set status = "
    status = "'"+status+"'"
    query = query + status
    
    docID = "'"+docID+"'"
    query = query + "where docid ="
    query = query + docID
    myCursor.execute(query)
    mydb.commit()
    
def get_docID():
     myCursor = mydb.cursor()
     query = "drop database docusign"
     myCursor.execute(query)
     
     
def valid_signerID(username):
    info = getUserInfo(username)
    if (len(info) == 0):
       return 0
    else:
        return 1

     
     #query = "select docid from documents where documents.signer =  " 
     #username = "'"+username+"'"
     #query = query + username
     #myCursor.execute(query)
     #usersInfo = myCursor.fetchall()
     #return usersInfo  


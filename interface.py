2# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 18:06:42 2020

@author: hp
"""



import database as rd  
import signature as sd

import os


def signing():
    username=input("Enter Username:\t")
    #print(rd.getUserInfo(username))
    if(len(rd.getUserInfo(username))>=1):
        print("\nUsername already exists. Try a different one")
        signing()
    else:
        passwd=input("Enter a password:\t")
        name=input("Enter your name:\t")
        mail=input("Enter your E-Mail ID:\t")
        key = sd.generate_keys()
       
        rd.insert("usersInfo","Docusign",[username,name,passwd,mail])
        rd.insert("usersKeys","Docusign",[username,key[0],key[1]])   #private,public
        print("Created succesfully")
        welcome()
        
            

def logging():
    username=input("enter your username:\t")
    
    if(len(rd.getUserInfo(username))==0):
        print("No account with this Username.")
        welcome()
    else:
        password=input("enter your password:\t")
        db=rd.getUserInfo(username)
        #print(db)
        if(username==db[0][0] and password==db[0][2]):
            print("\n \t\t\t Successfully logged in!\n\n")
            homepage(username)
        else:
            print("Wrong credentials.2")
            welcome()
        
def welcome():
    #welcome page
    print("\n\t\t\t\t WELCOME TO DIGISIGN\n")
    print("Enter any one of the following options(number only)\n")
    print("1. Signup\n")
    print("2. Login\n")
    print("3. Exit\n")
    
    
    while True:
        try:
            num = input("Please enter your choice: ")
            num = int(num)
            break
        except ValueError:
            print("Not a valid integer! Please try again ...")
    
    if(num==1):
        print("\nPlease enter required details")
        signing()
    elif(num==2):
        print("\nPlease enter your login details:")
        logging()
    elif(num==3):
        print("\nExiting DigiSign\n")
        os._exit(1)
    else:
        print("\nIncorrect option selected\n")
        welcome()
        
def valid_document(filename):
    path = os.getcwd()
    for root, dir, files in os.walk(path):
        if filename in files:
            return 1
    return 0
def request_for_signature(username):
    print("Enter the document name to be signed:")
    docu_name = input()
    if(valid_document(docu_name)):
        print("\nEnter a valid Signer ID")
        signer = input()
        if(rd.valid_signerID(signer)):
            docu_id = docu_name + username + signer
            status="0"
            rd.insert("documents","Docusign",[docu_id,docu_name,username,signer,status])
            print("\nSuccessfully requested for Signature from "+signer+"\n")
            input("Press Enter to continue...")
            homepage(username)
        else:
            print("Please enter valid signer id")
            request_for_signature(username)
    else:
        print("\nPlease enter valid document name\n")
        request_for_signature(username)
    
    
def signing_doc(username):
    info = rd.display_signer_documents(username)
    if(len(info)==0):
        print("No documents to Sign")
        homepage(username)
    else:
        #print("S.No Document_Name Requested_By")
        print("The documents to be signed are:\n")
        for i in range(0,len(info)):
            print(i+1," ",info[i][0]," ",info[i][1])
    
        print("\nSelect any one valid Serial No.")
        num = 1;
        while True:
            try:
                num = input("Please enter your choice: ")
                num = int(num)
                break
            except ValueError:
                print("Not a valid integer! Please try again ...")
        if(num>len(info) or num<=0):
            print("Invalid number")
            signing_doc(username)
        else:
            docname = info[num-1][0]
            print("\n Choose the Hash algorithm to be used")
            print("1.SHA")
            print("2.MD5")
            count=1
            hash1 = '0'
            while(count==1):
                while True:
                    try:
                        hash_choice = input("Please enter your choice: ")
                        hash_choice = int(hash_choice)
                        break
                    except ValueError:
                        print("Not a valid integer! Please try again ...")
                if(hash_choice==1):
                    hash1="1"
                    count=0
                elif(hash_choice==2):
                    hash1="2"
                    count=0
                else:
                    print("Invalid input")
            docID = info[num-1][2]
            
            sd.sign_document(docname,username,docID,int(hash1))
            rd.update_sign_status(docID,hash1)
            
            print("You have successfully signed the document")
            input("Press Enter to continue...")
   


         
            
def verify_doc(username):
    info = rd.display_verifier_documents(username)
    if(len(info)==0):
        print("No documents to verify")
        homepage(username)
    else:
        #print("Sl.No doc_name signer_id status")
        status=["Unsigned","Signed by SHA","Signed by MD5"]
        
        print("The signatures of the following documents can be verified\n")
        for i in range(0,len(info)):
            print(i+1," ",info[i][0],"\t",info[i][1],"\t",status[int(info[i][3])])
        
        print("\n\nSelect any one valid Serial No.")
        while True:
            try:
                num = input("Please enter your choice: ")
                num = int(num)
                break
            except ValueError:
                print("Not a valid integer! Please try again ...")
        if(num>len(info) or num<=0):
            print("invalid number")
            verify_doc(username)
        else:
            docname = info[i-1][0]
            hashchoice=info[i-1][3]
            pubkey=rd.getKeys(info[i-1][1])
            publickey=pubkey[1]

            docID = info[i-1][2]
            
           
            if(sd.verify_signature(docname, publickey, docID, hashchoice)==1):
                print("\n \t \t \t The signature is authentic.")
            else: 
                print("\n \t \t \t The signature is not authentic.")
                
    input("Press Enter to continue...")
 
def homepage(username):
    
    print("\n \t\t \t  Welcome to Your Home Page, "+username+"\n")
    print("Enter any one of the following options(number only)\n")
    print("1. Request for signature\n")
    print("2. Sign a Document\n")
    print("3. Check signature status\n")
    print("4. Verify signature\n")
    print("5. Logout\n")
    
    
    while True:
        try:
            num = input("Please enter your choice: ")
            num = int(num)
            break
        except ValueError:
            print("Not a valid integer! Please try again ...")
        
    
    if(num==1):
        print("\nYes, Requesting for signature. Please enter the required details.\n")
        request_for_signature(username)
    elif(num==2):
        print("\nDisplaying documents to be signed:\n")
        signing_doc(username)
    elif(num==3):
        print("\nChecking Status\n")
        info=rd.checkstatus(username)
        status=["Unsigned","Signed by SHA","Signed by MD5"]
        #print("sl no.  doc_name   signer_id   status")
        for i in range(0,len(info)):
            print(i+1," ",info[i][0]," ",info[i][1]," ",status[int(info[i][2])])
        input("Press Enter to continue...")
            
    elif(num==4):
        print("Yes, verifying signature\n")
        verify_doc(username)
        
        
         
        #verifySignature(docname,pubKey,docID,hashfn)
    elif(num==5):
        print("Logging out")
        welcome()
        
    else:
        print("invalid input")  
    homepage(username)
welcome()
#a = rd.getTableValues("usersKeys", "Docusign")

#print(len(a))
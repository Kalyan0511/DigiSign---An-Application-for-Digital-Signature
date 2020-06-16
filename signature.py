# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 18:19:03 2020

@author: hp
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 09:21:59 2020

@author: kk
"""

from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA

import database as db


# This fucntion return a private key and a public key in a list.
# output: [privatekey, publickey]
def generate_keys():
    key = RSA.generate(2048)
    priv = key.exportKey(format='PEM', passphrase=None, pkcs=1)
    pub = key.publickey().exportKey(format='PEM')
    return [priv.decode("utf-8"),pub.decode("utf-8")]



def encode_key(key):
    given_key = bytes(key,"utf-8")
    key = RSA.importKey(given_key)
    return key



def create_hash(data,hashchoice):
    Hash = SHA256.new(data)
    if(hashchoice == 1):
        return Hash
    elif(hashchoice == 2):
        Hash = MD5.new(data)
    return Hash
   

def encrypt_rsa(data,key):
     enc_data = key.encrypt(data,32)
     return enc_data[0]
 
def decrypt_rsa(data,key):
    dec_data = key.publickey().decrypt(data)
    return dec_data[0]
    


        
# This function creates a digital signature and stores it in the same directory as the document.
# INPUT: document name, Username of the user who wants to sign, document ID and
# hashchoice - 1 or 2, 1 is SHA and 2 is MD5
# OUTPUT: creates a digital signature

def sign_document(docname,username, docID, hashchoice):
    
    
    keys = db.getKeys(username)
    privkey = encode_key(keys[0])
    
    fp = open(docname,"rb")
    message = fp.read()
    fp.close()
    
    Hash = create_hash(message,hashchoice)
    signature = pss.new(privkey).sign(Hash)
    
    outfile = docID+"_hash"
    out = open(outfile,"wb")
    out.write(signature)
    out.close()
    
def verify_signature(docname, publickey, docID, hashchoice):
    
    
    pubkey = encode_key(publickey)
    
    fp = open(docname,"rb")
    message = fp.read()
    fp.close()
    
    fp = open(docID+"_hash","rb")
    signature = fp.read()
    
    Hash = create_hash(message,hashchoice)
    verifier = pss.new(pubkey)
    try:
        verifier.verify(Hash, signature)
        #print("The signature is authentic.")
        return 1
    except (ValueError, TypeError):
        #print("The signature is not authentic.")
        return 0
    


#def main():
    
#    docname = input("enter the name of document:\n")
#    sign_document(docname,"kk","12345",1)
    
#    a = verify_signature(docname,"","12345",1)
    
#    print(a)
    

if __name__=="__main__":
    keys = generate_keys()
    print(keys[0])
    print(len(keys[1]))
    #    main()
    
    
    
    






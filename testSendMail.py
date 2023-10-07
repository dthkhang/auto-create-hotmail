import os, pymongo,certifi,smtplib
from typing import Collection
from pymongo import MongoClient
from io import open_code
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
password = os.environ.get("*****")
ca = certifi.where()
url = f"******"
connection = MongoClient(url,tlsCAFile=ca)
collection = connection['dbn_users']['col_users']
findS = list(collection.find({}))
    #count user
with open(r'../ToolRegMail/userlogin.txt', 'w') as user:
    countUser = 0
    for elementsUser in findS:
        user.write(elementsUser['user'])
        user.write('\n')
        countUser += 1
pathRemoveI = '../ToolRegMail/userlogin.txt'
if os.path.isfile(pathRemoveI):
        os.remove(pathRemoveI)
print("You have " + str(countUser) + " in Database")
i = 0
y = 0
s = 0
data = 0
for data in range(countUser):
    with open(r'../ToolRegMail/UserLogin.txt', 'w') as user:
        for elementsUser in findS:
            user.write(elementsUser['user'])
            user.write('\n')
    fileU = open(r'../ToolRegMail/UserLogin.txt')
    DataEmail = fileU.readlines()
    email = DataEmail[i].strip()
    mailsend = DataEmail[i-1].strip()
    print("Email: " + str(i+1) + email)
    print("Send to: " + mailsend)
    i += 1
        # #pass
    with open(r'../ToolRegMail/PassLogin.txt', 'w') as pas:
        for elementsPas in findS:
            pas.write(elementsPas['pass'])
            pas.write('\n')
    fileP = open(r'../ToolRegMail/PassLogin.txt')
    DataPwd = fileP.readlines()
    pwd = DataPwd[y].strip()
    print("Pass: " + pwd)
    pathRemoveI = '../ToolRegMail/UserLogin.txt'
    pathRemoveII = '../ToolRegMail/PassLogin.txt'
    if os.path.isfile(pathRemoveI):
        os.remove(pathRemoveI)
    if os.path.isfile(pathRemoveII):
        os.remove(pathRemoveII)
    y += 1
        #subject & body
    fileS = open(r'../ToolRegMail/content.txt')
        # dataSub = fileS.readlines()
        # subject = 'How do you feel to day?'
    fileS = open(r'../ToolRegMail/content.txt')
    dataBody = fileS.readlines()
    body = "".join(dataBody)
        #message

    message = f"""Form: {email}
    To:{mailsend}
    Subject: How do you feel to day?\n
    {body}
    """
    client = smtplib.SMTP("smtp-mail.outlook.com",587)
    client.starttls()
    client.login(email,pwd)
    client.sendmail(email,mailsend,message)
    print('\n')
    print("Mail thanh cong nha hihi")
    print('\n')
    pathRemoveI = '../ToolRegMail/UserLogin.txt'
    pathRemoveII = '../ToolRegMail/PassLogin.txt'
    if os.path.isfile(pathRemoveI):
        os.remove(pathRemoveI)
    if os.path.isfile(pathRemoveII):
        os.remove(pathRemoveII)
client.quit()

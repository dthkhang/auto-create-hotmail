from posixpath import split
from dotenv import load_dotenv, find_dotenv
import os,pprint,certifi,time
from datetime import datetime
import numpy as np
from pymongo import MongoClient
# sltk = int(input('Nhap sltk '))
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
ca = certifi.where()
url = f"mongodb+srv://khang:{password}@cluster0.nujj6h1.mongodb.net/?retryWrites=true&w=majority"
connection = MongoClient(url,tlsCAFile=ca)
collection = connection['dbn_users']['col_users']
findS = list(collection.find({}))
print(findS)
# with open(r'../ToolRegMail/UserLogin.txt', 'w') as accout: #tạo file txt chứa tài khoản vừa đăng kí để phân nhiệm vụ cho từng luồng
#     for elments in findS:
#         accout.write(elments['user'])
#         accout.write('\n')
# dataLogin = open('UserLogin.txt').readlines()
# listUserLogin = np.array_split(dataLogin, int(sltk))



    
from email.headerregistry import HeaderRegistry
from io import open_code
from webbrowser import Chrome
from selenium import webdriver #từ thư viện selenium lấy webdriver của chrome để get link chrome
from selenium.webdriver.common.by import By #từ thư viện selenium lấy By tìm các element trong link vừa get
from selenium.webdriver.support.ui import WebDriverWait          # => 2 bộ này dùng để chờ các element của web xuất hiện để thục hiện cái dòng lệnh auto (fake người dùng)
from selenium.webdriver.support import expected_conditions as ec # =>
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy,ProxyType
import time  #xử lý các tác vụ liên quan đến thời gian
from datetime import datetime
import os, sys, pprint,random
from random import randint
import threading #thư viện để chạy xử lý đa luồng
import numpy
from typing import Collection
import pymongo
from pymongo import MongoClient
import json,certifi
from dotenv import load_dotenv, find_dotenv

sltk = int(input("Nhap so luong can chay:"))
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
ca = certifi.where()
url = f"mongodb+srv://khang:{password}@cluster0.nujj6h1.mongodb.net/?retryWrites=true&w=majority"
connection = MongoClient(url,tlsCAFile=ca)
collection = connection['dbn_users']['col_users']
findS = list(collection.find({}))

with open(r'../ToolRegMail/UserLogin.txt', 'w') as accout: #tạo file txt chứa tài khoản vừa đăng kí để phân nhiệm vụ cho từng luồng
    for elments in findS:
        accout.write(elments['user'])
        accout.write('\n')
dataUserLogin = open('UserLogin.txt').readlines()
listUserLogin = numpy.array_split(dataUserLogin, int(sltk))

with open(r'../ToolRegMail/PassLogin.txt', 'w') as accout: #tạo file txt chứa tài khoản vừa đăng kí để phân nhiệm vụ cho từng luồng
    for elments in findS:
        accout.write(elments['pass'])
        accout.write('\n')
dataPassLogin = open('PassLogin.txt').readlines()
listPassLogin = numpy.array_split(dataPassLogin, int(sltk))
proxy_ip_port = '192.168.1.20:4001'
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxy_ip_port
proxy.ssl_proxy = proxy_ip_port
capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)
def run(numOfMulti):
    PROXY = '192.168.1.20:4001'
    print("Dang chay luong ", numOfMulti)
    inputUserLogin = listUserLogin[numOfMulti][0]
    inputPassLogin = listPassLogin[numOfMulti][0]
    chrome_options = webdriver.ChromeOptions() #truy cấp đến các options của chrome
    chrome_options.add_argument("--incognito") #bật chế độ ẩn danh để không lưu thông tin tài khoản
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-site-isolation-trials")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service('./driver/chromedriver')
    driver = webdriver.Chrome(service = service, options = chrome_options,desired_capabilities=capabilities) #trỏ đến chromedriver và chọn options ẩn danh, tắt websecurity, cache
    driver.execute_cdp_cmd("Page.setBypassCSP", {"enabled": True})
    x = numOfMulti * 520
    y =  50
    driver.set_window_rect(x,y,100,670)
    driver.get("https://login.live.com/")
    time.sleep(1)
    driver.find_element(By.XPATH,'/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]').send_keys(inputUserLogin)
    time.sleep(2)
    driver.find_element(By.XPATH,'/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input').send_keys(inputPassLogin)
    time.sleep(2)
    driver.execute_script("document.querySelectorAll('#idBtn_Back')[0].click()")
    time.sleep(2)
    driver.execute_script("document.querySelectorAll('#O365_MainLink_NavMenu')[0].click()") 
    time.sleep(2)
    driver.execute_script("document.querySelectorAll('#O365_AppTile_Mail')[0].click()")
    pathRemoveI = '../ToolRegMail/UserLogin.txt'
    pathRemoveII = '../ToolRegMail/PassLogin.txt'
    if os.path.isfile(pathRemoveI):
        os.remove(pathRemoveI)
    if os.path.isfile(pathRemoveII):
        os.remove(pathRemoveII)
    time.sleep(1000)
threads = []
for numOfMulti in range(sltk):
    threads += [threading.Thread(target=run, args={numOfMulti},)]
for t in threads:
    t.start() 
for t in threads:
    t.join() 
print("Exit")
from ast import arg
from email.headerregistry import HeaderRegistry
from io import open_code
from multiprocessing.connection import wait
from webbrowser import Chrome
from selenium import webdriver #từ thư viện selenium lấy webdriver của chrome để get link chrome
from selenium.webdriver.common.by import By #từ thư viện selenium lấy By tìm các element trong link vừa get
from selenium.webdriver.support.ui import WebDriverWait          # => 2 bộ này dùng để chờ các element của web xuất hiện để thục hiện cái dòng lệnh auto (fake người dùng)
from selenium.webdriver.support import expected_conditions as ec # =>
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy,ProxyType
import os, sys, pprint,numpy,json,certifi,random,threading,pymongo,requests,time
from datetime import datetime
from random import randint
from anycaptcha import FunCaptchaProxylessTask, AnycaptchaClient
from typing import Collection
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
#-----------------------------------------------------------
def regmail():
    dataUser = []
    sltk = int(input("nhap sltk can dang ky: "))
    userName = str(input("nhap username can dang ky: "))
    passWord = input("nhap password can dang ky: ")
    list_ho = ['Bùi','Trần','Nguyễn','Dương','Phan','Châu','Trương','Lê','Phạm','Hoàng','Huỳnh','Đặng','Ngô','Võ',]   #
    list_ten = ['Khang','Tài','Hoàn','Tiến','Khoa','Quân','Xuân','Trang','Như','Kiệt','Khải','Trực','Thịnh','Thông',] #
    ho = random.choice(list_ho)                                                                                       # radom chọn tên
    ten = random.choice(list_ten)                                                                                     #
    i = 0
    while i < sltk:
        userMail = userName + str(i) +"@hotmail.com"
        dataUser.append(userMail)
        i += 1
    with open(r'../ToolRegMail/src/User.txt', 'w') as accout: #tạo file txt chứa tài khoản vừa đăng kí để phân nhiệm vụ cho từng luồng
        for elements in range(len(dataUser)):
            accout.write(dataUser[elements])
            accout.write('\n')
    data = open(r'../ToolRegMail/src/User.txt').readlines()
    listUserMulti = numpy.array_split(data, int(sltk))
    #-----------------------------------------------------------
    def FunCaptcha():
        # try:
        data_any={
            "clientKey":"687cb679534e45a1bd565811ccfc8834",
            "task":{
                "type":"FunCaptchaTaskProxyless",
                "websiteURL":"https://signup.live.com/signup?lic=1&uaid=9b23f83c11f440f8993626a59f3aac7f",
                "websitePublicKey":"B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
            },
            "softId":847,
            "languagePool":"en"
        }
        posat=requests.post("https://api.anycaptcha.com/getBalance",data={"clientKey": "687cb679534e45a1bd565811ccfc8834"}).json()
        if float(posat["balance"])<0.003:
            print("Hết tiền")
            return "money"
        post=requests.post("https://api.anycaptcha.com/createTask",json=data_any).json()
        taskId=post["taskId"]
        result=requests.post("https://api.anycaptcha.com/getTaskResult",data={"clientKey":"687cb679534e45a1bd565811ccfc8834","taskId":taskId}).json()
        if result["errorId"]==2:
            exit()
        if result["status"]=="ready" and result["errorId"]==0:
            return result["solution"]["token"]
    #-----------------------------------------------------------
    def getDatabase():
        load_dotenv(find_dotenv())
        password = os.environ.get("MONGODB_PWD")
        ca = certifi.where()
        url = f"mongodb+srv://khang:{password}@cluster0.nujj6h1.mongodb.net/?retryWrites=true&w=majority"
        connection = MongoClient(url,tlsCAFile=ca)
        collection = connection['dbn_users']['col_users']
        now = datetime.now()
        dayTime = now.strftime("%d/%m/%Y %H:%M")
        for elements in range(len(dataUser)):
            data = {"user": dataUser[elements], "pass": passWord, "time": dayTime}
            collection.insert_one(data)
    # -----------------------------------------------------------
    proxy_ip_port = '192.168.1.20:4001'
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = proxy_ip_port
    proxy.ssl_proxy = proxy_ip_port
    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(capabilities)
    def run(numOfMulti):
        PROXY = '192.168.1.20:4001'
        print("Loading in ", numOfMulti)
        inputUser = listUserMulti[numOfMulti][0]
        chrome_options = webdriver.ChromeOptions() #truy cấp đến các options của chrome
        chrome_options.add_argument("--incognito") #bật chế độ ẩn danh để không lưu thông tin tài khoản
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-site-isolation-trials")
        chrome_options.add_argument("--disable-application-cache")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--proxy-sever=%s" %PROXY)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service('./driver/chromedriver')
        driver = webdriver.Chrome(service = service, options = chrome_options,desired_capabilities=capabilities) #trỏ đến chromedriver và chọn options ẩn danh, tắt websecurity, cache
        driver.execute_cdp_cmd("Page.setBypassCSP", {"enabled": True})
        x = numOfMulti * 520
        y =  50
        driver.set_window_rect(x,y,100,670)
        driver.get("https://signup.live.com/?lic=1") #get link để mở link
        time.sleep(1)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[1]/fieldset/div[1]/div[3]/div[2]/div/input').send_keys(inputUser)
        time.sleep(2)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[3]/div/input[2]').send_keys(passWord)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[5]/div/label/input').click()
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[7]/div/div/div[2]/input').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[1]/div[3]/div[1]/input').send_keys(ho)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[1]/div[3]/div[2]/input').send_keys(ten)
        time.sleep(0.5)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[2]/div/div/div[2]/input').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[4]/div[3]/div[1]/select/option[2]').click()
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[4]/div[3]/div[2]/select/option[2]').click()
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[4]/div[3]/div[3]/input').send_keys(random.randint(1968,2002))
        time.sleep(0.5)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[6]/div/div/div[2]/input').click()
        waiting = WebDriverWait(driver,10).until(
            ec.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[2]'))
        )
        time.sleep(4)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[3]/iframe')
        time.sleep(2)
        token = FunCaptcha()
        driver.execute_script("""var anyCaptchaToken = '"""+token+"""';var enc = document.getElementById('enforcementFrame');
                                            var encWin = enc.contentWindow || enc;
                                            var encDoc = enc.contentDocument || encWin.document;
                                            let script = encDoc.createElement('SCRIPT');
                                            script.append('function AnyCaptchaSubmit(token) { parent.postMessage(JSON.stringify({ eventId: "challenge-complete", payload: { sessionToken: token } }), "*") }');
                                            encDoc.documentElement.appendChild(script);
                                            encWin.AnyCaptchaSubmit(anyCaptchaToken);""")
        time.sleep(10)
        driver.execute_script("document.querySelectorAll('#idBtn_Back')[0].click()")
        #remove file User.txt
        pathRemove = '../ToolRegMail/src/User.txt'
        if os.path.isfile(pathRemove):
            os.remove(pathRemove)
        getDatabase()
        #add data user to account.csv
        with open(r'../../ToolRegMail/account.csv', 'a+', encoding='utf-8-sig') as account:
            header = account.write('Tài Khoản;Mật Khẩu;Thời Gian Tạo\n')
            now = datetime.now()
            dayTime = now.strftime("%d/%m/%Y %H:%M")
            for elements in range(len(dataUser)):
                row = account.write(dataUser[elements] + ';' + passWord + ';' + dayTime + '\n')
        time.sleep(4)
        driver.quit()
    threads = []
    for numOfMulti in range(sltk):
        threads += [threading.Thread(target=run, args={numOfMulti},)]
    for t in threads:
        t.start() 
    for t in threads:
        t.join() 
    print("Create Account Success")
    print("Account will be saved to account.csv and MongoDB")
from weakref import proxy
import requests,random,time,threading
from webbrowser import Chrome
from selenium import webdriver #từ thư viện selenium lấy webdriver của chrome để get link chrome
from selenium.webdriver.common.by import By #từ thư viện selenium lấy By tìm các element trong link vừa get
from selenium.webdriver.support.ui import WebDriverWait          # => 2 bộ này dùng để chờ các element của web xuất hiện để thục hiện cái dòng lệnh auto (fake người dùng)
from selenium.webdriver.support import expected_conditions as ec # =>
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy,ProxyType
sltk = int(input("So luong:"))
# proxy = str(input('Enter your Proxy: '))

proxy_ip_port = '192.168.1.20:4001'
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxy_ip_port
proxy.ssl_proxy = proxy_ip_port
capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)

def run(numOfMulti):
    PROXY = '192.168.1.20:4001'
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
    driver.get('https://whoer.net/')    
    time.sleep(100)

threads = []
for numOfMulti in range(sltk):
    threads += [threading.Thread(target=run, args={numOfMulti},)]
for t in threads:
    t.start() 
for t in threads:
    t.join()
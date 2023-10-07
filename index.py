from getpass import getpass
import sys,os

from src.reg import regmail
from src.send import sendmail
from src.logo.logo import logo1,logo2,cnt
from dotenv import load_dotenv, find_dotenv

def check():
    options = int(input("=> Select here: "))
    if options == 1:
        regmail()
    elif options == 2:
        sendmail()
    elif options == 3:
        print("Comming soon!")
    elif options == 4:
        os.system('clear')
        sys.exit("Thanks for that, see at next time bro!")
    cnt()
    exitSys = str(input("=> Enter here: "))
    if exitSys == 'yes':
        os.system('clear')
        logo2()
        check()
    if exitSys == 'no':
        sys.exit("Thanks for that, see at next time bro!")
    else:
        os.system('clear')
        sys.exit("Wrong key! See you later")
while True:
    load_dotenv(find_dotenv())
    key = os.environ.get("KEY")
    inputKey = getpass("Enter your KEY to continue: ")
    if key == inputKey:
        login = """
        \033[1;91m         --  Logged in successfully --"""
        print(login)
        logo1()
        check()
    else:
        sys.exit("Try again or contact to Admin for continue!")

import sys, time
def logo1():
    background = """ 
\033[1;92m╔══════════════════════════════════════════════════════════════╗ 
\033[1;93m ================== \033[1;96m 21CT112 - 304LAB - LHU \033[1;93m===================
\033[1;92m╚══════════════════════════════════════════════════════════════╝\n
\033[1;95mPlease select the option you want to make:\n
\033[1;96m1: Regmail (Outlook)\n
\033[1;96m2: Sendmail\n
\033[1;96m3: Checkmail\n
\033[1;96m4: Exit
\033[1;97m
"""
    for i in background: 
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.004)    

def logo2():
    background = """ 
\033[1;95mPlease select the option you want to make:
\033[1;96m1: Regmail (Outlook)
\033[1;96m2: Sendmail
\033[1;96m3: Checkmail
\033[1;96m4: Exit
\033[1;97m
"""
    for i in background: 
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.004)   

def cnt():
    background = """ 
\033[1;91mDo you want continue? Please enter Yes or No to continue!
\033[1;97m
"""
    for i in background: 
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.004)    

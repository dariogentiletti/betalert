######################################################################
######################################################################
##
##                      BETALERT v0.2
##        (https://github.com/dariogentiletti/betalert)
##
##       Soccer-rating.com webscraper for Tipster bets 
##                    by dariogentiletti
##       
##
######################################################################
######################################################################


import requests, re, notify2, time, sys
from bs4 import BeautifulSoup
from data import tipsters_url, ICON_PATH
#import PySimpleGUI as sg 


def connectWebsite(URL):
    '''Connect to a website and extract the HTML code'''

    try: # Check if it is connected to internet
        page = requests.get(URL)
        if "Soccer-Rating.com" in page:
            content = page.content
            raise
    except:
        print("Internet Connection Error!")
    content = page.content
    return content


def soupIt(content):
    '''Use BeautifulSoup library to syntax the HTML content'''

    soup = BeautifulSoup(content, 'html.parser')
    return soup


def findTip(soup):
    '''Extract the tip of the day from Soccer-Rating tipster page
    that has been syntaxed by BeautifulSoup'''

    # Find the section with tips of the day
    focus_soup = soup.find_all("table", attrs={"cellpadding": "3"})

    # Exploit the value that they exclusively insert for the tips suggested from the tipster
    regex_25 = "1/25"

    if re.search(regex_25, str(focus_soup[1])):
        tip = focus_soup[0].text.split("*")[0] # The tips of the day
        tip = re.split("[0-9]/25", str(tip))[1:]
        
        tip_temp = focus_soup[1].text.split("*")[0] # The tips of tomorrow
        tip_temp = re.split("[0-9]/25", str(tip_temp))[1:]
        
        tip.extend(tip_temp)
        
        
    else:
        tip = focus_soup[0].text.split("*")[0] # The tips of the day
        tip = re.split("[0-9]/25", tip)[1:]


    return tip


def sendNotification(lst, tipster):
    # logo for notification

    # initiate Notify2 plugin
    notify2.init("BetAlert") 

    # create Notification object
    n = notify2.Notification(None) 
      
    # set urgency level 
    n.set_urgency(notify2.URGENCY_NORMAL) 
      
    # set timeout for a notification 
    n.set_timeout(1000) 
    
    # show notification on screen 
    if len(lst) > 1:
        for count, item in enumerate(lst):
            n.update("BetAlert -- {} new tips from {}! ({} / {})".format(len(lst), tipster, count+1, len(lst)), item, icon = ICON_PATH)
            n.show()
            time.sleep(5) # Cooldown of 5 seconds between tips of same tipster
    else:
            n.update("BetAlert -- New Tip from {}!".format(tipster), lst[0])
            n.show()
      
 
def findCurrentTime():
    '''Find current time in hours:minutes:seconds'''

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time


def findTipsterCode(url):
    '''Find code of Soccer-Rating.com for Tipsters'''
    foo = url.split('=')
    return foo[-1]


def findTipsterName(dic, pos): 
    '''Find code of Soccer-Rating.com for Tipsters (NOT USED)'''

    return list(dic.keys()[pos])


def createInitDictionary(lst):
    '''Create initial dictionary to store tips'''
    foo = dict()
    for key in lst:
        foo[key] = []
    return foo


def betAlerts(dic_data):

    # Settings
    cooldownTime = 1200 # How much time between each check, in seconds. Default: 1200 (i.e. 20 minutes)

    # Activate if you want to have output printed on a file and not on a console
    #sys.stdout=open("betalert_log.txt","w")

    # Initialize variables 'money' and 'data' and 'i'
    money = ["NA"]
    data = createInitDictionary(dic_data) # Tipsters_url is imported by data.py file
    i = 1

    while True:

        for tipster, url in dic_data.items():
            
            content = connectWebsite(url)
            soup = soupIt(content)
            temp = findTip(soup) 

            # Activate when debugging
            #print("START IF LOOP FOR TIPSTER:{} \n  TEMP:{} \n DICT: {}".format(tipster, temp, data))

            if len(temp[0])<2: # To check if there is no bet of the day
                print("No bets of the day from the tipster {}.".format(tipster))
                print("---------------------------")
                continue

            elif temp in data[tipster]: # To avoid send notifications if already did before for that game
                print("No new tips from the tipster {} since the last check.".format(tipster))
                print("---------------------------")
                continue
            
            else:
                money = temp

                # Add tip to the dictionary of tipsters:tips
                data[tipster].append(money)

                # Send notification to the desktop with Notify2
                sendNotification(money, tipster)
                
                # Messages in console to track activity
                print(money)
                current_time = findCurrentTime()
                print("Tip Notification from {} sent at {}!".format(tipster, current_time))
                print("---------------------------")

        print("****** Check number {} completed. Next one coming in 20 minutes. ******".format(i))
        print("\n")
        print("_______________________________________________________________________")
        i = i+1
        time.sleep(cooldownTime)

    # Activate if want to have output printed on a file and not on a console
    #sys.stdout.close()





def main():
   betAlerts(tipsters_url)



main()






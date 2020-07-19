######################################################################
######################################################################
##
##                      BETALERT v0.1
##  
##       Soccer-rating.com webscraper for Tipster bets 
##
##                    by dariogentiletti
##
######################################################################
######################################################################


import requests, re, notify2, time, sys
from bs4 import BeautifulSoup
from data import tipsters_url
import PySimpleGUI as sg 


def connectWebsite(URL):
    '''Connect to a website and extract the HTML code'''

    page = requests.get(URL)
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

    # Split to extract only the tip 
    tip = focus_soup[0].text.split("*")[0].split(" 1/25 ")
    return tip


def sendNotification(lst, tipster):
    # logo for notification
    ICON_PATH = None  

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
            n.update("BetAlert -- {} new tips from {}! ({} / {})".format(len(lst), tipster, count+1, len(lst)), item)
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
   
    sg.theme('BluePurple') 
       
    layout = [[sg.Text('Your typed characters appear here:'), 
               sg.Text(size=(15,1), key='-OUTPUT-')], 
              [sg.Input(key='-IN-')], 
              [sg.Button('Display'), sg.Button('Exit')]] 
      
    window = sg.Window('Introduction', layout) 
      
    while True: 
        event, values = window.read() 
        print(event, values) 
          
        if event in  (None, 'Exit'): 
            break
          
        if event == 'Display': 
            # Update the "output" text element 
            # to be the value of "input" element 
            window['-OUTPUT-'].update(values['-IN-']) 
      
    window.close() 




if __name__ == "__main__":
    main()






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


import requests, re, notify2, time 
from bs4 import BeautifulSoup


def connectWebsite(URL):
    page = requests.get(URL)
    content = page.content
    return content

def soupIt(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup

def findTip(soup):
    soup
    return

def sendNotification(lst):
    # logo for notification
    ICON_PATH = None  

    # initiate Notify plugin
    notify2.init("BetAlert") 

    # create Notification object
    n = notify2.Notification(None, icon = ICON_PATH) 
      
    # set urgency level 
    n.set_urgency(notify2.URGENCY_NORMAL) 
      
    # set timeout for a notification 
    n.set_timeout(10000) 
    
    # show notification on screen  
    for item in lst:
        n.update(item)
        n.show()
        time.sleep(10)
      
 



def main():
    content = connectWebsite('http://www.soccer-rating.com/picks?top=1&ts=1366') # Tipster ID 3788
    soup = soupIt(content)
    focus_soup = soup.find_all("table", attrs={"cellpadding": "3"})


    '''Extracting the tip of the day'''
    # Extract text for the first table containing tips of the day and encode it as ascii
    temp = focus_soup[0].text.split("*")[0].split(" 1/25 ") # Split to extract only the tip


    if len(temp[0])<1: # To check if there is no bet of the day
        print("No bets of the day from the tipster")
    if 'money' in locals():
        if temp == money: # To avoid send notifications if already did before for that game
            print("No new bets from the last check")
    else:
        money = temp
        print("NOTIFICA!!!")
        sendNotification(money)
        print(money)



if __name__ == "__main__":
    main()





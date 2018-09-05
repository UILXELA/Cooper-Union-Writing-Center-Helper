from lxml import etree
import urllib.request
import urllib
import requests
import time
import datetime
import random
import itchat
from bs4 import BeautifulSoup
from http import cookiejar
import json

session = requests.session()
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}

#Define a function that recieves a html and outputs a xml
def getxml(html):
    return etree.HTML(html)

#Login
def login(email, pasw):
    loginurl = "https://cooper.mywconline.com/index.php"
    #o = requests.get(loginurl, headers = headers)
    #xsrf = getxml(o.content).xpath('//input[@name = "_xsrf"]/@value')
    #print (xsrf)
    formdata = {
        #'_xsrf':xsrf[0],
        'email':email,
        'password':pasw,
        'scheduleid':'sc15b87f7e8c1ce4',
        'setCookie':'true',
        'login':'Log In'
    }
    response = session.post(url=loginurl,data=formdata,headers=headers)
    response = session.get("https://cooper.mywconline.com/schedule.php?date=10-16-2017&scheduleid=sc1599b1048f2535", headers = headers)
  
    with open("cookies.txt",'w') as f:
        json.dump(session.cookies.get_dict(),f)
    with open("login.html","wb") as f:
        f.write(response.content)

    with open("cookies.txt",'r') as f:
        cookies = json.load(f)
    session.cookies.update(cookies)

def CheckSpot(id):
    checkUrl = "https://cooper.mywconline.com/schedule.php?focus=&scheduleid=sc1599b1048f2535&date=10-23-2017"
    response2 = session.get(checkUrl, headers = headers)
#    print(response2.url)
    soup = BeautifulSoup(response2.content,'lxml')
    for div in soup.body.find_all('div', attrs={'style':'width:100%; padding-bottom: 25px; height: auto; border-top: solid #CCCCCC 1px; border-bottom: solid #CCCCCC 1px; background-color:#EbEbEb;'}):
        for div1 in  div.find_all('div', attrs={'style':'width:100%; overflow:auto;'}):
            for table in div1.find_all('table', class_ ='sample4'):
                tr1 = table.find('tr')
                date = tr1.td.a['onmouseover'][34:37]
                for tr in table.find_all('tr', class_='cellColor'):
                    for td in tr.find_all('td', attrs={'colspan':'1'}):
                        global boolea
                        boolean = '#3579DC' not in td['style'] and '#42426F' not in td['style']
                        if boolean:
                            msg = '\n\n\n\n\nSpots Avaliable on ' + date
                            print(msg)
                            send_notification(msg, id)
                            #print(itchat.send('There is a spot', toUserName= None))    for debug
                            #print(itchat.get_friends())
                            print('Time:')
                            displayTime()

def send_notification(msg, remarkName):
    memberList = itchat.search_friends(remarkName = remarkName)
    # if not full match, you may use this
    # memberList = filter(lambda m: nickName in m['NickName'], itchat.get_contract()[1:])
    for member in memberList:
        itchat.send(msg, member['UserName'])
    #    time.sleep(.5)
    #time.sleep(3)

def displayTime():
    now = datetime.datetime.now()
    print (now.strftime('%Y-%m-%d %H:%M:%S'))


boolean = True
itchat.auto_login(enableCmdQR=-2)

email = input('Your cooper account: ')
pasw = input('your password: ')
wechatID = input('wechat contact name: ')
login(email, pasw)
print('\n\n\n\Start Time:')
displayTime()
while boolean:
    CheckSpot(wechatID)
    time.sleep(random.uniform(50, 100))

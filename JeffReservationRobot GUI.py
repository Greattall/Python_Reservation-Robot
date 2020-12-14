import requests
import shutil
from bs4 import BeautifulSoup
rs = requests.session()
from IPython.display import Image
import PySimpleGUI as sg
import time
import datetime
global STATUS
STATUS = 'Fail'

global RESULT
RESULT = '預約失敗'

global TargetTime
TargetTime = 999999
def getCurrentTime():
        return time.strftime("%Y-%m-%d %H:%M:%S")
def getDay():
        return datetime.date.today() + datetime.timedelta(days=1)
def getTimeValue():
        return int(time.strftime("%H%M%S"))

def getCheckCode():
    res=rs.get('https://www.tyht-fitness.com.tw/booking/ball/login/captcha',stream=True,verify=False)
    f = open('check.png','wb')
    shutil.copyfileobj(res.raw, f)
    f.close()
    #----For python IDLE----#
    #from PIL import Image
    #img = Image.open('check.png')
    #img.show()
    #----For python IDLE----#

def getFace(var):
     if var=='A' : return '3-1'
     if var=='B' : return '3-2'
     if var=='C' : return '3-3'
     if var=='D' : return '3-4'
    
    



def Logging():
    global STATUS
   # Image('check.png')

    #CheckCode = input ("Please Enter Graphic Check Code : ")
#Get Value From GUI
    account   = values['ID']
    password  = values['PW']
    CheckCode = values['CK2']
#Get Value From GUI
#----Logging----#
    UserData ={
        #'account':'CJ07M52',
        #'password':'61801377',
        'account':account,
        'password':password,
        'code':CheckCode
    }
    r1 = rs.post("https://www.tyht-fitness.com.tw/booking/ball/login",data=UserData,verify=False)
    print(r1.text)
    if '登入成功' in r1.text :
        STATUS = 'Success'
#----Logging----#




def Fightting():
    global TargetTime
    global RESULT
#----Fightting----#
    r2 = rs.get("https://www.tyht-fitness.com.tw/booking/ball/main")
#print(r2.text)
    soup = BeautifulSoup(r2.text,"html.parser") #將網頁資料以html.parser
    tokenValue = soup.find("input").attrs["value"]
#result = soup.find("form")
    print(tokenValue)
#Get value From GUI
    date     = values['Day']
    time     = values['TD']
    face     = getFace(values['FACE'])
    partner  = values['PID']
    Ppassword= values['PPW']
#Get value From GUI
    SelectDate  ={
        'date':date
    }
    r3=rs.post("https://www.tyht-fitness.com.tw/booking/ball/main/selectDate",data=SelectDate)
    
    SelectBall ={
        'id':'1425' # Fix Badminton
    }
    r4=rs.post("https://www.tyht-fitness.com.tw/booking/ball/main/selectBall",data=SelectBall)

    SelectTime ={
        'time':time
    }
    r5=rs.post("https://www.tyht-fitness.com.tw/booking/ball/main/selectTime",data=SelectTime)

    PartnerData ={
        'token':tokenValue,
        'face':face,
        'partner':partner,
        'password':Ppassword
    }
    r6 = rs.post("https://www.tyht-fitness.com.tw/booking/ball/main",data=PartnerData,verify=False)
    print(r6.text)
    if '預約成功' in r6.text :
            TargetTime = 999999
            RESULT = '預約成功'

#----Fightting----#




layout = [
        [sg.Text('洪教授機機人幫你搶場地',text_color='yellow',font=('新細明體',20))],
        [sg.Text('會員編號 :'),sg.Input('請輸入會員編號',key='ID')],
        [sg.Text('密碼        :'),sg.Input('身分證後3碼/生日後2碼/手機後3碼',key='PW')],
        [sg.Text('驗證碼    :',key='CK1'),sg.Input('請輸入驗證碼，皆為大寫半形英文',key='CK2')],
        [sg.Button('取得驗證碼'),sg.Image(key='CKF')],
        [sg.Button('會員登入'),sg.Text(STATUS,visible=False,size=(7,1),key='STATUS')],
        [sg.Text('日期       :'),sg.Input(getDay(),key='Day')],
        [sg.Text('類別       :'),sg.InputCombo(['羽球'],['羽球'],key='Cla',size=(20,2))],
        [sg.Text('時段       :'),sg.Input('18:30~19:00',key='TD')],
        [sg.Text('球面       :'),sg.InputCombo(['A','B','C','D'],['D'],key='FACE',size=(20,2))],
        [sg.Text('夥伴編號 :'),sg.Input('請輸入夥伴編號',key='PID')],
        [sg.Text('夥伴密碼 :'),sg.Input('身分證後3碼/生日後2碼/手機後3碼',key='PPW')],
        [sg.Text('目標時間 :'),sg.Input('',key='TT')],
        [sg.Button('StartTimer'),sg.Text(RESULT,visible=False,size=(15,1),key='RESULT')],
        [sg.Button('Exit')],
        [sg.Text('當前時間 :'),sg.Text(getCurrentTime(),key='-Time-')]
          ]

window = sg.Window('Jeff_ReservationRobot_GUI', layout)

while True:  # Event Loop
    event, values = window.read(timeout=1000)
    window['-Time-'].update(getCurrentTime())
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        sg.popup('離開視窗!', text_color='red') 
        break
    if event == '搶爆':
        Fightting()
        #print(values['ID'])
        #print(values['PW'])
        #print(values['Cla'])
        #print(values['CK2'])
    if event == '會員登入':
        Logging()
        window['STATUS'].update(STATUS)
        window['STATUS'].update(visible=True)
    if event == '取得驗證碼':
        getCheckCode()
        window['CKF'].update('check.png')
        #window['CK1'].update(visible=True)
        #window['CK2'].update(visible=True)
    if event == 'StartTimer':
        TargetTime = int(values['TT'])
        window['RESULT'].update('Start Counting...')
        window['RESULT'].update(visible=True)
        print('Start Counting...')
    if getTimeValue() > TargetTime:
       # print("Alert!Alert!Alert!Alert!")
        Fightting()
        window['RESULT'].update(RESULT)


window.close()

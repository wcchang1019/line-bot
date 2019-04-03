import time
import pythoncom
from linebot import LineBotApi
from linebot.models import TextSendMessage
import comtypes.client
CHANNEL_ACCESS_TOKEN = 'SiGEgA71amegCyRbTJ7LkbM+mGrKnpiDnUmgwrcei5T6ozmLcd919xKfzqQO5q0DSKMSgE6XuSy88T36ts3IHgNZRnVVj1KXBuzYhcPFNqvQfuXr1zQzGI1M/lfsnplnmT09NmCgQmRvhNxpjKmdHwdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '7e6fbaa6f8546ec31c586d925deb0c43'
USER_ID = 'U0842cd9c4beca2eda16af2f3fd8988eb'

comtypes.client.GetModule('dll/SKCOM.dll')
import comtypes.gen.SKCOMLib as sk
skC = comtypes.client.CreateObject(sk.SKCenterLib, interface=sk.ISKCenterLib)
skO = comtypes.client.CreateObject(sk.SKOrderLib, interface=sk.ISKOrderLib)


def login():
    try:
        # skC.SKCenterLib_SetLogPath(os.path.split(os.path.realpath(__file__))[0] + "\\CapitalLog_Order")
        with open('confidential.txt') as f:
            confidential = f.readlines()
        confidential = [x.strip() for x in confidential]
        global global_id
        global_id = confidential[0]
        stat = skC.SKCenterLib_login(confidential[0], confidential[1])
        if stat == 0:
            print('【 Login successful 】')
        else:
            print("Login", stat, "Login")
    except Exception as e:
        print("error！", e)


def order_initialize():
    try:
        stat = skO.SKOrderLib_Initialize()
        if stat == 0:
            print("【 Order initialize successful 】")
        else:
            print("Order", stat, "SKOrderLib_Initialize")
    except Exception as e:
        print("error！", e)


def read_certificate():
    try:
        stat = skO.ReadCertByID(global_id)
        if stat == 0:
            print('【 Read certificate successful 】')
        else:
            print("Order", stat, "ReadCertByID")
    except Exception as e:
        print("error！", e)


def get_account():
    try:
        stat = skO.GetUserAccount()
        if stat == 0:
            print('【 GetUserAccount successful 】')
        else:
            print('【 GetUserAccount error code:' + str(stat) + '】')
    except Exception as e:
        print("error！", e)


def get_open_position(SKOrderEvent):
    try:
        stat = skO.GetOpenInterest(global_id, global_account[0])
        if stat == 0:
            print('【 GetOpenPosition successful 】')
        else:
            print('【 GetOpenPosition error code:' + str(stat) + '】')
            return stat
        while True:
            pythoncom.PumpWaitingMessages()
            if SKOrderEvent.return_check:
                break
            # print(global_now_open_position)
            time.sleep(0.05)
        return stat
    except Exception as e:
        print("error!", e)


class SKOrderLibEvent:
    def __init__(self):
        return_check = False

    def OnAccount(self, bstrLogInID, bstrAccountData):
        strValues = bstrAccountData.split(',')
        strAccount = strValues[1] + strValues[3]
        if strValues[0] in ['TF', 'OF']:
            global_account.append(strAccount)

    def OnOpenInterest(self, bstrData):
        tmp = bstrData.split(',')
        if tmp[0] == '##':
            self.return_check = True
        else:
            global_now_open_position.append(tmp)

    def OnFutureRights(self, bstrData):
        print(bstrData.split(','))


def position_to_string(position):
    s = ''
    try:
        for p in position:
            s += p[2] + ',' + p[3] + ',' + str(int(p[4]) + int(p[5])) + ',' + str(int(p[6])/1000) + '\n'
        return s[:-1]
    except:
        return None


if __name__ == '__main__':
    global global_account, global_now_open_position
    global_account = []
    global_now_open_position = []
    SKOrderEvent = SKOrderLibEvent()
    SKOrderLibEventHandler = comtypes.client.GetEvents(skO, SKOrderEvent)
    skC.SKCenterLib_ResetServer("morder1.capital.com.tw")  # Simulation platform
    login()
    order_initialize()
    read_certificate()
    get_account()
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_text = ''
    while True:
        global_now_open_position = []
        SKOrderEvent.return_check = False
        stat = get_open_position(SKOrderEvent)
        if stat != 0:
            time.sleep(1)
            continue
        tmp = position_to_string(global_now_open_position)
        print(tmp)
        if line_bot_text != tmp:
            line_bot_text = tmp
            if line_bot_text is not None:
                line_bot_api.push_message(USER_ID, TextSendMessage(text=line_bot_text))
            else:
                line_bot_api.push_message(USER_ID, TextSendMessage(text='目前無艙位'))
            print('push success')
        time.sleep(5)

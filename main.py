#   by ReYeS
#     _;)  ~~8:> ~~8:>
#   Update by V¡ktor

parameters = {

    "community-link":
        "http://aminoapps.com/invite/72R2WWRYE3"
    
}

###################
emailFile = "acc.json"
###################

import os
import time
import json
import hmac
import base64
import random
import datetime
from base64 import b64encode
from hmac import new
from binascii import hexlify
from hashlib import sha1

try:
    import pytz
    import requests
    from flask import Flask
    from json_minify import json_minify
except:
    os.system("pip3 install pytz requests flask json_minify")
finally:
    import requests
    from flask import Flask
    from json_minify import json_minify

from threading import Thread
from uuid import uuid4
from hashlib import sha1

#-----------------FLASK-APP-----------------
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "~~8;> ~~8;>"
    
def run(): flask_app.run(host = '0.0.0.0', port = random.randint(2000, 9000))
#----------------------------------------------------

class Client:
    def __init__(self, deviceId=None):
        self.api = "https://service.narvii.com/api/v1"
        self.device_Id = self.generate_device_Id() if not deviceId else deviceId
        self.headers = {
    "NDCDEVICEID": self.device_Id,
    "SMDEVICEID":
        "b89d9a00-f78e-46a3-bd54-6507d68b343c",
    "Accept-Language": "en-EN",
    "Content-Type":
        "application/json; charset=utf-8",
    "User-Agent":
        "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)",
        "Host": "service.narvii.com",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"}
        self.sid, self.auid = None, None

    def generate_signature_message(self, data):
        signature_message = b64encode(bytes.fromhex("42") + new(bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93"),data.encode("utf-8"), sha1).digest()).decode("utf-8")
        self.headers["NDC-MSG-SIG"]=signature_message
        return signature_message

    def generate_device_Id(self):
        identifier = os.urandom(20)
        mac = new(bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F"), bytes.fromhex("42") + identifier, sha1)
        return f"42{identifier.hex()}{mac.hexdigest()}".upper()

    def login(self, email: str, password: str):
        data = json.dumps({
             "email": email,
             "secret": f"0 {password}",
             "deviceID": self.device_Id,
             "clientType": 100,
             "action": "normal",
             "timestamp": (int(time.time() * 1000))})
        self.generate_signature_message(data = data)
        request = requests.post(f"{self.api}/g/s/auth/login", data=data, headers=self.headers).json()
        try:
            self.sid = request["sid"]
            self.auid = request["auid"]
        except: pass
        return request

    def join_community(self, comId: int, inviteId: str = None):
        data = {"timestamp": int(time.time() * 1000)}
        if inviteId: data["invitationId"] = inviteId
        data = json.dumps(data)
        self.generate_signature_message(data=data)
        request = requests.post(f"{self.api}/x{comId}/s/community/join?sid={self.sid}", data=data, headers=self.headers).json()
        return request

    def send_active_object(self, comId: int, timers: list=None, tz: int = -time.timezone // 1000):
        data = {
            "userActiveTimeChunkList": timers,
            "timestamp": int(time.time() * 1000),
            "optInAdsFlags": 2147483647,
            "timezone": tz
            }
        data = json_minify(json.dumps(data))
        self.generate_signature_message(data = data)
        request = requests.post(f"{self.api}/x{comId}/s/community/stats/user-active-time?sid={self.sid}", data=data, headers=self.headers).json()
        return request

    def watch_ad(self):
        return requests.post(f"{self.api}/g/s/wallet/ads/video/start?sid={self.sid}", headers=self.headers).json()

    def get_from_link(self, link: str):
        return requests.get(f"{self.api}/g/s/link-resolution?q={link}", headers=self.headers).json()

    def lottery(self, comId, time_zone: str = -int(time.timezone) // 1000):
        data = json.dumps({
            "timezone": time_zone,
            "timestamp": int(time.time() * 1000)})
        self.generate_signature_message(data = data)
        request = requests.post(f"{self.api}/x{comId}/s/check-in/lottery?sid={self.sid}", data=data, headers=self.headers).json()
        return request

    def tapcoins(self):
        data = {"reward":{"ad_unit_id":"t00_tapjoy_android_master_checkinwallet_rewardedvideo_322","credentials_type":"publisher","custom_json":{"hashed_user_id":f"{self.auid}"},"demand_type":"sdk_bidding","event_id":None,"network":"facebook","placement_tag":"default","reward_name":"Amino Coin","reward_valid":"true","reward_value":2,"shared_id":"dc042f0c-0c80-4dfd-9fde-87a5979d0d2f","version_id":"1569147951493","waterfall_id":"dc042f0c-0c80-4dfd-9fde-87a5979d0d2f"}, "app":{"bundle_id":"com.narvii.amino.master","current_orientation":"portrait","release_version":"3.4.33567","user_agent":"Dalvik\/2.1.0 (Linux; U; Android 10; G8231 Build\/41.2.A.0.219; com.narvii.amino.master\/3.4.33567)"},"date_created":1620295485,"session_id":"49374c2c-1aa3-4094-b603-1cf2720dca67","device_user":{"country":"US","device":{"architecture":"aarch64","carrier":{"country_code":602,"name":"Vodafone","network_code":0},"is_phone":"true","model":"GT-S5360","model_type":"Samsung","operating_system":"android","operating_system_version":"29","screen_size":{"height":2260,"resolution":2.55,"width":1080}},"do_not_track":"false","idfa":"7495ec00-0490-4d53-8b9a-b5cc31ba885b","ip_address":"","locale":"en","timezone":{"location":"Asia\/Seoul","offset":"GMT+09:00"},"volume_enabled":"true"}}
        data["reward"]["event_id"] = str(uuid4())
        request = requests.post("https://ads.tapdaq.com/v4/analytics/reward", json=data, headers={"cookies":"__cfduid=d0c98f07df2594b5f4aad802942cae1f01619569096", "authorization":"Basic NWJiNTM0OWUxYzlkNDQwMDA2NzUwNjgwOmM0ZDJmYmIxLTVlYjItNDM5MC05MDk3LTkxZjlmMjQ5NDI4OA=="})
        return request.text

class Config:
    def __init__(self):
        with open(emailFile, "r") as config:
            self.account_list = [d for d in json.load(config)]

class App:
    def __init__(self):
        self.client = Client()
        extensions = self.client.get_from_link(parameters["community-link"])["linkInfoV2"]["extensions"]
        self.comId = extensions["community"]["ndcId"]
        try: self.invitationId = extensions["invitationId"]
        except: self.invitationId = None

    def tzc(self):
        UTC = {"+11":'+660',"+10":'+600',"+09":'+540',"+08":'+480',"+07":'+420',"+06":'+360',"+05":'+300',"+04":'+240',"+03":'+180',"+02":'+120',"+01":'+60',"GMT":'+0',"-01":'-60',"-02":'-120',"-03":'-180',"-04":'-240',"-05":'-300',"-06":'-360',"-07":'-420',"-08":'-480',"-09":'-540',"-10":'-600',"-11":'-660',"-12":'+720'}
        zones = ['Etc/GMT-11','Etc/GMT-10','Etc/GMT-9','Etc/GMT-8','Etc/GMT-7','Etc/GMT-6','Etc/GMT-5','Etc/GMT-4','Etc/GMT-3','Etc/GMT-2','Etc/GMT-1','Etc/GMT0','Etc/GMT+1','Etc/GMT+2','Etc/GMT+3','Etc/GMT+4','Etc/GMT+5','Etc/GMT+6','Etc/GMT+7','Etc/GMT+8','Etc/GMT+9','Etc/GMT+10','Etc/GMT+11','Etc/GMT+12']
        for _ in zones:
            H = datetime.datetime.now(pytz.timezone(_)).strftime("%H"); Z = datetime.datetime.now(pytz.timezone(_)).strftime("%Z")
            if H=="23": break
        return int(UTC[Z])

    def generation(self, email, password, device):
        self.email,self.password = email,password
        self.client = Client(device)
        try:
            print(f"\n[\033[1;31mcoins-generator\033[0m][\033[1;34mlogin\033[0m][{email}]: {self.client.login(email = self.email, password = self.password)['api:message']}.")
            print(f"[\033[1;31mcoins-generator\033[0m][\033[1;36mjoin-community\033[0m]: {self.client.join_community(comId = self.comId, inviteId = self.invitationId)['api:message']}.")
            print(f"[\033[1;31mcoins-generator\033[0m][\033[1;32mlottery\033[0m]: {self.client.lottery(comId = self.comId, time_zone = self.tzc())['api:message']}")
            print(f"[\033[1;31mcoins-generator\033[0m][\033[1;33mwatch-ad\033[0m]: {self.client.watch_ad()['api:message']}.")
            for i in range(20):
                if self.client.tapcoins() == '':
                    if i < 9: print(f"[\033[1;31mcoins-generator\033[0m][\033[1;36mtapcoins\033[0m][ {i + 1}]: OK.")
                    else: print(f"[\033[1;31mcoins-generator\033[0m][\033[1;36mtapcoins\033[0m][{i + 1}]: OK.")
                else: print(f"[\033[1;31mcoins-generator\033[0m][\033[1;36mtapcoins\033[0m][??]: Error.")
            for i2 in range(24):
                print(f"[\033[1;31mcoins-generator\033[0m][\033[1;35mmain-proccess\033[0m][{email}]: {self.client.send_active_object(comId = self.comId, timers = [{'start': int(time.time()), 'end': int(time.time()) + 300} for _ in range(50)], tz = self.tzc())['api:message']}.")
                time.sleep(1.1)
            print(f"[\033[1;31mcoins-generator\033[0m][\033[1;25;32mend\033[0m][{email}]: Finished.")
        except Exception as error: print(f"[\033[1;31mC01?-G3?3R4?0R\033[0m]][\033[1;31merror\033[0m]]: {error}")

    def run(self):
        print("\033[1;31m @@@@@@   @@@@@@@@@@   @@@  @@@  @@@   @@@@@@ \033[0m     \033[1;32m @@@@@@@   @@@@@@   @@@  @@@  @@@   @@@@@@\033[0m\n\033[1;31m@@@@@@@@  @@@@@@@@@@@  @@@  @@@@ @@@  @@@@@@@@\033[0m     \033[1;32m@@@@@@@@  @@@@@@@@  @@@  @@@@ @@@  @@@@@@@\033[0m\n\033[1;31m@@!  @@@  @@! @@! @@!  @@!  @@!@!@@@  @@!  @@@\033[0m     \033[1;32m!@@       @@!  @@@  @@!  @@!@!@@@  !@@\033[0m\n\033[1;31m!@!  @!@  !@! !@! !@!  !@!  !@!!@!@!  !@!  @!@\033[0m     \033[1;32m!@!       !@!  @!@  !@!  !@!!@!@!  !@!\033[0m\n\033[1;31m@!@!@!@!  @!! !!@ @!@  !!@  @!@ !!@!  @!@  !@!\033[0m     \033[1;32m!@!       @!@  !@!  !!@  @!@ !!@!  !!@@!!\033[0m\n\033[1;31m!!!@!!!!  !@!   ! !@!  !!!  !@!  !!!  !@!  !!!\033[0m     \033[1;32m!!!       !@!  !!!  !!!  !@!  !!!   !!@!!!\033[0m\n\033[1;31m!!:  !!!  !!:     !!:  !!:  !!:  !!!  !!:  !!!\033[0m     \033[1;32m:!!       !!:  !!!  !!:  !!:  !!!       !:!\033[0m\n\033[1;31m:!:  !:!  :!:     :!:  :!:  :!:  !:!  :!:  !:!\033[0m     \033[1;32m:!:       :!:  !:!  :!:  :!:  !:!      !:!\033[0m\n\033[1;31m::   :::  :::     ::    ::   ::   ::  ::::: ::\033[0m     \033[1;32m ::: :::  ::::: ::   ::   ::   ::  :::: ::\033[0m\n\033[1;31m :   : :   :      :    :    ::    :    : :  : \033[0m     \033[1;32m :: :: :   : :  :   :    ::    :   :: : :\033[0m\n\033[1;33m @@@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@    @@@@@@   @@@@@@@   @@@@@@   @@@@@@@\033[0m\n\033[1;33m@@@@@@@@@  @@@@@@@@  @@@@ @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@  @@@@@@@@  @@@@@@@@\033[0m\n\033[1;33m!@@        @@!       @@!@!@@@  @@!       @@!  @@@  @@!  @@@    @@!    @@!  @@@  @@!  @@@\033[0m\n\033[1;33m!@!        !@!       !@!!@!@!  !@!       !@!  @!@  !@!  @!@    !@!    !@!  @!@  !@!  @!@\033[0m\n\033[1;33m!@! @!@!@  @!!!:!    @!@ !!@!  @!!!:!    @!@!!@!   @!@!@!@!    @!!    @!@  !@!  @!@!!@!\033[0m\n\033[1;33m!!! !!@!!  !!!!!:    !@!  !!!  !!!!!:    !!@!@!    !!!@!!!!    !!!    !@!  !!!  !!@!@!\033[0m\n\033[1;33m:!!   !!:  !!:       !!:  !!!  !!:       !!: :!!   !!:  !!!    !!:    !!:  !!!  !!: :!!\033[0m\n\033[1;33m:!:   !::  :!:       :!:  !:!  :!:       :!:  !:!  :!:  !:!    :!:    :!:  !:!  :!:  !:!\033[0m\n\033[1;33m ::: ::::   :: ::::   ::   ::   :: ::::  ::   :::  ::   :::     ::    ::::: ::  ::   :::\033[0m\n\033[1;33m :: :: :   : :: ::   ::    :   : :: ::    :   : :   :   : :     :      : :  :    :   : :\033[0m\n\033[1;35m__By ReYeS\033[0m / \033[1;36mREPLIT_EDITION\033[0m\n")
        while True:
            for acc in Config().account_list:
                e = acc['email']
                p = acc['password']
                d = acc['device']
                self.generation(e, p, d)

if __name__ == "__main__":
    Thread(target=run).start()
    App().run()
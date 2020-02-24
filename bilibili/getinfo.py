import requests
import json
class GetInfo:
    cookies = 0
    json = 0
    uname = 0;
    mid = 0;
    following = 0;
    face = 0;
    def __init__(self):

        pass

    def init(self, cookies):
        requests.packages.urllib3.disable_warnings();
        self.cookies = cookies
        print ('init结束')

    def getuinfo(self):
        url = "https://api.bilibili.com/x/web-interface/nav";
        self.json  = json.loads(self.get(url))
        self.uname = self.json['data']['uname']
        self.face = self.json['data']['face']
        self.mid = self.json['data']['wallet']['mid']
        url = "https://api.bilibili.com/x/relation/stat?jsonp=jsonp&vmid="+str(self.mid)
        self.json  = json.loads(self.get(url))
        self.following = self.json['data']['following']
        return self;
    def get(self, url, data={}):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/63.0.3239.132 Safari/537.36",
            "Cookie": self.cookies,
        }

        r = requests.get(url=url, headers=headers, params=data, timeout=10, verify=False)

        return r.content.decode()




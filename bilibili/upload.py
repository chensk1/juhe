import requests
import json
from urllib.parse import quote
import re
import threading


class Upload:
    json = 0
    cookies = 0
    url = 0
    upload_id = 0
    name = 0
    post_json = 0
    thread_size = 1

    def __init__(self):

        pass

    def init(self, name, size, cookies):
        requests.packages.urllib3.disable_warnings();
        self.cookies = cookies
        self.name = quote(name)
        url = 'https://member.bilibili.com/preupload?name=%s&size=%s&r=upos&profile=ugcupos%%2Fbup&ssl=0&version=2.7.1&build=2070100&os=upos&upcdn=ws' \
              % (self.name, size)

        self.json = data = json.loads(self.get(url))

        if data['OK'] == 1:
            self.url = 'https:' + data['endpoint'] + data['upos_uri'].split('upos:/')[1]
            self.get_upload_id()
            print(data)
            return True
        else:
            return False

    def run(self, file):
        global lock, k, list

        k = 0
        lock = 1  # 用于判断是否上传完毕

        threads = []

        for i in range(1, self.thread_size+1):
            t = T(i, "Thread" + str(i), i, self, file)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        json = {'parts': {}}
        t = 0
        for i in list:
            json['parts'][t] = {'partNumber': i, 'eTag': 'etag'}
            t = t + 1
        self.end(json)
        print('上传完成')

    def end(self, json):
        src = '?output=json&name=%s&profile=ugcupos%%2Fbup&uploadId=%s&biz_id=%s' % (
        self.name, self.upload_id, str(self.json['biz_id']))
        print(self.post(self.url + src, json))
        url = 'https://member.bilibili.com/x/vu/web/add?csrf=' + self.csrf()
        print(url)
        print(self.post_json)
        print(self.post(url, self.post_json))

    def get_upload_id(self):
        data = json.loads(self.post(self.url + '?uploads&output=json'))
        self.upload_id = data['upload_id']
        print(data)

    def get(self, url, data={}):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/63.0.3239.132 Safari/537.36",
            "Cookie": self.cookies,
        }

        r = requests.get(url=url, headers=headers, params=data, timeout=10, verify=False)
        return r.content.decode()

    def post(self, url, json=0, data={}):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/63.0.3239.132 Safari/537.36",
            "Cookie": self.cookies,
            "Origin": 'https://member.bilibili.com',
            "Referer": 'https://member.bilibili.com/video/upload.html',
            'X-Upos-Auth': self.json['auth'],
        }
        if json == 0:
            r = requests.post(url=url, headers=headers, data=data, timeout=10, verify=False)
        else:
            r = requests.post(url=url, headers=headers, json=json, timeout=10, verify=False)
        return r.content.decode()

    def put(self, url, file, put_size):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/63.0.3239.132 Safari/537.36",
            "Content-Length": str(put_size),
            "Cookie": self.cookies,
            "Origin": 'https://member.bilibili.com',
            "Referer": 'https://member.bilibili.com/video/upload.html',
            'X-Upos-Auth': self.json['auth'],
        }

        r = requests.put(url=url, headers=headers, data=file, timeout=999999, verify=False)
        return r.content.decode()

    def csrf(self):
        searchObj = re.search('bili_jct=(.*?);', self.cookies + ';');
       # searchObj = re.search(r'bili_jct=(.*?);', self.cookies, re.M | re.I)
        return searchObj.group(1)

    def set_post_json(self, json):
        filename = self.json['upos_uri'].split('upos://ugc/')[1].split('.mp4')[0]
        json['videos'][0]['filename'] = filename
        self.post_json = json


threadLock = threading.Lock()


class T(threading.Thread):

    def __init__(self, ThreadID, name, counter, upload, file):
        threading.Thread.__init__(self)
        self.threadID = ThreadID
        self.name = name
        self.counter = counter
        self.upload = upload
        self.file = file

    def run(self):
        global lock, k, list

        list = []
        file = self.file

        while True:
            put_size = self.upload.json['chunk_size']
            print(put_size);
            threadLock.acquire()
            k = k + 1
            threadLock.release()

            threadLock.acquire()
            p = k + 1 - 1
            threadLock.release()

            st_put_size = put_size * (k - 1)
            ed_put_size = put_size * p
            print(self.upload.thread_size)
            if ed_put_size >= int(file.size):  # 当上传结束时数据大小大于等于 文件大小时

                ed_put_size = file.size
                put_size = int(ed_put_size) % put_size
                if lock != self.upload.thread_size:
                    lock = lock + 1

            if lock == self.upload.thread_size:  # 当lock自增两次时上传完毕
                break

            files = file.read(self.upload.json['chunk_size'])
            src = '?partNumber=%s&uploadId=%s&chunk=%s&chunks=191&size=%s&start=%s&end=%s&total=%s' \
                  % (str(p), self.upload.upload_id, str(k), str(put_size), str(st_put_size), str(ed_put_size),
                     str(file.size))
            threadLock.acquire()
            list.append(p)
            threadLock.release()
            print(src)
            print(self.upload.put(self.upload.url + src, files, put_size))

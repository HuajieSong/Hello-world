#-*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado
import os
import urllib
import json
import ssl
import requests
from parsePlist import parse_plist

#__APP_PATH = {"ios": {"1": "iOS/psnger/"}}


#把发版包存到本地服务器
class DownloadHandler(tornado.web.RequestHandler):
    def get(self):
        self.func()

    def post(self):
        self.func()

    def func(self):

        app_version = self.get_argument('app_version')[0]

        package_name = self.get_argument("app_version")
        platform = self.get_argument("platform")
        download_url = self.get_argument("download_url")
        app_id = self.get_argument("app_id")
        branch = self.get_argument("branch")

        # download_url = args.get('download_url')[0]
        # platform=args.get('platform')[0]    #区分平台 iOS还是Android
        # app_id=args.get('app_id')[0]             #端类型 dmtc的app_ID 还是driver
        # #task_id=args.get('task_id')           #任务id  打包的任务id
        # package_name=app_version
        # branch_type = args.get("branch")
        ssl._create_default_https_context = ssl._create_unverified_context

        self.write(tornado.escape.json_encode({"errno":0, "message":"success"}))

        if platform in ['iOS','ios']:
            if int(app_id) == 1:
                package_path ='iOS/psnger/'
            elif int(app_id) == 2:
                package_path = 'iOS/driver/1.plist'
        elif platform in ['Android', 'android']:
            if int(app_id) == 1:
                package_path = 'Android/psnger/'
            elif int(app_id) == 2:
                package_path = 'Android/driver/'

        try:
            result = True
            if 'plist' in download_url:
                urllib.request.urlretrieve(download_url, package_path +package_name+ download_url.split('/')[-1])
                if not os.path.exists(package_path + download_url.split('/')[-1]):
                    result = False
                download_url = parse_plist(package_path + download_url.split('/')[-1])
                if not download_url:
                    result = False
            urllib.request.urlretrieve(download_url, package_path + download_url.split('/')[-1])
            if result is True:
                self.write(tornado.escape.json_encode({"errno": 0, "message": "success"}))
            else:
                self.write(tornado.escape.json_encode({"errno": 1, "message": "success"}))
        except Exception as error:
            print(error)
            self.write(tornado.escape.json_encode({"errno": 1, "message": "failed"}))



#把最新debug包上传到didifarm
class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('get method upload to didifarm')
    def post(self):
        self.write('post method upload to didifarm')


app = tornado.web.Application([
    (r"/getDownloadUrl", DownloadHandler),(r"/uploadToDidifarm", UploadHandler)
])

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    import tornado.httpserver
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8090)
    print("test server init ...")
    tornado.ioloop.IOLoop.instance().start()

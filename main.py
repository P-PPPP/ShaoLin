# -*- coding: UTF-8 -*-

import webview,webbrowser,os,sys,threading
from lib import connectCore as core


class Api():
    '''与页面交互'''
    def destory(self):
        window.destroy()

    def stage1(self):
        t = core.network().server()
        t.start()

    def stage1AutoSearch(self,content):
        self.stage1()
        window.evaluate_js("snackbar('socket服务已创建，监听端口为29999')")
        window.evaluate_js("stage2('"+core.searchPort().list2json()+"')")
        

if __name__ == '__main__':
    api = Api()
    url = "file:" + os.getcwd().replace("\\","/") + "/ui/index.html"
    #url = "index.html"
    window = webview.create_window(title="",url=url,js_api=api)
    webview.start(debug=True)

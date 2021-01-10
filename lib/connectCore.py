import socket , requests, threading
from time import ctime
class network():
    ip = ""

    def __init__(self):
        self.ip = self.myIp()
        
    def myIp(self):
        import socket
        try: 
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
            s.connect(('8.8.8.8',80)) 
            ip = s.getsockname()[0] 
        finally: 
            s.close() 
        return ip

    class server(threading.Thread):

        def run(self):
            self.SocketServer()

        def SocketServer(self):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            host = network.ip
            port = 29999
            s.bind((host,port))
            s.listen(5)
            while True:
                c,addr=s.accept()
                print("connected from ", addr)
                message = c.recv(1024).decode()
                print(message.encode('utf-8'))
                c.send("yes it is!".encode('utf-8'))
            return True

    def SocketClient(self,ip):

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = ip
        port = 29999
        s.connect((host,port))
        s.send('is this shaolin?'.encode('utf-8'))
        while True:
            info = s.recv(1024).decode()
            print(info.encode('utf-8'))
        s.close()

class searchPort():
    class devices():
        def __init__(self,deviceIp,deviceType):
            self.ip = deviceIp
            self.type = deviceType

    activeips = []
    import os,sys,socket
    ip = network().ip

    def __init__(self):
        self.ping_all()

    def my_os(self):    
        import platform
        return platform.system()

    def ping_ip(self,ip):
        import os,sys
        if self.my_os() == 'Windows':
            p_w = 'n'
        elif self.my_os() == 'Linux':
            p_w = 'c'
        else:
            sys.exit()
        output = os.popen('ping -%s 1 %s'%(p_w,ip)).readlines()
        for w in output:
            if str(w).upper().find('TTL')>=0:
                self.activeips.append(ip)

    def ping_all(self):     
        import threading,time
        pre_ip = self.ip.split('.')[:-1]
        for i in range(1,256):
            add = ('.'.join(pre_ip)+'.'+str(i))
            threading._start_new_thread(self.ping_ip,(add,))
            time.sleep(0.1)
    
    def list2json(self):
        import json
        command = '{"data":['
        tmp = ""
        for i in self.activeips:
            tmp = tmp + str({"device-ip":self.devices(i,"laptop").ip,"device-type":self.devices(i,"laptop").type}) + ","
        command = command + tmp[::-1].replace(",","",1)[::-1] +"]}"
        return command.replace("'",'"')
            

import threading
class downloader(threading.Thread):
    def __init__(self,url,startpoint,end,f,lock):
        super(downloader,self).__init__()
        self.url = url
        self.startpoint = startpoint
        self.end = end
        self.fd = f
        self.lock = lock
        
    def download(self):
        #print("start downloading thread %s" % (self.getName()))
        headers = {"Range":"bytes=%s-%s" % (self.startpoint,self.end)}
        res = requests.get(self.url,headers=headers)
        self.fd.seek(self.startpoint)
        self.fd.write(res.content)
        #print("stop thread %s"%(self.getName()))
        self.fd.close()
        self.lock.release()


    def run(self):
        self.download()

class downloaderControl():
    '''  
    downloaderControl().config["url"]='http://localhost/shaolin/jieni.jpg'
    downloaderControl().controller()
    '''
    #这个start变量和threading里面重复了，md
    threadList = []
    config = {
        "url":"",
        "threadNum":8
    }
    length = 0
    startpoint = 0
    end = -1
    
    fileName = ""

    def get_info(self):
        self.fileName = self.config["url"].split('/')[-1]
        r = requests.head(self.config["url"])
        self.length = int(r.headers["Content-Length"])
        self.step = self.length // self.config["threadNum"]

    def controller(self):
        import os
        self.get_info()
        lock = threading.BoundedSemaphore(self.config["threadNum"])
        tmpf = open(self.fileName,'w')
        tmpf.close()

        with open(self.fileName,'rb+') as f:
            fileno = f.fileno()
            while self.end < self.length - 1:
                self.startpoint = self.end +1
                self.end = self.startpoint + self.step -1
                if self.end > self.length:
                    self.end = self.length
                dup = os.dup(fileno)
                #print(self.startpoint,self.end)
                lock.acquire()
                fd = os.fdopen(dup,'rb+',-1)
                t = downloader(self.config["url"],self.startpoint,self.end,fd,lock)
                self.threadList.append(t)
                t.start()
            
            for i in self.threadList:
                i.join()
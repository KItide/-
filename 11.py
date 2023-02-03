import requests
import os,sys,hashlib
import argparse

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) LySharkTools'}

def CheckFinger(url,flag,keyworld):
    if flag == 0:
        ret = requests.get(url=url,headers=headers,timeout=1)
        text = ret.text
        md5=hashlib.md5()
        md5.update(text.encode('utf-8'))
        print("目标网页Hash值:  {}".format(md5.hexdigest()))
    else:
        fp = open(keyworld,"r")
        for i in fp.readlines():
            path = url + eval(i.replace("\n", ""))["Path"]
            hash = eval(i.replace("\n", ""))["Hash"]
            web = eval(i.replace("\n", ""))["WebServer"]
            ret = requests.get(url=path, headers=headers, timeout=1)
            if ret.status_code == 200:
                text = ret.text
                md5 = hashlib.md5()
                md5.update(text.encode('utf-8'))
                if md5.hexdigest() == hash:
                    print("目标Hash：{}  CMS页面类型：{} ".format(hash,web))
                else:
                    continue

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",dest="mode",help="设置检查类型 [check/get]")
    parser.add_argument("-u","--url",dest="url",help="指定需要检测的网站地址")
    parser.add_argument("-f","--file",dest="file",help="指定字典数据库 data.json")
    args = parser.parse_args()
    if args.mode == "get" and args.url:
        CheckFinger(args.url,0,args.file)
    # 检测目标容器类型: main.py --mode=check -u https://www.xxx.com -f data.json
    elif args.mode == "check" and args.url and args.file:
        CheckFinger(args.url,1,args.file)
    else:
        parser.print_help()

#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import threading
import argparse, sys
import time, os
from queue import Queue

url_list = []
queue = Queue()

headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70',
}



def get_time():
    return '[' + time.strftime("%H:%M:%S", time.localtime()) + '] '


def get_url(path):
    with open(path, "r", encoding='ISO-8859-1') as f:
        for url in f.readlines():
            url_list.append(url.strip())
        return url_list


def Go_scan(url):
    while not queue.empty():
        url_path = queue.get(timeout=1)
        new_url = url + url_path
        res = requests.get(new_url, headers=headers, timeout=5)
        # print(res.status_code)
        status_code = "[" + str(res.status_code) + "]"
        if str(res.status_code) != "404":
            print(get_time(), status_code, new_url)


def thread(Number, url):
    threadlist = []
    for pwd in url_list:
        queue.put(pwd)

    for x in range(Number):
        t = threading.Thread(target=Go_scan, args=(url,))
        threadlist.append(t)

    for t in threadlist:
        t.start()

def usage():
    if len(sys.argv) !=2:
        print("用法: " + os.path.basename(sys.argv[0]) + " python dir_scan.py -u [url]http://www.test.com[/url] -d /root/dir.txt")
        print("用法: " + os.path.basename(sys.argv[0]) + "  python dir_scan.py -u [url]http://www.test.com[/url] -t 30 -d /root/dir.txt")
        sys.exit()
def main():
    usage()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''\
use examples:
 python dir_scan.py -u [url]http://www.test.com[/url] -d /root/dir.txt
 python dir_scan.py -u [url]http://www.test.com[/url] -t 30 -d /root/dir.txt
 ''')
    parser.add_argument("-u", "--url", help="scan target address", dest='url')
    parser.add_argument("-t", "--thread", help="Number of threads", default="20", type=int, dest='thread')
    parser.add_argument("-d", "--Dictionaries", help="Dictionary of Blasting Loading",
                        dest="Dictionaries")
    args = parser.parse_args()
    Number = args.thread
    url = args.url
    url_path = args.Dictionaries
    get_url(url_path)
    print(get_time(), "[INFO] Start scanning----\n")
    time.sleep(1.5)
    thread(Number, url)


if __name__ == '__main__':
    main()
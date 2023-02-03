# 使用python 3.8版本

import nmap
def scan_system(domain_name):
    nm = nmap.PortScanner()  # 创建扫描对象
    os_list = []
    try:
        scan_result = nm.scan(hosts=domain_name, arguments='-O')  # 添加扫描参数
        for i, j in scan_result['scan'].items():  # 将扫描结果转成字典
            if j['osmatch']:  # 判断是否有osmatch
                for k in j['osmatch']:
                    for os in k['osclass']:
                        print(domain_name,os['osfamily'],'\n')
                        os_list.append(os['osfamily'])  # osfamily对应的是操作系统家族
            else:
                break
    except Exception as e:
        print(domain_name, 'None\n')  # 当链接不能被访问时，抛出异常
    print(domain_name, max(os_list, key=os_list.count))


if __name__ == "__main__":
    url = ['127.0.0.1',]# url列表
    for i in range(len(url)):
        scan_system(url[i])
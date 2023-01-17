import requests
import re
import os
import json
import datetime

# You can run python from the website https://repl.it/languages
# requirements:
# requests==2.21.0

import re
from time import sleep
from multiprocessing import Pool, Manager

url = 'https://checkerproxy.net/api/archive/2023-01-17'

date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
proxy_file =  os.path.join(os.getcwd(), date_str)

def test_ip(ip,port,proxy_file):
    try:
        proxy = {
            "http": "socks5://"+ip+':'+port,
            "https": "socks5://"+ip+':'+port
            }
        url = "http://www.baidu.com/"
        req = requests.get(url, proxies=proxy, timeout=2)
        print (ip+':'+port)
        with open(proxy_file, 'a+') as f:
            f.write(ip+':'+port+"\n")
    except ConnectTimout:
        print()
    except Exception as err:
        print(err, type(err))

def save_proxy(json_str):
    proxy_list = json.loads(json_str)
    print('Get {} proxies.'.format(len(proxy_list)))
    proxy_list = list(filter(lambda dic:dic['type']==4, proxy_list))
    proxy_list.sort(key=lambda p:p['timeout'], reverse=False)
    p = Pool(60)
    q = Manager().Queue()
    for proxy_dic in proxy_list:
        rip = proxy_dic['addr'].split(':')[0]
        rport = proxy_dic['addr'].split(':')[1]
        # print(rip, rport, proxy_dic['timeout'], proxy_dic['type'])
        p.apply_async(test_ip,args=(rip,rport,proxy_file))
    p.close()
    p.join()

def get_index(url):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'}
    print('Getting the website...')
    try:
        rsp = requests.get(url=url, headers=header)
        if rsp.status_code == 200:
            print('Success.')
            html = rsp.text
            return html
        else:
            exit('Can not get the website.')
    except ConnectionError:
        exit('ConnectionError.')

def main():
    html = get_index(url)
    save_proxy(html)


if __name__ == '__main__':
    main()
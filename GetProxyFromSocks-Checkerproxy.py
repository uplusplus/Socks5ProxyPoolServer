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

url = 'https://checkerproxy.net/api/archive/2023-01-18'



class ProxyVerify(object):
    def __init__(self):
        # 利用匿名函数模拟一个不可序列化象
        # 更常见的错误写法是，在这里初始化一个数据库的长链接
        self.url = "http://www.baidu.com/"
        self.timeout = 2
        date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        self.proxy_file =  os.path.join(os.getcwd(), date_str)

    def test_ip(self, ip, port):
        try:
            proxy = {
                "http": "socks5://"+ip+':'+port,
                "https": "socks5://"+ip+':'+port
            }
            req = requests.get(self.url, timeout=self.timeout, proxies=proxy)
            with open(self.proxy_file, 'a+') as f:
                f.write(ip+':'+port+"\n")
            return(ip+':'+port)
        except requests.exceptions.ConnectTimeout:
            return ""
        except requests.exceptions.ReadTimeout:
            return ""
        except requests.exceptions.ConnectionError:
            return ""
        except Exception as err:
            return err

    @staticmethod
    def call_back(res):
        if(len(res)>0):
            print(f'{res}')

    @staticmethod
    def err_call_back(err):
        print(f'出错啦~ error：{str(err), type(err)}')
        


def save_proxy(json_str):
    proxy_list = json.loads(json_str)
    print('Get {} proxies.'.format(len(proxy_list)))
    proxy_list = list(filter(lambda dic:dic['type']==4, proxy_list))
    proxy_list.sort(key=lambda p:p['timeout'], reverse=False)
    p = Pool(60)
    q = Manager().Queue()
    proxyVerify = ProxyVerify()
    for proxy_dic in proxy_list:
        rip = proxy_dic['addr'].split(':')[0]
        rport = proxy_dic['addr'].split(':')[1]
#        print(rip, rport, proxy_dic['timeout'], proxy_dic['type'])
        p.apply_async(proxyVerify.test_ip,
            args=(rip,rport,),
            callback=ProxyVerify.call_back,
            error_callback=ProxyVerify.err_call_back
        )
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
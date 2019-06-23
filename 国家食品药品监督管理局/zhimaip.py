# -*- coding: utf-8 -*-
import requests
import datetime
import pandas as pd
import os
os.environ['NO_PROXY'] = 'webapi.http.zhimacangku.com'
def getdailione(iptime) :
    # url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=3&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
    url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time='+ str(iptime) +'&ts=1&ys=1&cs=1&lb=1&sb=0&pb=45&mr=2&regions='
    res = requests.get(url,timeout = 30)
    data = res.json()
    if (data['success'] == False) and (u'设置为白名单！' in data['msg']) : 
        localip = data['msg'][2:-7]
        url2 = 'http://web.http.cnapi.cc/index/index/save_white?neek=32663&appkey=70983af331adf651c11a85c9d3740e12&white=' +localip
        res = requests.get(url2,timeout = 30)
        res = requests.get(url,timeout = 30)
        data = res.json()    
    if data['success'] == True :
        newip = 'http://' +str(data['data'][0]['ip']) + ':' + str(data['data'][0]['port'])
        expiretimestr = str(data['data'][0]['expire_time'])
        expiretime = datetime.datetime.strptime(expiretimestr, "%Y-%m-%d %H:%M:%S")
        return newip,expiretime
    else :
        return 0,0


def getdailis(num,iptime) :

    # url = 'http://webapi.http.zhimacangku.com/getip?num='+str(num+10)+'&type=2&pro=&city=0&yys=0&port=1&time=3&ts=1&ys=1&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
    url = 'http://webapi.http.zhimacangku.com/getip?num='+str(num+10)+'&type=2&pro=&city=0&yys=0&port=1&time='+ str(iptime) +'&ts=1&ys=1&cs=1&lb=1&sb=0&pb=45&mr=2&regions='
    res = requests.get(url)
    data = res.json()
    if (data['success'] == False) and (u'设置为白名单！' in data['msg']) : 
        localip = data['msg'][2:-7]
        url2 = 'http://web.http.cnapi.cc/index/index/save_white?neek=32663&appkey=70983af331adf651c11a85c9d3740e12&white=' +localip
        res = requests.get(url2,timeout = 30)
        res = requests.get(url,timeout = 30)
        data = res.json()    
    if data['success'] == True :
        df = pd.DataFrame(data['data'])
        df = df.sort_values(['isp','expire_time'],ascending=[True,False])[:num]
        iplist = list('http://' + df.ip + ':' + df.port.apply(str))
        timefunc = lambda x:datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
        expiretimelist = list(df.expire_time.apply(timefunc))
        return iplist,expiretimelist,df
    else :
        return 0,0,0









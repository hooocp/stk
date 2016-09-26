#!/bin/python
#coding:utf-8

import sys, urllib, urllib2, json, stock_ids
import pandas as pd
import time 

url = 'http://apis.baidu.com/apistore/stockservice/stock?stockid={stock_id}&list=1'

timestamp =  time.strftime( '%-Y-%-m-%-d-%-H-%-M')


stock_ids=stock_ids.stock_id()
all_contents=[]
n=0
f= open('./all'+timestamp.replace('-','-'),'a')
for stock_id in stock_ids:
    req = urllib2.Request(url.format(stock_id=stock_id))
    req.add_header("apikey", "010721d55352bdc690ec61735cbbd3fe")
    resp = urllib2.urlopen(req)
    content = resp.read()
    if(content):
        con_j = json.loads(content)
        if con_j['errMsg'] == 'success':
            all_contents.append(con_j['retData']['stockinfo'][0])
        f.write(content+'\n')
        print('passed: ',n)
        n += 1
f.close()

df = pd.DataFrame(all_contents)
df_s= df[['code','date','openningPrice','closingPrice','hPrice','hPrice','currentPrice','growthPercent','dealnumber','turnover']]
df_s.to_csv('test.csv')





# -*- coding: utf-8 -*-
import sys, urllib, urllib2, json

url = 'http://apis.baidu.com/apistore/stockservice/stock?stockid=sz002230,sh600795&list=1'


req = urllib2.Request(url)

req.add_header("apikey", "010721d55352bdc690ec61735cbbd3fe")

resp = urllib2.urlopen(req)
content = resp.read()
if(content):
        print(content)

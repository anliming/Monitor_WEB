#!/usr/bin/python
#encoding=utf-8
import requests
import json
import sys,time,os
from task.tasks import send_mail

index_xhr = [
    {"name":"首页","url":"http://m.yktour.com.cn/#/home"},
    {"name":"出境游","url":"http://m.yktour.com.cn/index/getCmsRecommendedProducts?sid=0&start_city_name=%E5%8C%97%E4%BA%AC&_json=true&_=1519267991592"},
    {"name":"精选路线","url":"http://m.yktour.com.cn/index/getCompetitiveProductList?currentCity=%E5%8C%97%E4%BA%AC&_json=true&_=1519267991591"},
    {"name":"滚屏Banner","url":"http://m.yktour.com.cn/product/getProductPopularizeImages?navId=1&_json=true&_=1519267991590"},
    {"name":"获取当前城市-北京","url":"http://m.yktour.com.cn/appindex/getLocationCity?_json=true&_=1519267991589"},
    {"name":"检查是否登录","url":"http://m.yktour.com.cn/member/checkLogin"},
    {"name":"??","url":"http://test.activity.yktour.com.cn/wx/sign/query"}
    ]

def get_default_arg():
    return time.strftime("%Y-%m-%d %X", time.localtime())+"    "+sys.argv[0] + "  " 

def get_url(url):
    name = url["name"]
    url = url["url"]
    html = requests.get(url=url,timeout=10)
    if html.status_code == 200:
        if name == "首页":
            if html.content:
                print get_default_arg()+name+"    检查正常"
            else:
                print get_default_arg()+name+"    检查失败，请及时处理"
                msg={'name':name+" 检查异常","errmsg":get_default_arg()+name+"    异常"}
                result = send_mail.delay(msg)
		print result.status
        else:
            res = json.loads(html.content)
            if res:
                print get_default_arg()+name+"    检查正常"
            else: 
                print get_default_arg()+name+"    检查失败，请及时处理"
                msg={'name':name+" 检查异常","errmsg":get_default_arg()+name+"    异常"}
                result = send_mail.delay(msg)
		print result.status
    else:
        html = requests.post(url)
        if html.status_code == 200:
            res = json.loads(html.content)
            if res:
                print get_default_arg() +name+" 检查正常"
            else: 
                print get_default_arg() +name+" 检查失败，请及时处理"
                msg={'name':name+" 检查异常","errmsg":get_default_arg()+name+"    异常"}
                result = send_mail.delay(msg)
		print result.status
	
if __name__ == "__main__":
    for url in index_xhr:
        try:
            get_url(url)
        except Exception as e:
            print e
            msg={'name':"警告!!!检查ToC_app"+" "+url["name"]+"失败","errmsg":get_default_arg()+"\n"+e.message}
            result = send_mail.delay(msg)

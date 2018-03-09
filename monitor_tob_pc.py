#!/usr/bin/python
#encoding=utf-8
import requests
import json
import sys,time,os
from task.tasks import send_mail

data = {
    'password': 'xxxx',
    'username': 'sdddd'
}

index_xhr = [
    {"name":"获取用户信息","url":"https://bpm.yktour.com.cn/ykly-tob-web/getUserInfo"},
    {"name":"获取用户菜单列表","url":"https://bpm.yktour.com.cn/ykly-tob-web/b/login/getUserMenus"},
    {"name":"获取弹窗通知","url":"https://bpm.yktour.com.cn/ykly-tob-web/b/index/publishNotice/query"},
    {"name":"获取首页图片","url":"https://bpm.yktour.com.cn/ykly-tob-web/scmParamNotice/indexImg"},
    {"name":"获取联系我们","url":"https://bpm.yktour.com.cn/ykly-tob-web/b/index/contactUs/batchquery"},
    {"name":"获取常见问题","url":"https://bpm.yktour.com.cn/ykly-tob-web/b/index/commonProblem/batchquery"},
    {"name":"获取最新公告","url":"https://bpm.yktour.com.cn/ykly-tob-web/b/index/publishNotice/batchquery"},	
    {"name":"查询跟团游","url":"https://bpm.yktour.com.cn/ykly-tob-web/productquery/gty/loadltype?producttype=1"},	
    {"name":"查询我的订单","url":"https://bpm.yktour.com.cn/ykly-tob-web/productquery/gty/loadltype?producttype=1"}
]

def get_default_arg():
    file_name = sys.argv[0].split(".")[0]
    return time.strftime("%Y-%m-%d %X", time.localtime())+" "+file_name + " " 

def user_login(data):
    data={'password': '1qaw3','username': 'anliming'}
    url = "https://bpm.yktour.com.cn/ykly-tob-web/b/login/formLogin"
    s_requests=requests.Session()
    html = s_requests.post(url=url,data=data) 
    return s_requests
def get_url(url):
    name = url["name"]
    url = url["url"]
    html = s_requests.get(url=url,timeout=10)
    if html.status_code == 200:
        if name == "获取首页图片":
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
        html = s_requests.post(url)
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
    s_requests=user_login(data)
    for url in index_xhr:
        try:
            get_url(url)
        except Exception as e:
            print e
	    msg={'name':"警告!!!检查TOB-PC"+" "+url["name"]+"失败","errmsg":get_default_arg()+"\n"+e.message}
            result = send_mail.delay(msg)

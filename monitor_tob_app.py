#!/usr/bin/python
#encoding=utf-8
import requests
import json
import sys,time,os
from task.tasks import send_mail

#requests 传递的参数
data = {
    "_Android":"false",
    "_IOS":"false",
    "loginName":"XXXXXX",
    "passWord":"XXX",
    "type":"3",
}
#URL检查列表
index_xhr = [
    {"name":"首页","url":"http://ylty.yktour.com.cn/"},
    {"name":"查询用户信息","url":"http://ylty.yktour.com.cn/mbpm/user/common/query/info?_=1519454228535"},
    {"name":"查询城市信息","url":"http://ylty.yktour.com.cn/mbpm/product/city/query/info?_=1519454228536"},
    {"name":"查询用户信息","url":"http://ylty.yktour.com.cn/mbpm/user/common/query/info?_=1519454228537"},
    {"name":"查询首页产品信息","url":"http://ylty.yktour.com.cn/mbpm/product/productlist/indexquery?startCityName=%E5%8C%97%E4%BA%AC&_=1519454228538"},
]

#设置提示格式
def get_default_arg():
    file_name = sys.argv[0].split(".")[0]  #获取monitor程序名称
    return time.strftime("%Y-%m-%d %X", time.localtime())+" "+file_name + " "  #返回格式化的名称
#登录，获取session
def user_login(data):
    url = "http://ylty.yktour.com.cn/mbpm/user/common/newlogin"
    s_requests=requests.Session()   #使用requests 的Seesion模块
    html = s_requests.post(url=url,data=data) 
    return s_requests # 返回带有session的requests

#遍历URL列表，
def get_url(url):
    name = url["name"]
    url = url["url"]
    html = s_requests.get(url=url,timeout=10)    #先用GET方法尝试
    if html.status_code == 200:   #如果http状态码为200，进一步判断
        if name == "首页":
            if html.content:
                print get_default_arg()+name+"    检查正常"
            else:
                print get_default_arg()+name+"    检查失败，请及时处理"
                msg={'name':name+" 检查异常","errmsg":get_default_arg()+name+"    异常"}
                result = send_mail.delay(msg)
		print result.status
        else:
            res = json.loads(html.content)    #将返回的数据进行json解析，失败则报警
            if res:
                print get_default_arg()+name+"    检查正常"
            else: 
                print get_default_arg()+name+"    检查失败，请及时处理"
                msg={'name':name+" 检查异常","errmsg":get_default_arg()+name+"    异常"}
                result = send_mail.delay(msg) #调用异步发送邮件报警的在这里
		print result.status
    else:
        html = s_requests.post(url)      #使用POST方法尝试
        if html.status_code == 200:
            res = json.loads(html.content)
            if res:
                print get_default_arg() +name+" 检查正常"
            else: 
                print get_default_arg() +name+" 检查失败，请及时处理"
                msg={'name':name+" 检查异常","errmsg":get_default_arg()+name+"    异常"}
                result = send_mail.delay(msg) #调用异步发送邮件报警的在这里

		print result.status
	
if __name__ == "__main__":
    s_requests=user_login(data)
    for url in index_xhr:
        try:
            get_url(url)
        except Exception as e:
            print e
	    msg={'name':"警告!!!检查TOB_APP"+" "+url["name"]+"失败","errmsg":get_default_arg()+"\n"+e.message}
            result = send_mail.delay(msg)  #调用异步发送邮件报警的在这里

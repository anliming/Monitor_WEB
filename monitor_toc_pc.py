#!/usr/bin/python
#encoding=utf-8
import requests
import json
import sys,time,os
from task.tasks import send_mail

index_xhr = [
    {"name":"首页","url":"http://www.yktour.com.cn"},
    {"name":"热门推荐","url":"http://www.yktour.com.cn/ykly-toc-web/c/navindex/getCHotRecommends"},
    {"name":"导航栏","url":"http://www.yktour.com.cn/ykly-toc-web/c/navindex/topmenu?cityName=%E5%8C%97%E4%BA%AC"},
    {"name":"轮播图","url":"http://www.yktour.com.cn/ykly-toc-web/c/navindex/indexAdverts?topMuId=1&cityName=%E5%8C%97%E4%BA%AC"},
    {"name":"左侧菜单","url":"http://www.yktour.com.cn/ykly-toc-web/c/navindex/leftmenu?topMuId=1&cityName=%E5%8C%97%E4%BA%AC"},
    {"name":"楼层","url":"http://www.yktour.com.cn/ykly-toc-web/floorPc/getFListByNavId?navId=1"},
    {"name":"静态文件时间戳","url":"http://static.yktour.com.cn/www/assets/activity_timer.json?v=1519436189063"},
    {"name":"友情链接","url":"http://www.yktour.com.cn/ykly-toc-web/c/navindex/getPartners?pageSize=15&pageNo=1"}
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
            msg={'name':"警告!!!ToC_PC"+" "+url["name"]+"失败","errmsg":get_default_arg()+"\n"+e.message}

            result = send_mail.delay(msg)

#encoding=utf-8
from __future__ import absolute_import
from task.celery import app
import yagmail
import os
@app.task
def add(x, y):
    return x + y
@app.task
def send_mail(msg,to="ops@xx.com.cn"):
    yag = yagmail.SMTP(user='xxx@126.com', password='xxx',smtp_ssl=True,host='smtp.126.com',)
    try:
        yag.send(to=to,subject=msg["name"],contents=msg["errmsg"])
        return 'Send mail success'
    except Exception as e:
        return e
@app.task
def run_monitor_toc_app():
    Result=os.popen("/bin/python /home/anliming/monitor_proj/monitor_toc_app.py")
    return Result.read()
@app.task
def run_monitor_toc_pc():
    Result=os.popen("/bin/python /home/anliming/monitor_proj/monitor_toc_pc.py")
    return Result.read()

@app.task
def run_monitor_tob_pc():
    Result=os.popen("/bin/python /home/anliming/monitor_proj/monitor_tob_pc.py")
    return Result.read()
@app.task
def run_monitor_tob_app():
    Result=os.popen("/bin/python /home/anliming/monitor_proj/monitor_tob_app.py")
    return Result.read()

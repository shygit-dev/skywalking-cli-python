#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Tile:
# Author:shy
import requests
import time
import smtplib
from email.mime.text import MIMEText
import re

def interface_filter(endpointName):
    """
    设置接口黑名单
    :param endpointName:
    :return: 【1|0】
    """
    with open("blackname_list","r",encoding="utf-8") as f:
        bn_list = f.read()
    match_result = re.search(endpointName,bn_list)
    if match_result == None:
        print("提示：接口不存在黑名单中")
        return 1
    print("提示：接口在黑名单中")
    return 0

def trace_erro_interface(start_time,end_time,sw_url,per_page_size,trace_detail_addr):
    """
    skywalking trace功能对错误接口进行过滤，默认最大一次获取2000条数据，每分钟执行一次
    :param start_time:
    :param end_time:
    :return:
    """
    url = sw_url
    data = {
          "query": "query queryTraces($condition: TraceQueryCondition) {\n  data: queryBasicTraces(condition: $condition) {\n    traces {\n      key: segmentId\n      endpointNames\n      duration\n      start\n      isError\n      traceIds\n    }\n    total\n  }}",
          "variables": {
            "condition": {
              "queryDuration": {
                "start": start_time, #"2021-12-07 1734"
                "end": end_time,
                "step": "MINUTE"
              },
              "traceState": "ERROR",
              "paging": {
                "pageNum": 1,
                "pageSize": per_page_size,
                "needTotal": "true"
              },
              "queryOrder": "BY_START_TIME"
              # "traceId": "b669d0069be84fce82261901de412e7c.430.16388637511348105"
            }
          }
        }

    result = requests.request(method="post",url=url,json=data)
    i = 0
    # print(result.content)
    # print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float("%s.%s" % (trace["start"][0:10],trace["start"][10:])))))
    with open("mail.html","w",encoding="utf-8") as f:
        f.write('<head><meta charset="UTF-8"><title>Title</title><style>.t {border-right: 2px solid black;border-bottom: 2px solid black;}.t th,td {border-top: 2px solid black;border-left: 2px solid black;font-size: 10px;}</style></head><body><div style="color:red;font-size=15px;">最近15分钟统计：</div><table class="t" border="0" cellspacing="0" cellpadding="10px"><thead><tr style="background-color: deepskyblue"><th style="width: 100px;">时间</th><th>持续时长</th><th>接口名称</th><th>追踪ID</th></tr></thead><tbody>')
    for trace in result.json()["data"]["data"]["traces"]:
        # print(trace["endpointNames"])
        print("时间：%s\n" % time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float("%s.%s" % (trace["start"][0:10],trace["start"][10:])))),
              "持续时长：%s\n" % trace["duration"],
              "接口名称：%s\n" % trace["endpointNames"][0],
              "跟踪ID：%s" % trace["traceIds"][0])
        # print(time.localtime(1638869640.194))
        i+=1
        print(i)
        s_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float("%s.%s" % (trace["start"][0:10],trace["start"][10:]))))
        dur_time =  trace["duration"]
        endpointName = trace["endpointNames"][0]
        trace_id = trace["traceIds"][0]

        # 调用接口过滤功能
        result = interface_filter(endpointName)
        if result == 0:
            print("哥们进入黑名单了！",endpointName)
            continue

        with open("mail.html","a",encoding="utf-8") as f:
            f.write('<tr><td>%s</td><td>%s</td><td>%s</td><td><a href="http://%s/query?trace_id=%s">%s</a></td></tr>' %(s_time,dur_time,endpointName,trace_detail_addr,trace_id,trace_id))
    with open("mail.html","a",encoding="utf-8") as f:
        f.write('</tbody></table></body>')


def send_mail(receiver):
    """
    发送报错接口邮件
    :return:
    """
    server = "mail.liuheqinqiang.com"
    sender = "sa@liuheqinqiang.com"
    sender_pwd = "1qaz@WSX"
    send_addr = "sa@liuheqinqiang.com"

    receiver = receiver
    with open("mail.html","r",encoding="utf-8") as f:
        content = f.read()
    if re.search("<td>",content) == None:
        print("无报错接口！",content)
        return 0
    print("邮件前",content)
    msg_mail = MIMEText(content,"html","utf-8")
    msg_mail["Subject"] = "Skywalking报错接口统计"
    msg_mail["From"] = sender
    msg_mail["To"] = receiver

    server_obj = smtplib.SMTP_SSL(server)
    server_obj.connect(server,465)
    server_obj.login(sender,sender_pwd)
    server_obj.sendmail(send_addr,receiver,msg_mail.as_string())


if __name__ == "__main__":
    # 设定查询时间间隔，默认900s（15min）
    end_time = time.time()
    start_time = end_time - 900
    start_time=time.strftime("%Y-%m-%d %H%M",time.localtime(start_time))
    end_time = time.strftime("%Y-%m-%d %H%M", time.localtime(end_time))
    print(start_time)
    print(end_time)
    sw_url = "http://172.16.53.232:9412/graphql" # skywalking的前端服务的地址和端口
    per_page_size = 5000  #指定一次显示接口条数
    trace_detail_addr = "127.0.0.1:5000" # trace-id详细日志要访问的地址，该地址为sw-trace-id.py启动后的服务地址

    receiver = "shihaiyan@liuheqinqiang.com,test1@liuheqinqiang.com"  #报警邮件接收人地址

    trace_erro_interface(start_time,end_time,sw_url,per_page_size,trace_detail_addr)
    send_mail(receiver)
    # interface_filter()

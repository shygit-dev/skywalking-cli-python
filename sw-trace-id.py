#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Tile:
# Author:shy
import requests
import time
from flask import Flask,request
app = Flask(__name__)

@app.route("/query",methods=["get"])
def trace_id_query():
    """
    查询指定trace_id详细日志信息
    :return: f.read()
    """
    trace_id = request.args.get("trace_id")
    url="http://172.16.53.232:9412/graphql"
    # url="http://skywalking.roulw.com/graphql"
    data = {
      "query": "query queryTrace($traceId: ID!) {\n  trace: queryTrace(traceId: $traceId) {\n    spans {\n      traceId\n      segmentId\n      spanId\n      parentSpanId\n      refs {\n        traceId\n        parentSegmentId\n        parentSpanId\n        type\n      }\n      serviceCode\n      serviceInstanceName\n      startTime\n      endTime\n      endpointName\n      type\n      peer\n      component\n      isError\n      layer\n      tags {\n        key\n        value\n      }\n      logs {\n        time\n        data {\n          key\n          value\n        }\n      }\n    }\n  }\n  }",
      "variables": {
        "traceId": trace_id
      }
    }

    result = requests.request(method="post",url=url,json=data)
    with open("detail_log", "w", encoding="utf-8") as f:
        f.write("<div style='color: red;font-size: 30px;'>生产Skywalking报错接口跟踪日志日志：<br /></div>")
    for trace_id in result.json()["data"]["trace"]["spans"]:

        if trace_id["isError"]:
            # print(trace_id)
            print("服务名称：%s\n" % trace_id["serviceCode"],
                  "开始时间：%s\n" % trace_id["startTime"],
                  "接口名称：%s\n" % trace_id["endpointName"],
                  "peer名称：%s\n" % trace_id["peer"],
                  "tags名称：%s\n" % trace_id["tags"],
                  "详细日志：%s" % trace_id["logs"])
            content = "服务名称：%s<br />开始时间：%s<br />接口名称：%s<br />peer名称：%s<br />tags名称：%s" % (trace_id["serviceCode"],trace_id["startTime"],trace_id["endpointName"],trace_id["peer"],trace_id["tags"])
            with open("detail_log","a",encoding="utf-8") as f:
                f.write(content)
                f.write("<br />********详细日志**********<br />")
            for logs in trace_id["logs"]:
                for log in logs["data"]:
                    if log["key"] == "message":
                        print(log["value"])
                        with open("detail_log","a",encoding="utf-8") as f:
                            f.write(log["value"])
                        # return log["value"]
                    elif log["key"] == "stack":
                        print(log["value"])
                        with open("detail_log","a",encoding="utf-8") as f:
                            f.write(log["value"])
            with open("detail_log", "a", encoding="utf-8") as f:
                f.write("<div style='color: red;font-size: 20px;'><br />========下一个接口信息=========<br /></div>")
    with open("detail_log","r",encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    # trace_id = "14447ae7199c40a2b9862411daba180b.2142.16388920322367785"
    # trace_id_query(trace_id)
    app.run()
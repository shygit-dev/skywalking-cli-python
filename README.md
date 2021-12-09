# skywalking-cli-python
实现了对skywalking的追踪（trace）部分的错误接口过滤、黑名单、邮件通知、指定trace_id详细日志查询<br />
<h1>使用方式</h1>

<h2>该项目包含两部分：第1部分  </h2>
  1、 sw-trace.py主要用于获取skywalking中trace部分的错误接口，同时实现了对“错误接口”进行黑名单配置。 <br /> 
  2、 blackname_list中配置要过滤掉的黑名单接口，每行一个黑名单接口。  <br />
  3、 sw-trace.py同时实现了对获取错误接口后生成html文档，并将该文件以邮件方式发送至指定邮箱。<br />
  4、 启动
  
  ```Python
   # python trace-id.py
  ```
  
    结果：
  

|时间|持续时长|接口名称|追踪ID|
|----|----|----|----|
| 2021-12-09 13:13:37  | 396 | 	{GET}/admin/users/queryByTel  | [14447ae7199c40a2b9862411daba180b.2135.16390267834874185](http://ip:port/query?trace_id=14447ae7199c40a2b9862411daba180b.2135.16390267834874185) |

  
<h2> 该项目包含两部分：第2部分 </h2>
  1、主要用来和第一部分进行错误接口联动查询。<br /> 
  2、通过第一部分接口的trace-id，来获取trace-id对应的详细错误日志。<br /> 
  3、该部分主要通过flask启动一个服务实现，该服务用来想skywalking server请求获取对应的详细日志。<br /> 
  4、启动方式<br /> 
  
  ```Python
  # nohup python3 sw-trace-id.py &
  ```
  
  后续
  ==
  ---
      联系方式：906184891@qq.com
      欢迎大家后续补充修改，共同学习。


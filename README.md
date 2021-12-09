# skywalking-cli-python
实现了对skywalking的追踪（trace）部分的错误接口过滤、黑名单、邮件通知、指定trace_id详细日志查询<br />
<h1>使用方式</h1>
<div>
<h2>该项目包含两部分：第1部分  </h2>
  1、trace-id.py主要用于获取skywalking中trace部分的错误接口，同时实现了对“错误接口”进行黑名单配置。 <br /> 
  2、black_list中配置要过滤掉的黑名单接口，每行一个黑名单接口。  <br />
  3、trace-id.py同时实现了对获取错误接口后生成html文档，并将该文件以邮件方式发送至指定邮箱。<br />  
<h2> 该项目包含两部分：第2部分 </h2>
  
</div>

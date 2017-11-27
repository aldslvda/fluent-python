## 网络是怎样连接的 ##
### 一. 浏览器生成请求 -- 探索浏览器内部 ###

#### 1. 概览
浏览器发出一个请求会经历下面四步：

- 生成http请求消息
- 向DNS服务器查询web服务器的IP（如果使用的是域名）
- 全世界的DNS服务器接力使得ip查询顺利进行
- 委托协议栈发送消息

#### 2. 生成http请求消息
1. URL 统一资源定位符 由协议+地址+路径组成，开头部分决定了协议（“http:”“ftp:”“file:”“mailto:”）     
2. 浏览器解析url是将它拆分解析的，如http请求的url,会拆分成http://, 域名/ip, 路径。     文件名为index.html/default.html时可以被省略。    
3. HTTP的基本思路:**HTTP 协议定义了客户端和服务器之间交互的消息内容和步骤**，客户端发送的请求包含“对什么”（URI）进行什么样的操作(Method)
![F1.1](https://github.com/aldslvda/blog-images/blob/master/H-N-C-1.1.png?raw=true)  
收到HTTP请求后，服务器会根据Method和URI决定“对什么进行什么操作”，然后将结果放在响应消息中返回给客户端，浏览器对返回的消息做出展示，一次HTTP请求就完成了。
4. 生成HTTP请求:
http消息在格式上有很严格的规定, 浏览器会按照规范生成请求。   
请求消息的第一行称为请求行，这行开头的Method决定了"作何种操作"
请求消息一般分为三部分Request(请求行), HEADERS(消息头), BODY(消息体)
响应消息也分为三部分，分别是STATUS（状态行）, HEADERS(消息头), BODY(消息体)
![F1.2](https://github.com/aldslvda/blog-images/blob/master/H-N-C-1.2.png?raw=true)  
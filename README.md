# BilibiliAgent
## [langchain+RAG]基于B站视频字幕的多轮对话Agent  
### 项目简介
本项目可以通过Agent帮你快速看完很多个视频！  
配好api-key并设置关键词之后，本项目先在b站中获取相关视频，然后根据视频的bv号和aid爬取视频的字幕，并基于视频字幕构建向量数据库。  
本项目调用了通义千问的api构建具有多轮对话功能的Agent，并添加了百度智能云的api，使得Agent可以进行联网搜索。  
### 环境配置
#### 必要库安装
执行`pip install -r requirements.txt`安装必要库  
#### api-key获取
##### 通义千问api-key获取
新注册的用户有1,000,000个token的免费额度，只是学习用途的话完全够用了  
我也试过用OpenAI的api，个人感觉还是用通义千问更加稳定一些。  
传送门：https://bailian.console.aliyun.com/?tab=model#/api-key  
点击右上角“创建我的api-key获取”
![image](https://github.com/user-attachments/assets/58d83430-efa1-4765-8faf-7bedc1c24ba2)
如果要查询自己还剩多少个token的免费额度，可以在百炼控制台的`模型广场-选择模型-查看详情`里查询：
![image](https://github.com/user-attachments/assets/86085c78-11bc-45b8-b94a-9d0e2f2e9ed9)
![image](https://github.com/user-attachments/assets/0c6d1b8a-db00-43cc-ac3e-64d4f7a278ca)
##### 百度智能云api-key获取
升级版的百度搜索功能，每天免费额度100次，学习用途也够用了  
传送门：https://console.bce.baidu.com/qianfan/ais/console/apiKey  
![image](https://github.com/user-attachments/assets/eb65a573-d0e2-40a0-a0d9-9a58596dbf3a)
#### User-Agent以及Cookie获取
打开网页版b站（我是以账号登录状态打开的），右键选择`检查`或者按F12打开开发工具  
在右上方的侧边栏选择`网络`，找一个`名称`里的请求点开，在请求标头里找到自己的User-Agent以及Cookie，如果没有Cookie就换一个点开
![image](https://github.com/user-attachments/assets/96c52345-46a2-4775-b673-cd2b6174434c)
#### 配置config文件

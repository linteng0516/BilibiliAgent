# BilibiliAgent
## [langchain+RAG]基于B站视频字幕的多轮对话Agent  
### 项目简介
本项目可以通过Agent帮你快速看完很多个视频！  
配好api-key并设置关键词之后，本项目先在b站中获取相关视频，然后根据视频的bv号和aid爬取视频的字幕，并基于视频字幕构建向量数据库。  
本项目调用了通义千问的api构建具有多轮对话功能的Agent，并添加了百度智能云的api，使得Agent可以进行联网搜索。  
### 环境配置
#### 必要库安装
执行`pip install -r requirements.txt`安装必要库  
#### 从huggingface下载文件
传送门：https://huggingface.co/maidalun1020/bce-embedding-base_v1/tree/main
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
完成环境配置后已经完成一大半啦，接下来把上面获得的内容复制到`config.json`的对应参数中，并根据个人喜欢配置其他参数即可。  
config文件的参数解释如下：
| 参数名称  | 参数含义 |
| ------------- | ------------- |
| keyword  | 搜索视频的关键词  |
| output_dir  | 存放输出文件的目录  |
| search_url  | 调用b站搜索api的url  |
| get_cid_url  | 获取视频cid（分p视频）的url  |
| get_subtitle_url  | 获取视频字幕的url  |
| headers  | 发起请求的标头 |
| cookie  | 发起请求的cookie（没有这个会被拦截） |
| time_range  | 筛选视频发布时间：从若干天前到今天  |
| max_pages  | 获取视频的页数（一页10个视频）  |
| model_name  | bce-embedding-base_v1目录的完整路径  |
| model_kwargs  | 模型参数  |
| encode_kwargs  | 模型参数  |
| model  | 调用通义千问模型的名称  |
| api_key  | 通义千问模型的api_key  |
| baidu_url  | 调用百度智能云搜索api的url  |
| baidu_headers  | 调用百度智能云搜索的请求标头  |
#### 运行程序
按照从1到3的顺序依次运行程序，4和5二选一运行。
下面对程序4和5进行演示，搜索关键词为`电影 推荐`
![image](https://github.com/user-attachments/assets/2ec73dd9-efa7-4957-b92c-e1f20ea08432)
![image](https://github.com/user-attachments/assets/a360699c-612a-4156-baae-c7ef788d8f5e)


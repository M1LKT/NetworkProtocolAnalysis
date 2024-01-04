### :computer: FLASK+VUE2制作的模仿WIRESHARK功能的在线网络协议解析器

😼M1LKTEA 2023.12.30

#### 简介
这仅是一个用来完成杭州电子科技大学的网络协议分析课程的实验3、4的项目（已通过验收），所以功能很不完善，之后可能会有更新。欢迎学弟学妹下载这个项目。

#### 下载方法

1.`git clone https://github.com/M1LKT/NetworkProtocolAnalysis.git` 下载项目到本地

2.`pip install -r requirements.txt`下载后端依赖

#### 使用方法
在文件路径中打开powershell，执行命令
`./start.ps1`

终端启动完成后自动进入流量抓取页面

后端默认开在5000端口，前端在8080端口，如有需求自己在配置文件中修改。

#### 使用说明
流量抓取页面：选择指定的网卡，输入需要抓取的流量数量（输入0时抓取5条）和过滤条件（采用BPF过滤规则），随后会返回流量数据(最多解析到TCP/UDP层次)。

PCAP文件分析页面：将pcap文件上传，随后会返回对文件的统计分析。

#### 2024.1.4更新
在分析页面接入了星火大模型辅助分析，使用者需要在按照backend\utils\StarFireAPI\config.json.example的格式创建config.json，详细参数参考讯飞星火的api文档：`https://www.xfyun.cn/doc/spark/Web.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E`
# Claude-free

[**English**](./README.md) | [**中文简体**](./README_zh_CN.md)


这个项目利用了slack上的claude服务，将其抽取出来，从而可以完美的替代claude官方的api服务。

1.首先你需要配置config.py文件，你需要做的是将slack的token,claude的用户id以及你的channel_id配置好。其中channel_id是否配置取决于你是否想在请求时携带自定义的channel_id。如果channel_id不配置，那么在发送消息的api的请求就必须要传入一个channel_id。如果配置则在请求中channel_id缺失的情况下会默认采用配置中的channel_id。如果请求中的channel_id不为空，则始终采用请求的channel_id值。

对于如何注册以及配置slack等参数，你可以参考这个视频：[[SLACK配置视频]](https://www.bilibili.com/video/BV1Lz4y1B7Hs/?spm_id_from=333.337.search-card.all.click&vd_source=0f2e34b3c4cefb6fccb9eb108ab54e1a)
不过在配置权限时除了视频中的权限外，还需要配置users:read权限，这个权限是用来检测配置的claude_id是否存在，汇总:[channels:history,channels:read,channels:write,groups:history,groups:read,groups:write,chat:write, im:history, im:write, mpi,users:read]

channel_id 应该应为频道id，请不要使用私聊，且请在频道中添加claude。

WORKERS 参数代表同时可处理的请求个数，根据实际情况调整。

相关的链接：

token获取：https://api.slack.com/

api文档：https://api.slack.com/methods

websocket文档：https://api.slack.com/apis/connections

2.当你配置好了config.py，并正确安装python后，你可以通过点击[**start_service.bat**](./start_service.bat) 来启动服务，它会自动安装相关依赖并启动。

相关接口：

1.发送和接受回复: 

URL: 127.0.0.1:8000/claude/send

REQUEST BODY: 
>{
"channel_id" : "channel_id",
"conversation_key" : "conversation_key",
"message": "为我写个故事"
}

> channel_id 为可选项，可以向不同的频道发送消息，或者不传则向config.py中配置的频道发送消息。

> conversation_key 代表了一次对话的key，如果想开始新的对话，可以留空，新对话产生的conversation_key将会在响应中得到。

2.查询指定回复：

URL: 127.0.0.1:8000/claude/receive_reply

REQUEST BODY:
> {
"channel_id" : "channel_id",
"conversation_key" : "conversation_key",
"message_key": "message_key"
}

> 参数部分与接口1基本一致，message_key可以在接口1的响应中得到。

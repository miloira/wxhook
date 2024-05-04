# WxHook

## 简介

WxHook是一个基于dll注入实现的python微信机器人框架，支持多种接口、高扩展性、多线程事件高并发，让你轻松应对海量消息，为你的需求实现提供便捷灵活的支持。

支持的接口
1. hook同步消息
2. 取消hook同步消息
3. hook日志
4. 取消hook日志
5. 检查登录状态
6. 获取用户信息
7. 发送文本消息
8. 发送图片消息
9. 发送文件消息
10. 发送表情消息
11. 发送小程序消息
12. 发送群@消息
13. 发送拍一拍消息
14. 获取联系人列表
15. 获取联系人详情
16. 创建群聊
17. 退出群聊
18. 获取群详情
19. 获取群成员列表
20. 添加群成员
21. 删除群成员
22. 邀请群成员
23. 修改群成员昵称
24. 设置群置顶消息
25. 移除群置顶消息
26. 转发消息
27. 获取朋友圈首页
28. 获取朋友圈下一页
29. 收藏消息
30. 收藏图片
31. 下载附件
32. 转发公众号消息
33. 转发公众号消息通过消息ID
34. 解码图片
35. 获取语音通过消息ID
36. 图片文本识别
37. 获取数据库句柄
38. 执行SQL命令
39. 测试
  
## 微信版本下载
- [WeChatSetup3.9.5.81.exe](https://github.com/tom-snow/wechat-windows-versions/releases/download/v3.9.5.81/WeChatSetup-3.9.5.81.exe)

## 安装

```bash
pip install wxhook
```

## 使用示例

消息事件处理例子
```python
# import os
# os.environ["WXHOOK_LOG_LEVEL"] = "INFO" # 修改日志输出级别
import time

from wxhook import Bot
from wxhook import events
from wxhook.model import Event


def on_login(bot: Bot):
    bot.send_text("filehelper", "登录成功之后会触发这个函数")


def on_start(bot: Bot):
    print("微信客户端打开之后会触发这个函数")


def on_stop(bot: Bot):
    bot.send_text("filehelper", "关闭微信客户端之前会触发这个函数")
    time.sleep(1)  # 防止客户端关闭太快导致消息发送失败


bot = Bot(
    on_login=on_login,
    on_start=on_start,
    on_stop=on_stop
)


# 消息回调地址
# bot.set_webhook_url("http://127.0.0.1:8000")

@bot.handle(events.TEXT_MESSAGE, once=True)
def on_message(bot: Bot, event: Event):
    bot.send_text("filehelper", "这条消息只会发送一次哦")


@bot.handle(events.TEXT_MESSAGE)
def on_message(bot: Bot, event: Event):
    if event.fromUser != bot.info.wxid:
        bot.send_text(event.fromUser, event.content)


@bot.handle([events.IMAGE_MESSAGE, events.EMOJI_MESSAGE, events.VIDEO_MESSAGE])
def on_message(bot: Bot, event: Event):
    if event.fromUser != bot.info.wxid:
        if event.type == events.IMAGE_MESSAGE:
            bot.send_text(event.fromUser, "图片消息")
        elif event.type == events.EMOJI_MESSAGE:
            bot.send_text(event.fromUser, "表情消息")
        elif event.type == events.VIDEO_MESSAGE:
            bot.send_text(event.fromUser, "视频消息")


bot.run()
```

接口使用例子
```python
import os
import json

from wxhook import Bot
from wxhook import events
from wxhook.model import Event

# faked_version="3.9.10.19"解除微信低版本登录限制
bot = Bot()

msgid_list = []


@bot.handle(events.TEXT_MESSAGE)
def on_text_message(bot: Bot, event: Event):
    self_id = bot.info.wxid
    content = event.content
    sender = event.fromUser
    msg_id = event.msgId
    if sender != self_id:
        if content.find("发送文本") != -1:
            bot.send_text(sender, "这是一条文本消息")
        elif content.find("发送图片") != -1:
            bot.send_image(sender, os.path.abspath("test.png"))
        elif content.find("发送表情") != -1:
            bot.send_emotion(sender, os.path.abspath("test.png"))
        elif content.find("发送文件") != -1:
            print(print(bot.send_file(sender, os.path.abspath("test.xlsx"))))
        elif content.find("发送音频") != -1:
            bot.send_file(sender, os.path.abspath("test.mp3"))
        elif content.find("发送视频") != -1:
            print(bot.send_file(sender, os.path.abspath("test.mp4")))
        elif content.find("创建群聊") != -1:
            bot.create_room(["wxid1", "wxid2"])
        elif content.find("获取群成员列表") != -1:
            print(bot.get_room_members("<chatroomid>"))
        elif content.find("删除群成员") != -1:
            bot.delete_room_member("<chatroomid>", ["<wxid>"])
        elif content.find("添加群成员") != -1:
            bot.add_room_member("<chatroomid>", ["<wxid>"])
        elif content.find("邀请群成员") != -1:
            bot.invite_room_member("<chatroomid>", ["<wxid>"])
        elif content.find("修改在群聊中的昵称") != -1:
            print(bot.modify_member_nickname(sender, "<self-wxid>", "测试机器人"))
        elif content.find("退出群聊") != -1:
            bot.quit_room("<chatroomid>")
        elif content.find("at全体成员") != -1:
            bot.send_room_at(sender, ["notify@all", "<wxid>"], "这是一条at全体成员的消息")
        elif content.find("发送群at") != -1:
            bot.send_room_at(sender, ["<wxid1>", "<wxid2>"], "这是一条at群成员的消息")
        elif content.find("发送群聊拍一拍") != -1:
            bot.send_pat(sender, "wxid_vqj81fdula0x22")
        elif content.find("发送私聊拍一拍") != -1:
            bot.send_pat(sender, sender)
        elif content.find("置顶消息") != -1:
            bot.top_msg(msg_id)
            msgid_list.append(msg_id)
        elif content.find("取消置顶的消息") != -1:
            bot.remove_top_msg(sender, msgid_list.pop())
        elif content.find("获取联系人列表") != -1:
            bot.send_text(sender, json.dumps(bot.get_contacts()))
        elif content.find("获取联系人详情") != -1:
            bot.send_text(sender, json.dumps(bot.get_contact("<wxid>")))
        elif content.find("获取群详情") != -1:
            print(bot.get_room("<chatroomid>"))
        elif content.find("收藏消息") != -1:
            bot.collect_msg(msg_id)
        elif content.find("收藏图片") != -1:
            bot.collect_image(sender, os.path.abspath("test.png"))
        elif content.find("ocr") != -1:
            print(bot.ocr(os.path.abspath("test.png")))

bot.run()
```

QQ交流群:625920216

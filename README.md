# WxHook

## 简介

WxHook是一个基于dll注入实现的python微信机器人框架，支持多种接口、高扩展性、多线程消息处理，让你轻松应对海量消息，为你的需求实现提供便捷灵活的支持。

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

```python
# import os
# os.environ["WXHOOK_LOG_LEVEL"] = "INFO" # 修改日志输出级别
# os.environ["WXHOOK_LOG_FORMAT"] = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>" # 修改日志输出格式
from wxhook import Bot
from wxhook import events
from wxhook.model import Event


def on_login(bot: Bot, event: Event):
    print("登录成功之后会触发这个函数")


def on_start(bot: Bot):
    print("微信客户端打开之后会触发这个函数")


def on_stop(bot: Bot):
    print("关闭微信客户端之前会触发这个函数")


def on_before_message(bot: Bot, event: Event):
    print("消息事件处理之前")


def on_after_message(bot: Bot, event: Event):
    print("消息事件处理之后")


bot = Bot(
    # faked_version="3.9.10.19", # 解除微信低版本限制
    on_login=on_login,
    on_start=on_start,
    on_stop=on_stop,
    on_before_message=on_before_message,
    on_after_message=on_after_message
)


# 消息回调地址
# bot.set_webhook_url("http://127.0.0.1:8000")

@bot.handle(events.TEXT_MESSAGE)
def on_message(bot: Bot, event: Event):
    bot.send_text("filehelper", "hello world!")


bot.run()
```

QQ交流群：705791428

开源版本：

微信3.9.5.81版本开发框架项目地址：https://github.com/miloira/wxhook

微信3.9.2.23版本开发框架项目地址：https://github.com/miloira/wxhelper

# 🎉新版本pywechat已发布，请进QQ群：705791428获取！
同时支持微信`3.x`版本和`4.x`版本的微信机器人框架

**使用须知**
1. 微信号头像必须设置，否则框架无法正常运行。
2. 微信`4.x`版本首次使用本框架，请运行示例代码调起微信后扫码登录。

```python
from loguru import logger

logger.remove()

from pywechat import WeChat, events
from pywechat.utils import go_wechat3

# 支持微信版本 3.6.0.18/3.9.10.19/3.9.10.27/3.9.11.17/3.9.12.15/3.9.12.45/4.0.1.21/4.0.3.22/4.1.0.34/4.1.2.17
wechat = WeChat("4.1.2.17")


@wechat.handle(events.WINDOW_HANDLE_CHANGE_MESSAGE)
def _(bot: WeChat, event: dict):
    # 解除微信3.x登录低版本限制
    if bot.version.startswith("3") and event["data"].get("login_hwnd"):
        go_wechat3(event["data"]["pid"], "all", "Windows 11 x64", "Windows 10 x86", bot.version, "3.9.12.56")
        bot.refresh_qrcode(event["client_id"])


@wechat.handle(events.USER_LOGIN_MESSAGE)
def _(bot: WeChat, event: dict):
    print(f"已登录：{event}")


@wechat.handle(events.USER_LOGOUT_MESSAGE)
def _(bot: WeChat, event: dict):
    print(f"已退出登录：{event}")


@wechat.handle(events.TEXT_MESSAGE)
def _(bot: WeChat, event: dict):
    print(f"收到文本消息：{event}")


wechat.run()
```
**特色功能**

1.支持不同微信版本

2.微信3.x登录出现低版本可自动解除

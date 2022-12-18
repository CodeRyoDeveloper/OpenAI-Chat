import discord
import requests
import json

# 设置 Discord intents
intents = discord.Intents().all()
intents.message_content = True
client = discord.Client(intents=intents)

channel_id = "channel id"

# 建立一个字典，用来储存每个使用者的聊天纪录
chat_history = {}

@client.event
async def on_message(message):
    # 取得使用者 ID 和聊天内容

    user_id = message.author.id
    # 只取 "AI" 後面的字串
    chat_content = message.content
    # 如果聊天內容不是以 "AI" 開頭，則直接跳過
    if not chat_content.startswith("AI"):
        return
    # 取得聊天內容，並去掉頭尾的双引號
    chat_content = chat_content.split("\"")[1]
    # 如果使用者 ID 不在字典中，則新增一个记录
    if user_id not in chat_history:
        chat_history[user_id] = []

    # 取得使用者的聊天纪录
    user_history = chat_history[user_id]

    # 如果聊天次数大于 30，則清除除了前一次聊天纪录以外的记忆
    if len(user_history) > 30:
        user_history = user_history[-1:]

    # 使用 OpenAI API 回复使用者的訊息
    headers = {
        "Authorization": "Bearer openapikey"
    }
    data = {
    "model": "text-davinci-003",
    "prompt": f"{' '.join(user_history)} {chat_content}",
    "max_tokens": 1024,
    "temperature": 0.5,
}
    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    if response.status_code == 200:
        jsondata = response.json()
        print(response.json())
        response_text = jsondata['choices'][0]['text']
        # 将回复的文本傳回 Discord 频道
        channel=client.get_channel(channel_id)
        await message.channel.send(response_text)
    else:
        # 处理错误
        print(response.json())
        pass

    # 将使用者的聊天纪录加入聊天纪录中
    user_history.append(chat_content)
client.run("bot token")

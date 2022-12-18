import discord
import requests
import json

# 设置 Discord intents
intents = discord.Intents().all()
intents.message_content = True
client = discord.Client(intents=intents)

channel_id = "1053925215266144329"

# 建立一个字典，用来储存每个使用者的聊天纪录
chat_history = {}

@client.event
async def on_message(message):
    # 取得使用者 ID 和聊天内容
    user_id = message.author.id
    chat_content = message.content
    model = "text-davinci-003"
    res = ""
    # 如果訊息的格式符合 "AIclearALL"，則進行處理
    if chat_content == "AIclearALL":
        # 清除所有使用者的聊天紀錄
        chat_history.clear()
        # 將文本傳回 Discord 頻道
        channel=client.get_channel(channel_id)
        # Tag the user in the response message
        res = "已清除所有使用者的聊天紀錄"
        await message.channel.send(f"{message.author.mention}, {res}")
        return
    # 如果訊息的格式符合 "AIclear"，則進行處理
    elif chat_content == "AIclear":
        # 将使用者的聊天纪录清除
        chat_history[user_id] = []
        # 将文本傳回 Discord 频道
        channel=client.get_channel(channel_id)
        res = "已清除聊天紀錄"
        await message.channel.send(f"{message.author.mention}, {res}")
        return
    # 如果訊息的格式符合 "AIcode" + 內容，則進行處理
    elif chat_content.startswith('AIcode"'):
        # 去除頭尾的双引號
        chat_content = chat_content.strip('"')
        # 將字符串分割成三個部分，取出第二個部分的內容
        chat_content = chat_content.split('"')[1]
        model = "code-davinci-002"
    # 如果訊息的格式符合 "AI" + 內容 + "，則進行處理
    elif chat_content.startswith('AI"'):
        # 去除頭尾的双引號
        chat_content = chat_content.strip('"')
        # 將字符串分割成三個部分，取出第二個部分的內容
        chat_content = chat_content.split('"')[1]
        model = "text-davinci-003"
    else:
        # 如果訊息的格式不符合，則跳過不處理
        return
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
        "Authorization": "Bearer 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"
    }
    data = {
    "model": model,
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
        res = response_text
        await message.channel.send(f"{message.author.mention}, {res}")
    else:
        # 处理错误
        print(response.json())
        pass

    # 将使用者的聊天纪录加入聊天纪录中
    user_history.append(chat_content)
client.run("OTYyMzc5ODkzNzQyNjM3MTM4.GebakN.le65jHaY-0Sxbq6tC9-90R31acLryJuPTn2nrI")

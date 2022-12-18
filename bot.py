import discord
import requests

# 设置 Discord intents
intents = discord.Intents().all()
intents.message_content = True
client = discord.Client(intents=intents)

channel_id = "962354694997540935"

# 建立一个字典，用来储存每个使用者的聊天纪录
chat_history = {}

@client.event
async def on_message(message):
    # 取得使用者 ID 和聊天内容
    user_id = message.author.id
    chat_content = message.content
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
    "model": "text-davinci-002",
    "prompt": f"{' '.join(user_history)} {chat_content}",
    "max_tokens": 1024,
    "temperature": 0.5,
}
    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    if response.status_code == 200:
        print(response.json())
        response_text = response.json()['text']
        # 将回复的文本傳回 Discord 频道
        channel=client.get_channel(channel_id)
        await message.channel.send(response_text)
    else:
        # 处理错误
        print(response.json())
        pass

    # 将使用者的聊天纪录加入聊天纪录中
    user_history.append(chat_content)
client.run("key")

import discord
from discord.ext import tasks
import aiohttp
import os
from keep_alive import keep_alive # استدعاء السيرفر الوهمي

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

# حط هنا ID الروم اللي البوت هيبعت فيها إشعارات الألعاب
CHANNEL_ID = 123456789012345678  
sent_games = [] 

@client.event
async def on_ready():
    print(f'✅ البوت شغال دلوقتي باسم: {client.user}')
    if not check_free_games.is_running():
        check_free_games.start()

@tasks.loop(hours=1)
async def check_free_games():
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        return

    url = "https://www.gamerpower.com/api/filter?platform=epic-games-store.steam&type=game"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                games = await response.json()
                for game in games:
                    game_id = game['id']
                    if game_id not in sent_games:
                        sent_games.append(game_id)
                        title = game['title']
                        link = game['open_giveaway']
                        platform = game['platforms']
                        
                        view = discord.ui.View()
                        view.add_item(discord.ui.Button(label="احصل عليها الآن", url=link))
                        
                        await channel.send(
                            f"🚨 **لعبة مجانية جديدة نزلت على {platform}!**\n🎮 الاسم: **{title}**", 
                            view=view
                        )
                        break 

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()

    if "السلام عليكم" in msg:
        await message.channel.send(f"وعليكم السلام يا {message.author.name}! نورت السيرفر 🌸")

    if msg == "s":
        web_link = "https://store.steampowered.com/search/?maxprice=free&specials=1"
        app_link = "https://spectacular-empanada-fe9ba6.netlify.app/"
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Open in Browser", url=web_link))
        view.add_item(discord.ui.Button(label="Open App", url=app_link))
        await message.channel.send("🕹️ **عروض Steam الحالية:**", view=view)

    if msg == "e":
        epic_link = "https://store.epicgames.com/en-US/free-games"
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Open in Browser", url=epic_link))
        view.add_item(discord.ui.Button(label="Open App", url=epic_link))
        await message.channel.send("🎮 **ألعاب Epic المجانية:**", view=view)

# 1. تشغيل السيرفر الوهمي عشان Render ميفصلش البوت
keep_alive()

# 2. تشغيل البوت باستخدام التوكن من إعدادات Render
token = os.environ.get("DISCORD_TOKEN")
if token:
    client.run(token)
else:
    print("❌ خطأ: لم يتم العثور على التوكن!")

import discord
from discord.ext import commands
import json
import youtube_dl
import random
import requests
import asyncio
from discord import FFmpegOpusAudio
from dotenv import load_dotenv, find_dotenv
from time import *
import datetime
from io import BytesIO
from PIL import Image
import urlextract
import os
import pytesseract
import cv2
import numpy as np
import openai


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="marong.help"))
    print(f"{bot.user} is ready!\n*-----* Online *-----*")

invalid_command_embed= discord.Embed(title = "**Invalid Command.**",colour = discord.Colour.from_rgb(255,0,0))
invalid_command_embed.add_field(name="输入 ***marong.help*** 以查看详细使用 marong 的指令",value = "`!p`/`!play` - **播放音乐** \n `!pars`/`!解析` - **解析抖音视频(__注意:大于8MB的视频不能预览__)** \n `!setup` - **自动设置频道(仅限管理员)**")
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(embed = invalid_command_embed, delete_after = 30)

music_channel = []
autochat_channel = []
ragechat = []
mathsolverchannel = []
problemsolverchannel = []

load_dotenv(find_dotenv())
MAORNG_TOKEN = os.getenv('MARONG_TOKEN')
MARONG_SPOTIFY_TOKEN = os.getenv('MARONG_SPOTIFY_TOKEN')
TIANXING_TOKEN = os.getenv('TIANXING_TOKEN')
PUBG_TOKEN = os.getenv('PUBG_TOKEN')
SPOTIFY_CLIENT = os.getenv('spotify_client')
OWNTHINK_TOKEN = os.getenv('OWNTHINK_TOKEN')
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn',}
YTDL_OPTIONS = {'format': 'bestaudio/best','extractaudio': True,'audioformat': 'mp3','outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s','restrictfilenames': True,'noplaylist': True,'nocheckcertificate': True,'ignoreerrors': False,'logtostderr': False,'quiet': True,'no_warnings': True,'default_search': 'auto','source_address': '0.0.0.0',}

help_menu = discord.Embed(title = "**marong 指令/说明书：**",colour = discord.Colour.from_rgb(0,255,255))
help_menu.add_field(name = "marong.help",value = "**自动设置：(__仅管理员__)**\n`!setup` \n\u200b﹒自动设置`\U0001F4AC｜﹒小助手`和 `\U0001F3B6｜﹒公共点歌` 频道\n\n**解析抖音视频：**\n`!pars`  `!解析`\n\u200b﹒输入抖音链接，支持解析图片/直播/视频，只要后缀内容包含链接就行(抖音平台老是傻逼鬼畜，所以有时候发生404其实是抖音平台的问题)\n\n**火力全开：(__真的是火力全开__)**\n`!ragersetup`\n \u200b﹒建立嘴臭频道，让你体验一下暴力marong\n\n**播放音乐：**\n`!p`  `!play`  `!PLAY`  `!P` \n \u200b﹒输入歌名/链接(__如果点歌频道已存在，不需要加任何前缀，直接输入歌名/链接即可__)\n \u200b \u200b﹒Example: `!play 周杰伦 晴天` `!play youtube链接`\n\n**断开语音连接：**\n`!d`  `!disconnect`  `!leave`\n \u200b﹒断开语音连接/中断音乐\n\n**下一首歌：**\n`!skip` \n \u200b﹒播放下一首歌\n\n**暂停/继续**\n`!pause/!resume` \n\u200b﹒暂停播放/继续播放(__***如果点歌频道已存在，直接点击\U000025B6即可***__)\n\n**用户聊天历史记录**\n`!history`\n\u200b﹒查询用户发送的历史信息，默认数值为前100条(__**已删除的信息也能被查询到**__) \n\u200b\u200b﹒Example: `!history @用户 200(要查询多少条信息)`\n\n**删除用户信息**\n`!clean`  `!clear`  `!purge`\n \u200b﹒删除用户的信息(默认数值为100条)\n\u200b\u200b﹒Example: `!purge @用户 200(要删除多少条信息)`")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('marong.help') or message.content.startswith('marong.help'):
        return await message.channel.send(embed = help_menu)
    if message.channel.id in mathsolverchannel:
        if message.attachments:
            if len(message.attachments) == 1:
                if message.attachments[0].content_type in ('image/jpeg', 'image/jpg', 'image/png'):
                    img = Image.open(BytesIO(requests.get(message.attachments[0].url).content)) 
                    image = cv2.threshold(cv2.cvtColor(np.array(img),cv2.COLOR_BGR2GRAY),0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    text = pytesseract.image_to_string(image)
                    await message.send(text)
                    await message.add_reaction('\U00002705')
                else:
                    embed_nomathatt= discord.Embed(title = "**Invalid File Type.**",colour = discord.Colour.from_rgb(255,0,0))
                    embed_nomathatt.add_field(name="**支持文件类型:**",value = f"**.jpeg**\n**.jpg**\n**.png**\n\n**Only Take One Attachment.\n遇到问题了？找{message.guild.owner}**")
                    await message.channel.reply(embed = embed_nomathatt, delete_after = 7)
            else:
                embed_nomathatt= discord.Embed(title = "**Too much Attachments.**",colour = discord.Colour.from_rgb(255,0,0))
                embed_nomathatt.add_field(name="**支持文件类型:**",value = f"**.jpeg**\n**.jpg**\n**.png**\n\n**Only Take One Attachment.\n遇到问题了？找{message.guild.owner}**")
                await message.channel.reply(embed = embed_nomathatt, delete_after = 7)
        else:
            embed_nomathatt= discord.Embed(title = "**No Attachments Found.**",colour = discord.Colour.from_rgb(255,0,0))
            embed_nomathatt.add_field(name="**支持文件类型:**",value = f"**.jpeg**\n**.jpg**\n**.png**\n\n**Only Take One Attachment.\n遇到问题了？找{message.guild.owner}**")
            await message.channel.reply(embed = embed_nomathatt, delete_after = 7)
    if message.channel.id in autochat_channel:
        response = requests.get(f"https://api.ownthink.com/bot?appid=marong&userid={OWNTHINK_TOKEN}d&spoken={message.content}")
        dict_data = json.loads(response.text)
        await message.reply(dict_data['data']['info']['text'])
    if message.channel.id in ragechat:
        response = requests.get("https://fun.886.be//api.php?level=max")
        await message.reply(response.text)
    if message.channel.id in music_channel:
        if message.content.startswith('!'):
            pass
        else:
            ctx = await bot.get_context(message)
            await play(ctx,item = message.content)
        await message.delete()
    if message.channel.id in problemsolverchannel:
        openai.api_key = os.getenv("OPENAI")
        response = openai.Completion.create(model="text-curie-001",prompt=message.content,max_tokens=250,temperature=0.2)
        text = response["choices"][0]['text']
        if len(text) != 0:
            await message.reply(response["choices"][0]['text'])
        else:
            await message.reply('Can you say more?')
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, member:discord.Member):
    if (reaction.message.channel.id in music_channel) and (member != bot.user):
        await reaction.remove(member)
        if not member.guild.voice_client.is_connected():
            return await reaction.message.channel.send(embed = discord.Embed(title = "**Not playing anything.**",colour = discord.Colour.from_rgb(255,0,0)), delete_after = 2)
        if member not in member.guild.voice_client.channel.members:
            return await reaction.message.channel.send(embed = discord.Embed(title = "**Invalid access.**",colour = discord.Colour.from_rgb(255,0,0)), delete_after = 2)
        if reaction.emoji == "\U000025B6":
            if member.guild.voice_client.is_playing():
                member.guild.voice_client.pause()
                embed_paused= discord.Embed(title = "**Paused.**",colour = discord.Colour.from_rgb(0,255,255))
                await reaction.message.channel.send(embed = embed_paused, delete_after = 2)
            elif member.guild.voice_client.is_paused():
                member.guild.voice_client.resume()
                embed_paused= discord.Embed(title = "**Resumed.**",colour = discord.Colour.from_rgb(0,255,255))
                await reaction.message.channel.send(embed = embed_paused, delete_after = 2)
        if reaction.emoji == "\U000023ED":
            await skip(reaction.message, member.guild.voice_client)
        if reaction.emoji == "\U0001F500":
            bot.queue = random.shuffle(bot.queue)

@bot.command(aliases = ["clean","clear"])
@commands.has_permissions(administrator = True)
async def purge(ctx,*,member:discord.Member = None, limit: int = 100):
    if ctx.author.bot:
        return
    else:
        channel = ctx.message.channel
        msgs = []
        if member == None:
            async for i in channel.history(limit = limit):
                    msgs.append(i)
        else:
            async for i in channel.history(limit = limit):
                if i.author == member:
                    msgs.append(i)
        await channel.delete_messages(msgs)

@bot.command()
@commands.has_permissions(administrator = True)
async def history(ctx,*,member:discord.Member = None, limit:int = 100):
    if ctx.author.bot:
        return
    msgs = []
    if member == None:
        async for i in ctx.message.channel.history(limit = limit):
            if not ctx.message.attachments:
                msgs.append(i.content)
    else:
        async for i in ctx.message.channel.history(limit = limit):
            if not ctx.message.attachments:
                if i.author == member:
                    msgs.append(i.content)
    await ctx.send(msgs)

@bot.command(aliases = ["解析"])
async def pars(ctx,*,rest):
    url = urlextract.URLExtract().find_urls(rest)
    if len(url) == 0:
        await ctx.send(embed = discord.Embed(title = "**Found no link.**",colour = discord.Colour.from_rgb(255,0,0)), delete_after = 4)
    elif len(url) > 1:
        await ctx.send(embed = discord.Embed(title = "**Too much link.**",colour = discord.Colour.from_rgb(255,0,0)), delete_after = 4)
    elif len(url) == 1:
        result = requests.get(f"https://api.cooluc.com/?url={url[0]}")
        result_data = json.loads(result.text)
        if result_data['success'] == True:
            nickname = result_data['nickname']
            if "视频" in result_data['msg']:
                videodesc,video_url = result_data["desc"],result_data['video']
                await ctx.send(content = f"{ctx.message.author.mention}你的视频解析好了:\n**{nickname}: {videodesc}**\n*{video_url}*")
            elif "图" in result_data['msg']:
                imagedesc,image_url = result_data['desc'],result_data['images']
                await ctx.send(content = f"{ctx.message.author.mention}你的图片解析好了:\n**{nickname}: {imagedesc}**\n*{image_url}*")
            elif "直播" in result_data['msg']:
                livetitle, m3u8, flv = result_data['title'],result_data['hls_pull_url'],result_data['flv_pull_url']
                await ctx.send(content = f"**{ctx.message.author.mention}\n{nickname}的直播解析好了: {livetitle}**\n*{m3u8}\n{flv}*")
            await ctx.message.delete()
        elif result_data['success'] == False:
            await ctx.send(embed = discord.Embed(title = f"**Error 404. Video can't be access**",colour = discord.Colour.from_rgb(255,0,0)), delete_after = 4)
    else:
        await ctx.send(embed = discord.Embed(title = f"**Invalid.**",colour = discord.Colour.from_rgb(255,0,0)), delete_after = 4)

@bot.command()
async def pubg(ctx, player_id):
    header = {"Authorization": "Bearer "+PUBG_TOKEN,"Accept": "application/vnd.api+json"}
    response = requests.get(url=f"https://api.pubg.com/shards/steam/players?filter[playerNames]={player_id}",headers=header)
    print(json.loads(response.text)[id])

@bot.command()
async def spotify(ctx,*,item):
    pass 

@bot.command(aliases = ["mathsetup","mathsolversetup"])
@commands.has_permissions(administrator = True)
async def mathchannelsetup(ctx,*,categoryname = "应用",channelname = "📐｜﹒数学解析"):
    if ctx.author.bot:
        return
    else:
        category = discord.utils.get(ctx.guild.categories, name=categoryname)
        if category is None:
            await ctx.guild.create_category(categoryname,position = 0)
        channel = discord.utils.get(ctx.guild.text_channels,name = channelname)
        if channel is None:
            await ctx.guild.create_text_channel(channelname)
        channel = discord.utils.get(ctx.guild.text_channels,name = channelname)
        category = discord.utils.get(ctx.guild.channels, name=categoryname)
        await channel.edit(category=category)
        channel_id = int(channel.id)
        mathsolverchannel.append(channel_id)

music_pubic_embed = discord.Embed(title= "**Join a voice channel to start playing!**",description="[Commands](https://www.youtube.com/ \"Hovertext\")",colour = discord.Colour.from_rgb(0,255,255))
music_pubic_embed.add_field(name = f"__**Playlist Queue:\n**__", value = f"** Not Playing any Songs **")
music_pubic_embed.set_image(url= "https://cutewallpaper.org/21/pixel-art-gif-background/Pin-on-arts-and-crafts-shi.gif")
music_pubic_embed.set_footer(text = "**Merry Christmas!** \U0001F384")
bot.var = None
music_channel_name = "\U0001F3B6｜﹒公共点歌"
helper_channel_name = "\U0001F4AC｜﹒马rong聊天"
problemsolver_channel_name = "\U0001F4A1｜﹒小助手"
category_name = "MARONG"
@bot.command()
@commands.has_permissions(administrator = True)
async def setup(ctx):
    if ctx.author.bot:
        return
    else:
        settingup = await ctx.send(embed = discord.Embed(title = f"**Setting up...**",colour = discord.Colour.from_rgb(0,255,255)))
        category = discord.utils.get(ctx.guild.categories, name=category_name)
        if category is None:
            await ctx.guild.create_category(category_name,position = 0)
        category = discord.utils.get(ctx.guild.categories, name = category_name)
        channel_music = discord.utils.get(ctx.guild.text_channels,name = music_channel_name)
        if channel_music is None:
            await ctx.guild.create_text_channel(music_channel_name)
        channel_music = discord.utils.get(ctx.guild.text_channels,name = music_channel_name)
        await channel_music.edit(category=category)
        await channel_music.purge(limit = 20)
        bot.var = await channel_music.send(embed = music_pubic_embed)
        for i in ["\U000023EE","\U000025B6","\U000023ED","\U0001F500","\U0001F501","\U0001F502","\U00002B50","\U0000274C"]:
            await bot.var.add_reaction(i)
        music_channel.append(int(channel_music.id))
        channel_helper = discord.utils.get(ctx.guild.text_channels,name = helper_channel_name)
        if channel_helper is None:
            await ctx.guild.create_text_channel(helper_channel_name)
        channel_helper = discord.utils.get(ctx.guild.text_channels,name = helper_channel_name)
        await channel_helper.edit(category=category)
        autochat_channel.append(int(channel_helper.id))
        channel_solver = discord.utils.get(ctx.guild.text_channels,name = problemsolver_channel_name)
        if channel_solver is None:
            await ctx.guild.create_text_channel(problemsolver_channel_name)
        channel_solver = discord.utils.get(ctx.guild.text_channels,name = problemsolver_channel_name)
        await channel_solver.edit(category=category)
        problemsolverchannel.append(int(channel_solver.id))
        await settingup.delete()
        await ctx.send(embed = discord.Embed(title = f"**Done!**",colour = discord.Colour.from_rgb(0,255,255)),delete_after = 1.5)

@bot.command()
@commands.has_permissions(administrator = True)
async def ragersetup(ctx,*,categoryname = "18+！",channelname = "\U0001F4A2｜﹒火力全开"):
    if ctx.author.bot:
        return
    else:
        category = discord.utils.get(ctx.guild.categories, name=categoryname)
        if category is None:
            await ctx.guild.create_category(categoryname,position = 0)
        channel = discord.utils.get(ctx.guild.text_channels,name = channelname)
        if channel is None:
            await ctx.guild.create_text_channel(channelname)
        channel = discord.utils.get(ctx.guild.text_channels,name = channelname)
        category = discord.utils.get(ctx.guild.channels, name=categoryname)
        await channel.edit(category=category)
        channel_id = int(channel.id)
        ragechat.append(channel_id)

bot.time = 0
bot.queue = []
bot.songindex = 0
bot.yes = True
async def check(voice_client):
    if bot.songindex < len(bot.queue):
        video = bot.queue[bot.songindex]
        audio = await FFmpegOpusAudio.from_probe(video['formats'][0]['url'],**FFMPEG_OPTIONS)
        duration = f"{video['duration']//60}:{video['duration']%60}"
        video_embed = discord.Embed(title= f"\U0001F3B6 **__Now playing__:**\n {video['title']}",description=f"[**Duration - {duration}**]({video['webpage_url']} \"Hovertext\")",colour = discord.Colour.from_rgb(0,255,255))
        if len((bot.queue[bot.songindex+1:])) > 0:
            playlist = ('\n'.join([str(i['title']) for i in bot.queue[bot.songindex+1:]]))
        else:
            playlist = '**No song in playlist queue.'
        video_embed.add_field(name = f"__**Playlist Queue:\n**__", value = f"{playlist}")
        video_embed.set_image(url = video['thumbnail'])
        video_embed.set_footer(text = f"**Merry Christmas!\U0001F384")
        await bot.var.edit(embed = video_embed)
        bot.yes = False
        bot.songindex += 1
        voice_client.play(source = audio, after=lambda x: (await check(voice_client) for _ in '_').__anext__())
    else:
        if not voice_client.is_playing():
            if bot.yes != True:
                await bot.var.edit(embed = music_pubic_embed)
                bot.yes = True
            if bot.time == 2:
                await voice_client.disconnect()
                bot.queue = []
                bot.time = 0
                await check(voice_client)
            else:
                await asyncio.sleep(60)
                bot.time += 1
                await check(voice_client)
        else:
            bot.time = 0
            await asyncio.sleep(60)
            await check(voice_client)


@bot.command(aliases = ["p","P","PLAY"])
async def play(ctx,*,item = None):
    if ctx.author.bot:
        return
    if not ctx.author.voice:
        return await ctx.send(embed = discord.Embed(title = "**Please Join a voice channel to play a song.**",colour = discord.Colour.from_rgb(255,0,0)), delete_after = 4)
    if item == None:
        return await ctx.send(embed = discord.Embed(title = "**Please enter a url or song name.**",colour = discord.Colour.from_rgb(255,0,0)), delete_after = 4)
    with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ydl:
        try:
            requests.get(item) 
        except:
            video = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
        else:
            video = ydl.extract_info(item, download=False)
    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
    elif (ctx.voice_client.is_playing()) and (ctx.author.voice.channel != ctx.guild.voice_client.channel):
        return await ctx.send(embed = discord.Embed(title = f"**Occupied at {ctx.guild.voice_client.channel.mention}.**",colour = discord.Colour.from_rgb(255,0,0)), delete_after = 4)
    else:
        await ctx.guild.voice_client.move_to(ctx.author.voice.channel)
    if ctx.voice_client.is_playing():
        return bot.queue.append(video)
    playlist = "\n".join([i['title'] for i in bot.queue])
    audio = await FFmpegOpusAudio.from_probe(video['formats'][0]['url'],**FFMPEG_OPTIONS)
    duration = f"{video['duration']//60}:{video['duration']%60}"
    video_embed = discord.Embed(title= f"\U0001F3B6 **__Now playing__:**\n {video['title']}",description=f"[**Duration - {duration}**]({video['webpage_url']} \"Hovertext\")",colour = discord.Colour.from_rgb(0,255,255))
    video_embed.add_field(name = f"__**Playlist Queue:\n**__", value = f"**{playlist}**")
    video_embed.set_image(url = video['thumbnail'])
    video_embed.set_footer(text = f"**Merry Christmas!\U0001F384")
    await bot.var.edit(embed = video_embed)
    bot.yes = False
    ctx.voice_client.play(source = audio, after=lambda x: (await check(ctx.voice_client) for _ in '_').__anext__())

@bot.command(pass_context = True,aliases = ["d","leave"])
async def disconnect(ctx):
    leaving_message = ["**我走了哟～ 你们不要想我哦～ :flushed:**",
    "**好，我滚，下次别让我再见到你个臭逼 :angry:**",
    "**你好讨厌呀～ 你这样我会想你的～:flushed:**",
    "**我走之前可以闻一下你的xifu吗？:face_with_hand_over_mouth:**",
    "**你讨厌厌了啦～ :pleading_face: **",
    "**下次见面我tm一拳打死你**",
    "**md臭傻逼 :angry:\n我真的***:face_with_symbols_over_mouth: **",
    "我谢谢你妈 :face_with_symbols_over_mouth: "]
    if ctx.author.bot:
        return
    if (ctx.voice_client):
        await bot.var.edit(embed = music_pubic_embed)
        bot.yes = True
        bot.queue = []
        await ctx.guild.voice_client.disconnect()
        await ctx.send(random.choice(leaving_message), delete_after = 5)
    else:
        await ctx.send("**我都不在语音频道，你是傻逼吗？:angry:**")

@bot.command()
async def pause(ctx):
    if ctx.author.bot:
        return
    else:
        ctx.voice_client.pause()
        await ctx.send(content = "**OK，我闭上我条嘴** :flushed:", delete_after = 5)

@bot.command()
async def resume(ctx):
    if ctx.author.bot:
        return
    else:
        ctx.voice_client.resume()
        await ctx.send(content = "**我又继续了喔** :flushed:", delete_after = 5)

@bot.command()
async def skip(message,voice_client):
    voice_client.stop()
    await message.channel.send(content = "**Skipped**", delete_after = 5)
    await check(voice_client)
    
bot.run(MAORNG_TOKEN)
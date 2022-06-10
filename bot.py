import discord
import asyncio
from youtubesearchpython import VideosSearch
from discord.ext import commands
import urllib.parse, urllib.request, re
import json
import random
import os
import youtube_dl

client = commands.Bot(command_prefix = "$", help_command = None)

@client.event
async def on_ready():
    print("ready to go.")
    
@client.command()
async def search(ctx,*,query):
    query_string = urllib.parse.urlencode({'search_query': query})
    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})',
                                htm_content.read().decode())
    await ctx.channel.send('http://www.youtube.com/watch?v=' + search_results[0])

@client.command()
async def mp3(ctx,*,search):
    await ctx.reply("Please be patient. This could take up to 5 minutes.")
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})',
                                htm_content.read().decode())
    url = f"http://www.youtube.com/watch?v=" + search_results[0]
    ydl_opts = {
        'outtmpl': 'output.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        ydl.download([url])

    await ctx.reply(video_title + "\n" + f"ID: {search_results[0]}", file=discord.File('output.mp3'))
    await asyncio.sleep(5)
    os.system("del output.mp3")

client.run("PLACEHOLDER")
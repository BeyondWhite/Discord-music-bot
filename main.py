#import libraries
import discord
import os
import time
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from keep_alive import keep_alive 

#intent
intents = discord.Intents.default()
intents.members = True
#check queue
queues = {}
def check_queue(ctx, id):
  if queues[id] !={}:
    voice = ctx.guild.voice_client
    source = queues[id].pop(0)
    voice.play(source, after=lambda x=0: check_queue(ctx, ctx.message.guild.id))

#command prefix
client = commands.Bot(command_prefix = '>', intents=intents, help_command=None)
#bot status
@client.event
async def on_ready():
  activity = discord.Game(name='Deemo')
  await client.change_presence(status=discord.Status.online, activity=activity)
  print('Log in as {0.user}'.format(client))
  print('-------------------')

#Test
@client.command(pass_context = True)
async def hi(ctx):
  embed = discord.Embed(colour = discord.Colour.magenta())
  embed.add_field(name='`Hi Im Deemo Bot`', value='『'+ ctx.author.mention +'』' , inline=True)
  await ctx.send(embed=embed)
@client.command(pass_context = True)
async def hii(ctx):
  embed = discord.Embed(colour = discord.Colour.magenta())
  embed.add_field(name='Hi Im Deemo Bot', value='\u200b' , inline=True)
  await ctx.send(embed=embed)  


#help command
@client.command(pass_context = True)
async def help(ctx):
  embed = discord.Embed(colour = discord.Colour.magenta())
  embed.set_author(name='Command prefix: >')
  embed.add_field(name='help', value='Show available commands', inline=False)
  embed.add_field(name='join', value='Deemo join voice', inline=False)
  embed.add_field(name='leave', value='Deemo leave voice', inline=False)    
  embed.add_field(name='play or p', value='Play song from youtube url or song name', inline=False)
  embed.add_field(name='queue or q', value='Queue song', inline=False)
  embed.add_field(name='pause', value='Pause song', inline=False)
  embed.add_field(name='resume', value='Resume song', inline=False)
  embed.add_field(name='skip', value='Skip to next song in queue', inline=False)
  embed.add_field(name='stop', value='Stop song', inline=False)
  embed.add_field(name='clear', value='clear message(s)', inline=False)
  embed.add_field(name='More commands will be added in the future', value='Note: ...', inline=False)

  await ctx.send(embed=embed)

#command for fun 
@client.command()
async def hello(ctx):
  await ctx.send('Hello Im Deemo Bot')

@client.command()
async def botngu(ctx):
  await ctx.send('Bot không ngu \nBạn mới ngu')

@client.command()
async def code(ctx):
  embed = discord.Embed(colour = discord.Colour.magenta())
  embed.set_image(url='https://cdn.discordapp.com/attachments/887238639812214805/902385983381712926/unknown.png')
  await ctx.send(embed=embed)

#command music
#join command
@client.command(pass_context = True)
async def join(ctx):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
      await voice.move_to(channel)
    else:
      voice = await channel.connect()      
    await ctx.send(':microphone: `Join voice`')
  else:
    await ctx.send('`You are not in a voice channel`')
#leave command 
@client.command(pass_context = True)
async def leave(ctx):
  if (ctx.voice_client):
    await ctx.guild.voice_client.disconnect()
    await ctx.send(':wave: `Leave voice`')
  else:
    await ctx.send('`Deemo is not in a voice channel`')
#play/p queue/q command
#play
@client.command(pass_context = True)
async def play(ctx, *, url):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
      await voice.move_to(channel)
    else:
      voice = await channel.connect()
  else:
    await ctx.send('`You are not in a voice channel`')
  YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'default_search':"ytsearch"}
  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  voice = get(client.voice_clients, guild=ctx.guild)
  with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      if 'entries' in info:
        url = info["entries"][0]["formats"][0]['url']
      elif 'formats' in info:
        url = info["formats"][0]['url']
  title = info.get('title')
  if title == None:
    title = info['entries'][0]['title']        
#  URL = info['url']
#  source = (FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
  source = (FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
  if voice.is_playing():
    guild_id = ctx.message.guild.id
    if guild_id in queues:
      queues[guild_id].append(source)
    else:
      queues[guild_id] = [source]

    embed_q = discord.Embed(colour = discord.Colour.magenta())
    embed_q.add_field(name='『  '+str(title) + '  』added to queue', value='『'+ctx.author.mention+'』' , inline=False)
    await ctx.send(embed=embed_q)    
  else:
#      voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
      voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
      embed_p = discord.Embed(colour = discord.Colour.magenta())
      embed_p.add_field(name=':headphones: Playing:『  ' + str(title)+' 』', value='『'+ctx.author.mention+'』' , inline=False)
      await ctx.send(embed=embed_p)
#queue 
#source = (FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
@client.command(pass_context = True)
async def queue(ctx, *, url):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
      await voice.move_to(channel)
    else:
      voice = await channel.connect()
  else:
    await ctx.send('`You are not in a voice channel`')

  YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'default_search':"ytsearch"}
  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  voice = get(client.voice_clients, guild=ctx.guild)
  with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      if 'entries' in info:
        url = info["entries"][0]["formats"][0]['url']
      elif 'formats' in info:
        url = info["formats"][0]['url']
  title = info.get('title')
  if title == None:
    title = info['entries'][0]['title']        
#  URL = info['url']
#  source = (FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
  source = (FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
  if voice.is_playing():
    guild_id = ctx.message.guild.id
    if guild_id in queues:
      queues[guild_id].append(source)
    else:
      queues[guild_id] = [source]

    embed_q = discord.Embed(colour = discord.Colour.magenta())
    embed_q.add_field(name='『  '+str(title) + '  』added to queue', value='『'+ctx.author.mention+'』' , inline=False)
    await ctx.send(embed=embed_q)    
  else:
#      voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
      voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
      embed_p = discord.Embed(colour = discord.Colour.magenta())
      embed_p.add_field(name=':headphones: Playing:『  ' + str(title)+' 』', value='『'+ctx.author.mention+'』' , inline=False)
      await ctx.send(embed=embed_p)
#q
@client.command(pass_context = True)
async def q(ctx,* , url):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
      await voice.move_to(channel)
    else:
      voice = await channel.connect()
  else:
    await ctx.send('`You are not in a voice channel`')

  YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'default_search':"ytsearch"}
  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  voice = get(client.voice_clients, guild=ctx.guild)
  with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      if 'entries' in info:
        url = info["entries"][0]["formats"][0]['url']
      elif 'formats' in info:
        url = info["formats"][0]['url']
  title = info.get('title')
  if title == None:
    title = info['entries'][0]['title']        
#  URL = info['url']
#  source = (FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
  source = (FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
  if voice.is_playing():
    guild_id = ctx.message.guild.id
    if guild_id in queues:
      queues[guild_id].append(source)
    else:
      queues[guild_id] = [source]

    embed_q = discord.Embed(colour = discord.Colour.magenta())
    embed_q.add_field(name='『  '+str(title) + '  』added to queue', value='『'+ctx.author.mention+'』' , inline=False)
    await ctx.send(embed=embed_q)    
  else:
#      voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
      voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
      embed_p = discord.Embed(colour = discord.Colour.magenta())
      embed_p.add_field(name=':headphones: Playing:『  ' + str(title)+' 』', value='『'+ctx.author.mention+'』' , inline=False)
      await ctx.send(embed=embed_p)

#p
@client.command(pass_context = True)
async def p(ctx, *, url):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
      await voice.move_to(channel)
    else:
      voice = await channel.connect()
  else:
    await ctx.send('`You are not in a voice channel`')

  YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'default_search':"ytsearch"}
  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  voice = get(client.voice_clients, guild=ctx.guild)
  with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      if 'entries' in info:
        url = info["entries"][0]["formats"][0]['url']
      elif 'formats' in info:
        url = info["formats"][0]['url']
  title = info.get('title')
  if title == None:
    title = info['entries'][0]['title']        
#  URL = info['url']
#  source = (FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
  source = (FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
  if voice.is_playing():
    guild_id = ctx.message.guild.id
    if guild_id in queues:
      queues[guild_id].append(source)
    else:
      queues[guild_id] = [source]

    embed_q = discord.Embed(colour = discord.Colour.magenta())
    embed_q.add_field(name='『  '+str(title) + '  』added to queue', value='『'+ctx.author.mention+'』' , inline=False)
    await ctx.send(embed=embed_q)    
  else:
#      voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
      voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
      embed_p = discord.Embed(colour = discord.Colour.magenta())
      embed_p.add_field(name=':headphones: Playing:『  ' + str(title)+' 』', value='『'+ctx.author.mention+'』' , inline=False)
      await ctx.send(embed=embed_p)
#pause command
@client.command(pass_context = True)
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if not (ctx.author.voice):
    await ctx.send('`You are not in voice`')
  else:  
    if voice.is_playing():
      voice.pause()
      await ctx.send(':pause_button: `Paused`')
    else:
      await ctx.send('`Currently playing no audio`')
      
      
#resume command
@client.command(pass_context = True)
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if not (ctx.author.voice):
    await ctx.send('`You are not in voice`')
  else:  
    if voice.is_paused():
      voice.resume()
      await ctx.send(':play_pause: `Resume`')
    else:
      await ctx.send("`The audio is not pause`")

#skip command
@client.command(pass_context = True)
async def skip(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if not (ctx.author.voice):
    await ctx.send('`You are not in voice`')
  else:
    if voice.is_playing():
      voice.stop()
      await ctx.send(':track_next: `Skip`')
    else:
      await ctx.send('`Currently playing no audio`')
#stop command
@client.command(pass_context = True)
async def stop(ctx):
  await ctx.guild.voice_client.disconnect()
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
      await voice.move_to(channel)
    else:
      voice = await channel.connect()   
    await ctx.send(':stop_button: `Stop playing`')
#clear command
@client.command()
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount+1)
  await ctx.send(':x: `Messages deleted`')
  time.sleep(3)
  await ctx.channel.purge(limit=1)    

keep_alive()
client.run(os.environ['TOKEN'])

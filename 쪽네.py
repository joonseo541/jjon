import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from bs4 import BeautifulSoup
import urllib
import youtube_dl
import datetime
import random
import os

client = commands.Bot(command_prefix = '쪽네야 ')
client.remove_command("help")

token = '없다'

@client.event
async def on_ready():
    print("Bot status :: online")
    latancy = client.latency
    game = discord.Game(f"'쪽네야 도움말'을 입력해주세요. | {round(latancy * 1000)}ms")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.command()
async def 핑(ctx):
    latancy = client.latency
    await ctx.send(f":ping_pong:퐁! {round(latancy * 1000)}ms")

@client.command()
async def 도움말(ctx):
    embed = discord.Embed(title=f"도움말", colour=0x2483CD)
    embed.add_field(name=f"챗(chat) 명령어", value=f"따라해, 청소, \n쪽파서버주소, 바보\n블로그검색", inline=False)
    embed.add_field(name=f"정보(Info) 명령어", value=f"핑, 내정보", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def 따라해(ctx, *, content: str):
    await ctx.send(content)

@client.command(name="청소", pass_context=True)
async def _clear(ctx, *, amount=5):
    if(ctx.author.guild_permissions.administrator):
        await ctx.message.delete()
        await ctx.channel.send('청소했어요!!')
    else:
        await ctx.send("{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author))

@client.command()
async def 내정보(ctx):
    date = datetime.datetime.utcfromtimestamp(((int(ctx.author.id) >> 22) + 1420070400000) / 1000)
    embed = discord.Embed(title=ctx.author.display_name + "님의 정보", colour=0x09EE1A)
    embed.add_field(name='이름', value=ctx.author.name, inline=False)
    embed.add_field(name='서버닉네임', value=ctx.author.display_name, inline=False)
    embed.add_field(name='가입일', value=str(date.year) + '년' + str(date.month) + '월' + str(date.day) + '일', inline=False)
    embed.add_field(name='아이디', value=ctx.author.id, inline=False)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def 쪽파서버주소(ctx):
    embed = discord.Embed(title=f"쪽파서버주소", colour=0xEE09AC)
    embed.add_field(name=f"야생서버주소", value=f"147.135.71.42:26829", inline=False)
    embed.add_field(name=f"본서버주소", value=f"joonseo541.kro.kr", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def 바보(ctx):
    await ctx.send('제가 바보라구여? 바보아니에요!!')

@client.command(name="블로그검색")
async def _search_blog(ctx, *, search_query):
    temp = 0
    url_base = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="
    url = url_base + urllib.parse.quote(search_query)
    title = ["", "", "", "", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
    link = ["", "", "", "", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    result = soup.find_all('a', "sh_blog_title _sp_each_url _sp_each_title")
    embed = discord.Embed(title="검색 결과", description=" ", color=0x00ff56)
    for n in result:
        if temp == 5: # 더 많은 검색 : 숫자(3)를 늘리셔야 합니다.
            break
        title[temp] = n.get("title")
        link[temp] = n.get("href")
        embed.add_field(name=title[temp], value=link[temp], inline=False)
        temp+=1
    embed.set_footer(text="검색 완료!")
    await ctx.send(embed=embed)

@client.command(name="뮤트", pass_context=True)
async def _mute(ctx, member: discord.Member=None):
    if(ctx.author.guild_permissions.administrator):
        member = member or ctx.message.author
        await member.add_roles(get(ctx.guild.roles, name="뮤트"))
        await ctx.channel.send(str(member)+"에게 입을 막았습니다.")
    else:
        await ctx.send("{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author))

@client.command(name="언뮤트", pass_context=True)
async def _unmute(ctx, member: discord.Member=None):
    if(ctx.author.guild_permissions.administrator):
        member = member or ctx.message.author
        await member.remove_roles(get(ctx.guild.roles, name='뮤트'))
        await ctx.send(str(member)+"의 입을 풀었습니다.")
    else:
        await ctx.send("{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author))

@client.command(name="로드")
async def load_commands(ctx, extension):
    if(ctx.author.guild_permissions.administrator):
        client.load_extension(f"Cogs.{extension}")
        await ctx.send(f":white_check_mark: {extension}을(를) 로드했습니다!")
    else:
        await ctx.send("{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author))

@client.command(name="언로드")
async def unload_commands(ctx, extension):
    if(ctx.author.guild_permissions.administrator):
        client.unload_extension(f"Cogs.{extension}")
        await ctx.send(f":white_check_mark: {extension}을(를) 언로드했습니다!")
    else:
        await ctx.send("{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author))

@client.command(name="리로드")
async def reload_commands(ctx, extension=None):
    if(ctx.author.guild_permissions.administrator):
        if extension is None:
            for filename in os.listdir("Cogs"):
                if filename.endswith(".py"):
                    client.unload_extension(f"Cogs.{filename[:-3]}")
                    client.load_extension(f"Cogs.{filename[:-3]}")
                    await ctx.send(":white_check_mark: 모든 명령어를 다시 불러왔습니다!")
        else:
            client.unload_extension(f"Cogs.{extension}")
            client.load_extension(f"Cogs.{extension}")
            await ctx.send(f":white_check_mark: {extension}을(를) 다시 불러왔습니다!")
    else:
        await ctx.send("{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author))

client.run(token)

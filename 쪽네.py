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

bot = commands.Bot(command_prefix = '쪽네야 ')

@bot.event
async def on_ready():
    print("Bot status :: online")
    latancy = bot.latency
    game = discord.Game(f"'쪽네야 도움말'을 입력해주세요. | {round(latancy * 1000)}ms")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def 핑(ctx):
    latancy = bot.latency
    await ctx.send(f":ping_pong:퐁! {round(latancy * 1000)}ms")

@bot.command()
async def 도움말(ctx):
    embed = discord.Embed(title=f"도움말", colour=0x2483CD)
    embed.add_field(name=f"챗(chat) 명령어", value=f"따라해, 청소, \n쪽파서버주소, 바보\n블로그검색", inline=False)
    embed.add_field(name=f"정보(Info) 명령어", value=f"핑, 내정보", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def 따라해(ctx, *, content: str):
    await ctx.send(content)

@bot.command(name="청소", pass_context=True)
async def _clear(ctx, *, amount=5):
    await ctx.channel.send(limit=amount)
    await ctx.send("청소하였어요!")

@bot.command()
async def 내정보(ctx):
    date = datetime.datetime.utcfromtimestamp(((int(ctx.author.id) >> 22) + 1420070400000) / 1000)
    embed = discord.Embed(title=ctx.author.display_name + "님의 정보", colour=0x09EE1A)
    embed.add_field(name='이름', value=ctx.author.name, inline=False)
    embed.add_field(name='서버닉네임', value=ctx.author.display_name, inline=False)
    embed.add_field(name='가입일', value=str(date.year) + '년' + str(date.month) + '월' + str(date.day) + '일', inline=False)
    embed.add_field(name='아이디', value=ctx.author.id, inline=False)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def 쪽파서버주소(ctx):
    embed = discord.Embed(title=f"쪽파서버주소", colour=0xEE09AC)
    embed.add_field(name=f"야생서버주소", value=f"147.135.71.42:26829", inline=False)
    embed.add_field(name=f"본서버주소", value=f"joonseo541.kro.kr", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def 바보(ctx):
    await ctx.send('제가 바보라구여? 바보아니에요!!')

@bot.command(name="블로그검색")
async def _search_blog(ctx, *, search_query):
    temp = 0
    url_base = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="
    url = url_base + urllib.parse.quote(search_query)
    title = ["", "", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
    link = ["", "", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    result = soup.find_all('a', "sh_blog_title _sp_each_url _sp_each_title")
    embed = discord.Embed(title="검색 결과", description=" ", color=0x00ff56)
    for n in result:
        if temp == 3: # 더 많은 검색 : 숫자(3)를 늘리셔야 합니다.
            break
        title[temp] = n.get("title")
        link[temp] = n.get("href")
        embed.add_field(name=title[temp], value=link[temp], inline=False)
        temp+=1
    embed.set_footer(text="검색 완료!")
    await ctx.send(embed=embed)

bot.run(os.environ['token'])
import discord
from discord.ext import commands

class Core(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def 기다려(self, ctx):
        await ctx.send('시러여')

def setup(client):
    client.add_cog(Core(client))
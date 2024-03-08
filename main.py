import discord
import dotenv
import os
from user import User

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

bot = discord.Bot()

@bot.slash_command(name="ping", description="Tells you the bot latency")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"Pong! Latency is {bot.latency}")

@bot.slash_command(name="profile", description="Shows your profile")
async def profile(ctx: discord.ApplicationContext):
    user = User(ctx.user.id, ctx.user.name)
    await ctx.respond(embed=user.getUserEmbed())
        
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online")


cogs_list = [
    'blackjack',
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')
bot.run(token)
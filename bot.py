# bot.py
import os
import random
from discord import channel
import yfinance as yf
from discord.ext import commands
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='@!')

# @bot.command(name="ok")
# async def hello(ctx):
#     button=Button(label="Click me!", style=discord.ButtonStyle.green,)
#     view=View()
#     view.add_item(button)
#     await ctx.send("Hi!", view=view)

top_stock_companies = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN', 'FB', 'BRK-B', 'SPY',
                       'BABA', 'JPM', 'WMT', 'V', 'T', 'UNH', 'PFE', 'INTC', 'VZ', 'ORCL','RELIANCE.NS']

stocks = {"RELIANCE":"Reliance Industries Ltd(L)", "ADANIPORTS":"Adani Ports and Special Economic Zone Ltd(L)", "ITC":"ITC Ltd(L)"}

if not os.path.exists("images"):
    os.mkdir("images")

@bot.command(name='99',help='Aese hee sexy lag raha tha')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name="get-list", help="Check list of companies for which stock details can be fetched.")
async def get_list(ctx):
    for key, value in stocks.items():
        # await ctx.send(key)
        # await ctx.send(value)

        await ctx.send(' {} : {}'.format(key, value))
# @bot.command(name='roll_dice', help='Simulates rolling dice.')
# async def roll(ctx, number_of_dice: int, number_of_sides: int):
#     dice = [
#         str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)
        
#     ]
#     await ctx.send(', '.join(dice))

# @bot.command(name='create-channel')
# @commands.has_role('admin')
# async def create_channel(ctx, channel_name='real-python'):
#     guild = ctx.guild
#     existing_channel = discord.utils.get(guild.channels, name=channel_name)
#     if not existing_channel:
#         print(f'Creating a new channel: {channel_name}')
#         await guild.create_text_channel(channel_name)
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.errors.CheckFailure):
#         await ctx.send('You do not have the correct role for this command.')

@bot.command(name='stock', help='Enter the name of the company')
async def stock(ctx,stock_name):
    msft = yf.Ticker(stock_name)
    embed=discord.Embed(title=msft.info['longName'], url=msft.info['website'], description="For now just description", color=0xFF5733)
    embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=msft.info['logo_url'])
    embed.add_field(name="Country", value=msft.info['country'], inline=True)
    embed.add_field(name="Sector", value=msft.info['sector'], inline=True)
    embed.set_footer(text="Phone no: {}".format(msft.info['phone']))
    await ctx.send(embed=embed)




# @bot.command()
# async def embed(ctx):
#     embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
#     embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
#     await ctx.send(embed=embed)

@bot.command(name="prev-stock-data", help="Check previous day stock data of a company.")
async def stock_data(ctx, stock_company):

    if stock_company in top_stock_companies:
        stock_company_df = yf.download(stock_company, period="2d")
        msg = create_msg(stock_company, stock_company_df)

        stock_company_df = yf.download(
            stock_company, period="2d", interval="1m")
        stock_company_df[0:390].plot(y='Close', linewidth=0.85)

        plt.xlabel('Datetime')
        plt.ylabel('Close')
        plt.title('Stock prices of {company} for previous day'.format(
            company=stock_company))

        plt.savefig('images/stock_previous_day.png')

        await ctx.send(msg, file=discord.File('images/stock_previous_day.png'))

        os.remove('images/stock_previous_day.png')
    else:
        await ctx.send("Stock data for {stockCompany} doesn't exist!".format(stockCompany=stock_company))  


def create_msg(top_stock_company, top_stock_company_df):
    date = str(top_stock_company_df.head(1).index[0]).split(' ')[0]
    msg = '''\
        {company} EOF Data
        - Date: {Date}
        - Open: {Open}
        - High: {High}
        - Low: {Low}
        - Close: {Close}
        - Adj Close: {Adj_Close}
        - Volume: {Volume}\
     '''.format(company=top_stock_company, Date=date, Open=top_stock_company_df.iat[0, 0], High=top_stock_company_df.iat[0, 1], Low=top_stock_company_df.iat[0, 2], Close=top_stock_company_df.iat[0, 3], Adj_Close=top_stock_company_df.iat[0, 4], Volume=top_stock_company_df.iat[0, 5])

    return msg      
bot.run(TOKEN)
# bot.py
import os
import random
import yfinance as yf
from discord.ext import commands
from dotenv import load_dotenv
import matplotlib.pyplot as plt

import discord



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='@!')

stocks = {"RELIANCE":"Reliance Industries Ltd(L)", "ADANIPORTS":"Adani Ports and Special Economic Zone Ltd(L)", "ITC":"ITC Ltd(L)"}


# @bot.command(name='99',help='Aese hee sexy lag raha tha')
# async def nine_nine(ctx):
#     brooklyn_99_quotes = [
#         'I\'m the human form of the 💯 emoji.',
#         'Bingpot!',
#         (
#             'Cool. Cool cool cool cool cool cool cool, '
#             'no doubt no doubt no doubt no doubt.'
#         ),
#     ]

#     response = random.choice(brooklyn_99_quotes)
#     await ctx.send(response)

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

# @bot.command(name='stock', help='Enter the name of the company')
# async def stock(ctx,stock_name: str):
#     msft = yf.Ticker(stock_name)
#     await ctx.send(msft.info['zip'])
# bot.run(TOKEN)

df = None
df_not_none = False
count = 0
random_company = ''
nrows = 0

if not os.path.exists("images"):
    os.mkdir("images")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="get-list", help="Check list of companies for which stock details can be fetched.")
async def get_list(ctx):
   
 
    for key, value in stocks.items():
        # await ctx.send(key)
        # await ctx.send(value)

        await ctx.send(' {} : {}'.format(key, value))

@bot.command(name="prev-stock-data", help="Check previous day stock data of a company.")
async def stock_data(ctx, stock_company):

    if stock_company in stocks.keys:
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


def create_msg(stocks, stocks_df):
    date = str(stocks_df.head(1).index[0]).split(' ')[0]
    msg = '''\
        {company} EOF Data
        - Date: {Date}
        - Open: {Open}
        - High: {High}
        - Low: {Low}
        - Close: {Close}
        - Adj Close: {Adj_Close}
        - Volume: {Volume}\
     '''.format(company=stocks, Date=date, Open=stocks_df.iat[0, 0], High=stocks_df.iat[0, 1], Low=stocks_df.iat[0, 2], Close=stocks_df.iat[0, 3], Adj_Close=stocks_df.iat[0, 4], Volume=stocks_df.iat[0, 5])

    return msg      

bot.run(TOKEN)


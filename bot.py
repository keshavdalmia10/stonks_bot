# bot.py
import os
import random
from discord import emoji,channel
import yfinance as yf
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import discord
import plotly.graph_objects as go
import pandas as pd




load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()



bot = commands.Bot(command_prefix='@!',intents=intents)


top_stock_companies = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN', 'FB', 'BRK-B', 'SPY',
                       'BABA', 'JPM', 'WMT', 'V', 'T', 'UNH', 'PFE', 'INTC', 'VZ', 'ORCL','RELIANCE.NS']

stocks = {"RELIANCE":"Reliance Industries Ltd(L)", "ADANIPORTS":"Adani Ports and Special Economic Zone Ltd(L)", "ITC":"ITC Ltd(L)"}

if not os.path.exists("images"):
    os.mkdir("images")


@bot.command(name="get-list", help="Check list of companies for which stock details can be fetched.")
async def get_list(ctx):
    list=""
    for key, value in stocks.items():
        temp='🔹 {} : {}\n'.format(key, value)
        list+=temp
    embed=discord.Embed(title="List of Companies", description=list, color=0x57FF33)
    await ctx.send(embed=embed)

@bot.command(name='dailystats', help='Provides daily stats')
async def get_list(ctx):
    d=[':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:',':nine:']
    html_text=requests.get('https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php').text
    soup= BeautifulSoup(html_text,'lxml')
    top_table=soup.find('div', class_='bsr_table hist_tbl_hm')
    comp_table=top_table.find('tbody')
    comp_rows=comp_table.find('tr')
    embedgain=discord.Embed(title='Top Gainers', color=0xFF5733)
    embedlose=discord.Embed(title='Top Losers', color=0xFF5733)
    for i in range(5):
        namee=comp_rows.td.span.h3.a.text
        high=comp_rows.next_element.next_element.next_sibling.next_sibling
        low=high.next_sibling.next_element
        last_price=low.next_sibling.next_element
        prev_close=last_price.next_sibling.next_element
        change=prev_close.next_sibling.next_element
        gain=change.next_sibling.next_element
        embedgain.add_field(name='{} {}- `{}`**%**'.format(d[i],namee,gain.text), value="*High*-{}\n*Low*-{} \n*Last price*-{}\n*Prevclose*-{}  *Change*-{} ".format(high.text,low.text,last_price.text,prev_close.text,change.text), inline=False)
        comp_rows=comp_rows.next_sibling.next_element

    html_text2=requests.get('https://www.moneycontrol.com/stocks/marketstats/nseloser/index.php').text
    soup2= BeautifulSoup(html_text2,'lxml')
    top_table2=soup2.find('div', class_='bsr_table hist_tbl_hm')
    comp_table2=top_table2.find('tbody')
    comp_rows2=comp_table2.find('tr')
    for i in range(5):
        namee=comp_rows2.td.span.h3.a.text
        high=comp_rows2.next_element.next_element.next_sibling.next_sibling
        low=high.next_sibling.next_element
        last_price=low.next_sibling.next_element
        prev_close=last_price.next_sibling.next_element
        change=prev_close.next_sibling.next_element
        gain=change.next_sibling.next_element    
        embedlose.add_field(name='{} {}- `{}`**%**'.format(d[i],namee,gain.text), value="*High*-{}\n*Low*-{} \n*Last price*-{}\n*Prevclose*-{}  *Change*-{} ".format(high.text,low.text,last_price.text,prev_close.text,change.text), inline=False)
        comp_rows2=comp_rows2.next_sibling.next_element
    button1=Button(label="Top Gainers", style=discord.ButtonStyle.green,emoji="🔺")  
    button2=Button(label="Top Losers", style=discord.ButtonStyle.green,emoji="🔻")
    async def button_callback(interaction):
        await interaction.response.edit_message(embed=embedgain, view=view)
    button1.callback=button_callback
    async def button_callback(interaction):
        await interaction.response.edit_message(embed=embedlose, view=view)
    button2.callback=button_callback
    view=View()
    view.add_item(button1)
    view.add_item(button2)
    await ctx.send(embed=embedgain,view=view)



@bot.command(name='stock', help='Enter the name of the company')
async def stock(ctx,stock_name):
    stock_name=stock_name+".NS"
    msft = yf.Ticker(stock_name)
    embed1=discord.Embed(title=msft.info['longName'], url=msft.info['website'], color=0xFF5733)
    embed1.add_field(name="Previous Close", value=msft.info['previousClose'], inline=True)
    embed1.add_field(name="Open", value=msft.info['open'], inline=True)
    cap=format(msft.info['marketCap']/1000000000000, ".3f")
    embed1.add_field(name="Market Cap", value="{}T".format(cap), inline=True)
    embed1.add_field(name="Bid", value=msft.info['bid'], inline=True)
    embed1.add_field(name="Beta", value=format(msft.info['beta'],".2f"), inline=True)
    embed1.add_field(name="PE Ratio", value=format(msft.info['trailingPE'],".2f"), inline=True)
    embed1.add_field(name="EPS", value=format(msft.info['trailingEps'],".2f"), inline=True)
    embed1.add_field(name="Ask", value=msft.info['ask'], inline=True)
    embed1.add_field(name="Day's Range", value="{} - {}".format(msft.info['dayLow'],msft.info['dayHigh']), inline=False)
    embed1.add_field(name="52 week Range", value="{} - {}".format(msft.info['fiftyTwoWeekLow'],msft.info['fiftyTwoWeekHigh']), inline=False)
    embed1.add_field(name="Forward Dividend & Yield", value="{}({}%)".format(msft.info['dividendRate'],msft.info['dividendYield']*100), inline=False)
    embed1.add_field(name="Volume", value="{:,}".format(msft.info['volume']), inline=True)
    embed1.add_field(name="Ex-Dividend Date", value=msft.info['exDividendDate'], inline=True)
    embed1.add_field(name="Avg. Volume", value="{:,}".format(msft.info['averageVolume']), inline=True)
    embed1.add_field(name="1y Target Est", value=msft.info['targetMeanPrice'], inline=True)
    embed3=discord.Embed(title=msft.info['longName'], url=msft.info['website'], color=0xFF5733)
    # embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", author=ctx.author.avatar_url)
    embed3.set_thumbnail(url=msft.info['logo_url'])
    embed3.add_field(name="Sector", value=msft.info['sector'], inline=True)
    embed3.add_field(name="Industry", value=msft.info['industry'], inline=True)
    embed3.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    embed2=discord.Embed(title=msft.news[0]['title'], url=msft.news[0]['link'], description="Publisher: {}".format(msft.news[0]['publisher']), color=0xFF5733)
    for i in range (2,6):
        embed2.add_field(name=msft.news[i]['title'], value="Publisher: {}".format(msft.news[0]['publisher']), inline=False)
    button1=Button(label="Analytics", style=discord.ButtonStyle.green,emoji="📊")
    button2=Button(label="News", style=discord.ButtonStyle.green,emoji="📰")
    button3=Button(label="About", style=discord.ButtonStyle.green,emoji="👁‍🗨")
    async def button_callback(interaction):
        await interaction.response.edit_message(embed=embed1, view=view)
    button1.callback=button_callback
    async def button_callback(interaction):
        await interaction.response.edit_message(embed=embed2, view=view)
    button2.callback=button_callback
    async def button_callback(interaction):
        await interaction.response.edit_message(embed=embed3, view=view)
    button3.callback=button_callback
    
    view=View()
    
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    
    await ctx.send(embed=embed1,view=view)

@bot.command(name='chart', help='Enter the name of the company')
async def stock_data(ctx, stock_company):
    stock = yf.Ticker('TSLA')
    data = stock.history(period="100d")
    data.to_csv('yahoo.csv')

    df = pd.read_csv('yahoo.csv')
    candlestick = go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])
    fig = go.Figure(data=[candlestick])
    fig.write_image("images/yourfile.png") 

    await ctx.send(file=discord.File('images/yourfile.png'))
    os.remove('images/yourfile.png')




@bot.command(name='tanmay')
async def tanmay(ctx):
    embed=discord.Embed(title="Title", description="For now just description", color=0xFF5733)
    embed2=discord.Embed(title="EMBED 2", description="THIS IS EMBED 2", color=0x5733FF)
    button=Button(label="Click me!", style=discord.ButtonStyle.green, emoji="😊" )
    async def button_callback(interaction):
        await interaction.response.edit_message(content="You clicked",embed=embed2, view=None)
    button.callback=button_callback
    view = View()
    view.add_item(button)
    await ctx.send("Hi!",embed=embed, view=view)
    

    
@bot.command(name='ipo')
async def tanmay(ctx):
    list=""
    ipohtml_text=requests.get('https://zerodha.com/ipo/').text
    iposoup= BeautifulSoup(ipohtml_text,'lxml')
    iposection=iposoup.find('section', id='ipo')
    upcoming_ipo_talbe = iposection.find('tbody')
    n=len(upcoming_ipo_talbe.find_all("tr")) # no.of upcoming IPOs
    iporow=upcoming_ipo_talbe.find('tr')
    for i in range (n):
        stock=iporow.td
        date=stock.next_sibling.next_element                             #IPO date
        listing_date=date.next_sibling.next_element                      #listing date
        price_range=listing_date.next_sibling.next_element               #price range
        min_qnt=price_range.next_sibling.next_element                    #min quantity  
        rhp_link=min_qnt.next_sibling.next_element.find('a').get('href')
        temp="🔹 **{}** : {}\n".format(stock.text.lstrip().rstrip(), "[RHP]"+"("+rhp_link+")")
        list+=temp
        iporow=iporow.next_sibling.next_element
    ipoembed=discord.Embed(title="Upcoming IPOs", description=list, color=0xFF5733)
    view = View()
    await ctx.send(embed=ipoembed, view=view)
   



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




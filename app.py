import discord
import os
import json
import random
import urllib.parse
import requests
from dotenv import load_dotenv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

load_dotenv()
TOKEN = os.getenv('TOKEN')
client = discord.Client()

#API to extract COVID data based on user input
def covidtracker(country):
	link="https://covid-19.dataflowkit.com/v1/"+country
	covid=requests.get(link)
	data=covid.json()
	activecases=data['Active Cases_text']
	namecountry=data['Country_text']
	lastupdate=data['Last Update']
	newcases=data['New Cases_text']
	newdeaths=data['New Deaths_text']
	totalcases=data['Total Cases_text']
	totaldeaths=data['Total Deaths_text']
	totalrecovered=data['Total Recovered_text']
	if (newcases=="" and newdeaths==""):
		newcases="Not yet updated"
		newdeaths="Not yet updated"
	covidresult= "Country: "+namecountry+".\n"+"Last Update: "+lastupdate+".\n"+"Active Cases: "+activecases+".\n"+"Total Cases: "+totalcases+".\n"+"New Cases: "+newcases+".\n"+"Total Deaths: "+totaldeaths+".\n"+"New Deaths: "+newdeaths+".\n"+"Total Recovered: "+totalrecovered+"."
	return covidresult

#web scraping module to extract last updated spreadsheet from school website
def lastemploi():
	links=[]
	url = "https://ensaf.ac.ma/?controller=pages&action=emplois"
	req = Request(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'})
	var1=urlopen(req)
	rawhtml=var1.read()
	scrape=soup(rawhtml,'lxml')
	info=scrape.find('div',class_='table-responsive')
	test=info.tbody
	auto=test.tr
	module=auto.select_one("tr td:nth-of-type(3)")
	for link in module.find_all('a'):
		autourl=link.get('href')
	links.append(autourl)
	return links[-1]

#API for math equations

def mathcalculator(parse):
	link="http://api.mathjs.org/v4/?expr="+parse
	results=requests.get(link)
	data=results.json()
	calcul="Le resultat du calcul est "+str(data)
	return calcul

#API for weather data
def get_weather(City):
	link="http://api.openweathermap.org/data/2.5/weather?q="+str(City)+"&appid="+apikey+"&units=metric"
	weather=requests.get(link)
	data=weather.json()
	main=data['main']
	temperature=main['temp']
	humid=main['humidity']
	wind=data ['wind']
	speed=wind['speed']
	celsius= "La température est de "+ str(temperature)+""
	return celsius
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
def check(author):
	def inner_check(message):
		return message.author==author
	return inner_check
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('temp'):
    	await message.channel.send("Which city?")
    	msg= await client.wait_for('message',timeout=30)
    	City=msg.content
    	celsius=get_weather(City)
    	await message.channel.send(str(City)+": "+str(celsius))

    if message.content.startswith('calcul'):
    	await message.channel.send("write op")
    	expr= await client.wait_for('message',timeout=45)
    	equation=expr.content
    	print(equation)
    	parse=urllib.parse.quote(equation,safe='')
    	print(parse)
    	calcul=mathcalculator(parse)
    	await message.channel.send(calcul)

    if message.content.startswith('$covid'):
    	await message.channel.send("Which Country?")
    	msg2= await client.wait_for('message',timeout=30)
    	country=msg2.content
    	covid=covidtracker(country)
    	await message.channel.send(covid)

    if message.content.startswith('$emploi'):
    	lien= lastemploi()
    	await message.channel.send(lien)

client.run(TOKEN)

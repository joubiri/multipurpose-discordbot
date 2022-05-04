import discord
import os
import json
import random
import urllib.parse
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
client = discord.Client()

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

def mathcalculator(parse):
	link="http://api.mathjs.org/v4/?expr="+parse
	results=requests.get(link)
	data=results.json()
	calcul="Le resultat du calcul est "+str(data)
	return calcul

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
client.run(TOKEN)

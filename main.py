import discord
from flask import Flask
from dotenv import load_dotenv
import os
import json
import requests 
import http.server
import socketserver
#starts a webserver so that repl.it keeps it online 
import flaskwebsvr

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot = discord.Client()


@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name="!q username"))
  guild_count = 0
  for guild in bot.guilds:
    print(f"- {guild.id} (name: {guild.name})")
    guild_count = guild_count + 1
  print("speedrunapiBot is in " + str(guild_count) + " guilds.")


@bot.event
async def on_message(message):
  

  
  if message.content[:3] == "!q " :
    m=str()


    try:
      urel=str(("https://www.speedrun.com/api/v1/users?lookup=" + message.content[3:]))
      response = requests.get(urel) 
      #print(urel)
      json_data = json.loads(response.text)
      usrurel = json_data.get("data")[0].get("links")[1].get("uri")

      
      


      usrid=str(json_data.get("data")[0].get("id"))
      rsps2=requests.get(usrurel)
      usrdata=json.loads(rsps2.text)
      #print(rsps2.text)
      print(usrid)
      e=0
      w=0
      v=0
      for i in usrdata.get("data"):
        
        if usrdata.get("data")[e].get("status").get("status")=="verified":
          v=v+1
          #print("verified!")
          ldrbrd=requests.get(usrdata.get("data")[e].get("links")[2].get("uri"))
          ldbrdd=json.loads(ldrbrd.text)
          try:
            ldr=requests.get(ldbrdd.get("data").get("links")[5].get("uri"))
            ldrj=json.loads(ldr.text)
            #print(usrid)
            #print(ldrj.get("data").get("runs")[0].get("run").get("players")[0].get("id"))
            if usrid==ldrj.get("data").get("runs")[0].get("run").get("players")[0].get("id"):
              #print("wr")
              w=w+1
          except:
            pass
        e=e+1

      tstri=str(json_data.get("data")[0].get("names").get("international")+ "'s profile")

      #m=m+"Username:"+json_data.get("data")[0].get("names").get("international")+"\n"
      #m=m+"User Id: "+str(json_data.get("data")[0].get("id"))+"\n"
      #m=m+"User Signup Date: "+str(json_data.get("data")[0].get("signup"))[:-10]+"\n"
      #m=m+"Total Runs: " + str(e) + "\n"
      #m=m+"World Records: " + str(w) + "\n"
      #m=m+"Verified Runs: " + str(v) + "\n"
      #m=m+"Profile Link: https://www.speedrun.com/user/"+json_data.get("data")[0].get("names").get("international")+"\n"
      lnk=str("https://www.speedrun.com/user/"+json_data.get("data")[0].get("names").get("international"))
      embedVar = discord.Embed(title=tstri, color=0x386b39)
      embedVar.add_field(name="User ID: ", value=str(json_data.get("data")[0].get("id")), inline=False)
      embedVar.add_field(name="User Signup Date: ", value=str(json_data.get("data")[0].get("signup"))[:-10], inline=False)
      embedVar.add_field(name="Total Runs:", value=str(e), inline=False)
      embedVar.add_field(name="World Record Runs: ", value= str(w), inline=False)
      embedVar.add_field(name="Verified Runs: ", value=str(v), inline=False)
      embedVar.add_field(name="Profile Link: ", value=lnk, inline=False)
      await message.channel.send(embed=embedVar)
    
      #n = (json_data["data"])
      #await message.channel.send(m)
    except:
      print("failed")
    


bot.run(DISCORD_TOKEN)



PORT = 8600

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("Server started at localhost:" + str(PORT))
    httpd.serve_forever()
    pass

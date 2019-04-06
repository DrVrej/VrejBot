import discord
import sys
import os
from random import randint

bot = discord.Client()
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# https://discordpy.readthedocs.io/en/rewrite/api.html

@bot.event
async def on_member_join(member)
	print(member)
	print(member.id)
	for channel in member.server.channels:
		if str(channel) == "bot-log":
			await channel.send("```Member status: " + str(member.status))

@bot.event
async def on_message(message):
    # Sharnag e, minag yete as bot-e tag yegher e!
    m_org = message.content # Original message
    m = m_org # The one that will be edited
    botTagged = False # Yete robot-e, tag yegher e, sharnage
    for v in message.mentions: # Nayir amen martignere vor tag yegher en
        if v == bot.user: # Yete robotne, gerna sharnagel
            botTagged = True
        m = m.replace("<@" + str(v.id) + ">","").strip() # serpe martigneroon anoonere
    if botTagged == False:
        return
    
    print("-----------------------------")
    print("Author: " + str(message.author))
    
    try:
        print("Message Arrived: " + m) # Make sure it's a unreconginzed letter
        m = m.lower()
    except UnicodeEncodeError:
        m = m.translate(non_bmp_map)
        print("unreconginzed Message Arrived: " + m)

    # Yete yes em, mi sharnager!
    if message.author == bot.user: return
    
    if m == "": await message.channel.send("You didn't type anything! :thinking: :angry:"); return
    
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    if vj_Match_Start(m,["hello", "hi", "greetings", "allo"]) == True: await message.channel.send(vj_PickRandom(["Hello!", "Hi!", "Greetings!", "Allo!"])); return
    if vj_Match_Start(m,["how are you", "how you doing", "are you good"]) == True: await message.channel.send(vj_PickRandom(["I am good! You?", "I am doing great! how about you?", "Good, you?"])); return
    
    if vj_Match_Any(m,["cookie", "$cookkie"]) == True: await message.channel.send(":cookie:"); return
    if vj_Match_Any(m,["armenia", "hayastan", "armo"]) == True: await message.channel.send(":flag_am:"); return
    if vj_Match_Any(m,["gay"]) == True: await message.channel.send(":rainbow_flag:"); return

    # Yete pame chi hasgena:
    await message.channel.send("I don't recognize your message! Sorry :frowning:")

def vj_PickRandom(tbl):
    if isinstance(tbl, list):
        return tbl[randint(0,len(tbl)-1)]
    return tbl

def vj_Match_Start(item,a):
    for v in a:
        if item.startswith(str(v)):
            return True
    return False

def vj_Match_Any(item,a):
    for v in a:
        if item.find(v) != -1:
            return True
    return False

#kakhni_tive = #open("kakhni_tive.txt", "r")
bot.run(os.environ["KAKHNI_TIVE"])
import discord
import sys
import os
from random import randint
from boto.s3.connection import S3Connection

client = discord.Client()
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# Garevor namagner:
hello_a = ["hello", "hi", "greetings", "allo"]
hello = ["Hello!", "Hi!", "Greetings!", "Allo!"]
good_a = ["how are you", "how you doing", "are you good"]
good = ["I am good! You?", "I am doing great! how about you?", "Good, you?"]

# https://discordpy.readthedocs.io/en/rewrite/api.html
@client.event
async def on_message(message):
    print("-----------------------------")
    print("Author: " + str(message.author))

    # Sharnag e, minag yete as bot-e tag yegher e!
    m_org = message.content # Original message
    m = m_org # The one that will be edited
    botTagged = False # Yete robot-e, tag yegher e, sharnage
    for v in message.mentions: # Nayir amen martignere vor tag yegher en
        if v == client.user: # Yete robotne, gerna sharnagel
            botTagged = True
        m = m.replace("<@" + str(v.id) + ">","").strip() # serpe martigneroon anoonere
    if botTagged == False:
        return
    
    try:
        print("Message Arrived: " + m) # Make sure it's a unreconginzed letter
        m = m.lower()
    except UnicodeEncodeError:
        m = m.translate(non_bmp_map)
        print("unreconginzed Message Arrived: " + m)

    # Yete yes em, mi sharnager!
    if message.author == client.user: return
    
    if m == "": await message.channel.send("You didn't type anything! :thinking: :angry:"); return
    
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    if vj_Match_Start(m,hello_a) == True: await message.channel.send(hello[randint(0,len(hello)-1)]); return
    if vj_Match_Start(m,good_a) == True: await message.channel.send(good[randint(0,len(good)-1)]); return
    
    if vj_Match_Any(m,["cookie"]) == True: await message.channel.send(":cookie:"); return
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

kakhni_tive = S3Connection(os.environ['KAKHNI_TIVE']) #open("kakhni_tive.txt", "r"
print(kakhni_tive)
client.run(kakhni_tive.readline())

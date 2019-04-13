import discord
import sys
import os
from random import randint

bot = discord.Client()
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# https://discordpy.readthedocs.io/en/rewrite/api.html

@bot.event
async def on_member_join(member):
	#print(member.avatar_url)
	#print(member.color)
	for channel in member.guild.channels:
		if str(channel) == "bot-log":
			await channel.send(":inbox_tray: **MEMBER JOINED** [*" + str(member.joined_at) + "*]\n:busts_in_silhouette: `Name: " + str(member) + " [ID: " + str(member.id) + "]`\n:tools: `Account Created: " + str(member.created_at) + "`\n:iphone: `On Mobile: " + str(member.is_on_mobile()) + "`\n:trophy: `Highest Rank: " + str(member.top_role) + "`")

@bot.event
async def on_message(message):
    # Sharnag e, minag yete as bot-e tag yegher e!
    m_org = message.content # Original message
    m = m_org # The one that will be edited
    botTagged = False # Yete robot-e, tag yegher e, sharnage
    
    # Oknagan hramaner:
    mh = m_org.strip() # Asiga minag hramaneroun hamar bidi kordzadzvi!
    for v in message.mentions: # Nayir amen martignere vor tag yegher en
        mh = mh.replace("<@" + str(v.id) + ">","").strip() # serpe martigneroon anoonere
    if vj_Match_Exact(mh,["-help"]) == True: await message.channel.send("```ini\n[-sg | -steam] = Steam Group\n[-i | -invite] = Discord Server\n[-vjbase | -vjb | -vj] = VJ Base Workshop Page\n[-vjof | -vjunof | -vjcol | -vjcollection] = VJ Base Official and Unofficial Addons\n[-server | -sfiles] = DrVrej's Server Files\n[-im] = Broken / Incompatible Addons\n```"); return
    if vj_Match_Exact(mh,["-sg", "-steam"]) == True: await message.channel.send("Steam Group: https://steamcommunity.com/groups/vrejgaming"); return
    if vj_Match_Exact(mh,["-i", "-invite"]) == True: await message.channel.send("Discord Invite: https://discordapp.com/invite/zwQjrdG"); return
    if vj_Match_Exact(mh,["-vjbase", "-vjb", "-vj"]) == True: await message.channel.send("VJ Base Workshop Page: https://steamcommunity.com/sharedfiles/filedetails/?id=131759821"); return
    if vj_Match_Exact(mh,["-vjof", "-vjunof", "-vjcol", "-vjcollection"]) == True: await message.channel.send("VJ Base Official and Unofficial Addons: https://steamcommunity.com/sharedfiles/filedetails/?id=1080924955"); return
    if vj_Match_Exact(mh,["-server", "-sfiles"]) == True: await message.channel.send("DrVrej's Server Files: https://steamcommunity.com/sharedfiles/filedetails/?id=157267702"); return
    if vj_Match_Exact(mh,["-im"]) == True: await message.channel.send("Broken / Incompatible Addons: https://steamcommunity.com/sharedfiles/filedetails/?id=1129493108"); return
    
    for v in message.mentions: # Nayir amen martignere vor tag yegher en
        if v == bot.user: # Yete robotne, gerna sharnagel
            botTagged = True
        m = m.replace("<@" + str(v.id) + ">","").strip() # serpe martigneroon anoonere
    if botTagged == False:
        return

    print("-----------------------------")
    print("Author: " + str(message.author))
    
    try:
        print("Message Arrived: " + m) # Make sure it's a unrecognized letter
        m = m.lower()
    except UnicodeEncodeError:
        m = m.translate(non_bmp_map)
        print("unrecognized Message Arrived: " + m)

    # Yete yes em, mi sharnager!
    if message.author == bot.user: return
    
    if m == "": await message.channel.send("You didn't type anything! :thinking: :angry:"); return
    
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    async def vj_PrintMessage(s):
        await message.channel.send("<@" + str(message.author.id) + "> " + s)
    
    if vj_Match_Start(m,["hello", "hi", "greetings", "allo"]) == True: await vj_PrintMessage(vj_PickRandom(["Hello!", "Hi!", "Greetings!", "Allo!"])); return
    if vj_Match_Start(m,["how are you", "how you doing", "are you good"]) == True: await vj_PrintMessage(vj_PickRandom(["I am good! You?", "I am doing great! how about you?", "Good, you?"])); return
    if vj_Match_Start(m,["are you a bot", "you are a bot", "you a bot"]) == True: await vj_PrintMessage(vj_PickRandom(["I am a bot!", "I know I am a bot!", " I am robot!", "BEEP BOOP BEEP BOOP"])); return
    
    if vj_Match_Any(m,["who created you", "your owner", "your creator", "your author", "your dad", "your parents", "your father"]) == True: await vj_PrintMessage("DrVrej created me!"); return
    if vj_Match_Any(m,["your mother", "your mom", "who is your mom"]) == True: await vj_PrintMessage("I don't have a mother!"); return
    
    if vj_Match_Any(m,["<:hl3:562737648926457893>", "hl3", "half life 3"]) == True: await vj_PrintMessage(vj_PickRandom(["In your dreams you will see <:hl3:562737648926457893>!", "Release date: December 29, 9999", "Never. :eye:"])); return
    if vj_Match_Any(m,["cookie", u"\U0001F36A"]) == True: await vj_PrintMessage(":cookie:"); return
    if vj_Match_Any(m,["armenia", "hayastan", "armo", "🇦🇲"]) == True: await vj_PrintMessage("Long Live Armenia! :flag_am:"); return
    if vj_Match_Any(m,["gay", u"\U0001F3F3\uFE0F\u200D\U0001F308"]) == True: await vj_PrintMessage(":rainbow_flag:"); return
    if vj_Match_Any(m,["i am happy", u"\U0001F600", u"\U0001F603", u"\U0001F604", u"\U0001F601", u"\U000FE332", u"\U0001F60A", u"\U0001F642", u"\u263A", u"\U0001F607", u"\U0001F643"]) == True: await vj_PrintMessage(vj_PickRandom([u"\U0001F600", u"\U0001F603", u"\U0001F604", u"\U0001F601", u"\U000FE332", u"\U0001F60A", u"\U0001F642", u"\U000FE336", u"\U0001F607", u"\U0001F643"])); return

    # Yete pame chi hasgena:      "I don't recognize your message! Sorry :frowning:"
    await vj_PrintMessage(vj_PickRandom(["Yes you are!", "No you!", "Tell me more!", "Okay?", "Cool story!", "Understandable, have a nice day!", "You wot m8?!", "I was in the chest club."]))

def vj_PickRandom(tbl):
    if isinstance(tbl, list):
        return tbl[randint(0,len(tbl)-1)]
    return tbl

def vj_Match_Exact(item,a):
    for v in a:
        if item == v:
            return True
    return False

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

kakhni_tive = None
try:
   os.environ["KAKHNI_TIVE"]
   kakhni_tive = os.environ["KAKHNI_TIVE"]
except KeyError:
   kakhni_tive = open("kakhni_tive.txt", "r").readline()
bot.run(kakhni_tive)

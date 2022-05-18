import discord
import sys
import os
import datetime
import bot_funcs as vjf

########## Notes ##########
# discord.py docs = https://discordpy.readthedocs.io/en/latest/api.html
# Manual run = python bot_main.py
# Check for outdated packages = pip list --outdated
# Update all packages = pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
# Update discord.py = pip install --upgrade discord.py

intents = discord.Intents.all()  # A factory method that creates a Intents with everything enabled.
bot = discord.Client(intents=intents)
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

########## Channel IDs ##########
idChanVoice_Stat = 562276245174485002 # Fake voice channel (Used for stat display)
idRole_Member = 390961994645241871
idRole_Quarantine = 463809123427811328

async def vj_update_stats():
	# Loop through all the servers that we are in
	for g in bot.guilds:
		numEveryone = len(g.members)
		numBots = len(vjf.GetBots(g.members))
		# Everyone,     (Everyone - bots - members - quarantine),     Bots
		chName = "👤" + str(numEveryone) + " 🆕" + str(numEveryone - numBots - len(vjf.GetRank(g.members, idRole_Member)) - len(vjf.GetRank(g.members, idRole_Quarantine))) + " 🤖" + str(numBots)
		
		# Get the fake voice channel, make sure it exists and finally update the stats!
		getChan = vjf.GetChannel(g.channels, discord.ChannelType.voice, idChanVoice_Stat)
		if getChan != None:
			await getChan.edit(name = chName, reason = "Updating server stats...")

@bot.event
async def on_ready():
	await vj_update_stats()
	print("VrejBot Has successfully loaded!")

@bot.event
async def on_member_join(member):
	#print(member.avatar_url)
	#print(member.color)
	await vj_update_stats()
	for channel in member.guild.channels:
		if str(channel) == "bot-log":
			await channel.send(":inbox_tray: **MEMBER JOINED** [*" + vjf.Format_Time(member.joined_at) + "*]\n:busts_in_silhouette: `Name: " + str(member) + " [ID: " + str(member.id) + "]`\n:tools: `Account Created: " + vjf.Format_Time(member.created_at) + "`\n:iphone: `On Mobile: " + str(member.is_on_mobile()) + "`\n:trophy: `Highest Rank: " + str(member.top_role) + "`")

@bot.event
async def on_member_remove(member):
	await vj_update_stats()
	for channel in member.guild.channels:
		if str(channel) == "bot-log":
			await channel.send(":outbox_tray: **MEMBER LEFT** [*" + vjf.Format_Time(datetime.datetime.now()) + "*]\n:busts_in_silhouette: `Name: " + str(member) + " [ID: " + str(member.id) + "]`\n:tools: `Account Created: " + vjf.Format_Time(member.created_at) + "`\n:iphone: `On Mobile: " + str(member.is_on_mobile()) + "`\n:trophy: `Highest Rank: " + str(member.top_role) + "`\n:inbox_tray:`Join Date: " + vjf.Format_Time(member.joined_at) + "`")

@bot.event
async def on_member_update(before, after):
	# before – The Member that updated their profile with the old info. ||| after – The Member that updated their profile with the updated info.
	if before.roles != after.roles: # Nayir, yete martoun role-ere pokhvetsan
		await vj_update_stats()
#	print("Member updated!")

@bot.event
async def on_message(message):
	m_org = message.content # Original message
	m = m_org # The one that will be edited
	botTagged = False # Yete robote, tag yegher e, sharnage
	# Unused
	#isAdmin = vjf.IsAdmin(message.author) # Nayir yete medzavor e
	getUserInfo = False # Amen tag yeghadz martigneroun masin hamar ge ker e (-u, -user)
	
	# Link hramaner:
	mh = m_org.strip() # Asiga minag hramaneroun hamar bidi kordzadzvi!
	for v in message.mentions: # Nayir amen martignere vor tag yegher en
		mh = mh.replace("<@" + str(v.id) + ">","").strip() # serpe martigneroon anoonere
	if vjf.Match_Exact(mh,["-help", "-h", "-?"]) == True: await message.channel.send("```ini\n[-sg | -steam] = Steam Group\n[-i | -invite] = Discord Server (Invite link)\n[-vjbase | -vjb | -vj] = VJ Base Workshop Page\n[-vjgit] = VJ Base GitHub Page\n[-hlr] = Half-Life Resurgence GitHub Page\n[-vjof | -vjunof | -vjcol | -vjcollection] = VJ Base Official and Unofficial Addons\n[-server | -sfiles] = DrVrej's Server Files\n[-im] = Broken / Incompatible Addons\n[-suggestion] = Create a suggestion for anything related to this group\n[-u | -user] = Returns the information of the given user(s)\n```"); return
	if vjf.Match_Exact(mh,["-sg", "-steam"]) == True: await message.channel.send("Steam Group: https://steamcommunity.com/groups/vrejgaming"); return
	if vjf.Match_Exact(mh,["-i", "-invite"]) == True: await message.channel.send("Discord Invite: https://discordapp.com/invite/zwQjrdG"); return
	if vjf.Match_Exact(mh,["-vjbase", "-vjb", "-vj"]) == True: await message.channel.send("VJ Base Workshop Page: https://steamcommunity.com/sharedfiles/filedetails/?id=131759821"); return
	if vjf.Match_Exact(mh,["-vjgit"]) == True: await message.channel.send("VJ Base GitHub Page: https://github.com/DrVrej/VJ-Base"); return
	if vjf.Match_Exact(mh,["-vjof", "-vjunof", "-vjcol", "-vjcollection"]) == True: await message.channel.send("VJ Base Official and Unofficial Addons: https://steamcommunity.com/sharedfiles/filedetails/?id=1080924955"); return
	if vjf.Match_Exact(mh,["-server", "-sfiles"]) == True: await message.channel.send("DrVrej's Server Files: https://steamcommunity.com/sharedfiles/filedetails/?id=157267702"); return
	if vjf.Match_Exact(mh,["-im"]) == True: await message.channel.send("Broken / Incompatible Addons: https://steamcommunity.com/sharedfiles/filedetails/?id=1129493108"); return
	if vjf.Match_Exact(mh,["-hlr"]) == True: await message.channel.send("Half-Life Resurgence (Base): https://github.com/VJ-HLR-Developers/Half-Life-Resurgence"); return
	
	# Oknagan hramaner:
	if vjf.Match_Start(mh,["-u", "-user",]) == True: getUserInfo = True
	
	# Suggestion Command and make sure the sender doesn't have a restricted roles!
	if vjf.Match_Start(mh,["-suggestion"]) == True and len(vjf.GetRank([message.author],630501693984997447)) < 1:
		finalMsg = ":notepad_spiral: **Suggestion by <@!" + str(message.author.id) + "> **[*" + vjf.Format_Time(datetime.datetime.now()) + "*] :notepad_spiral:\n" + (str(message.content).replace("-suggestion","").strip())
		numAttach = 0
		for v in message.attachments: # Amen negarnere ara
			numAttach = numAttach + 1
			finalMsg = finalMsg + " \nImage " + str(numAttach) + ": " + (v.url) # Meg, meg aveltsour negarnere namagin mech
		getChan = vjf.GetChannel(message.guild.channels, discord.ChannelType.text, 629101812208631808) # Pendre "suggestion" channele
		if getChan != None:
			await getChan.send(finalMsg)
			await message.delete()
			return
	
	# If the message is from VrejBot, and its the suggestion reply, then tag it with approve/disapprove emojis
	if message.author == bot.user and vjf.Match_Any(m_org,["Suggestion by"]) == True:
		await message.add_reaction("\U00002705")
		await message.add_reaction("\U0000274c")
	
	for v in message.mentions: # Nayir amen martignere vor tag yegher en
		if v == bot.user: # Yete robotne, gerna sharnagel
			botTagged = True
		if getUserInfo == True:
			#if isAdmin == True: # Yete medzavor e, sharnag e
			await message.channel.send(":information_source: **MEMBER INFORMATION** [*" + vjf.Format_Time(datetime.datetime.now()) + "*]\n:busts_in_silhouette: `Name: " + str(v) + " [ID: " + str(v.id) + "]`\n:tools: `Account Created: " + vjf.Format_Time(v.created_at) + "`\n:iphone: `On Mobile: " + str(v.is_on_mobile()) + "`\n:trophy: `Highest Rank: " + str(v.top_role) + "`\n:inbox_tray:`Join Date: " + vjf.Format_Time(v.joined_at) + "`")
			#else: # Medzavor chene, ese martoun vor chi gernar as hramane sharnagel
				#await message.channel.send("<@!" + str(message.author.id) + ">, you must be an administrator to use that command!");
		m = m.replace("<@" + str(v.id) + ">","").strip() # serpe martigneroon anoonere
	
	# Sharnag e, minag yete as bot-e tag yegher e!
	if botTagged == False: return

	print("-----------------------------")
	print("Author: " + str(message.author) + " [" + vjf.Format_Time(message.created_at) + "]")
	
	try:
		print("Message Arrived: " + m) # Make sure it's a unrecognized letter
		m = m.lower()
	except UnicodeEncodeError:
		m = m.translate(non_bmp_map)
		print("unrecognized Message Arrived: " + m)

	# Yete yes em, mi sharnager!
	if message.author == bot.user: return
	
	# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	async def vj_PrintMessage(s):
		await message.channel.send("<@!" + str(message.author.id) + "> " + s)
	
	if m == "": await vj_PrintMessage("You didn't type anything! :thinking: :angry:"); return
	
	if vjf.Match_Start(m,["hello", "hi", "greetings", "allo"]) == True: await vj_PrintMessage(vjf.PickRandom(["Hello!", "Hi!", "Greetings!", "Allo!"])); return
	if vjf.Match_Start(m,["how are you", "how you doing", "are you good"]) == True: await vj_PrintMessage(vjf.PickRandom(["I am good! You?", "I am doing great! how about you?", "Good, you?"])); return
	if vjf.Match_Start(m,["are you a bot", "you are a bot", "you a bot"]) == True: await vj_PrintMessage(vjf.PickRandom(["I am a bot!", "I know I am a bot!", " I am robot!", "BEEP BOOP BEEP BOOP"])); return
	if vjf.Match_Start(m,["talk to hgrunt"]) == True: await message.channel.send(vjf.PickRandom(["<@!396884008501510144> Hello!"])); return
	
	if vjf.Match_Any(m,["who created you", "your owner", "your creator", "your author", "your dad", "your parents", "your father"]) == True: await vj_PrintMessage("DrVrej created me!"); return
	if vjf.Match_Any(m,["your mother", "your mom", "who is your mom"]) == True: await vj_PrintMessage("I don't have a mother!"); return
	if vjf.Match_Any(m,["tell me a fact", "fact", "say a fact", "tell a fact", "say fact", "tell fact", "fun fact"]) == True: await vj_PrintMessage("Fun Fact! " + vjf.PickRandom(["Armenia is the first Christian nation!", "VJ Base stands for Vrej Base.", "VrejGaming was originally made on May 8th, 2011!", "VJ Base was originally created during Garry's Mod 12!", "Armenia's anthem is 'Mer Hayrenik', which stands for 'Our Fatherland'", "Armenia is one of the 10 ancient nations that still exists!", "Vrej in Armenian means Vengeance or Revenge.", "Armenian language has its own unique alphabet. grammar and sentence system!", "VJ Base 2.0 was released on January 1, 2015!", "VJ Base was the first addon for Garry's Mod to bring extensive customization. Soon after release, many addons began to follow the idea of customization.", "Half-Life Resurgence is the largest SNPC pack made by DrVrej!"])); return
	
	if vjf.Match_Any(m,["<:hl3:562737648926457893>", "hl3", "half life 3"]) == True: await vj_PrintMessage(vjf.PickRandom(["In your dreams you will see <:hl3:562737648926457893>!", "Release date: December 29, 9999", "Never. :eye:"])); return
	if vjf.Match_Any(m,["cookie", u"\U0001F36A"]) == True: await vj_PrintMessage(":cookie:"); return
	if vjf.Match_Any(m,["armenia", "hayastan", "armo", "🇦🇲"]) == True: await vj_PrintMessage("Long Live Armenia! :flag_am:"); return
	if vjf.Match_Any(m,["happy", u"\U0001F600", u"\U0001F603", u"\U0001F604", u"\U0001F601", u"\U000FE332", u"\U0001F60A", u"\U0001F642", u"\u263A", u"\U0001F607", u"\U0001F643"]) == True: await vj_PrintMessage(vjf.PickRandom([u"\U0001F600", u"\U0001F603", u"\U0001F604", u"\U0001F601", u"\U000FE332", u"\U0001F60A", u"\U0001F642", u"\U000FE336", u"\U0001F607", u"\U0001F643"])); return
	
	# Yete pame chi hasgena:	  "I don't recognize your message! Sorry :frowning:"
	await vj_PrintMessage(vjf.PickRandom(["ENT.Zombie = true", "Yes you are!", "No you!", "Tell me more!", "Okay?", "Cool story!", "Understandable, have a nice day!", "You wot m8?!", "I was in the chest club.", "If you say so!", "I like trains.", "If you say so...", "I agree.", "I disagree."]))

kakhniTive = None
try:
   os.environ["KAKHNI_TIVE"]
   kakhniTive = os.environ["KAKHNI_TIVE"]
except KeyError:
   kakhniTive = open("kakhni_tive.txt", "r").readline()
bot.run(kakhniTive)
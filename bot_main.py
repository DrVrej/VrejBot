import datetime
import logging
import os

import discord
import bot_funcs as vjf

########## Notes ##########
# discord.py docs = https://discordpy.readthedocs.io/en/latest/api.html
# Manual run = python bot_main.py
#
# Check for outdated packages = pip list --outdated
# Update all packages = pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
# Update discord.py = pip install --upgrade discord.py
###########################

bot = discord.Client(intents=discord.Intents.all())  # A factory method that creates a Intents with everything enabled
logger = logging.getLogger("vrejbot")  # Sets up Discord logging, source: https://github.com/Rapptz/discord.py/blob/master/discord/utils.py#L1305

########## Server IDs ##########
SERVER_VREJGAMING = 390951701655584778
SERVER_PORTS = 563046572191907905

########## Channel IDs ##########
idChannel_Stats = {
	SERVER_VREJGAMING: 562276245174485002,
	SERVER_PORTS: 630267198635638786,
}
idChannel_Log = {
	SERVER_VREJGAMING: 391189293965508608,
	SERVER_PORTS: 564176507044364289,
}

########## Role IDs ##########
idRole_Member = {
	SERVER_VREJGAMING: 390961994645241871,
	SERVER_PORTS: 1011456428046827602,
}


# ANSI style codes for terminal
class STYLE:
	RESET = "\x1b[0m"
	SERVER_NAME = "\x1b[3;38;5;117m"
	DISCORD_DEBUG = "\x1b[40;1m"
	DISCORD_INFO = "\x1b[34;1m"
	DISCORD_WARNING = "\x1b[33;1m"
	DISCORD_ERROR = "\x1b[31m"
	DISCORD_CRITICAL = "\x1b[41m"


# Update the stats channel if the server has one!
async def vjUpdateStats(guild):
	serverID = guild.id
	numEveryone = len(guild.members)
	numBots = len(vjf.GetBots(guild.members))
	if serverID in idChannel_Stats:  # Make sure the key exists in the dictionary before attempting to look it up!
		statChan = vjf.GetChannel(guild.channels, discord.ChannelType.voice, idChannel_Stats[serverID])
		if statChan != None:  # If this server has a stat channel...
			logger.info(f"{STYLE.SERVER_NAME}{guild.name}{STYLE.RESET} : Updating server stats with {numEveryone} members")
			textStat = "Unknown Stats!"
			if serverID == SERVER_VREJGAMING:
				# Everyone,     Verified,     (Everyone - bots - members - quarantine - verified),     Bots
				textStat = f"👥{numEveryone} 📦{len(vjf.GetRank(guild.members, 979356390474780672))} 🚪{numEveryone - numBots - len(vjf.GetRank(guild.members, idRole_Member[serverID])) - len(vjf.GetRank(guild.members, 463809123427811328)) - len(vjf.GetRank(guild.members, 979356390474780672))} 🤖{numBots}"
			elif serverID == SERVER_PORTS:
				# Everyone,     (Everyone - bots - members),     Bots
				textStat = f"👥{numEveryone} 🚪{numEveryone - numBots - len(vjf.GetRank(guild.members, idRole_Member[serverID]))} 🤖{numBots}"
			try:
				await statChan.edit(name=textStat, reason="Updating server stats")
			except discord.HTTPException as err:
				logger.error(f"Error updating stats! (HTTPException)! {err}")


@bot.event
async def on_ready():
	await bot.change_presence(
		status=discord.Status.online,
		activity=discord.Activity(
			name="💬 Need help? Type -help",
			state=f"Serving {len(bot.guilds)} servers!",
			type=discord.ActivityType.competing,
		),
	)
	for g in bot.guilds:
		await vjUpdateStats(g)
	logger.info("initialized successfully!")


@bot.event
async def on_member_join(member):
	curGuild = member.guild
	logChan = vjf.GetChannel(curGuild.channels, discord.ChannelType.text, idChannel_Log[curGuild.id])
	if logChan != None:  # If this server has a log channel...
		await logChan.send(":inbox_tray: **MEMBER JOINED** [*" + vjf.Format_Time(member.joined_at) + "*]\n:busts_in_silhouette: `Name: " + str(member) + " [ID: " + str(member.id) + "]`\n:tools: `Account Created: " + vjf.Format_Time(member.created_at) + "`\n:iphone: `On Mobile: " + str(member.is_on_mobile()) + "`\n:trophy: `Highest Rank: " + str(member.top_role) + "`")
	await vjUpdateStats(curGuild)


@bot.event
async def on_member_remove(member):
	curGuild = member.guild
	logChan = vjf.GetChannel(curGuild.channels, discord.ChannelType.text, idChannel_Log[curGuild.id])
	if logChan != None:  # If this server has a log channel...
		await logChan.send(":outbox_tray: **MEMBER LEFT** [*" + vjf.Format_Time(datetime.datetime.now()) + "*]\n:busts_in_silhouette: `Name: " + str(member) + " [ID: " + str(member.id) + "]`\n:tools: `Account Created: " + vjf.Format_Time(member.created_at) + "`\n:iphone: `On Mobile: " + str(member.is_on_mobile()) + "`\n:trophy: `Highest Rank: " + str(member.top_role) + "`\n:inbox_tray:`Join Date: " + vjf.Format_Time(member.joined_at) + "`")
	await vjUpdateStats(curGuild)


@bot.event
async def on_member_update(before, after):
	# logger.info("Member updated!")
	# before – The Member that updated their profile with the old info. ||| after – The Member that updated their profile with the updated info.
	if before.roles != after.roles:  # Nayir, yete martoun role-ere pokhvetsan
		await vjUpdateStats(after.guild)


@bot.event
async def on_message(message):
	serverID = message.guild.id
	content = message.content  # Unedited message
	contentEdited = content  # Edited message
	botTagged = False
	# authorIsAdmin = vjf.IsAdmin(message.author)
	getUserInfo = False  # For user info command

	# Link hramaner:
	mh = content.strip()  # Asiga minag hramaneroun hamar bidi kordzadzvi!
	for v in message.mentions:  # Serpe martigneroon anoonere
		mh = mh.replace(f"<@{v.id}>", "").strip()

	# Help command
	if vjf.Match_Exact(mh, ["-help", "-h", "-?"]):
		if serverID == SERVER_VREJGAMING:
			await message.channel.send("```ini\n[-sg | -steam] = Steam Group\n[-i | -invite] = Discord Server (Invite link)\n[-vjbase | -vjb | -vj] = VJ Base Workshop Page\n[-vjgit] = VJ Base GitHub Page\n[-hlr] = Half-Life Resurgence GitHub Page\n[-server | -sfiles] = DrVrej's Server Files\n[-im] = Broken / Incompatible Addons\n[-u | -user] = Returns the information of the given user(s)\n```")
		else:
			await message.channel.send("```ini\n[-u | -user] = Returns the information of the given user(s)\n```")
		return

	# VrejGaming commands
	if serverID == SERVER_VREJGAMING:
		# fmt: off
		if vjf.Match_Exact(mh, ["-sg", "-steam"]): await message.channel.send("Steam Group: https://steamcommunity.com/groups/vrejgaming"); return
		if vjf.Match_Exact(mh, ["-i", "-invite"]): await message.channel.send("Discord Invite: https://discordapp.com/invite/zwQjrdG"); return
		if vjf.Match_Exact(mh, ["-vjbase", "-vjb", "-vj"]): await message.channel.send("VJ Base Workshop Page: https://steamcommunity.com/sharedfiles/filedetails/?id=131759821"); return
		if vjf.Match_Exact(mh, ["-vjgit"]): await message.channel.send("VJ Base GitHub Page: https://github.com/DrVrej/VJ-Base"); return
		if vjf.Match_Exact(mh, ["-server", "-sfiles"]): await message.channel.send("DrVrej's Server Files: https://steamcommunity.com/sharedfiles/filedetails/?id=157267702"); return
		if vjf.Match_Exact(mh, ["-im"]): await message.channel.send("Broken / Incompatible Addons: https://steamcommunity.com/sharedfiles/filedetails/?id=1129493108"); return
		if vjf.Match_Exact(mh, ["-hlr"]): await message.channel.send("Half-Life Resurgence (Base): https://github.com/VJ-HLR-Developers/Half-Life-Resurgence"); return
		# fmt: on

	# Commands for all servers
	if vjf.Match_Start(mh, ["-u", "-user"]):
		getUserInfo = True

	for v in message.mentions:  # Nayir amen martignere vor tag yegher en
		if v == bot.user:  # Yete robotne, gerna sharnagel
			botTagged = True
		if getUserInfo:
			await message.channel.send(":information_source: **MEMBER INFORMATION** [*" + vjf.Format_Time(datetime.datetime.now()) + "*]\n:busts_in_silhouette: `Name: " + str(v) + " [ID: " + str(v.id) + "]`\n:tools: `Account Created: " + vjf.Format_Time(v.created_at) + "`\n:iphone: `On Mobile: " + str(v.is_on_mobile()) + "`\n:trophy: `Highest Rank: " + str(v.top_role) + "`\n:inbox_tray:`Join Date: " + vjf.Format_Time(v.joined_at) + "`")
		contentEdited = contentEdited.replace("<@" + str(v.id) + ">", "").strip()  # serpe martigneroon anoonere

	# Sharnag e, minag yete as bot-e tag yegher e!
	if not botTagged:
		return

	logger.info(f"messaged arrived : @{message.author} , #{message.channel} , {vjf.Format_Time(message.created_at)} , Content = {contentEdited}")
	contentEdited = contentEdited.lower()

	# Yete yes em, mi sharnager!
	if message.author == bot.user:
		return

	# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	async def vj_PrintMessage(s):
		await message.channel.send("<@!" + str(message.author.id) + "> " + s)

	if contentEdited == "":
		await vj_PrintMessage("You didn't type anything! :thinking: :angry:")
		return

	if vjf.Match_Start(contentEdited, ["hello", "hi", "greetings", "allo"]):
		await vj_PrintMessage(vjf.PickRandom(["Hello!", "Hi!", "Greetings!", "Allo!"]))
		return
	if vjf.Match_Start(contentEdited, ["how are you", "how you doing", "are you good"]):
		await vj_PrintMessage(vjf.PickRandom(["I am good! You?", "I am doing great! how about you?", "Good, you?"]))
		return
	if vjf.Match_Start(contentEdited, ["are you a bot", "you are a bot", "you a bot"]):
		await vj_PrintMessage(vjf.PickRandom(["I am a bot!", "I know I am a bot!", " I am robot!", "BEEP BOOP BEEP BOOP"]))
		return
	if vjf.Match_Start(contentEdited, ["talk to hgrunt"]):
		await message.channel.send(vjf.PickRandom(["<@!396884008501510144> Hello!"]))
		return
	if vjf.Match_Any(contentEdited, ["who created you", "your owner", "your creator", "your author", "your dad", "your parents", "your father"]):
		await vj_PrintMessage("DrVrej created me!")
		return
	if vjf.Match_Any(contentEdited, ["your mother", "your mom", "who is your mom"]):
		await vj_PrintMessage("I don't have a mother!")
		return
	if vjf.Match_Any(contentEdited, ["<:hl3:562737648926457893>", "hl3", "half life 3"]):
		await vj_PrintMessage(vjf.PickRandom(["In your dreams you will see <:hl3:562737648926457893>!", "Release date: December 29, 9999", "Never. :eye:"]))
		return
	if vjf.Match_Any(contentEdited, ["cookie", "\U0001f36a"]):
		await vj_PrintMessage(":cookie:")
		return
	if vjf.Match_Any(contentEdited, ["armenia", "hayastan", "armo", "🇦🇲"]):
		await vj_PrintMessage("Long Live Armenia! :flag_am:")
		return
	if vjf.Match_Any(contentEdited, ["happy", "\U0001f600", "\U0001f603", "\U0001f604", "\U0001f601", "\U000fe332", "\U0001f60a", "\U0001f642", "\u263a", "\U0001f607", "\U0001f643"]):
		await vj_PrintMessage(vjf.PickRandom(["\U0001f600", "\U0001f603", "\U0001f604", "\U0001f601", "\U000fe332", "\U0001f60a", "\U0001f642", "\U000fe336", "\U0001f607", "\U0001f643"]))
		return

	if serverID == SERVER_VREJGAMING and vjf.Match_Any(contentEdited, ["tell me a fact", "fact", "say a fact", "tell a fact", "say fact", "tell fact", "fun fact"]):
		await vj_PrintMessage("Fun Fact! " + vjf.PickRandom(["Armenia is the first Christian nation!", "VJ Base stands for Vrej Base.", "VrejGaming was originally made on May 8th, 2011!", "VJ Base was originally created during Garry's Mod 12!", "Armenia's anthem is 'Mer Hayrenik', which stands for 'Our Fatherland'", "Armenia is one of the 10 ancient nations that still exists!", "Vrej in Armenian means Vengeance or Revenge.", "Armenian language has its own unique alphabet. grammar and sentence system!", "VJ Base 2.0 was released on January 1, 2015!", "VJ Base was the first addon for Garry's Mod to bring extensive customization. Soon after release, many addons began to follow the idea of customization.", "Half-Life Resurgence is the largest SNPC pack made by DrVrej!"]))
		return

	# Yete pame chi hasgena:	  "I don't recognize your message! Sorry :frowning:"
	await vj_PrintMessage(vjf.PickRandom(["ENT.Zombie = true", "Yes you are!", "No you!", "Tell me more!", "Okay?", "Cool story!", "Understandable, have a nice day!", "You wot m8?!", "I was in the chest club.", "If you say so!", "I like trains.", "If you say so...", "I agree.", "I disagree."]))


kakhni_tive = os.getenv("KAKHNI_TIVE")
if not kakhni_tive:
	with open("kakhni_tive.txt") as file:
		kakhni_tive = file.readline().strip()
bot.run(kakhni_tive, root_logger=True)

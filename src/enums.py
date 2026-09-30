class ID:
	class VREJGAMING:
		SERVER = 390951701655584778
		CHAN_STATS = 562276245174485002
		CHAN_LOG = 391189293965508608
		ROLE_MEMBER = 390961994645241871

	class PORTS:
		SERVER = 563046572191907905
		CHAN_STATS = 630267198635638786
		CHAN_LOG = 564176507044364289
		ROLE_MEMBER = 1011456428046827602

	@classmethod
	def __class_getitem__(self, serverID):
		for server in self.__dict__.values():
			if getattr(server, "SERVER", None) == serverID:
				return server
		return None


# ANSI style codes for terminal
class STYLE:
	RESET = "\x1b[0m"
	SERVER_NAME = "\x1b[3;38;5;117m"
	DISCORD_DEBUG = "\x1b[40;1m"
	DISCORD_INFO = "\x1b[34;1m"
	DISCORD_WARNING = "\x1b[33;1m"
	DISCORD_ERROR = "\x1b[31m"
	DISCORD_CRITICAL = "\x1b[41m"

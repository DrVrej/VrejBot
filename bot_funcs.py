from random import randint


def PickRandom(tbl):
    if isinstance(tbl, list):
        return tbl[randint(0, len(tbl) - 1)]
    return tbl


def Match_Exact(item, a):
    for v in a:
        if item == v:
            return True
    return False


def Match_Start(item, a):
    for v in a:
        if item.startswith(str(v)):
            return True
    return False


def Match_Any(item, a):
    for v in a:
        if item.find(v) != -1:
            return True
    return False


def Format_Time(t):
    # t = jamnage
    return t.strftime("%B %d, %Y | %I:%M:%S %p")


def IsAdmin(member):
    # member = The member to check if is admin
    return member.guild_permissions.administrator


def GetBots(members):
    # members = List of members to search
    result = []  # Barab array shine
    for v in members:  # Amen antamnere ara
        if v.bot == True:  # Yete antame robot e, aveltsour ays antame array-in mech
            result.append(v)
    return result


def GetRank(members, rid):
    # members = List of members to search
    # rid = The ID to check for
    result = []  # Barab array shine
    for v in members:  # Amen antamnere ara
        if v.bot == True:  # Mi tseker robotnere hashvevin!
            continue
        for r in v.roles:  # Antamin role-ere ara
            if r.id == rid:  # Yete noun role-en ounine, aveltsour ays antame array-in mech
                result.append(v)
                break
    return result


def GetChannel(ch, ty, id):
    # ch = The list of channels to search
    # ty = The type of channels to search for | discord.ChannelType. ---> [text , voice , category]
    # id = The id to search for
    result = None
    for v in ch:
        if v.type == ty and v.id == id:
            return v
    return result

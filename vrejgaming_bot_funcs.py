import discord
import sys
import os
import datetime
from random import randint

def PickRandom(tbl):
    if isinstance(tbl, list):
        return tbl[randint(0,len(tbl)-1)]
    return tbl

def Match_Exact(item,a):
    for v in a:
        if item == v:
            return True
    return False

def Match_Start(item,a):
    for v in a:
        if item.startswith(str(v)):
            return True
    return False

def Match_Any(item,a):
    for v in a:
        if item.find(v) != -1:
            return True
    return False
    
def Format_Time(t):
    return t.strftime("%B %d, %Y | %I:%M:%S %p")
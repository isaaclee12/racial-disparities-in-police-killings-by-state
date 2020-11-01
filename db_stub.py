import pymongo
import re
import math
"""
This file is just a small copy of mongoDB/mongoDB.py for flask testing.
"""

def initDB():
    # Set up connection with MongoClient
    uri = "mongodb+srv://iwlee:EggCheeseBeansToast@uspolicekillings.ezqox.mongodb.net/US_Police_Killings?retryWrites=true&w=majority"
    myclient = pymongo.MongoClient(uri)
    global mydb
    # Set up database
    mydb = myclient["police_killings"]


def getTotalKillingsForState(state):
    mycol = mydb["US_Police_Killings"]
    myquery = {"State": state}
    killings = mycol.find(myquery).count()
    return killings


def getBlackKillingsForState(state):
    """Number of killings in state x of black people."""
    mycol = mydb["US_Police_Killings"]
    blackQuery = {"$and": [
        {"State": state},
        {"Race with imputations": "African-American/Black"}
    ]}
    blackDoc = mycol.find(blackQuery)
    return blackDoc.count()


def getNotBlackKillingsForState(state):
    """Number of killings in state x of those who are not black."""
    mycol = mydb["US_Police_Killings"]

    notBlackQuery = {"$and": [{"State": state},
                      {"Race with imputations": {"$ne": "African-American/Black"}}
                     ]}
    notBlackDoc = mycol.find(notBlackQuery)
    return notBlackDoc.count()


def getPercentBlackKillingsForState(state):
    """Percent of people in state x killed by police who are black"""
    black_killings = getBlackKillingsForState(state)
    total_killings = getTotalKillingsForState(state)
    percent = (black_killings / total_killings) * 100
    return float('%.2f'%(percent)) # truncate to two decimal places

import pymongo
import re

def counter(mydoc):

    # Initialize counter
    ct = 0

    # Increment counter for every instance found
    for x in mydoc:
        ct += 1

    # Return count
    return ct


def initDB():

    # Set up connection with MongoClient
    myclient = pymongo.MongoClient("mongodb+srv://iwlee:EggCheeseBeansToast@uspolicekillings.ezqox.mongodb.net/US_Police_Killings?retryWrites=true&w=majority")

    # Set up databases
    global mydb
    mydb = myclient["police_killings"]



def queryDB(state_abbrev):

    # Get States
    mycol = mydb["US_Police_Killings"]

    # Choose a State
    state = "CA"

    blackQuery = {"$and": [
        {"State": state},
        {"Race with imputations": "African-American/Black"}
    ]}

    notBlackQuery = {"$and": [{"State": state},
                      {"Race with imputations": {"$ne": "African-American/Black"}}
                     ]}

    blackDoc = mycol.find(blackQuery)
    notBlackDoc = mycol.find(notBlackQuery)

    # Uncomment this to print all killings - be warned, this takes a long time
    # for x in notBlackDoc:
    #     print(x)

    blackKillings = counter(blackDoc)
    print("Number of killings in", state, "of Black People: ", blackKillings)

    notBlackKillings = counter(notBlackDoc)
    print("Number of killings in", state, "of those who are not Black: ", notBlackKillings)

    percentKillingsBlack = (blackKillings / (blackKillings + notBlackKillings)) * 100
    print("Percentage of people in", state, "killed by police who are Black: ", format(percentKillingsBlack, '.2f'), "%")

    # Get States
    demographics = mydb["US_State_Demographics_By_Race"]

    blackDemographics = demographics.find({"Location": "California"}, {"Black": 1, "_id": 0})

    for x in blackDemographics:

        try:
            percentageBlack = re.search(": '(.+?)'}", str(x)).group(1)

        except AttributeError:
            print("Error: demographic not found")
            percentageBlack = ""

    percentageBlack  = float(percentageBlack) * 100
    message = ""

    if (percentageBlack < percentKillingsBlack):

        message += ("The percent of people killed by police in " + state + " is " + str(
            format(percentKillingsBlack, '.2f')) + "%, ")
        message += ("even though only " + str(percentageBlack) + "% of " + state + "'s population is Black. ")
        blackDisparity = (percentKillingsBlack / percentageBlack)

        message += ("The percent of people killed by police in " + state + " who are not Black is " + str(
            format((100 - percentKillingsBlack), '.2f')) + "%, ")
        message += ("whereas " + str((100 - percentageBlack)) + "% of " + state + "'s population is not Black. ")
        notBlackDisparity = ((100 - percentKillingsBlack) / (100 - percentageBlack))

        message += ("Therefore, a black person is (statistically speaking) " + str(
            format(blackDisparity / notBlackDisparity,
                   '.2f')) + " times more likely to be killed by police than someone who is not Black in " + state + ". ")

    else:

        message += ("The percent of people killed by police in " + state + " is " + str(
            format(percentKillingsBlack, '.2f')) + "%, ")
        message += ("where " + str(percentageBlack) + "% of " + state + "'s population is Black. ")
        blackDisparity = (percentKillingsBlack / percentageBlack)

        message += ("The percent of people killed by police in " + state + " who are not Black is " + str(
            format((100 - percentKillingsBlack), '.2f')) + "%, ")
        message += ("whereas " + str((100 - percentageBlack)) + "% of " + state + "'s population is not Black. ")
        notBlackDisparity = ((100 - percentKillingsBlack) / (100 - percentageBlack))

        message += ("Therefore, a black person is (statistically speaking) " + str(
            format((notBlackDisparity / blackDisparity),
                '.2f')) + " times less likely to be killed by police than someone who is not Black in " + state + ". ")

    return message

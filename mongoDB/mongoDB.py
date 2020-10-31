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


def main():

    # FILE STUFF

    """
    # Open file w/ utf-8 encoding (This circumvents a Unicode error)
    global police_killings

    try:
        police_killings = open('/data/Fatal_Encounters_Police_Killings_2000_2020.csv', encoding='utf-8')

    except EOFError:
        print("Error: File could not be found/unable to open")

    finally:

        # Get first line
        line = police_killings.readline()

        # While there are still lines with content...
        while line != "":

            # Debug: Print Each Line
            # print(line)
            # TODO: Make line stuff happen

            # Get next line
            line = police_killings.readline()

    """

    # Set up connection with MongoClient
    myclient = pymongo.MongoClient("mongodb+srv://iwlee:EggCheeseBeansToast@uspolicekillings.ezqox.mongodb.net/US_Police_Killings?retryWrites=true&w=majority")

    # Set up database
    mydb = myclient["police_killings"]

    # Get States
    mycol = mydb["US_Police_Killings"]

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
    print("Number of killings in CA of Black People: ", blackKillings)

    notBlackKillings = counter(notBlackDoc)
    print("Number of killings in CA of those who are not Black: ", notBlackKillings)

    percentKillingsBlack = (blackKillings / (blackKillings + notBlackKillings)) * 100
    print("Percentage of people in CA killed by police who are Black: ", format(percentKillingsBlack, '.2f'), "%")



    # Get States
    demographics = mydb["US_State_Demographics_By_Race"]

    blackDemographics = demographics.find({"Location": "California"}, {"Black": 1, "_id": 0})

    for x in blackDemographics:

        try:
            percentageBlack = re.search(": '(.+?)'}", str(x)).group(1)

        except AttributeError:
            print("Error: demographic not found")
            percentageBlack = ""

        # print(percentageBlack)

    percentageBlack  = float(percentageBlack) * 100

    if (percentageBlack < percentKillingsBlack):

        print("The percent of people killed by police in " + state + " is " + str(format(percentKillingsBlack, '.2f')) + "%")
        print("Even though only " + str(percentageBlack) + "% of " + state + "'s population is Black")
        blackDisparity = (percentKillingsBlack / percentageBlack)
        # print("There is a disparity of " + str(format(disparity, '.2f')) + "%.")

        print("\nConversely, the percent of people killed by police in " + state + " is " + str(format((100 - percentKillingsBlack), '.2f')) + "%")
        print("Whereas " + str((100 - percentageBlack)) + "% of " + state + "'s population is not Black")
        notBlackDisparity = ((100 - percentKillingsBlack) / (100 - percentageBlack))
        # print("There is a disparity of " + str(format(disparity, '.2f')) + "%.")

        print("\nTherefore, a black person is (statistically speaking) " + str(format(blackDisparity/notBlackDisparity, '.2f')) + " times more likely to be killed by police than someone who is not Black in " + state)


    #print(blackDoc["Black"])
    # notBlackDoc = mycol.find(notBlackQuery)



main()

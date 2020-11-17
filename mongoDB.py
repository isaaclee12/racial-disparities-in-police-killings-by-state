import pymongo
import re
import sys

SIZE = 50
PERCENT_KILLINGS_BLACK_BY_STATE = []
POLICE_KILLINGS_ARRAY = []

us_state_abbrev = {
    'AL': 'Alabama',        'AK': 'Alaska',        'AZ': 'Arizona',
    'AR': 'Arkansas',       'CA': 'California',    'CO': 'Colorado',
    'CT': 'Connecticut',    'DE': 'Delaware',      'FL': 'Florida',
    'GA': 'Georgia',        'HI': 'Hawaii',        'ID': 'Idaho',
    'IL': 'Illinois',       'IN': 'Indiana',       'IA': 'Iowa',
    'KS': 'Kansas',         'KY': 'Kentucky',      'LA': 'Louisiana',
    'ME': 'Maine',          'MD': 'Maryland',      'MA': 'Massachusetts',
    'MI': 'Michigan',       'MN': 'Minnesota',     'MS': 'Mississippi',
    'MO': 'Missouri',       'MT': 'Montana',       'NE': 'Nebraska',
    'NV': 'Nevada',         'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico',     'NY': 'New York',      'NC': 'North Carolina',
    'ND': 'North Dakota',   'OH': 'Ohio',          'OK': 'Oklahoma',
    'OR': 'Oregon',         'PA': 'Pennsylvania',  'RI': 'Rhode Island',
    'SC': 'South Carolina', 'SD': 'South Dakota',  'TN': 'Tennessee',
    'TX': 'Texas',          'UT': 'Utah',          'VT': 'Vermont',
    'VA': 'Virginia',       'WA': 'Washington',    'WV': 'West Virginia',
    'WI': 'Wisconsin',      'WY': 'Wyoming',
}


def initDB(states):

    # Set up connection with MongoClient
    myclient = pymongo.MongoClient("mongodb+srv://iwlee:EggCheeseBeansToast@uspolicekillings.ezqox.mongodb.net/US_Police_Killings?retryWrites=true&w=majority")

    # Set up databases
    global mydb
    mydb = myclient["police_killings"]

    # Get States
    mycol = mydb["US_Police_Killings"]

    # Choose a State
    global PERCENT_KILLINGS_BLACK_BY_STATE
    global POLICE_KILLINGS_ARRAY
    rowct = 0

    print("Loading...")

    for state in states:
        blackQuery = {"$and": [
            {"State": state},
            {"Race with imputations": "African-American/Black"}
        ]}

        notBlackQuery = {"$and": [{"State": state},
                                  {"Race with imputations": {"$ne": "African-American/Black"}}
                                  ]}

        blackKillings = mycol.count_documents(blackQuery)
        notBlackKillings = mycol.count_documents(notBlackQuery)

        percentKillingsBlack = (blackKillings / (blackKillings + notBlackKillings)) * 100

        data = state, percentKillingsBlack
        #PERCENT_KILLINGS_BLACK_BY_STATE.append(data)
        # print(data)
        rowct += 1

    #for state in states:
        policeKillingsData = calculateStats(state, percentKillingsBlack) # , percentKillingsBlack
        #getDemographics(state)
        POLICE_KILLINGS_ARRAY.append(policeKillingsData)
        POLICE_KILLINGS_ARRAY.append(policeKillingsData)

    # for item in POLICE_KILLINGS_ARRAY:
    #     print(item)

def getDemographics(state_abbrev):
    # Get State Demographics
    demographics = mydb["US_State_Demographics_By_Race"]
    #
    blackDemographics = demographics.find({"Location": us_state_abbrev.get(state_abbrev)}, {"Black": 1, "_id": 0})

    for x in blackDemographics:

        try:
            percentPopulationBlack = re.search(": '(.+?)'}", str(x)).group(1)

        except AttributeError:
            print("Error: demographic not found")
            percentPopulationBlack = ""

    # Clean data
    if percentPopulationBlack == "<.01":
        percentPopulationBlack = .01

    percentPopulationBlack = float(percentPopulationBlack) * 100
    #percentPopulationNotBlack = 100 - percentPopulationBlack
    return percentPopulationBlack


def calculateStats(state_abbrev, percentKillingsBlack):

    #Get percent for this state
    # for item in PERCENT_KILLINGS_BLACK_BY_STATE:
    #     if item[0] == state_abbrev:
    # percentKillingsBlack = item[1]
    percentKillingsNotBlack = 100 - percentKillingsBlack

    # Get State Demographics
    demographics = mydb["US_State_Demographics_By_Race"]
    blackDemographics = demographics.find({"Location": us_state_abbrev.get(state_abbrev)}, {"Black": 1, "_id": 0})

    #Init
    percentPopulationBlack = .01

    for x in blackDemographics:

        try:
            percentPopulationBlack = re.search(": '(.+?)'}", str(x)).group(1)

        except AttributeError:
            print("Error: demographic not found")
            percentPopulationBlack = .01

    # Clean data
    if percentPopulationBlack == "<.01":
        percentPopulationBlack = .01

    # If % Black people is 0, set all to 0 except populationNotBlack
    # This prevents a divide-by-zero error
    if float(percentPopulationBlack) <= 0:
        percentPopulationBlack = 0
        percentPopulationNotBlack = 100
        blackDisparity = 0
        notBlackDisparity = 0
        totalDisparity = 0

        return state_abbrev, percentKillingsBlack, percentKillingsNotBlack, percentPopulationBlack, \
               percentPopulationNotBlack, blackDisparity, notBlackDisparity, totalDisparity

    #Otherwise, calculate disparities and add to array.
    else:
        percentPopulationBlack = float(percentPopulationBlack) * 100
        percentPopulationNotBlack = 100 - percentPopulationBlack

        blackDisparity = (percentKillingsBlack / percentPopulationBlack)
        notBlackDisparity = (percentKillingsNotBlack / percentPopulationNotBlack)

        totalDisparity = blackDisparity/notBlackDisparity

        return state_abbrev, percentKillingsBlack, percentKillingsNotBlack, percentPopulationBlack, \
               percentPopulationNotBlack, blackDisparity, notBlackDisparity, totalDisparity


def queryDB(state_abbrev):
    for item in POLICE_KILLINGS_ARRAY:
        if item[0] == state_abbrev:

            message = ""
            percentKillingsBlack = item[1]
            percentKillingsNotBlack = item[2]
            percentPopulationBlack = item[3]
            percentPopulationNotBlack = item[4]
            blackDisparity = item[5]
            notBlackDisparity = item[6]

            if percentPopulationBlack == 0:
                message += ("No data found for " + state_abbrev + "!")

            else:

                if (percentPopulationBlack < percentKillingsBlack):

                    message += (
                                "The percent of people killed by police in " + state_abbrev + " who are Black is " + str(
                            format(percentKillingsBlack, '.2f')) + "%, ")
                    message += ("even though only " + format(percentPopulationBlack,
                                                             '.2f') + "% of " + state_abbrev + "'s population is Black. ")

                    message += (
                                "The percent of people killed by police in " + state_abbrev + " who are not Black is " + str(
                            format(percentPopulationNotBlack, '.2f')) + "%, ")
                    message += ("whereas " + str(
                        percentPopulationNotBlack) + "% of " + state_abbrev + "'s population is not Black. ")

                    message += ("Therefore, a black person is (statistically speaking) " + str(
                        format(blackDisparity / notBlackDisparity,
                               '.2f')) + " times more likely to be killed by police than someone who is not Black in " + state_abbrev + ". ")

                else:

                    message += ("The percent of people killed by police in " + state_abbrev + " is " + str(
                        format(percentKillingsBlack, '.2f')) + "%, ")
                    message += ("where " + format(percentPopulationBlack,
                                                  '.2f') + "% of " + state_abbrev + "'s population is Black. ")

                    message += (
                                "The percent of people killed by police in " + state_abbrev + " who are not Black is " + str(
                            format(percentPopulationNotBlack, '.2f')) + "%, ")
                    message += ("whereas " + str(
                        percentPopulationNotBlack) + "% of " + state_abbrev + "'s population is not Black. ")

                    # Prevent divide by 0 error
                    if blackDisparity > 0:
                        message += ("Therefore, a black person is (statistically speaking) " + str(
                            format((notBlackDisparity / blackDisparity),
                                   '.2f')) + " times less likely to be killed by police than someone who is not Black in " + state_abbrev + ". ")
                    else:
                        message += ("NO BLACK DISPARITY")

            return message


def getPoliceKillingsArray():
    return POLICE_KILLINGS_ARRAY


#return state_abbrev, percentKillingsBlack, percentKillingsNotBlack, percentPopulationBlack,
#percentPopulationNotBlack, blackDisparity, notBlackDisparity, totalDisparity


def getPercentKillingsBlack(state_abbrev):
    for item in POLICE_KILLINGS_ARRAY:
        if item[0] == state_abbrev:
            return format(item[1], '.2f')


def getPercentKillingsNotBlack(state_abbrev):
    for item in POLICE_KILLINGS_ARRAY:
        if item[0] == state_abbrev:
            return format(item[2], '.2f')


def getPercentPopulationBlack(state_abbrev):
    for item in POLICE_KILLINGS_ARRAY:
        if item[0] == state_abbrev:
            return format(item[3], '.2f')


def getPercentPopulationNotBlack(state_abbrev):
    for item in POLICE_KILLINGS_ARRAY:
        if item[0] == state_abbrev:
            return format(item[4], '.2f')


def getBlackDisparity(state_abbrev):
    for item in POLICE_KILLINGS_ARRAY:
        if item[0] == state_abbrev:
            return format(item[5], '.2f')


def getNotBlackDisparity(state_abbrev):
    for item in POLICE_KILLINGS_ARRAY:
        if item[0] == state_abbrev:
            return format(item[6], '.2f')


def getTotalDisparity(state_abbrev):
    for item in POLICE_KILLINGS_ARRAY:
        if item[0] == state_abbrev:
            return format(item[7], '.2f')


# def main():
#
#     initDB(us_state_abbrev)
#
#     running = True
#     while running:
#
#         state = input("\nEnter a State: ")
#
#         if state in us_state_abbrev:
#
#             print(getPoliceKillingsArray())
#             print(queryDB(state))
#             print("% Killings Black:", getPercentKillingsBlack(state))
#             print("% Killings Not Black:",getPercentKillingsNotBlack(state))
#             print("% Population Black:",getPercentPopulationBlack(state))
#             print("% Population Not Black:",getPercentPopulationNotBlack(state))
#             print("Black Disparity of Police Killings to Population:", getBlackDisparity(state))
#             print("Non-Black Disparity of Police Killings to Population:", getNotBlackDisparity(state))
#             print("Disparity of Police Killings between Black and Non-Black People:", getTotalDisparity(state))
#
#         elif state == "exit":
#             running = False
#
#         else:
#             print("Error: Did not input a state abbreviation")
#
#     print("Goodbye!")
#
#     # print(queryDB("WY"))
#     # print(queryDB("CA"))
#     # functionality needed in mongoDB code:
#     #
#     # To render Pie chart 1:
#     # get total population for state
#     # get black population for state
#     #
#     # To render pie chart 2:
#     # get total killings for state
#     # get black killings for state
#
#
# main()

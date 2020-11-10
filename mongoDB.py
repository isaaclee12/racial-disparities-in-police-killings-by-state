import pymongo
import re
import sys
import numpy

SIZE = 50
PERCENT_KILLINGS_BLACK_BY_STATE = []
DATA_ARRAY = numpy.zeros((50, 3))
FINAL_DATA_ARRAY = []
# numpy.set_printoptions(threshold=sys.maxsize)

def counter(mydoc):

    # Initialize counter
    ct = 0

    # Increment counter for every instance found
    for x in mydoc:
        ct += 1

    # Return count
    return ct


def initDB(states):

    # Set up connection with MongoClient
    myclient = pymongo.MongoClient("mongodb+srv://iwlee:EggCheeseBeansToast@uspolicekillings.ezqox.mongodb.net/US_Police_Killings?retryWrites=true&w=majority")

    # Set up databases
    global mydb
    mydb = myclient["police_killings"]


    # Get States
    mycol = mydb["US_Police_Killings"]

    # Choose a State
    # state_abbrev = "CA"
    global PERCENT_KILLINGS_BLACK_BY_STATE
    global FINAL_DATA_ARRAY
    rowct = 0
    # percentKillingsBlackByState = []

    print("Beginning Loop")

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

        # print(blackKillings)

        # blackKillings = counter(blackDoc)
        # print("Number of killings in", state, "of Black People: ", blackKillings)

        # notBlackKillings = counter(notBlackDoc)
        # print("Number of killings in", state, "of those who are not Black: ", notBlackKillings)

        percentKillingsBlack = (blackKillings / (blackKillings + notBlackKillings)) * 100

        # Save abbrev for later
        state_abbrev = state

        data = state, percentKillingsBlack
        PERCENT_KILLINGS_BLACK_BY_STATE.append(data)
        print(data)
        rowct += 1

        # print("Percentage of people in", state, "killed by police who are Black: ", format(percentKillingsBlack, '.2f'),
        #       "%")

        # print(state, ": ", percentKillingsBlack)

        # blackItem = state, percentKillingsBlack
        # PERCENT_KILLINGS_BLACK_BY_STATE.append(blackItem)

    # print(PERCENT_KILLINGS_BLACK_BY_STATE)

    for state in states:
        finalData = state, calculateStats(state)
        FINAL_DATA_ARRAY.append(finalData)

    for item in FINAL_DATA_ARRAY:
        print(item)

    # for x in range(0, SIZE):
    #     print(DATA_ARRAY[x])

    # for item in PERCENT_KILLINGS_BLACK_BY_STATE:
    #     data = state_abbrev, calculateStats(item[0])
    #
    # print(FINAL_DATA_ARRAY)


def calculateStats(state_abbrev):

    #Get percent for this state
    for item in PERCENT_KILLINGS_BLACK_BY_STATE:
        if item[0] == state_abbrev:
            percentKillingsBlack = item[1]

    # Get States
    demographics = mydb["US_State_Demographics_By_Race"]

    blackDemographics = demographics.find({"Location": us_state_abbrev.get(state_abbrev)}, {"Black": 1, "_id": 0})

    for x in blackDemographics:

        try:
            percentageBlack = re.search(": '(.+?)'}", str(x)).group(1)

        except AttributeError:
            print("Error: demographic not found")
            percentageBlack = ""

    # Clean data
    if percentageBlack == "<.01":
        percentageBlack = .01

    percentageBlack  = float(percentageBlack) * 100
    message = ""

    if percentageBlack == 0:
        message += ("There's no Black people in " + state_abbrev + "!")
    else:

        if (percentageBlack < percentKillingsBlack):

            message += ("The percent of people killed by police in " + state_abbrev + " who are Black is " + str(
                format(percentKillingsBlack, '.2f')) + "%, ")
            message += ("even though only " + format(percentageBlack, '.2f') + "% of " + state_abbrev + "'s population is Black. ")
            blackDisparity = (percentKillingsBlack / percentageBlack)

            message += ("The percent of people killed by police in " + state_abbrev + " who are not Black is " + str(
                format((100 - percentKillingsBlack), '.2f')) + "%, ")
            message += ("whereas " + str((100 - percentageBlack)) + "% of " + state_abbrev + "'s population is not Black. ")
            notBlackDisparity = ((100 - percentKillingsBlack) / (100 - percentageBlack))

            message += ("Therefore, a black person is (statistically speaking) " + str(
                format(blackDisparity / notBlackDisparity,
                       '.2f')) + " times more likely to be killed by police than someone who is not Black in " + state_abbrev + ". ")

        else:

            message += ("The percent of people killed by police in " + state_abbrev + " is " + str(
                format(percentKillingsBlack, '.2f')) + "%, ")
            message += ("where " + format(percentageBlack, '.2f') + "% of " + state_abbrev + "'s population is Black. ")
            blackDisparity = (percentKillingsBlack / percentageBlack)

            message += ("The percent of people killed by police in " + state_abbrev + " who are not Black is " + str(
                format((100 - percentKillingsBlack), '.2f')) + "%, ")
            message += ("whereas " + str((100 - percentageBlack)) + "% of " + state_abbrev + "'s population is not Black. ")
            notBlackDisparity = ((100 - percentKillingsBlack) / (100 - percentageBlack))

            # Prevent divide by 0 error
            if blackDisparity > 0:
                message += ("Therefore, a black person is (statistically speaking) " + str(
                    format((notBlackDisparity / blackDisparity),
                           '.2f')) + " times less likely to be killed by police than someone who is not Black in " + state_abbrev + ". ")
            else:
                message += ("NO BLACK DISPARITY")

    return message


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


def queryDB(state_abbrev):
    for item in FINAL_DATA_ARRAY:
        if item[0] == state_abbrev:
            print(item[1])


def main():
    initDB(us_state_abbrev)
    print(queryDB("NY"))


main()

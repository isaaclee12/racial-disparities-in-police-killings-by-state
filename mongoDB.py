import pymongo


def counter(mydoc):

    # Initialize counter
    ct = 0

    # Increment counter for every instance found
    for x in mydoc:
        ct += 1

    # Return count
    return ct


def initDB():
    # FILE STUFF

    # Open file w/ utf-8 encoding (This circumvents a Unicode error)
    global police_killings

    try:
        police_killings = open('Fatal_Encounters_Police_Killings_2000_2020.csv', encoding='utf-8')

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

        # Set up connection with MongoClient
        myclient = pymongo.MongoClient("mongodb+srv://iwlee:EggCheeseBeansToast@uspolicekillings.ezqox.mongodb.net/US_Police_Killings?retryWrites=true&w=majority")

        # Set up database
        global mydb
        mydb = myclient["police_killings"]


def queryDB(state_abbrev):

        # Get States
        mycol = mydb["US_Police_Killings"]

        myquery = {"State": state_abbrev}

        mydoc = mycol.find(myquery)

        # Uncomment this to print all CA killings - be warned, this takes a long time
        # for x in mydoc:
        #     print(x)

        killings = counter(mydoc)

        return killings
        #print("Number of killings in CA: ", CA_killings)

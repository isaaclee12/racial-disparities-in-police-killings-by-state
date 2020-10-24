import pymongo

def counter(mydoc):

    ct = 0

    for x in mydoc:
        ct += 1

    return ct

def main():

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
        mydb = myclient["police_killings"]

        # Get States
        mycol = mydb["US_Police_Killings"]

        myquery = {"State": "CA"}

        mydoc = mycol.find(myquery)

        CA_killings = counter(mydoc)

        print("Number of killings in CA: ", CA_killings)


main()

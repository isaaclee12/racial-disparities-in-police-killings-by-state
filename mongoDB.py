import pymongo
#import dnspy

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

        # mongoDB

        # Set up connection with MongoClient
        myclient = pymongo.MongoClient("mongodb+srv://iwlee:EggCheeseBeansToast@uspolicekillings.ezqox.mongodb.net/US_Police_Killings?retryWrites=true&w=majority")

        # mongodb://localhost:27017/

        #mongodb+srv://iwlee:EggCheeseBeansToast@uspolicekillings.ezqox.mongodb.net/police_killings?retryWrites=true&w=majority

        # Set up database
        mydb = myclient["police_killings"]

        # Get States
        mycol = mydb["US_Police_Killings"]

        myquery = {"State": "CA"}

        mydoc = mycol.find() #myquery

        print("A")
        # for x in mydoc:
        #     print(x)

        # # Get list of databases in client server
        # dblist = mydb.list_collection_names()
        #
        # # Debug: Print Database List
        # print(mydb, "LIST: ", dblist)
        #
        # # If my database is in the list, print that it exists
        # if "mydatabase" in dblist:
        #     print("The database exists.")


main()

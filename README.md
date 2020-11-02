# CS-205-FInal-Project-Team-Five
Final Project

CS 205 Final Project Proposal
Team Members: Yousef Khan, Isaac Lee, Grace Bart, Phillip Nguyen

Languages:

• Python (/w pymongo and flask)

• HTML/CS

• Javascript

• PHP



Description:
Our team has decided to make a website that contains:

• A navigation bar

• A page with a description of the data

• A page with info about the authors

• A page with a map of the United States, where clicking on a U.S. state will show
statistics representing racial disparities in police killings.

▪ When the user clicks on a state, a http request is sent to the python server.
Then a query will be sent from python to the database, and the database will
return the requested data to python. The python program will then calculate
statistics based on the data and send the results to be draw via flask. The
statistics will them be drawn using flask in the form of pie charts and numeric
values.


User Instructions:
Run main.py through either an IDE or by navigating to this directory in your command line
and entering the following:

python main.py

(Try "python3 main.py", without quotes, if the first command doesn't work)

Then open your browser to http://127.0.0.1:5000/maptest to open the map. You can test the
functionality by clicking a state and waiting for the results to print. As of the moment,
it may take a few seconds to load the results. We hope to improve the loading time
in the future.
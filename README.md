# CS-205-FInal-Project-Team-Five

CS 205 Final Project

**Team Members:** Yousef Khan, Isaac Lee, Grace Bart, Phillip Nguyen

**Live Instance of Project:** http://134.209.76.43/dev/map.html

**Languages:**

- Python (/w pymongo and flask)

- HTML/CSS

- Javascript

- PHP


**Description**

Our team has decided to make a website that contains:

- A navigation bar

- A page with a description of the data

- A page with info about the authors

- A page with a map of the United States, where clicking on a U.S. state will show
statistics representing racial disparities in police killings.

- When the user clicks on a state, a http request is sent to the python server.
Then a query will be sent from python to the database, and the database will
return the requested data to python. The python program will then calculate
statistics based on the data and send the results to be draw via flask. The
statistics will them be drawn using flask in the form of pie charts and numeric
values.


**User Instructions:**
Run main.py through either an IDE or by navigating to this directory in your command line
and entering the following (see README_flask.md for more information):

python main.py

(Try "python3 main.py", without quotes, if the first command doesn't work)

Then open map.html in the browser (appearance may not match live instance if PHP is not
installed and configured correctly). You can test the functionality by clicking a state and waiting 
for the results to print.

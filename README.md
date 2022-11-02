This was my final project for my CS205 - Software Engineering course at the University of Vermont. This was my first exposure to working on a full stack project in a group setting. Much of this project was completed remotely due to COVID-19 restrictions.

Our team used a Trello board to keep our tasks organized, and we split responsibilities based on each end of the program. I was responsible for the MongoDB backend, as well as the Flask API. The others were responsible for web hosting, UI design, and front-end development.

Overall, this project was a great success. I thoroughly enjoyed working on this project as it leveraged my interest in working in an intersection of technology, data analysis, and social welfare.

Note - I plan to redploy this project at some point so that others may see the final result.

**Team Members:** Yousef Khan, Isaac Lee, Grace Bart, Phillip Nguyen

**Live Instance of Project:** http://134.209.76.43/dev/map.html (Site is currently down)

**File Descriptions**
main.py - The main flask code
mongoDB.py - The API code that links the mongoDB database to the front end
map.html - The main page with the interactive map

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

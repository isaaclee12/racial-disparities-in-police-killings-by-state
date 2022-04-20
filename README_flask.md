# Documentation [10/31/2020]

## Dependency Installation

Make sure that python3 and pip are installed. [link to pip documentation](https://pip.pypa.io/)

```
$ pip install flask flask-cors pymongo dnspython
```


## Developers Only: testing map + flask server locally (full stack)

Execute main.py and open either map.html or static/maptest.html in web browser.

Map should be fully interactable, that is, clicking on states should return relevant data.

## Developers Only: testing flask server locally (just RESTful API)

Execute main.py and open [http://localhost:5000/](http://localhost:5000/) in web browser

Example GET request:
```
http://localhost:5000/stats/state/vt
```
Should return:
```
{
  "blackDisparity": "2.56",
  "notBlackDisparity": "0.98",
  "percentKillingsBlack": "2.56",
  "percentKillingsNotBlack": "97.44",
  "percentPopulationBlack": "1.00",
  "percentPopulationNotBlack": "99.00",
  "stateName": "Vermont",
  "totalDisparity": "2.61",
  "totalPoliceKillings": "The percent of people killed by police in Vermont who are Black is 2.56%, \neven though only 1.00% of Vermont's population is Black. \nThe percent of people killed by police in Vermont who are not Black is 97.44%, \nwhereas 99.0% of Vermont's population is not Black. \nTherefore, the police are (statistically speaking) 2.61 times more likely to kill a Black person than a person of any other race in Vermont. "
}
```

## Developers Only: remote server setup

Observe the "switch two lines for live instance" comments for main.py and static/main.js.
The default behaviour is to run the local testing code; code for remote setup is commented out.

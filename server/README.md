# Documentation [10/31/2020]

## Dependency Installation

Make sure that python3 and pip are installed. [link to pip documentation](https://pip.pypa.io/)

```
$ pip install flask
$ pip install flask-cors
$ pip install pymongo
$ pip install dnspython
```


## Developers Only: testing map + flask server (full stack)

Execute main.py and open map/maptest.html in web browser. 

Map should be fully interactable, that is, clicking on states should return relevant data.

## Developers Only: testing flask server (just RESTful API)

Execute main.py and open [http://localhost:5000/](http://localhost:5000/) in web browser

Example GET request:
```
http://localhost:5000/stats/state/vt
```
Should return:
```
{
  "PercentBlackKillings": 2.56, 
  "stateName": "Vermont", 
  "totalBlackPoliceKillings": 1, 
  "totalNonBlackPoliceKillings": 38, 
  "totalPoliceKillings": 39
}
```

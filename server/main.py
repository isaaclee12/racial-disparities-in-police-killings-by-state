from flask import Flask, request, jsonify
from flask_cors import CORS
import random, sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mongoDB # import from parent directory

# Init Code: Starts up flask app and sets up database
app = Flask(__name__)
cors = CORS(app)
mongoDB.initDB()

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

@app.route('/', methods=['GET'])
def test():
    '''Developer help function of sorts.'''

    doc = "<h1>API:</h1> <p>GET: /stats/state/&lt;string:state_abbrev&gt;</p>"
    doc += "<blockquote> returns relevant statistics given a two-letter state abbreviation</blockquote>"
    return doc

@app.route('/stats/state/<string:state_abbrev>', methods=['GET'])
def statistics(state_abbrev):
    '''
    This function interfaces with database code to obtain data
    for a valid state and returns the result to the user.
    '''

    # initialize dictionary
    if state_abbrev.upper() not in us_state_abbrev:
        data = dict()
        data["error"] = "No such state"
        return jsonify(data)
    data = dict(stateName = us_state_abbrev[state_abbrev.upper()])
    data["totalPoliceShootings2018"] = mongoDB.queryDB(state_abbrev.upper())
    # TODO: return more useful data?
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)

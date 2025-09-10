from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import sys

# Add the parent directory to sys.path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mongoDB

# Init Code: Starts up flask app and sets up database
app = Flask(__name__, static_url_path='')
cors = CORS(app)

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

# Initialize database on startup
mongoDB.initDB(us_state_abbrev)

@app.route('/', methods=['GET'])
def test():
    '''Developer help function of sorts.'''
    doc = "<h1>API:</h1> <p>GET: /api/stats/state/&lt;string:state_abbrev&gt;</p>"
    doc += "<blockquote> returns relevant statistics given a two-letter state abbreviation</blockquote>"
    return doc

@app.route('/stats/state/<string:state_abbrev>', methods=['GET'])
def statistics(state_abbrev):
    '''
    This function interfaces with database code to obtain data
    for a valid state and returns the result to the user.
    '''
    
    state = state_abbrev.upper()
    # initialize dictionary
    if state not in us_state_abbrev:
        data = dict()
        data["error"] = "No such state"
        return jsonify(data)

    data = dict(stateName = us_state_abbrev[state])
    data["totalPoliceKillings"] = mongoDB.queryDB(state)
    data["percentKillingsBlack"] = mongoDB.getPercentKillingsBlack(state)
    data["percentKillingsNotBlack"] = mongoDB.getPercentKillingsNotBlack(state)
    data["percentPopulationBlack"] = mongoDB.getPercentPopulationBlack(state)
    data["percentPopulationNotBlack"] = mongoDB.getPercentPopulationNotBlack(state)
    data["blackDisparity"] = mongoDB.getBlackDisparity(state)
    data["notBlackDisparity"] = mongoDB.getNotBlackDisparity(state)
    data["totalDisparity"] = mongoDB.getTotalDisparity(state)

    return jsonify(data)

# Vercel automatically detects the 'app' variable as WSGI application
# No custom handler needed
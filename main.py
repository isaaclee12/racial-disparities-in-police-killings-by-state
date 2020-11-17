from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
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

mongoDB.initDB(us_state_abbrev)

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

    state = state_abbrev.upper()
    # initialize dictionary
    if state not in us_state_abbrev:
        data = dict()
        data["error"] = "No such state"
        return jsonify(data)

    data = dict(stateName = us_state_abbrev[state])
    data["totalPoliceKillings"] = mongoDB.queryDB(state) #us_state_abbrev,
    # mongoDB.getTotalKillingsForState(state)
    # data["totalBlackPoliceKillings"] = mongoDB.getBlackKillingsForState(state)
    # data["totalNonBlackPoliceKillings"] = mongoDB.getNotBlackKillingsForState(state)
    # data["PercentBlackKillings"] = mongoDB.getPercentBlackKillingsForState(state)
    return jsonify(data)

@app.route('/static', methods=['GET']) #, methods=['GET']
def map():
    return render_template("../static.html")

@app.route('/maptest', methods=['GET']) #, methods=['GET']
def maptest():
    return app.send_static_file("maptest.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)

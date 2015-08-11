import requests, urllib

# Base url for the google distancematrix api
DISTANCEMATRIX_BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'


class SteerClearDistanceMatrixClient():

    def __ini__(self, api_key=None):
        self.api_key = api_key

    def query_api(origins, destinations):
        query = build_query(origins, destinations)
        url = build_url(query)
        response = requests.get(url)
        return DMResponse(response)

    """
    build_url
    ---------
    Takes a query of key/value pairs and returns the
    correctly formatted google distancematrix api url
    """
    def build_url(query):
        return DISTANCEMATRIX_BASE_URL + '?' + urllib.urlencode(query)

    """
    build_query
    -----------
    Takes the list of origins and destinations and returns
    the correctly formated query dictionary.
    * origins - list of (lat,long) tuples of the origin positions
    * destinations - list of (lat,long) tuples of the destination positions
    * NOTE: correct format for query dictionary is {'origins': 'lat1,long1|...|latn,longn', 
    'destinations': 'lat1,long1|...|latn,longn'}
    """
    def build_query(origins, destinations):
        origins = map(lambda x: '%f,%f' % x, origins)
        destinations = map(lambda x: '%f,%f' % x, destinations)
        query = {
            'origins': '|'.join(origins),
            'destinations': '|'.join(destinations)
        }
        return query

"""
DMResponse
-------------
Response object for Google Distance Matrix API Response
"""
class DMResponse:

    """
    Constructor for DMResponse expects to be given a json object
    of the response from the distancematrix api
    """
    def __init__(self, data):
        self.data = data

    """
    get_eta
    -------
    Return the list of eta data values
    Response object looks like this: https://maps.googleapis.com/maps/api/distancematrix/json?origins=37.272042,-76.714027|37.273485,-76.719628&destinations=37.273485,-76.719628|37.280893,%20-76.719691
    """
    def get_eta(self):
        # bad response
        if not self.data:
            return None

        # get rows or return None
        rows = self.data.get(u'rows', None)
        if not rows:
            return None

        # Get all of the eta values in the response
        eta_list = []
        for row in rows:
            # get elements
            elements = row.get(u'elements', None)
            if not elements:
                return None

            eta = []
            # for every element, get the duration
            for element in elements:
                # if bad status, return None
                status = element.get(u'status', u'')
                if status != u'OK':
                    return None

                # get duration or return None
                duration = element.get(u'duration', None)
                if not duration:
                    return None

                # get eta value or return None
                value = duration.get(u'value', None)
                if not value:
                    return None

                # append to current list of eta values
                eta.append(value)

            # append list of eta values
            eta_list.append(eta)
        return eta_list

    """
    get_addresses
    -------------
    Return the origin and destination addresses
    """
    def get_addresses(self):
        # bad response
        if not self.data:
            return None

        # get addresses or return None
        origin_addresses = self.data.get(u'origin_addresses', None)
        destination_addresses = self.data.get(u'destination_addresses', None)
        if not origin_addresses or not destination_addresses:
            return None

        return (origin_addresses, destination_addresses)




"""
get_element_eta
---------------
Returns the eta value from the 'element' field in the google
distancematrix api json response
"""
def get_element_eta(element):
    if element is None:                         # check element object is not None
        return None
    if element.get(u'status', u'') != u'OK':    # check there were no errors in api request
        return None
    duration = element.get(u'duration', None)   # check for existence of duration field    
    if duration is None:
        return None
    return duration.get(u'value', None)         # return eta or None

"""
get_elements_eta
---------------
Returns all of the eta's from the 'elements' field in the google
distancematrix api json response
"""
def get_elements_eta(elements):
    if elements is None:                                     # check elements object is not None
       return None
    elements_eta_list = map(get_element_eta, elements)       # get all eta's
    if elements_eta_list == [] or None in elements_eta_list: # check that there were no errors in request
        return None
    return elements_eta_list

"""
get_row_eta
---------------
Returns all of the eta's from the 'row' field in the google
distancematrix api json response
"""
def get_row_eta(row):
    if row is None:                                         # check row object is not None
        return None
    return get_elements_eta(row.get(u'elements', None))     # get list of all eta's

"""
get_rows_eta
---------------
Returns the list of all of the eta_lists from the 
'rows' field in the google distancematrix api json response
"""
def get_rows_eta(rows, num_queries):
    if rows is None:                        # check that rows object is not None
        return None
    if len(rows) != num_queries:            # make sure number of location queries matches
        return None                         # the number of rows
    eta_list = map(get_row_eta, rows)       # get list of all eta_lists
    if eta_list == [] or None in eta_list:  # check that there were no erros in request
        return None
    return eta_list

"""
time_between_locations
------------------
Takes the current location, pickup location for the next ride
request, dropoff location for the next ride request all in lat/long
tuples and returns the time it will take in seconds to go from the
current location to the pickup location and the time it will take in
seconds to go from the pickup location to the dropoff location.
"""
def time_between_locations(origins, destinations):
    response = distancematrix_api(origins, destinations)  # get api response
    if response.status_code != requests.codes.ok:         # check for response errors
        return None
    data = response.json()                                # get json response
    rows = data.get(u'rows', None)                        # get 'rows' field
    eta_list = get_rows_eta(rows, len(origins))           # get list of all eta_lists
    return eta_list

import requests, urllib

# Base url for the google distancematrix api
DISTANCEMATRIX_BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'


class SteerClearDMClient():


    def query_api(self, origins, destinations):
        # build query string and url
        query = self._format_query(origins, destinations)
        url = self._build_url(query)

        # make request and check for bad response
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            return DMResponse(None)
        # return response object
        return DMResponse(response.json())

    """
    _format_query
    -----------
    Takes the list of origins and destinations and returns
    the correctly formated query dictionary.
    * origins - list of (lat,long) tuples of the origin positions
    * destinations - list of (lat,long) tuples of the destination positions
    * NOTE: correct format for query dictionary is {'origins': 'lat1,long1|...|latn,longn', 
    'destinations': 'lat1,long1|...|latn,longn'}
    """
    def _format_query(self, origins, destinations):
        origins = map(lambda x: '%f,%f' % x, origins)
        destinations = map(lambda x: '%f,%f' % x, destinations)
        query = {
            'origins': '|'.join(origins),
            'destinations': '|'.join(destinations)
        }
        return query

    """
    _build_url
    ---------
    Takes a query of key/value pairs and returns the
    correctly formatted google distancematrix api url
    """
    def _build_url(self, query):
        return DISTANCEMATRIX_BASE_URL + '?' + urllib.urlencode(query)

"""
DMResponse
-------------
Response object for Google Distance Matrix API Response
"""
class DMResponse():

    """
    Constructor for DMResponse expects to be given a json object
    of the response from the distancematrix api
    """
    def __init__(self, data):
        if data is not None and data.get(u'status', u'') != u'OK':
            self.data = None
        else:
            self.data = data

    def __eq__(self, other):
        return self.data == other.data

    """
    get_eta
    -------
    Return the list of eta data values
    Response object looks like this: https://maps.googleapis.com/maps/api/distancematrix/json?origins=37.272042,-76.714027|37.273485,-76.719628&destinations=37.273485,-76.719628|37.280893,%20-76.719691
    Returns a list of lists of all of the eta values
    """
    def get_eta(self):
        # bad response
        if not self.data:
            return None

        # get rows or return None
        rows = self.data.get(u'rows', None)
        if rows is None:
            print 'rows'
            return None

        # Get all of the eta values in the response
        eta_list = []
        for row in rows:
            # get elements
            elements = row.get(u'elements', None)
            if elements is None:
                print 'elements'
                return None

            eta = []
            # for every element, get the duration
            for element in elements:
                # if bad status, return None
                status = element.get(u'status', u'')
                if status != u'OK':
                    print 'status'
                    return None

                # get duration or return None
                duration = element.get(u'duration', None)
                if duration is None:
                    print 'duration'
                    return None

                # get eta value or return None
                value = duration.get(u'value', None)
                if value is None:
                    print 'value'
                    return None

                # append to current list of eta values
                eta.append(value)

            # append list of eta values
            eta_list.append(eta)

        # some part of the response was bad
        if eta_list == [] or [] in eta_list:
            return None
        return eta_list

    """
    get_addresses
    -------------
    Return the origin and destination addresses field in the response
    as a tuple of lists
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

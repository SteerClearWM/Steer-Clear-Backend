import requests, urllib

DISTANCEMATRIX_BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'

def build_url(query):
    return DISTANCEMATRIX_BASE_URL + '?' + urllib.urlencode(query)

def build_query(origins, destinations):
    origins = map(lambda x: '%f,%f' % x, origins)
    destinations = map(lambda x: '%f,%f' % x, destinations)
    query = {
        'origins': '|'.join(origins),
        'destinations': '|'.join(destinations)
    }
    return query

def build_distancematrix_url(origins, destinations):
    query = build_query(origins, destinations)
    return build_url(query)

def distancematrix_api(origins, destinations):
    url = build_distancematrix_url(origins, destinations)
    return requests.get(url)

def get_element_eta(element):
    if element is None:
        return None
    if element.get(u'status', u'') != u'OK':
        return None
    duration = element.get(u'duration', None)
    if duration is None:
        return None
    return duration.get(u'value', None)

def get_elements_eta(elements):
    if elements is None:
       return None
    elements_eta_list = map(get_element_eta, elements)
    if elements_eta_list == [] or None in elements_eta_list:
        return None
    return elements_eta_list

def get_row_eta(row):
    if row is None:
        return None
    return get_elements_eta(row.get(u'elements', None))

def get_rows_eta(rows, num_queries):
    if rows is None:
        return None
    if len(rows) != num_queries:
        return None
    eta_list = map(get_row_eta, rows)
    if eta_list == [] or None in eta_list:
        return None
    return eta_list

# def calculate_eta(origins, destinations):
#     url = build_distancematrix_url(origins, destinations)
#     response = requests.get(url)
#     if response.status_code != requests.codes.ok:
#         return None
#     data = response.json()
#     rows = data.get(u'rows', None)
#     if rows is None:
#         return None
#     elements = rows[0].get(u'elements', None)
#     if elements is None:
#         return None
#     ride = elements[0]
#     if ride.get(u'status', u'') != u'OK':
#         return None
#     duration = ride.get(u'duration', None)
#     if duration is None:
#         return None
#     return duration.get(u'value', None)

def time_between_rides(cur_ride, next_ride):
    origins = [
        (cur_ride.end_latitude, cur_ride.end_longitude), 
        (next_ride.start_latitude, next_ride.start_longitude)
    ]
    destinations = [
        (next_ride.start_latitude, next_ride.start_longitude),
        (next_ride.end_latitude, next_ride.end_longitude)
    ]
    response = distancematrix_api(origins, destinations)
    if response.status_code != requests.codes.ok:
        return None
    data = response.json()
    rows = data.get(u'rows', None)
    eta_list = get_rows_eta(rows, len(origins))
    if eta_list is None:
        return None
    return {
        'pickup_time_sec': eta_list[0][0],
        'travel_time_sec': eta_list[1][1]
    }

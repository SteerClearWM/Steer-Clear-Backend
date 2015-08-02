import requests
import sys

def main():
    r1 = requests.post('http://localhost:5000/login', data={'email': 'ryan', 'password': '1234'})
    if r1.status_code != 200:
        print "Error: User does not exist with emial=ryan and password=1234"
        sys.exit(1)

    payload = {
        'num_passengers': 3,
        'start_latitude': 37.273485,
        'start_longitude': -76.719628,
        'end_latitude': 37.280893,
        'end_longitude': -76.719691, 
    }

    r2 = requests.post('http://localhost:5000/api/rides', data=payload, cookies=r1.cookies)
    if r2.status_code != 201:
        print "Error: failed to create new ride"
        sys.exit(1)
    print "Successfully hailed new ride"

if __name__ == '__main__':
    main()

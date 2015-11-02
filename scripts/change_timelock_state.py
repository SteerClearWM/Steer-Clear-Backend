import requests, sys

def main():
    username = raw_input('Enter admin username: ')
    password = raw_input('Enter admin password: ')
    new_state = raw_input('Enter new state (on/off): ')

    r1 = requests.post('http://localhost:5000/login', data={'username': username, 'password': password})
    if r1.status_code != 200:
        print "Error: incorrect admin username=%s or password=%s" % (username, password)
        sys.exit(1)

    r2 = requests.post(
        'http://localhost:5000/api/timelock', 
        data={'new_state': new_state},
        cookies=r1.cookies
    )
    if r2.status_code != 201:
        print "Bad Status Code: %d" % r2.status_code
        print "Error: failed to change state of timelock"
        sys.exit(1)
    print "Successfully changed state to: " + new_state

if __name__ == '__main__':
    main()

from steerclear import app
import argparse

if __name__ == '__main__':
    # set up command line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', dest='port', type=int, default=5000, 
                        help='port number to run app on')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False)
    args = parser.parse_args()

    # run flask app with configurations
    app.run(port=args.port, debug=args.debug)

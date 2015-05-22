# Adds a new ride request to the queue
curl -d "num_passengers=4&\
start_latitude=10.0&\
start_longitude=50.1&\
end_latitude=1.01&\
end_longitude=5.07" 127.0.0.1:5000/rides
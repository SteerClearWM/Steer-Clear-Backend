# Adds a new ride request to the queue
curl -d "num_passengers=4&\
start_latitude=37.273485&\
start_longitude=-76.719628&\
end_latitude=37.280893&\
end_longitude=-76.719691" 127.0.0.1:5000/api/rides


// this code is executed when the page is finished loading
// for now ive just put examples of all the requests that can be made
// and logged their response objects to the console
$("document").ready(function() {
    console.log("before request");
    
    get_rides(function(data) {
        console.log(data);
    });

    get_ride(1, function(data) {
        console.log(data);
    });

    var ride = {
        "num_passengers": 4,
        "start_latitude": 37.273485,
        "start_longitude": -76.719628,
        "end_latitude": 37.280893,
        "end_longitude": -76.719691
    };
    create_ride(ride, function(data) {
        console.log(data);
    });

    delete_ride(3, function(data) {
        console.log(data);
    });
    
    console.log("after request");
});

// make a GET request to the server to get the list of rides
// in the queue. *callback* is the function that recieves the
// result of the request
function get_rides(callback) {
    $.get("rides", callback);
}

// takes the ride id of the rid object you
// wish to get and makes a GET request
// and attempts to get the ride object
function get_ride(ride_id, callback) {
    $.get("rides" + "/" + ride_id, callback);
}

// Takes a json object with the ride information
// and a callback function and makes a POST request
// and attempts to creat a new ride object
function create_ride(ride_info, callback) {
    $.post("rides", ride_info, callback, "json");
}

// Takes the id of the ride object you want to delete
// and makes a DELETE request to the server and
// attempts to delete the ride
function delete_ride(ride_id, callback) {
    $.ajax({
        url: "rides" + "/" + ride_id,
        type: "DELETE",
        success: callback,
    });
}


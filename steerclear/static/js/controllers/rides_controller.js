app.controller('RidesController', ['$scope', 'RidesService', function($scope, RidesService){

    var ride = {
        "num_passengers": 4,
        "start_latitude": 37.273485,
        "start_longitude": -76.719628,
        "end_latitude": 37 + Math.random(),
        "end_longitude": -76 + Math.random(),
        "phone": 15555555555
    };

    RidesService.createRide(ride)

		updateData = function() {
	      RidesService.getRides().then(function(data){
	          for (var i =0; i < data.rides.length; i++){
	              data.rides[i].pickup_address = data.rides[i].pickup_address || "Start Address Not Found";
	              data.rides[i].dropoff_address = data.rides[i].dropoff_address || "End Address Not Found";
	          };
	          $scope.rides = data.rides;
	    	});
    };

    updateData();
    setInterval('updateData()', 5000);

    $scope.deleteRide = function ( ride ) {
        if (confirm("Are you sure you want to delete this ride?")){
            del_index = $scope.rides.indexOf(ride);
            $scope.rides.splice(del_index,1);
            RidesService.deleteRide(ride.id);
        }
    };

    $scope.notify = function ( ride ) {
        RidesService.notify(ride.id);
        console.log("notified")
    }

    $scope.finishRide = function ( ride ) {
        if (confirm("Are you sure you want to finish this ride? It will be removed from the queue forever.")){
            del_index = $scope.rides.indexOf(ride);
            $scope.rides.splice(del_index,1);
            RidesService.deleteRide(ride.id);
        }
    };

}]);

app.controller('RidesController', ['$scope', 'RidesService', function($scope, RidesService){

	var ride = {
        "num_passengers": 4,
        "start_latitude": 37.273485,
        "start_longitude": -76.719628,
        "end_latitude": 37.280893,
        "end_longitude": -76.719691
    };

    // RidesService.createRide(ride)

	init = function() {
        RidesService.getRides().then(function(data){
    		$scope.rides = data.rides;
            for (var i =0; i < $scope.rides.length; i++){
                ride.address = "address";
                console.log(ride)
            };
	    }); 
    };

    init();

    $scope.deleteRide = function ( ride ) {
        del_index = $scope.rides.indexOf(ride);
        $scope.rides.splice(del_index,1);
        RidesService.deleteRide(ride.id);
    };

}]);
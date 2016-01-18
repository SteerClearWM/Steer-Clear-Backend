app.controller('RidesController', ['$scope', 'RidesService', '$window', function($scope, RidesService, $window){

    $scope.filter = "both"

    $scope.filterRides = function( filter ) {
        $scope.filter = filter;
        switch(filter) {
            case "both":
                $scope.rides = $scope.originalRides;
                break;
            case "on_campus":
                temp = [];
                for (var i=0; i < $scope.originalRides.length; i++){
                    if ($scope.originalRides[i].on_campus == true){
                        temp.push($scope.originalRides[i]);
                    }
                }
                $scope.rides = angular.copy(temp);
                break;
            case "off_campus":
                temp = [];
                for (var i=0; i < $scope.originalRides.length; i++){
                    if ($scope.originalRides[i].on_campus == false){
                        temp.push($scope.originalRides[i]);
                    }
                }
                $scope.rides = angular.copy(temp);
                break;
        }
    }

	updateData = function() {
      RidesService.getRides().then(function(data){
            for (var i =0; i < data.rides.length; i++){
              data.rides[i].pickup_address = data.rides[i].pickup_address || "Start Address Not Found";
              data.rides[i].dropoff_address = data.rides[i].dropoff_address || "End Address Not Found";
            };
        $scope.originalRides = angular.copy(data.rides);
            $scope.filterRides($scope.filter);
    	});
        console.log($scope.rides)
    };

    updateData();
    setInterval('updateData()', 5000);

    $scope.gps = function ( dlat, dlong, slat, slong ) {
        $scope.iOS = /iPad|iPhone|iPod/.test(navigator.platform);
        url = "maps.google.com?&daddr=" + dlat + "," + dlong
        if (slat & slong) {
            url = url + "&saddr=" + slat + "," + slong;
        }
        url += "&zoom=15";
        if ($scope.iOS) {
            window.open("comgooglemapsurl://" + url);
        } else {
            window.open("http://" + url, '_blank');
        }
    }

    $scope.deleteRide = function ( ride ) {
        if (confirm("Are you sure you want to delete this ride?")){
            del_index = $scope.rides.indexOf(ride);
            $scope.rides.splice(del_index,1);
            RidesService.deleteRide(ride.id);
        }
    };

    $scope.notify = function ( ride ) {
        if (confirm("Would you like to notify the user that their ride is ready?")) {
            response = RidesService.notify(ride.id)
        }
    }

    $scope.finishRide = function ( ride ) {
        if (confirm("Are you sure you want to finish this ride? It will be removed from the queue forever.")){
            del_index = $scope.rides.indexOf(ride);
            $scope.rides.splice(del_index,1);
            RidesService.deleteRide(ride.id);
        }
    };

    $scope.logout = function () {
        console.log("THing");
        if (confirm('Are you sure you want to log out?')){
            $window.location.href = '/logout';
        }
    };



    //For demo purposes....

    var ride = {
        "num_passengers": 4,
        "start_latitude": 37.273485,
        "start_longitude": -76.719628,
        "end_latitude": 37.273,
        "end_longitude": -76.719628,
        "phone": 15555555555
    };

    if (document.location.hostname == "localhost" || document.location.hostname == "127.0.0.1")
        RidesService.createRide(ride)

}]);
